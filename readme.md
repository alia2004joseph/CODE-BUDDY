# Coddy Buddy — CEDAT Registration System

A professional registration web application for **Coddy Buddy**, a student-led
program for engineering students at **CEDAT — College of Engineering, Design,
Art and Technology**.

This semester's focus: **Web Application Development** (HTML & CSS,
JavaScript, Python, Django, Django REST Framework, React, Git & GitHub).

Coding with **Alia Joseph** · WhatsApp: **0744 215 379**
**LEARN. BUILD. INNOVATE.**

---

## 1. What Is Coddy Buddy?

Coddy Buddy is a student-focused program created to help CEDAT engineering
students develop practical web application development skills and learn how
software can be used to solve real engineering problems. The program meets
**every Saturday**.

This repository contains the **registration web application** used by
students to sign up, and by organizers to manage and review registrations.

---

## 2. Purpose of This Application

- Allow CEDAT engineering students to register for the program online.
- Prevent duplicate registrations using each student's registration number.
- Store registrations safely in a **Google Sheet** (used as the database).
- Give the program organizers a private, password-protected **Admin
  Dashboard** to view statistics and download registration data.

---

## 3. Features

- 🎨 Clean, modern, mobile-friendly UI in a CEDAT-inspired dark navy /
  cyan / green theme.
- 📝 A complete registration form with personal, academic, and
  programming-background questions.
- ✅ Full form validation (required fields, email format, phone number
  format).
- 🔁 Duplicate-registration prevention based on registration number.
- 📊 A private Admin Dashboard with metrics, charts, a registrations
  table, and CSV export.
- 🔒 Admin access protected by a password stored in Streamlit secrets
  (never hard-coded).
- ☁️ Google Sheets used as the backend database — no separate database
  server needed.
- 🚀 Ready to deploy on **Streamlit Community Cloud**.

---

## 4. Technologies Used

| Purpose            | Technology              |
|---------------------|--------------------------|
| Web app framework   | Streamlit                |
| Data handling       | pandas                   |
| Google Sheets API   | gspread, google-auth     |
| Local configuration | python-dotenv (reference only — see note below) |

> **Note:** This is a standalone **Streamlit** application. It does **not**
> use Django or React, even though those technologies are part of what
> students learn in the Coddy Buddy program itself.

---

## 5. Project Structure

```
coddy-buddy-registration/
│
├── app.py                     # Main Streamlit application (all pages)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                 # Files/folders excluded from git
├── .env.example                # Reference of required configuration values
│
├── utils/
│   ├── __init__.py
│   ├── google_sheets.py       # Google Sheets connection & data operations
│   ├── validation.py          # Form validation helpers
│   └── constants.py           # Shared text, option lists, configuration
│
└── assets/
    └── README.md              # Notes on optional static assets (e.g. logo)
```

---

## 6. Prerequisites

- Python 3.9 or newer
- A Google account (for Google Sheets + Google Cloud service account)
- Git (for cloning/deploying)

---

## 7. Local Installation

### 7.1 Clone the repository

```bash
git clone https://github.com/your-username/coddy-buddy-registration.git
cd coddy-buddy-registration
```

### 7.2 Create a virtual environment

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 7.3 Install requirements

```bash
pip install -r requirements.txt
```

---

## 8. Configuring Google Sheets

The app uses a **Google Cloud service account** to read/write a Google
Sheet on behalf of the application (no student ever needs their own
Google account to register).

### 8.1 Create the Google Sheet

1. Create a new Google Sheet (e.g. named `Coddy Buddy Registrations`).
2. Leave it empty — the app will automatically create a worksheet named
   **`Registrations`** and add the header row the first time it runs.
