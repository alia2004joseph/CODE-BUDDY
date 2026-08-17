"""
validation.py

Form validation helpers for the Coddy Buddy registration form.
"""

import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^[+]?[-\d\s()]{7,20}$")


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    cleaned = phone.strip()
    if not PHONE_REGEX.match(cleaned):
        return False
    digit_count = len(re.sub(r"\D", "", cleaned))
    return 9 <= digit_count <= 13


def is_non_empty(value: str) -> bool:
    return bool(value and value.strip())


def validate_registration_form(form_data: dict) -> list:
    errors = []

    if not is_non_empty(form_data.get("full_name", "")):
        errors.append("Full Name is required.")

    phone = form_data.get("phone_number", "")
    if not is_non_empty(phone):
        errors.append("WhatsApp / Phone Number is required.")
    elif not is_valid_phone(phone):
        errors.append("Please enter a valid phone number.")

    email = form_data.get("email", "")
    if not is_non_empty(email):
        errors.append("Email Address is required.")
    elif not is_valid_email(email):
        errors.append("Please enter a valid email address.")

    if not is_non_empty(form_data.get("country", "")):
        errors.append("Country is required.")

    if form_data.get("student_status") == "Yes":
        if not is_non_empty(form_data.get("institution", "")):
            errors.append("Institution is required for students.")
        if not is_non_empty(form_data.get("field_program", "")):
            errors.append("Field / Program of Study is required for students.")
        if not is_non_empty(form_data.get("year_of_study", "")):
            errors.append("Year of Study is required for students.")
    else:
        if not is_non_empty(form_data.get("occupation_background", "")):
            errors.append("Occupation / Background is required.")

    if not is_non_empty(form_data.get("programming_experience", "")):
        errors.append("Programming experience is required.")

    technologies = form_data.get("technologies_used", [])
    if not technologies:
        errors.append("Please select at least one technology or None.")
    if "None" in technologies and len(technologies) > 1:
        errors.append("Select either None or other technologies, not both.")

    if not is_non_empty(form_data.get("motivation", "")):
        errors.append("Please tell us why you want to join Coddy Buddy.")

    if not is_non_empty(form_data.get("what_to_build", "")):
        errors.append("Please tell us what you would like to build.")

    if not is_non_empty(form_data.get("goals", "")):
        errors.append("Please tell us what you hope to achieve through Coddy Buddy.")

    if not is_non_empty(form_data.get("saturday_availability", "")):
        errors.append("Please let us know your Saturday availability.")

    referral_source = form_data.get("referral_source", "")
    if not is_non_empty(referral_source):
        errors.append("Please tell us how you heard about Coddy Buddy.")
    elif referral_source == "Other" and not is_non_empty(form_data.get("other_referral_source", "")):
        errors.append("Please specify how you heard about Coddy Buddy.")

    return errors
