"""
validation.py

Form validation helpers for the Coddy Buddy registration form.
All functions are pure (no Streamlit calls) so they are easy to test.
"""

import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Accepts numbers like: 0744215379, +256744215379, 256 744 215 379, 0744-215-379
PHONE_REGEX = re.compile(r"^[+]?[\d\s\-]{7,15}$")


def is_valid_email(email: str) -> bool:
    """Return True if the given string looks like a valid email address."""
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_valid_phone(phone: str) -> bool:
    """Return True if the given string looks like a reasonable phone number."""
    if not phone:
        return False
    cleaned = phone.strip()
    if not PHONE_REGEX.match(cleaned):
        return False
    digit_count = len(re.sub(r"\D", "", cleaned))
    # A reasonable phone number has between 9 and 13 digits
    return 9 <= digit_count <= 13


def is_non_empty(value: str) -> bool:
    """Return True if the given string has actual (non-whitespace) content."""
    return bool(value and value.strip())


def validate_registration_form(form_data: dict) -> list:
    """
    Validate the full registration form.

    Parameters
    ----------
    form_data : dict
        Dictionary containing the raw form values collected from the
        Streamlit widgets.

    Returns
    -------
    list[str]
        A list of human-readable error messages. An empty list means the
        form passed validation.
    """
    errors = []

    if not is_non_empty(form_data.get("full_name", "")):
        errors.append("Full Name is required.")

    if not is_non_empty(form_data.get("registration_number", "")):
        errors.append("Registration Number is required.")

    phone = form_data.get("phone_number", "")
    if not is_non_empty(phone):
        errors.append("WhatsApp / Phone Number is required.")
    elif not is_valid_phone(phone):
        errors.append("Please enter a valid phone number (e.g. 0744 215 379).")

    email = form_data.get("email", "")
    if not is_non_empty(email):
        errors.append("Email Address is required.")
    elif not is_valid_email(email):
        errors.append("Please enter a valid email address.")

    engineering_program = form_data.get("engineering_program", "")
    if not is_non_empty(engineering_program):
        errors.append("Engineering Program is required.")
    elif engineering_program == "Other" and not is_non_empty(
        form_data.get("other_engineering_program", "")
    ):
        errors.append("Please specify your engineering program.")

    if not is_non_empty(form_data.get("year_of_study", "")):
        errors.append("Year of Study is required.")

    if not is_non_empty(form_data.get("programming_experience", "")):
        errors.append("Previous programming experience is required.")

    how_heard = form_data.get("how_heard", "")
    if how_heard == "Other" and not is_non_empty(
        form_data.get("other_referral_source", "")
    ):
        errors.append("Please specify how you heard about Coddy Buddy.")

    if not is_non_empty(form_data.get("motivation", "")):
        errors.append("Please tell us why you want to join Coddy Buddy.")

    if not is_non_empty(form_data.get("saturday_availability", "")):
        errors.append("Please let us know if you can attend Saturday sessions.")

    return errors