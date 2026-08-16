"""
app.py

Main entry point for the Coddy Buddy CEDAT Registration Web Application.

Pages:
    - Home    : information about the program
    - Register: the student registration form
    - Admin   : password-protected dashboard for organizers

Run locally with:
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime

from utils.constants import (
    ATTENDANCE_OPTIONS,
    COPYRIGHT_TEXT,
    ENGINEERING_PROGRAMS,
    MSG_DUPLICATE_REGISTRATION,
    MSG_MISSING_CONFIG,
    MSG_SERVICE_UNAVAILABLE,
    PROGRAM_INTRO,
    PROGRAM_LEAD_NAME,
    PROGRAM_LEAD_WHATSAPP,
    PROGRAM_NAME,
    PROGRAM_SCHEDULE,
    PROGRAM_TAGLINE,
    PROGRAM_TIME,
    PROGRAMMING_EXPERIENCE_LEVELS,
    REFERRAL_SOURCES,
    TECHNOLOGIES_KNOWN,
    TECHNOLOGIES_TAUGHT,
    YEARS_OF_STUDY,
)
from utils.google_sheets import (
    GoogleSheetsError,
    add_registration,
    get_all_registrations,
    get_statistics,
    is_duplicate_registration,
)
from utils.validation import validate_registration_form

# ----------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Coddy Buddy | CEDAT Registration",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Global styling
# ----------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    :root {
        --navy: #0a1a2f;
        --navy-light: #10233d;
        --cyan: #22d3ee;
        --cyan-dark: #0891b2;
        --green: #34d399;
        --white: #f8fafc;
    }

    .stApp {
        background: radial-gradient(circle at top left, var(--navy-light), var(--navy) 60%);
        color: var(--white);
    }

    section[data-testid="stSidebar"] {
        background-color: #071120;
        border-right: 1px solid rgba(34, 211, 238, 0.15);
    }

    section[data-testid="stSidebar"] * {
        color: var(--white) !important;
    }

    h1, h2, h3, h4 {
        color: var(--white) !important;
    }

    .cb-hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
    }

    .cb-hero .cb-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: 2px;
        background: linear-gradient(90deg, var(--cyan), var(--green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .cb-hero .cb-subtitle {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--white);
        letter-spacing: 1px;
    }

    .cb-hero .cb-audience {
        font-size: 1rem;
        color: #94a3b8;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }

    .cb-tagline {
        display: inline-block;
        margin-top: 0.5rem;
        padding: 0.4rem 1.2rem;
        border: 1px solid var(--cyan);
        border-radius: 999px;
        color: var(--cyan);
        font-weight: 700;
        letter-spacing: 3px;
        font-size: 0.85rem;
    }

    .cb-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 1.6rem;
        margin-bottom: 1.4rem;
    }

    .cb-section h3 {
        color: var(--cyan) !important;
        margin-top: 0;
    }

    .cb-schedule-badge {
        display: inline-block;
        background: linear-gradient(90deg, var(--cyan-dark), var(--green));
        color: #04141f;
        font-weight: 800;
        letter-spacing: 2px;
        padding: 0.6rem 1.4rem;
        border-radius: 10px;
        font-size: 1.1rem;
        margin: 0.6rem 0;
    }

    .cb-contact {
        text-align: center;
        margin-top: 1rem;
        padding: 1.2rem;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
    }

    .cb-contact .lead-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--green);
    }

    .cb-pill {
        display: inline-block;
        background: rgba(34, 211, 238, 0.12);
        border: 1px solid rgba(34, 211, 238, 0.35);
        color: var(--cyan);
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }

    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, var(--cyan-dark), var(--green)) !important;
        color: #04141f !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        letter-spacing: 0.5px !important;
        width: 100%;
    }

    .stButton > button p,
    div[data-testid="stFormSubmitButton"] > button p {
        color: #04141f !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        opacity: 0.88 !important;
        color: #04141f !important;
    }

    .stButton > button:hover p,
    div[data-testid="stFormSubmitButton"] > button:hover p {
        color: #04141f !important;
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 1.5rem;
    }

    .cb-success-box {
        text-align: center;
        padding: 2rem;
        border-radius: 14px;
        background: rgba(52, 211, 153, 0.08);
        border: 1px solid rgba(52, 211, 153, 0.4);
    }

    .cb-copyright {
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        color: #64748b;
        font-size: 0.8rem;
        letter-spacing: 0.3px;
    }

    /* --- Form label & input contrast fixes --- */

    /* Widget labels (Full Name, Registration Number, etc.) */
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] p,
    div[data-testid="stWidgetLabel"] p,
    .stTextInput label p,
    .stTextArea label p,
    .stSelectbox label p,
    .stMultiSelect label p,
    .stRadio label p {
        color: var(--white) !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    /* Text input & text area fields: white background, dark readable text */
    div[data-testid="stForm"] input[type="text"],
    div[data-testid="stForm"] input[type="password"],
    div[data-testid="stForm"] textarea {
        background-color: #ffffff !important;
        color: #0a1a2f !important;
        border: 1px solid rgba(148, 163, 184, 0.4) !important;
        border-radius: 8px !important;
    }

    div[data-testid="stForm"] input[type="text"]::placeholder,
    div[data-testid="stForm"] input[type="password"]::placeholder,
    div[data-testid="stForm"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    /* Selectbox / multiselect closed control */
    div[data-testid="stForm"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #0a1a2f !important;
        border: 1px solid rgba(148, 163, 184, 0.4) !important;
        border-radius: 8px !important;
    }

    div[data-testid="stForm"] div[data-baseweb="select"] span {
        color: #0a1a2f !important;
    }

    /* Selectbox dropdown menu (rendered in a portal, outside the form) */
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li {
        color: #0a1a2f !important;
        background-color: #ffffff !important;
    }

    /* Multiselect selected-item tags */
    div[data-testid="stForm"] span[data-baseweb="tag"] {
        background-color: var(--cyan-dark) !important;
        color: #ffffff !important;
    }

    /* Radio button option text */
    div[data-testid="stForm"] div[role="radiogroup"] label span,
    div[data-testid="stForm"] div[role="radiogroup"] p {
        color: var(--white) !important;
    }

    /* Section subheadings inside the form (#### Personal Information, etc.) */
    div[data-testid="stForm"] h4 {
        color: var(--cyan) !important;
        margin-top: 1.2rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Shared UI fragments
# ----------------------------------------------------------------------
def render_hero():
    st.markdown(
        f"""
        <div class="cb-hero">
            <div class="cb-title">{PROGRAM_NAME}</div>
            <div class="cb-subtitle">Web Application Development</div>
            <div class="cb-audience">FOR CEDAT ENGINEERING STUDENTS</div>
            <div class="cb-tagline">{PROGRAM_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_contact_footer():
    st.markdown(
        f"""
        <div class="cb-contact">
            <div class="cb-schedule-badge">{PROGRAM_SCHEDULE} · {PROGRAM_TIME}</div>
            <p class="lead-name">Coding with {PROGRAM_LEAD_NAME}</p>
            <p>WhatsApp: {PROGRAM_LEAD_WHATSAPP}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_copyright_footer():
    current_year = datetime.now().year
    st.markdown(
        f"""
        <div class="cb-copyright">
            {COPYRIGHT_TEXT.format(year=current_year)}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# HOME PAGE
# ----------------------------------------------------------------------
def render_home_page():
    render_hero()

    st.markdown('<div class="cb-section">', unsafe_allow_html=True)
    st.markdown("### About Coddy Buddy")
    st.write(PROGRAM_INTRO)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="cb-section">', unsafe_allow_html=True)
        st.markdown("### What You'll Learn")
        pills = "".join(
            f'<span class="cb-pill">{tech}</span>' for tech in TECHNOLOGIES_TAUGHT
        )
        st.markdown(pills, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cb-section">', unsafe_allow_html=True)
        st.markdown("### Why Join")
        st.markdown(
            """
            - Build real, practical web applications from scratch
            - Learn directly alongside fellow CEDAT engineering students
            - Get hands-on experience with modern, in-demand tools
            - Understand how software can solve real engineering problems
            - Join a supportive, student-led learning community
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="cb-section">', unsafe_allow_html=True)
    st.markdown("### Ready to Join?")
    st.write(
        "Head over to the **Register** page from the sidebar to secure your spot "
        "in this semester's Coddy Buddy program."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    render_contact_footer()


# ----------------------------------------------------------------------
# REGISTER PAGE
# ----------------------------------------------------------------------
def render_registration_success():
    student_name = st.session_state.get("last_registered_name", "").strip()
    greeting = f"Congratulations, {student_name}! 🎉" if student_name else "🎉 Registration Successful!"

    st.markdown(
        f"""
        <div class="cb-success-box">
            <h2>{greeting}</h2>
            <p>Welcome to Coddy Buddy — CEDAT.</p>
            <p>You have successfully registered for the Web Application Development Program.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_contact_footer()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Register Another Student", use_container_width=True):
            st.session_state.registration_submitted = False
            st.session_state.last_registered_name = ""
            st.rerun()

    with col2:
        if st.button("🏠 Return to Home", use_container_width=True):
            st.session_state.registration_submitted = False
            st.session_state.last_registered_name = ""
            st.session_state.nav_choice = "Home"
            st.rerun()

    st.caption("All done? You can safely close this tab at any time.")


def render_registration_form():
    st.markdown('<div class="cb-hero">', unsafe_allow_html=True)
    st.markdown(
        '<div class="cb-title" style="font-size:2rem;">Register for Coddy Buddy</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("registration_form", clear_on_submit=False):
        st.markdown("#### Personal Information")
        full_name = st.text_input("Full Name *")
        registration_number = st.text_input("Registration Number *")
        phone_number = st.text_input("WhatsApp / Phone Number *", placeholder="e.g. 0744 215 379")
        email = st.text_input("Email Address *", placeholder="e.g. name@example.com")

        st.markdown("#### Academic Information")
        engineering_program = st.selectbox("Engineering Program *", ENGINEERING_PROGRAMS)
        other_engineering_program = ""
        if engineering_program == "Other":
            other_engineering_program = st.text_input("Please specify your engineering program *")

        year_of_study = st.selectbox("Year of Study *", YEARS_OF_STUDY)

        st.markdown("#### Programming Background")
        programming_experience = st.selectbox(
            "Previous programming experience *", PROGRAMMING_EXPERIENCE_LEVELS
        )
        technologies_used = st.multiselect(
            "Technologies previously used", TECHNOLOGIES_KNOWN, default=[]
        )
        how_heard = st.selectbox("How did you hear about Coddy Buddy?", REFERRAL_SOURCES)
        other_referral_source = ""
        if how_heard == "Other":
            other_referral_source = st.text_input("Please specify how you heard about us *")

        st.markdown("#### Motivation")
        motivation = st.text_area("Why do you want to join Coddy Buddy? *")
        engineering_problem = st.text_area(
            "What engineering problem would you like to solve using software?"
        )
        saturday_availability = st.radio(
            "Can you attend the Saturday sessions? *", ATTENDANCE_OPTIONS, horizontal=True
        )

        submitted = st.form_submit_button("Submit Registration")

    if not submitted:
        return

    form_data = {
        "full_name": full_name,
        "registration_number": registration_number,
        "phone_number": phone_number,
        "email": email,
        "engineering_program": engineering_program,
        "other_engineering_program": other_engineering_program,
        "year_of_study": year_of_study,
        "programming_experience": programming_experience,
        "how_heard": how_heard,
        "other_referral_source": other_referral_source,
        "motivation": motivation,
        "saturday_availability": saturday_availability,
    }

    errors = validate_registration_form(form_data)
    if errors:
        for error in errors:
            st.error(error)
        return

    try:
        if is_duplicate_registration(registration_number):
            st.warning(MSG_DUPLICATE_REGISTRATION)
            return

        row_data = {
            "Full Name": full_name.strip(),
            "Registration Number": registration_number.strip(),
            "Phone Number": phone_number.strip(),
            "Email": email.strip(),
            "Engineering Program": engineering_program,
            "Other Engineering Program": other_engineering_program.strip(),
            "Year of Study": year_of_study,
            "Programming Experience": programming_experience,
            "Technologies Used": ", ".join(technologies_used),
            "How They Heard": how_heard,
            "Other Referral Source": other_referral_source.strip(),
            "Motivation": motivation.strip(),
            "Engineering Problem": engineering_problem.strip(),
            "Saturday Availability": saturday_availability,
        }
        add_registration(row_data)
        st.session_state.registration_submitted = True
        st.session_state.last_registered_name = full_name.strip()
        st.rerun()

    except GoogleSheetsError:
        st.error(MSG_SERVICE_UNAVAILABLE)
    except Exception:  # noqa: BLE001
        st.error(MSG_SERVICE_UNAVAILABLE)


def render_register_page():
    if st.session_state.get("registration_submitted"):
        render_registration_success()
    else:
        render_registration_form()


# ----------------------------------------------------------------------
# ADMIN PAGE
# ----------------------------------------------------------------------
def check_admin_password() -> bool:
    """Render a password prompt and return True once authenticated."""
    if st.session_state.get("admin_authenticated"):
        return True

    st.markdown("### 🔒 Admin Login")

    if "admin_password" not in st.secrets:
        st.error(MSG_MISSING_CONFIG)
        return False

    with st.form("admin_login_form"):
        password = st.text_input("Admin Password", type="password")
        login_submitted = st.form_submit_button("Log In")

    if login_submitted:
        if password == st.secrets["admin_password"]:
            st.session_state.admin_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

    return False


def render_admin_dashboard():
    st.markdown("### 📊 Admin Dashboard")

    top_col1, top_col2 = st.columns([4, 1])
    with top_col2:
        if st.button("Log Out"):
            st.session_state.admin_authenticated = False
            st.rerun()

    try:
        df = get_all_registrations()
    except GoogleSheetsError as exc:
        st.error(MSG_SERVICE_UNAVAILABLE)
        # Safe to show technical detail here: this page is already
        # password-protected, so only the authenticated admin sees it.
        with st.expander("Technical details (admin only)"):
            st.code(str(exc))
            if exc.__cause__:
                st.code(f"{type(exc.__cause__).__name__}: {exc.__cause__}")
        return
    except Exception as exc:  # noqa: BLE001
        st.error(MSG_SERVICE_UNAVAILABLE)
        with st.expander("Technical details (admin only)"):
            st.code(f"{type(exc).__name__}: {exc}")
        return

    stats = get_statistics(df)

    if stats["total_students"] == 0:
        st.info("No registrations yet. Check back once students start signing up.")
        return

    st.metric("Total Registered Students", stats["total_students"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### By Engineering Program")
        if not stats["by_program"].empty:
            st.bar_chart(stats["by_program"])

        st.markdown("#### By Year of Study")
        if not stats["by_year"].empty:
            st.bar_chart(stats["by_year"])

        st.markdown("#### Saturday Availability")
        if not stats["by_availability"].empty:
            st.bar_chart(stats["by_availability"])

    with col2:
        st.markdown("#### By Programming Experience")
        if not stats["by_experience"].empty:
            st.bar_chart(stats["by_experience"])

        st.markdown("#### Technologies Students Already Know")
        if not stats["by_technology"].empty:
            st.bar_chart(stats["by_technology"])

    st.markdown("#### Registered Students")
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Registrations as CSV",
        data=csv_data,
        file_name="coddy_buddy_registrations.csv",
        mime="text/csv",
    )


def render_admin_page():
    if check_admin_password():
        render_admin_dashboard()


# ----------------------------------------------------------------------
# NAVIGATION / MAIN
# ----------------------------------------------------------------------
def main():
    if "registration_submitted" not in st.session_state:
        st.session_state.registration_submitted = False
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if "last_registered_name" not in st.session_state:
        st.session_state.last_registered_name = ""
    if "nav_choice" not in st.session_state:
        st.session_state.nav_choice = "Home"

    nav_options = ["Home", "Register", "Admin"]

    with st.sidebar:
        st.markdown(f"## {PROGRAM_NAME}")
        st.caption(PROGRAM_TAGLINE)
        page = st.radio(
            "Navigate",
            nav_options,
            key="nav_choice",
            label_visibility="collapsed",
        )
        st.markdown("---")
        st.caption(f"Coding with {PROGRAM_LEAD_NAME}")
        st.caption(f"WhatsApp: {PROGRAM_LEAD_WHATSAPP}")

    if page == "Home":
        render_home_page()
    elif page == "Register":
        render_register_page()
    elif page == "Admin":
        render_admin_page()

    render_copyright_footer()


if __name__ == "__main__":
    main()