3. Copy the Spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_IS_HERE/edit
   ```

### 8.2 Create a Google Cloud service account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable these two APIs for the project:
   - **Google Sheets API**
   - **Google Drive API**
4. Go to **APIs & Services → Credentials → Create Credentials → Service
   Account**.
5. Once created, open the service account, go to the **Keys** tab, and
   click **Add Key → Create New Key → JSON**. This downloads a JSON file
   containing your credentials.
6. **Keep this JSON file private.** Never commit it to GitHub.

### 8.3 Share the Google Sheet with the service account

1. Open the downloaded JSON file and copy the `client_email` value
   (it looks like `something@your-project.iam.gserviceaccount.com`).
2. Open your Google Sheet, click **Share**, and share it with that email
   address, giving it **Editor** access.

---

## 9. Configuring Streamlit Secrets

Streamlit apps read sensitive configuration from a `secrets.toml` file,
**not** from a `.env` file. The included `.env.example` simply lists which
values are required — use it as a reference while filling in the file
below.

### 9.1 Create the secrets file locally

Create a folder named `.streamlit` in the project root (if it doesn't
already exist), and inside it create a file named `secrets.toml`:

```
coddy-buddy-registration/
└── .streamlit/
    └── secrets.toml
```

### 9.2 Fill in `secrets.toml`

Use the values from your downloaded service-account JSON file and your
chosen admin password:

```toml
admin_password = "choose-a-strong-password"

[spreadsheet]
sheet_id = "your-google-sheet-id"
# Alternatively, instead of sheet_id you may use:
# sheet_name = "Coddy Buddy Registrations"

[gcp_service_account]
type = "service_account"
project_id = "ode-buddy-505620"
private_key_id = "24a6e580944da5086937fa11fa746048c368a1c2"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCul2/F7gPHBP7U\nL0Wk3r9aerTefaBidwOb+GaHSif7LkIURmYBlCU7iaxABWEbyAXTVP2vovJImavx\nxkkiNdvQzcVGX9foUCuqo2z1dyEO04V6O7gUlG/4QTvcZL3puH/rrKB3yQ3tJf7c\n5IxDXwuIzG4SO76PB1kz/OKt36SO+25rnhaY9RD8Eja+mu3ahz9X8zvHAad3XvZ7\n/In8Uo0Ar97jMQZMrVWL8cLyo8v/r2JALPLb1phujddnLYWrWm+XmpM/ElWXVIe5\nEdtMyLMmfz4HsG+HhyZ9Ty2p80lWnaLgii9kPG21OvCiMpmpEt6sek79vcHKb/TV\nkMbdnOg3AgMBAAECggEAQSaxxyKytinfDj81tfiJX7I6nGw01YmkBygC2qmJkeoJ\nLpe2qRAndLhDVwCq5DsYMWyd3lToJL9zsp1T3ThL9vdSjphlcYO5R8wEdPUnmOjF\n/n8ailN6FSICvJO7auQ2mDOrDggw8jYjjTqcPOfS3hGrYZJ54dXUK9pKnKfAOLps\nVfClb9pxoTb2bKZneypIb1U72N3tULJ2LnLvcvqUBXemAKhom+U5SEbLEFXdr+aT\nxVwhvHAzS7W6rRT06D0RcDvN3+dwsLVKCD6gTO1oWc/DD+MVjshN7evbNWdIxHWW\nzSHNWPCVN0Y01s/v4PPNou11MuFtshzUQYjV38NnAQKBgQDoSKneUrO3sRSS208N\no6EhJnF3YbL++63Gr8E+o9v7uv6RVvQRPa0vYQfneERtkf3latd4qTYxwVOYCwwz\ne9nbedBBk/GOhR2QBmmkH+JtEj+sqfdjgv8jP3dLF84oZokRc+/i7AOzMYhng81n\nkt/6QWx4TOsejUdM2F9uGYEnhwKBgQDAatYe+qMk6m4Gqnf2+dUUoT5SRmNHGvjh\nvZCmT7uU32eoPMiK1BGY1j/TXThzDW3JFM/AHdaVyFlqoAyIOokaTLb+jq8MqM3t\nFqNvv3jvVI+oe43ySg9KcOhJZKWbv5xdI/3tDvqx4/cT07sg/nYRfBrmrpN9byBh\n/2aHfOoF0QKBgQDRKSU02ZmUzfKtrqdHq9Earag8jJAGhJBdOcOz6Q7cZOx36SmL\nINOCt0fLyYMseup6G7P8pbn0IZZpcYFCFsL8m3rIojRAVmNhXjTgIgnclzMZAk+O\nntWpYqvDxaLQxEummJQo7McEI5UlSQy7uAjRKvpGdVS+RQ8wBiIgXPzsnwKBgGps\nrPGFfyaz4xccwi2AETLP3EB1XgO+D1oMFy1lfELjLdoHhIQEt5bpKXQmY0p/avGE\n6UNBPaaqoYov676NYbeCJtS05m0CEKPJmav9I058Xti5PdF81Og/errdSBvU5w89\nEP1FA7PQeqAkw6OEGpmhIt/kPv9pr2eEc5kMpgOBAoGBAM5HGSIeqsxoWiUvrrgb\nHaQ5U+DiRk1hMZUmOM0mp3zHAVbnmpXJ1ymyTJgsMz06LUJvJc9O7fse0EYb5C0A\neCvreXA7U+HH2R2az69+5pC1vDOzmlhh2KwMgEnFO/LXU+Q1CnjV+2pSTmoQwKfC\nggiTypOKFcGoE5WABmMbkuqq\n-----END PRIVATE KEY-----\n",KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "code-buddy@code-buddy-505620.iam.gserviceaccount.com"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/code-buddy%40code-buddy-505620.iam.gserviceaccount.com"
```

> ⚠️ `.streamlit/secrets.toml` is already listed in `.gitignore` and must
> **never** be committed to version control.

---

## 10. Running the Application Locally

Once dependencies are installed and `secrets.toml` is configured:

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) —
open it in your browser.

- **Home** — program information
- **Register** — the student registration form
- **Admin** — password-protected dashboard (use the password you set in
  `secrets.toml`)

---

## 11. Deploying on Streamlit Community Cloud

1. Push this repository to GitHub (make sure `.env`, `secrets.toml`, and
   any service-account JSON files are **not** included — check
   `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in.
