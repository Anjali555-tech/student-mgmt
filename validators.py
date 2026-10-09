import re


def validate_name(name):
    if name is None:
        return False, "Name cannot be empty."
    name = name.strip()
    if not name:
        return False, "Name cannot be empty."
    if len(name) < 2 or len(name) > 100:
        return False, "Name must be between 2 and 100 characters."
    if not re.match(r"^[A-Za-z\s.'-]+$", name):
        return False, "Name can only contain letters, spaces, and . ' -"
    return True, name


def validate_email(email):
    if email is None:
        return False, "Email cannot be empty."
    email = email.strip().lower()
    if not email:
        return False, "Email cannot be empty."
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False, "Invalid email format."
    if len(email) > 100:
        return False, "Email too long (max 100 characters)."
    return True, email


def validate_phone(phone):
    if phone is None:
        return True, None
    phone = phone.strip()
    if not phone:
        return True, None
    cleaned = phone.replace(" ", "").replace("-", "")
    if not re.match(r"^\+?\d{10,15}$", cleaned):
        return False, "Phone must be 10-15 digits (optional + prefix)."
    return True, cleaned


def validate_branch(branch):
    if branch is None:
        return False, "Branch cannot be empty."
    branch = branch.strip().upper()
    allowed = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIML", "DS"]
    if branch not in allowed:
        return False, f"Branch must be one of: {', '.join(allowed)}"
    return True, branch


def validate_year(year):
    if year is None:
        return False, "Year cannot be empty."
    try:
        year = int(year)
    except (ValueError, TypeError):
        return False, "Year must be a number."
    if not (1 <= year <= 5):
        return False, "Year must be between 1 and 5."
    return True, year


def validate_cgpa(cgpa):
    if cgpa is None or str(cgpa).strip() == "":
        return True, None
    try:
        cgpa = float(cgpa)
    except (ValueError, TypeError):
        return False, "CGPA must be a number."
    if not (0 <= cgpa <= 10):
        return False, "CGPA must be between 0 and 10."
    return True, round(cgpa, 2)