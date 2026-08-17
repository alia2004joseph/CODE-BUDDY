"""
google_sheets.py

Handles all interaction with Google Sheets, which acts as the database
for the Coddy Buddy Community Portal.
"""

import time
from datetime import datetime

import gspread
import pandas as pd
import streamlit as st
from google.oauth2.service_account import Credentials

from utils.constants import SHEET_HEADERS, WORKSHEET_NAME

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 1.5
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class GoogleSheetsError(Exception):
    pass


def _call_with_retry(func, *args, **kwargs):
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
            if status == 429 or (status and 500 <= status < 600):
                time.sleep(_RETRY_DELAY_SECONDS * (attempt + 1))
                continue
            raise
    raise last_exc


def _get_credentials():
    if "gcp_service_account" not in st.secrets:
        raise GoogleSheetsError("Google service account credentials are missing from secrets.")
    try:
        service_account_info = dict(st.secrets["gcp_service_account"])
        return Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Failed to build Google credentials.") from exc


@st.cache_resource(show_spinner=False)
def _get_client():
    try:
        return gspread.authorize(_get_credentials())
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Failed to authorize Google Sheets client.") from exc


def _get_spreadsheet():
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
        raise GoogleSheetsError("The configured Google Sheet could not be found.") from exc
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not open the Google Spreadsheet.") from exc

    raise GoogleSheetsError("No spreadsheet configuration was provided.")


def _get_worksheet():
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
            raise GoogleSheetsError("Could not create the registrations worksheet.") from exc

    _ensure_headers(worksheet)
    return worksheet


def _ensure_headers(worksheet):
    try:
        existing_values = _call_with_retry(worksheet.get_all_values)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not read the worksheet contents.") from exc

    if not existing_values:
        try:
            end_cell = gspread.utils.rowcol_to_a1(1, len(SHEET_HEADERS))
            _call_with_retry(
                worksheet.update,
                f"A1:{end_cell}",
                [SHEET_HEADERS],
                value_input_option="USER_ENTERED",
            )
        except Exception as exc:  # noqa: BLE001
            raise GoogleSheetsError("Could not create the header row.") from exc


def get_all_registrations() -> pd.DataFrame:
    worksheet = _get_worksheet()
    try:
        all_values = _call_with_retry(worksheet.get_all_values)
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not read registrations from Google Sheets.") from exc

    if not all_values or len(all_values) < 2:
        return pd.DataFrame(columns=SHEET_HEADERS)

    data_rows = all_values[1:]
    num_cols = len(SHEET_HEADERS)
    normalized_rows = []

    for row in data_rows:
        if not any((cell or "").strip() for cell in row):
            continue
        padded = row + [""] * (num_cols - len(row))
        normalized_rows.append(padded[:num_cols])

    if not normalized_rows:
        return pd.DataFrame(columns=SHEET_HEADERS)

    return pd.DataFrame(normalized_rows, columns=SHEET_HEADERS)


def _normalize(value: str) -> str:
    return str(value or "").strip().lower()


def is_duplicate_registration(email: str, phone_number: str | None = None) -> bool:
    if not email and not phone_number:
        return False

    df = get_all_registrations()
    if df.empty:
        return False

    email_match = False
    phone_match = False

    if email and "Email" in df.columns:
        email_match = _normalize(email) in set(df["Email"].astype(str).str.strip().str.lower())

    if phone_number and "Phone Number" in df.columns:
        phone_match = _normalize(phone_number) in set(df["Phone Number"].astype(str).str.strip().str.lower())

    return email_match or phone_match


def add_registration(data: dict) -> None:
    worksheet = _get_worksheet()
    row = [data.get(header, "") for header in SHEET_HEADERS]
    row[0] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        existing_values = _call_with_retry(worksheet.get_all_values)
        next_row_number = len(existing_values) + 1
        start_cell = gspread.utils.rowcol_to_a1(next_row_number, 1)
        end_cell = gspread.utils.rowcol_to_a1(next_row_number, len(SHEET_HEADERS))
        _call_with_retry(worksheet.update, f"{start_cell}:{end_cell}", [row], value_input_option="USER_ENTERED")
    except Exception as exc:  # noqa: BLE001
        raise GoogleSheetsError("Could not save the registration. Please try again.") from exc


def get_summary_tables(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total": 0,
            "students": pd.DataFrame(),
            "experience": pd.DataFrame(),
            "availability": pd.DataFrame(),
            "referrals": pd.DataFrame(),
            "institutions": pd.DataFrame(),
            "fields": pd.DataFrame(),
            "years": pd.DataFrame(),
            "technologies": pd.DataFrame(),
        }

    summary = {
        "total": len(df),
        "students": df.get("Student Status", pd.Series(dtype=str)).value_counts().reset_index(),
        "experience": df.get("Programming Experience", pd.Series(dtype=str)).value_counts().reset_index(),
        "availability": df.get("Saturday Availability", pd.Series(dtype=str)).value_counts().reset_index(),
        "referrals": df.get("Referral Source", pd.Series(dtype=str)).value_counts().reset_index(),
        "institutions": df.get("Institution", pd.Series(dtype=str)).value_counts().reset_index(),
        "fields": df.get("Field/Program", pd.Series(dtype=str)).value_counts().reset_index(),
        "years": df.get("Year of Study", pd.Series(dtype=str)).value_counts().reset_index(),
        "technologies": pd.Series(
            df.get("Technologies Used", pd.Series(dtype=str))
            .dropna()
            .astype(str)
            .str.split(",")
            .explode()
            .str.strip()
        ).value_counts().reset_index(),
    }

    for key, table in summary.items():
        if isinstance(table, pd.DataFrame) and not table.empty:
            table.columns = ["Value", "Count"]

    return summary
