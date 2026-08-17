"""
app.py

Main entry point for the Coddy Buddy Community Portal.
"""

from datetime import datetime

import streamlit as st

from utils.constants import (
    COMMUNITY_WHATSAPP_GROUP_LINK,
    COPYRIGHT_TEXT,
    LEARNING_PATH,
    MSG_DUPLICATE_REGISTRATION,
    MSG_MISSING_CONFIG,
    MSG_SERVICE_UNAVAILABLE,
    PROGRAM_DESCRIPTION,
    PROGRAM_FOCUS,
    PROGRAM_FREE_TEXT,
    PROGRAM_INTRO,
    PROGRAM_LEAD_NAME,
    PROGRAM_LEAD_WHATSAPP,
    PROGRAM_NAME,
    PROGRAM_SCHEDULE,
    PROGRAM_TAGLINE,
    PROGRAM_TIME,
    PROGRAM_VENUE,
    PROJECT_EXAMPLES,
    REFERRAL_SOURCES,
    SATURDAY_OPTIONS,
    STUDENT_OPTIONS,
    PROGRAMMING_EXPERIENCE_LEVELS,
    WHO_CAN_JOIN,
    TECHNOLOGIES_KNOWN,
)
from utils.google_sheets import (
    GoogleSheetsError,
    add_registration,
    get_all_registrations,
    get_summary_tables,
    is_duplicate_registration,
)
from utils.validation import validate_registration_form

