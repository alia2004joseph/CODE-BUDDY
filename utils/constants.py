"""
constants.py

Central place for all static configuration values, option lists,
and text strings used across the Coddy Buddy registration app.
Keeping these here avoids "magic strings" scattered through app.py.
"""

# ------------------------------------------------------------------
# Program identity
# ------------------------------------------------------------------
PROGRAM_NAME = "CODDY BUDDY"
PROGRAM_FOCUS = "WEB APPLICATION DEVELOPMENT"
PROGRAM_AUDIENCE = "FOR CEDAT ENGINEERING STUDENTS"
PROGRAM_TAGLINE = "LEARN. BUILD. INNOVATE."
PROGRAM_SCHEDULE = "EVERY SATURDAY"
PROGRAM_TIME = "10:00 AM – 12:00 PM"

PROGRAM_LEAD_NAME = "Alia Joseph"
PROGRAM_LEAD_WHATSAPP = "0744 215 379"

COPYRIGHT_TEXT = f"© {{year}} Coddy Buddy. Designed by {PROGRAM_LEAD_NAME}. All rights reserved."

PROGRAM_INTRO = (
    "Coddy Buddy is a student-focused program created to help CEDAT engineering "
    "students develop practical web application development skills and learn how "
    "software can be used to solve real engineering problems."
)

TECHNOLOGIES_TAUGHT = [
    "HTML & CSS",
    "JavaScript",
    "Python",
    "Django",
    "Django REST Framework",
    "React",
    "Git & GitHub",
]

# ------------------------------------------------------------------
# Google Sheet configuration
# ------------------------------------------------------------------
WORKSHEET_NAME = "Registrations"

SHEET_HEADERS = [
    "Timestamp",
    "Full Name",
    "Registration Number",
    "Phone Number",
    "Email",
    "Engineering Program",
    "Other Engineering Program",
    "Year of Study",
    "Programming Experience",
    "Technologies Used",
    "How They Heard",
    "Other Referral Source",
    "Motivation",
    "Engineering Problem",
    "Saturday Availability",
]

# ------------------------------------------------------------------
# Form option lists
# ------------------------------------------------------------------
ENGINEERING_PROGRAMS = [
    "Mechanical Engineering",
    "Electrical Engineering",
    "Civil Engineering",
    "Agricultural Engineering",
    "Telecommunications Engineering",
    "Other",
]

YEARS_OF_STUDY = [
    "Year 1",
    "Year 2",
    "Year 3",
    "Year 4",
    "Year 5",
    "Other",
]

PROGRAMMING_EXPERIENCE_LEVELS = [
    "No programming experience",
    "Beginner",
    "Intermediate",
    "Advanced",
]

TECHNOLOGIES_KNOWN = [
    "None",
    "HTML/CSS",
    "JavaScript",
    "Python",
    "Django",
    "Django REST Framework",
    "React",
    "Git/GitHub",
]

REFERRAL_SOURCES = [
    "WhatsApp",
    "Friend",
    "Class representative",
    "CEDAT announcement",
    "Poster",
    "Other",
]

ATTENDANCE_OPTIONS = [
    "Yes",
    "No",
    "Not always",
]

# ------------------------------------------------------------------
# Messages
# ------------------------------------------------------------------
MSG_DUPLICATE_REGISTRATION = "You have already registered for Coddy Buddy."
MSG_SERVICE_UNAVAILABLE = "Registration is temporarily unavailable. Please try again later."
MSG_INVALID_ADMIN_LOGIN = "Incorrect password. Please try again."
MSG_MISSING_CONFIG = (
    "The application is not fully configured yet. Please contact the program "
    "organizers or check the deployment configuration."
)