3. Click **New app**, and select your repository, branch, and `app.py`
   as the main file.
4. Before (or after) deploying, open **App settings → Secrets** and
   paste in the same contents you used in `secrets.toml` (Section 9.2).
5. Click **Deploy**. Streamlit Community Cloud will install
   `requirements.txt` automatically and launch the app.
6. Share the deployed link with CEDAT engineering students.

---

## 12. Configuring the Admin Password

The admin password is **not** stored anywhere in the code. It lives only
in:

- `secrets.toml` locally (key: `admin_password`), or
- the **Secrets** panel on Streamlit Community Cloud when deployed.

To change it, simply update that one value and restart/redeploy the app.
The password is never displayed anywhere in the application UI.

---

## 13. How the Google Sheets Database Works

- The app connects to Google Sheets using the service-account
  credentials from secrets.
- It looks for a worksheet named **`Registrations`** inside your
  spreadsheet — if it doesn't exist yet, the app creates it and writes
  the header row automatically.
- When a student submits the registration form:
  1. The form data is validated.
  2. The app checks the sheet for an existing row with the same
     **Registration Number**.
  3. If found, the student sees: *"You have already registered for
     Coddy Buddy."* and no new row is added.
  4. If not found, a new row is appended with a timestamp and all form
     answers.
- The Admin Dashboard reads all rows from the sheet to compute
  statistics and display the full registrations table.

---

## 14. Security & Privacy Considerations

- Registration data (names, phone numbers, emails, registration numbers,
  motivations) is **never shown on the public Home or Register pages**.
- Only the **Admin** page can display registration records, and it
  requires a correct password before revealing anything.
- Credentials (Google service account, admin password) are **only**
  ever read from Streamlit secrets — never hard-coded, logged, or
  displayed in the UI.
- `.gitignore` prevents `.env` files, `secrets.toml`, and any
  service-account JSON files from being committed accidentally.
- Errors are shown to users as friendly, non-technical messages (e.g.
  *"Registration is temporarily unavailable. Please try again later."*)
  so that internal error details or credentials are never exposed.

---

## 15. Support

For questions about the Coddy Buddy program itself, reach out on
WhatsApp: **0744 215 379** (Alia Joseph).