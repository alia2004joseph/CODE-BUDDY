"""
constants.py

Central place for all static configuration values, option lists,
and text strings used across the Coddy Buddy Community Portal.
"""

# ------------------------------------------------------------------
# Program identity
# ------------------------------------------------------------------
PROGRAM_NAME = "CODDY BUDDY"
PROGRAM_TAGLINE = "LEARN. BUILD. INNOVATE."
PROGRAM_DESCRIPTION = "A Student-Led Technology Community"
PROGRAM_FOCUS = "FULL-STACK WEB APPLICATION DEVELOPMENT"
PROGRAM_AUDIENCE = "Open to students, beginners, developers, and technology enthusiasts"
PROGRAM_SCHEDULE = "Every Saturday"
PROGRAM_TIME = "10:00 AM – 12:00 PM"
PROGRAM_VENUE = "Venue communicated to registered members"
PROGRAM_FREE_TEXT = "FREE OF CHARGE"

PROGRAM_LEAD_NAME = "Alia Joseph"
PROGRAM_LEAD_WHATSAPP = "0744 215 379"
COMMUNITY_WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/Kdq47XMq6Ix65qIkvgR1gk?s=cl&p=a&ilr=4"

COPYRIGHT_TEXT = f"© {{year}} Coddy Buddy. Designed by {PROGRAM_LEAD_NAME}. All rights reserved."

PROGRAM_INTRO = (
    "Coddy Buddy is a practical technology community where people learn software "
    "development, collaborate with others, and build real applications that solve "
    "real-world problems."
)

WHO_CAN_JOIN = [
    "University Students",
    "Beginners",
    "Engineering Students",
    "Computer Science / IT Students",
    "Developers",
    "Innovators",
    "Anyone interested in technology",
]

TECHNOLOGIES_TAUGHT = [
    "HTML",
    "CSS",
    "JavaScript",
    "Git & GitHub",
    "React",
    "Python",
    "Django",
    "Django REST Framework",
    "APIs",
    "Databases",
    "Authentication",
    "Deployment",
]

LEARNING_PATH = [
    "HTML & CSS",
    "JavaScript",
    "Git & GitHub",
    "Python",
    "Django",
    "Django REST Framework",
    "React",
    "Full-Stack Applications",
    "Deployment",
]

PROJECT_EXAMPLES = [
    "Student management systems",
    "Booking platforms",
    "Inventory systems",
    "Project management applications",
    "Community platforms",
    "Engineering solutions",
    "Campus solutions",
    "Personal projects",
    "Other real-world applications",
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
    "Class Representative",
    "University Announcement",
    "Poster",
    "Social Media",
    "Other",
]

SATURDAY_OPTIONS = ["Yes", "No", "Not always"]
STUDENT_OPTIONS = ["Yes", "No"]

# ------------------------------------------------------------------
# Google Sheet configuration
# ------------------------------------------------------------------
WORKSHEET_NAME = "Registrations"
SHEET_HEADERS = [
    "Timestamp",
    "Full Name",
    "Phone Number",
    "Email",
    "Student Status",
    "Institution",
    "Field/Program",
    "Year of Study",
    "Occupation/Background",
    "Programming Experience",
    "Technologies Used",
    "Motivation",
    "What They Want to Build",
    "Goals",
    "Saturday Availability",
    "Referral Source",
    "Other Referral Source",
]

# ------------------------------------------------------------------
# Messages
# ------------------------------------------------------------------
MSG_DUPLICATE_REGISTRATION = "You have already registered for Coddy Buddy."
MSG_SERVICE_UNAVAILABLE = "Registration is temporarily unavailable. Please try again later."
MSG_MISSING_CONFIG = (
    "The application is not fully configured yet. Please contact the program "
    "organizers or check the deployment configuration."
)