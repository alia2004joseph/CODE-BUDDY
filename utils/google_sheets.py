"""
google_sheets.py

Handles all interaction with Google Sheets, which acts as the database
for the Coddy Buddy registration system.

Responsibilities:
    - Authenticate with Google using a service account
    - Open the configured spreadsheet / worksheet
    - Ensure the header row exists
    - Read all registrations
    - Check for duplicate registration numbers
    - Add a new registration row
    - Compute simple statistics for the admin dashboard

Credentials are never hard-coded. They are read from Streamlit secrets
(`st.secrets`) when deployed, which is populated locally via a `.env`
file only for reference — Streamlit itself reads from
`.streamlit/secrets.toml` in local development.
"""

import time
from datetime import datetime

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from utils.constants import SHEET_HEADERS, WORKSHEET_NAME

# Google Sheets API has per-minute rate limits (commonly 60 read/write
# requests per minute per user on the default quota). Opening the
# spreadsheet, opening the worksheet, and reading values are each
# separate API calls, so a burst of activity (e.g. an admin refreshing
# the dashboard a few times quickly) can occasionally trip a 429 error.
# We retry transient failures with a short backoff before giving up.
_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 1.5


def _call_with_retry(func, *args, **kwargs):
    """Call a gspread function, retrying on transient/rate-limit errors."""
    last_exc = None
    for attempt in range(_MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except gspread.exceptions.APIError as exc:
            last_exc = exc
            status = None
            try:
                status = exc.response.status_code
            except Exception:  # noqa: BLE001
                pass
            # Retry on rate limiting (429) and transient server errors (5xx)
            if status == 429 or (status and 500 <= status < 600):
                time.sleep(_RETRY_DELAY_SECONDS * (attempt + 1))
                continue
            raise
    raise last_exc

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsError(Exception):
    """Raised when something goes wrong talking to Google Sheets."""


def _get_credentials():
    """
    Build Google service-account credentials from Streamlit secrets.

    Expects a `[gcp_service_account]` table in secrets.toml containing the
    standard service-account JSON fields (type, project_id, private_key,
    client_email, etc.).
    """
    if "gcp_service_account" not in st.secrets:
        raise GoogleSheetsError(
            "Google service account credentials are missing from secrets."
        )
    try:
        service_account_info = dict(st.secrets["gcp_service_account"])
        return Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Failed to build Google credentials.") from exc


@st.cache_resource(show_spinner=False)
def _get_client():
    """Create (and cache) an authorized gspread client."""
    credentials = _get_credentials()
    try:
        return gspread.authorize(credentials)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Failed to authorize Google Sheets client.") from exc


def _get_spreadsheet():
    """Open the configured spreadsheet by key or by name."""
    if "spreadsheet" not in st.secrets:
        raise GoogleSheetsError("Spreadsheet configuration is missing from secrets.")

    client = _get_client()
    spreadsheet_config = st.secrets["spreadsheet"]

    try:
        if spreadsheet_config.get("sheet_id"):
            return _call_with_retry(client.open_by_key, spreadsheet_config["sheet_id"])
        if spreadsheet_config.get("sheet_name"):
            return _call_with_retry(client.open, spreadsheet_config["sheet_name"])
    except gspread.exceptions.SpreadsheetNotFound as exc:
        raise GoogleSheetsError(
            "The configured Google Sheet could not be found. Please check the "
            "spreadsheet ID/name and sharing permissions."
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not open the Google Spreadsheet.") from exc

    raise GoogleSheetsError(
        "No 'sheet_id' or 'sheet_name' was provided in the spreadsheet configuration."
    )


def _get_worksheet():
    """Open (or create) the 'Registrations' worksheet and ensure headers exist."""
    spreadsheet = _get_spreadsheet()

    try:
        worksheet = _call_with_retry(spreadsheet.worksheet, WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        try:
            worksheet = _call_with_retry(
                spreadsheet.add_worksheet,
                title=WORKSHEET_NAME,
                rows=1000,
                cols=len(SHEET_HEADERS),
            )
        except Exception as exc:  # noqa: BLE001
            raise GoogleSheetsError(
                "Could not create the 'Registrations' worksheet."
            ) from exc

    _ensure_headers(worksheet)
    return worksheet


def _ensure_headers(worksheet):
    """Write the header row if the worksheet is currently empty."""
    try:
        existing_values = _call_with_retry(worksheet.get_all_values)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not read the worksheet contents.") from exc

    if not existing_values:
        try:
            end_cell = gspread.utils.rowcol_to_a1(1, len(SHEET_HEADERS))
            cell_range = f"A1:{end_cell}"
            _call_with_retry(
                worksheet.update,
                cell_range,
                [SHEET_HEADERS],
                value_input_option="USER_ENTERED",
            )
        except Exception as exc:  # noqa: BLE001
            raise GoogleSheetsError("Could not create the header row.") from exc


def get_all_registrations() -> pd.DataFrame:
    """
    Return all registrations as a pandas DataFrame.

    Returns an empty DataFrame (with correct columns) if there are no
    registrations yet.

    Note: this deliberately does NOT use gspread's `get_all_records()`,
    because that method raises an error if the header row contains any
    duplicate or blank cells (which easily happens with extra blank
    columns/formatting in a Google Sheet). Instead we read raw values
    and build the DataFrame manually, which is far more forgiving.
    """
    worksheet = _get_worksheet()
    try:
        all_values = _call_with_retry(worksheet.get_all_values)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not read registrations from Google Sheets.") from exc

    if not all_values or len(all_values) < 2:
        # Only the header row (or nothing) is present.
        return pd.DataFrame(columns=SHEET_HEADERS)

    header_row = all_values[0]
    data_rows = all_values[1:]

    # Trust our own known headers over whatever is literally in row 1,
    # so stray blank/duplicate/extra columns in the sheet can't break
    # DataFrame construction. We map by position, up to the number of
    # columns we actually expect.
    num_cols = len(SHEET_HEADERS)

    normalized_rows = []
    for row in data_rows:
        # Skip fully blank rows (e.g. trailing empty rows in the sheet)
        if not any(cell.strip() for cell in row):
            continue
        # Pad short rows / truncate long rows to match expected column count
        padded = row + [""] * (num_cols - len(row))
        normalized_rows.append(padded[:num_cols])

    if not normalized_rows:
        return pd.DataFrame(columns=SHEET_HEADERS)

    return pd.DataFrame(normalized_rows, columns=SHEET_HEADERS)


def is_duplicate_registration(registration_number: str) -> bool:
    """Check whether a registration number already exists in the sheet."""
    if not registration_number:
        return False

    df = get_all_registrations()
    if df.empty or "Registration Number" not in df.columns:
        return False

    normalized_input = registration_number.strip().lower()
    existing_numbers = (
        df["Registration Number"].astype(str).str.strip().str.lower()
    )
    return normalized_input in existing_numbers.values


def add_registration(data: dict) -> None:
    """
    Append a new registration row to the worksheet.

    Parameters
    ----------
    data : dict
        Dictionary keyed by the human-readable column names in
        `constants.SHEET_HEADERS`.

    Note: this deliberately does NOT use gspread's `append_row()`. That
    method asks the Sheets API to auto-detect the next empty row and
    starting column based on the shape of existing data in the sheet,
    which can misfire if there are any stray cells, extra formatting,
    or leftover columns elsewhere in the sheet (e.g. from manual edits)
    — causing new data to be written starting at the wrong column
    entirely. Instead, we explicitly compute the next empty row and
    write directly into columns A through O of that row, so data always
    lands under the correct headers regardless of what else is in the
    sheet.
    """
    worksheet = _get_worksheet()

    row = [data.get(header, "") for header in SHEET_HEADERS]
    row[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp

    try:
        existing_values = _call_with_retry(worksheet.get_all_values)
        next_row_number = len(existing_values) + 1  # 1-indexed; header is row 1

        start_cell = gspread.utils.rowcol_to_a1(next_row_number, 1)
        end_cell = gspread.utils.rowcol_to_a1(next_row_number, len(SHEET_HEADERS))
        cell_range = f"{start_cell}:{end_cell}"

        _call_with_retry(
            worksheet.update, cell_range, [row], value_input_option="USER_ENTERED"
        )
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not save the registration. Please try again.") from exc


def get_statistics(df: pd.DataFrame) -> dict:
    """
    Compute summary statistics for the admin dashboard.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame of all registrations (as returned by
        `get_all_registrations`).

    Returns
    -------
    dict
        A dictionary of precomputed statistics/series ready to be
        rendered as metrics and charts.
    """
    stats = {
        "total_students": 0,
        "by_program": pd.Series(dtype=int),
        "by_year": pd.Series(dtype=int),
        "by_experience": pd.Series(dtype=int),
        "by_availability": pd.Series(dtype=int),
        "by_technology": pd.Series(dtype=int),
    }

    if df.empty:
        return stats

    stats["total_students"] = len(df)

    if "Engineering Program" in df.columns:
        stats["by_program"] = df["Engineering Program"].value_counts()

    if "Year of Study" in df.columns:
        stats["by_year"] = df["Year of Study"].value_counts()

    if "Programming Experience" in df.columns:
        stats["by_experience"] = df["Programming Experience"].value_counts()

    if "Saturday Availability" in df.columns:
        stats["by_availability"] = df["Saturday Availability"].value_counts()

    if "Technologies Used" in df.columns:
        # Technologies are stored as a comma-separated string per student.
        tech_series = (
            df["Technologies Used"]
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
        )
        tech_series = tech_series[tech_series != ""]
        stats["by_technology"] = tech_series.value_counts()

    return stats