st.set_page_config(
    page_title="Coddy Buddy | Community Portal",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
:root {
    --navy: #07111f;
    --navy-2: #0c1d33;
    --card: rgba(255,255,255,0.05);
    --border: rgba(34, 211, 238, 0.18);
    --cyan: #22d3ee;
    --green: #34d399;
    --white: #f8fafc;
}
.stApp { background: linear-gradient(180deg, var(--navy-2), var(--navy)); color: var(--white); }
h1,h2,h3,h4,p,li,label { color: var(--white) !important; }
.cb-hero { padding: 2rem 0 1rem; text-align:center; }
.cb-title { font-size: 3rem; font-weight: 900; letter-spacing: 2px; background: linear-gradient(90deg, var(--cyan), var(--green)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.cb-subtitle { font-size: 1.2rem; font-weight: 700; }
.cb-desc { color: #cbd5e1; max-width: 860px; margin: 0 auto; }
.cb-section { background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 1.2rem; margin: 0.9rem 0; }
.cb-card { background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: 18px; padding: 1rem; height: 100%; }
.cb-pill { display:inline-block; padding: .35rem .75rem; margin: .25rem .25rem 0 0; border-radius: 999px; background: rgba(34,211,238,.12); color: var(--cyan); border: 1px solid rgba(34,211,238,.25); }
.stButton > button, div[data-testid="stFormSubmitButton"] > button { width:100%; background: linear-gradient(90deg, var(--cyan), var(--green)) !important; color:#04141f !important; font-weight:800 !important; border:none !important; border-radius: 12px !important; }
.cb-success { text-align:center; padding: 1.8rem; border-radius: 18px; border: 1px solid rgba(52,211,153,.4); background: rgba(52,211,153,.08); }
.cb-whatsapp-box { margin: 1.4rem auto 0.6rem; max-width: 520px; padding: 1.1rem 1.2rem; border-radius: 16px; background: rgba(37,211,102,.10); border: 1px solid rgba(37,211,102,.45); }
.cb-whatsapp-box p { margin: 0 0 0.9rem; }
.cb-whatsapp-btn { display:inline-block; padding: 0.85rem 1.8rem; border-radius: 999px; background: #25D366; color: #04140c !important; font-weight: 800; text-decoration: none !important; font-size: 1.05rem; box-shadow: 0 4px 14px rgba(37,211,102,.35); transition: transform .12s ease; }
.cb-whatsapp-btn:hover { transform: translateY(-2px); }

/* Fix: form field text was inheriting the page's white text color and
   landing on a light input background, making it invisible while typing.
   Force a readable dark text color (and background) on every input type. */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input {
    color: #0f172a !important;
    background-color: #f8fafc !important;
    caret-color: #0f172a !important;
    border: 1px solid var(--border) !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}
/* Selectbox / multiselect (built on BaseWeb) */
div[data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border-color: var(--border) !important;
}
div[data-baseweb="select"] input {
    color: #0f172a !important;
}
div[data-baseweb="select"] span {
    color: #0f172a !important;
}
/* Dropdown menu / options list */
ul[data-baseweb="menu"] li,
li[role="option"] {
    color: #0f172a !important;
    background-color: #f8fafc !important;
}
/* Multiselect selected-item tags */
span[data-baseweb="tag"] {
    color: #04141f !important;
    background-color: rgba(34,211,238,.35) !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def _is_secret_admin_entry() -> bool:
    """
    True only when the site is opened with the private admin query param,
    e.g. https://your-app-url/?admin=<key>

    The expected value defaults to "1" but can be overridden with
    `admin_url_key` in secrets.toml so the URL isn't guessable.
    """
    expected = str(st.secrets.get("admin_url_key", "1"))
    value = st.query_params.get("admin")
    return value == expected


def render_hero():
    st.markdown(
        f"""
        <div class="cb-hero">
            <div class="cb-title">{PROGRAM_NAME}</div>
            <div class="cb-subtitle">{PROGRAM_TAGLINE}</div>
            <p class="cb-desc">{PROGRAM_INTRO}</p>
            <p><strong>{PROGRAM_DESCRIPTION}</strong> · {PROGRAM_FOCUS}</p>
            <p><strong>No prior programming experience is required.</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_nav():
    return st.radio(
        "Navigate",
        ["Home", "About", "Program", "Projects", "Register", "Contact"],
        horizontal=True,
        label_visibility="collapsed",
    )


def render_card(title, body):
    st.markdown(f'<div class="cb-card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)


def home_page():
    render_hero()
    c1, c2 = st.columns(2)
    with c1:
        st.button("🚀 JOIN CODDY BUDDY", use_container_width=True, on_click=lambda: st.session_state.update(page="Register"))
    with c2:
        if st.button("📚 Explore the Program", use_container_width=True):
            st.session_state.page = "Program"

    st.markdown("## Key Value")
    a, b, c = st.columns(3)
    with a:
        render_card("🌱 LEARN", "Develop practical software development skills from beginner level.")
    with b:
        render_card("🚀 BUILD", "Turn ideas and real-world problems into working applications.")
    with c:
        render_card("🤝 COLLABORATE", "Learn with other students, developers and technology enthusiasts.")

    st.markdown("## WHO IS CODDY BUDDY FOR?")
    pills = "".join([f'<span class="cb-pill">{item}</span>' for item in WHO_CAN_JOIN])
    st.markdown(f"<div class='cb-section'>{pills}<p><strong>NO PRIOR PROGRAMMING EXPERIENCE REQUIRED</strong></p></div>", unsafe_allow_html=True)

    st.markdown("## THIS SEMESTER")
    st.markdown(f"<div class='cb-section'><h3>{PROGRAM_FOCUS}</h3><p>{PROGRAM_SCHEDULE} | {PROGRAM_TIME} | <strong>{PROGRAM_FREE_TEXT}</strong></p></div>", unsafe_allow_html=True)
    path = "<br>↓<br>".join(LEARNING_PATH)
    st.markdown(f"<div class='cb-section'><strong>{path}</strong></div>", unsafe_allow_html=True)

    st.markdown("## YOU WON'T JUST LEARN CODE. YOU WILL BUILD.")
    st.info("Coddy Buddy focuses on learning by doing. Participants will work on practical projects and learn how to turn ideas and real-world problems into software solutions.")
    st.write("Examples of what participants could build:")
    st.write("\n".join([f"• {item}" for item in PROJECT_EXAMPLES]))

    st.markdown("## LEARN → PRACTICE → BUILD → COLLABORATE → DEPLOY")
    st.write("Participants learn a concept, practice it, apply it to a project, collaborate with others, build complete applications, and eventually deploy their work.")

    st.markdown("## WEEKLY SESSIONS")
    st.markdown(f"<div class='cb-section'><h3>{PROGRAM_SCHEDULE}</h3><p><strong>⏰ {PROGRAM_TIME}</strong><br>📍 {PROGRAM_VENUE}<br>💰 <strong>{PROGRAM_FREE_TEXT}</strong></p></div>", unsafe_allow_html=True)


def about_page():
    st.markdown("## What is Coddy Buddy?")
    st.write("Coddy Buddy is a student-led technology community focused on practical learning, collaboration and building real-world software solutions.")
    st.write("It is designed to make software development more accessible to beginners while also giving experienced participants opportunities to collaborate, mentor and build.")
    st.success("Learn → Build → Collaborate → Innovate")


def program_page():
    st.markdown(f"## CURRENT PROGRAM\n### {PROGRAM_FOCUS}")
    stages = {
        "Stage 1 — Foundations": ["HTML", "CSS", "JavaScript", "Git/GitHub"],
        "Stage 2 — Frontend": ["React"],
        "Stage 3 — Backend": ["Python", "Django", "Django REST Framework"],
        "Stage 4 — Full Stack": ["React + DRF", "APIs", "Authentication", "Databases"],
        "Stage 5 — Building": ["Team projects", "Deployment", "Project presentation"],
    }
    for title, items in stages.items():
        st.markdown(f"### {title}")
        st.write("\n".join([f"• {item}" for item in items]))


def projects_page():
    st.markdown("## BUILD REAL THINGS")
    st.write("Participants will eventually work on practical projects across these categories:")
    st.write("\n".join([f"• {item}" for item in ["Education", "Engineering", "Business", "Campus Life", "Community", "Productivity", "Innovation"]]))
    st.success("Your idea could become the next Coddy Buddy project.")


def contact_page():
    st.markdown("## GET IN TOUCH")
    st.write(f"**Program Lead:** {PROGRAM_LEAD_NAME}")
    st.write(f"**WhatsApp:** {PROGRAM_LEAD_WHATSAPP}")
    st.write(f"**Sessions:** {PROGRAM_SCHEDULE}, {PROGRAM_TIME}")
    st.write(f"**Venue:** {PROGRAM_VENUE}")


def success_screen():
    name = st.session_state.get("last_registered_name", "").strip()
    greeting = f"Welcome to Coddy Buddy, {name}!" if name else "Welcome to Coddy Buddy!"
    st.markdown(
        f"""
        <div class="cb-success">
            <h2>🎉 Welcome to Coddy Buddy!</h2>
            <h3>{greeting}</h3>
            <p>Your registration was successful.</p>
            <p><strong>{PROGRAM_SCHEDULE}</strong><br><strong>{PROGRAM_TIME}</strong><br>{PROGRAM_VENUE}<br><strong>{PROGRAM_FREE_TEXT}</strong></p>
            <p><strong>Learn. Build. Innovate.</strong><br>Coding with {PROGRAM_LEAD_NAME}<br>WhatsApp: {PROGRAM_LEAD_WHATSAPP}</p>
            <div class="cb-whatsapp-box">
                <p>📱 Join the official Coddy Buddy WhatsApp group to receive announcements, updates, learning materials and information about our Saturday sessions.</p>
                <a class="cb-whatsapp-btn" href="{COMMUNITY_WHATSAPP_GROUP_LINK}" target="_blank" rel="noopener noreferrer">👉 JOIN THE WHATSAPP GROUP</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def register_page():
    st.markdown("# JOIN CODDY BUDDY")
    st.caption("Start your journey. Learn. Build. Innovate.")
    st.info("The program is completely free of charge.")

    if st.session_state.get("registration_submitted"):
        success_screen()
        return

    with st.form("registration_form"):
        st.markdown("### Personal Information")
        full_name = st.text_input("Full Name")
        phone_number = st.text_input("WhatsApp / Phone Number")
        email = st.text_input("Email Address")

        st.markdown("### Background")
        student_status = st.radio("Are you currently a student?", STUDENT_OPTIONS, horizontal=True)
        institution = ""
        field_program = ""
        year_of_study = ""
        occupation_background = ""
        if student_status == "Yes":
            institution = st.text_input("Institution")
            field_program = st.text_input("Field / Program of Study")
            year_of_study = st.text_input("Year of Study")
        else:
            occupation_background = st.text_input("Occupation / Background")

        st.markdown("### Programming Experience")
        programming_experience = st.selectbox("How would you describe your programming experience?", PROGRAMMING_EXPERIENCE_LEVELS)

        st.markdown("### Technologies")
        technologies_used = st.multiselect("Which technologies have you used before?", TECHNOLOGIES_KNOWN, default=["None"])

        st.markdown("### Motivation")
        motivation = st.text_area("Why do you want to join Coddy Buddy?")
        what_to_build = st.text_area("What would you like to build?")
        goals = st.text_area("What are you hoping to achieve through Coddy Buddy?")

        st.markdown("### Availability")
        saturday_availability = st.radio("Can you attend the Saturday sessions?", SATURDAY_OPTIONS, horizontal=True)

        st.markdown("### Referral")
        referral_source = st.selectbox("How did you hear about Coddy Buddy?", REFERRAL_SOURCES)
        other_referral_source = st.text_input("If Other, please specify") if referral_source == "Other" else ""

        submitted = st.form_submit_button("Submit Registration")

    if not submitted:
        return

    form_data = {
        "full_name": full_name,
        "phone_number": phone_number,
        "email": email,
        "student_status": student_status,
        "institution": institution,
        "field_program": field_program,
        "year_of_study": year_of_study,
        "occupation_background": occupation_background,
        "programming_experience": programming_experience,
        "technologies_used": technologies_used,
        "motivation": motivation,
        "what_to_build": what_to_build,
        "goals": goals,
        "saturday_availability": saturday_availability,
        "referral_source": referral_source,
        "other_referral_source": other_referral_source,
    }
    errors = validate_registration_form(form_data)
    if errors:
        for error in errors:
            st.error(error)
        return

    try:
        if is_duplicate_registration(email, phone_number):
            st.warning(MSG_DUPLICATE_REGISTRATION)
            return
        row_data = {
            "Full Name": full_name.strip(),
            "Phone Number": phone_number.strip(),
            "Email": email.strip(),
            "Student Status": student_status,
            "Institution": institution.strip(),
            "Field/Program": field_program.strip(),
            "Year of Study": year_of_study.strip(),
            "Occupation/Background": occupation_background.strip(),
            "Programming Experience": programming_experience,
            "Technologies Used": ", ".join(technologies_used),
            "Motivation": motivation.strip(),
            "What They Want to Build": what_to_build.strip(),
            "Goals": goals.strip(),
            "Saturday Availability": saturday_availability,
            "Referral Source": referral_source,
            "Other Referral Source": other_referral_source.strip(),
        }
        add_registration(row_data)
        st.session_state.registration_submitted = True
        st.session_state.last_registered_name = full_name.strip()
        st.rerun()
    except GoogleSheetsError:
        st.error(MSG_SERVICE_UNAVAILABLE)


def admin_page():
    if not st.secrets.get("admin_password"):
        st.error(MSG_MISSING_CONFIG)
        return
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    if not st.session_state.admin_authenticated:
        with st.form("admin_login"):
            secret_code = st.text_input("Hidden Admin Access Code", type="password")
            password = st.text_input("Admin Password", type="password")
            submitted = st.form_submit_button("Open Admin Dashboard")
        if submitted:
            if secret_code != st.secrets.get("admin_access_code", ""):
                st.error("Invalid access code.")
                return
            if password == st.secrets["admin_password"]:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        return

    st.markdown("## Admin Dashboard")
    if st.button("Log Out"):
        st.session_state.admin_authenticated = False
        st.rerun()

    try:
        df = get_all_registrations()
    except GoogleSheetsError:
        st.error(MSG_SERVICE_UNAVAILABLE)
        return

    summary = get_summary_tables(df)
    if summary["total"] == 0:
        st.info("No registrations yet.")
        return

    st.metric("Total registrations", summary["total"])
    st.markdown("### Summary Tables")
    for title, key in [
        ("Students / Non-students", "students"),
        ("Programming Experience", "experience"),
        ("Saturday Availability", "availability"),
        ("Referral Source", "referrals"),
    ]:
        st.markdown(f"#### {title}")
        st.dataframe(summary[key], use_container_width=True, hide_index=True)

    st.markdown("### Registrations")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download registrations as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="coddy_buddy_registrations.csv",
        mime="text/csv",
    )


def main():
    # Private admin entry point: when the URL contains the secret ?admin=...
    # query param, show ONLY the admin dashboard - no public nav, no other
    # pages. This must be checked before anything else is rendered.
    if _is_secret_admin_entry():
        admin_page()
        st.markdown(f"---\n{COPYRIGHT_TEXT.format(year=datetime.now().year)}")
        return

    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "registration_submitted" not in st.session_state:
        st.session_state.registration_submitted = False
    if "last_registered_name" not in st.session_state:
        st.session_state.last_registered_name = ""

    st.session_state.page = render_nav()

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "About":
        about_page()
    elif st.session_state.page == "Program":
        program_page()
    elif st.session_state.page == "Projects":
        projects_page()
    elif st.session_state.page == "Register":
        register_page()
    elif st.session_state.page == "Contact":
        contact_page()

    st.markdown(f"---\n{COPYRIGHT_TEXT.format(year=datetime.now().year)}")


if __name__ == "__main__":
    main()