# Coddy Buddy Community Portal

Coddy Buddy is a student-led technology community focused on practical learning, collaboration, and building real-world software solutions.

## Who can join?

- University students
- Beginners
- Engineering students
- Computer Science / IT students
- Developers
- Innovators
- Anyone interested in technology and software development

No prior programming experience is required.

## Current semester program

**Full-Stack Web Application Development**

Students will learn:
- HTML
- CSS
- JavaScript
- Git & GitHub
- React
- Python
- Django
- Django REST Framework
- REST APIs
- Databases
- Authentication
- Team development
- Testing
- Deployment

## Features

- Professional Streamlit community portal
- Home, About, Program, Projects, Register, Contact, and Admin pages
- Registration saved to Google Sheets
- Duplicate registration protection
- Password-protected admin dashboard
- Clean tables for registration review
- CSV export for admin use

## Technology stack

- Streamlit
- Python
- Pandas
- Google Sheets API
- GSpread
- Google Auth

## Project structure

```text
CODE-BUDDY/
├── app.py
├── utils/
│   ├── constants.py
│   ├── google_sheets.py
│   └── validation.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Local installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.streamlit/secrets.toml`.
5. Add your Google service account credentials and spreadsheet details.
6. Run the app:

```bash
streamlit run app.py
```

## Google Sheets configuration

The app uses Google Sheets as its database.

Add these secrets:

```toml
admin_password = "your-strong-password"

[spreadsheet]
sheet_id = "your_google_sheet_id"

[gcp_service_account]
# paste the full service account JSON fields here
```

The app will create or use a worksheet named `Registrations`.

## Streamlit secrets

Store all sensitive values in Streamlit secrets:
- admin password
- Google credentials
- spreadsheet ID

Do not hard-code secrets in the code.

## Admin configuration

The Admin page is password protected.

After login, the admin can:
- view registration summaries
- review the full registrations table
- download registrations as CSV

## Streamlit Community Cloud deployment

1. Push the repository to GitHub.
2. Deploy with Streamlit Community Cloud.
3. Add the same secrets in the Streamlit Cloud Secrets panel.
4. Ensure `app.py` is the entry point.

## Privacy considerations

- Registration data is not shown to public visitors.
- Admin access is password protected.
- Credentials are never displayed in the UI.
- Existing registrations should be preserved.
