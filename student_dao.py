from db import get_connection
from validators import (
    validate_name, validate_email, validate_phone,
    validate_branch, validate_year, validate_cgpa
)


# ============================================
# CREATE — Add a new student
# ============================================
def add_student(name, email, phone, branch, year, cgpa):
    """Validate inputs, then insert a new student. Returns (success, message)."""

    # Validate every field
    checks = [
        validate_name(name),
        validate_email(email),
        validate_phone(phone),
        validate_branch(branch),
        validate_year(year),
        validate_cgpa(cgpa),
    ]
    for ok, result in checks:
        if not ok:
            return False, result  # Return the first error message

    # All valid — unpack cleaned values
    _, name = validate_name(name)
    _, email = validate_email(email)
    _, phone = validate_phone(phone)
    _, branch = validate_branch(branch)
    _, year = validate_year(year)
    _, cgpa = validate_cgpa(cgpa)

    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO students (name, email, phone, branch, year, cgpa)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, email, phone, branch, year, cgpa)
        )
        conn.commit()
        new_id = cursor.lastrowid
        return True, f"Student added successfully with ID {new_id}."
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, f"Email '{email}' is already registered."
        return False, f"Error: {e}"
    finally:
        cursor.close()
        conn.close()


# ============================================
# READ — Get all students
# ============================================
def get_all_students():
    """Return a list of all students."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY id")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# ============================================
# READ — Get one student by ID
# ============================================
def get_student_by_id(student_id):
    """Return one student or None."""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


# ============================================
# SEARCH & FILTER
# ============================================
def search_students(name=None, branch=None, year=None):
    """Search by any combination of name (partial), branch, year."""
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE %s"
        params.append(f"%{name}%")
    if branch:
        query += " AND branch = %s"
        params.append(branch.upper())
    if year:
        query += " AND year = %s"
        params.append(year)

    query += " ORDER BY id"

    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# ============================================
# UPDATE — Modify an existing student
# ============================================
def update_student(student_id, name=None, email=None, phone=None,
                   branch=None, year=None, cgpa=None):
    """Update only the fields provided (others left unchanged)."""

    # Build the SET clause dynamically
    updates = []
    params = []

    if name is not None:
        ok, result = validate_name(name)
        if not ok: return False, result
        updates.append("name = %s"); params.append(result)

    if email is not None:
        ok, result = validate_email(email)
        if not ok: return False, result
        updates.append("email = %s"); params.append(result)

    if phone is not None:
        ok, result = validate_phone(phone)
        if not ok: return False, result
        updates.append("phone = %s"); params.append(result)

    if branch is not None:
        ok, result = validate_branch(branch)
        if not ok: return False, result
        updates.append("branch = %s"); params.append(result)

    if year is not None:
        ok, result = validate_year(year)
        if not ok: return False, result
        updates.append("year = %s"); params.append(result)

    if cgpa is not None:
        ok, result = validate_cgpa(cgpa)
        if not ok: return False, result
        updates.append("cgpa = %s"); params.append(result)

    if not updates:
        return False, "No fields to update."

    params.append(student_id)

    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()

        if cursor.rowcount == 0:
            return False, f"No student found with ID {student_id}."
        return True, "Student updated successfully."
    except Exception as e:
        if "Duplicate entry" in str(e):
            return False, "That email is already used by another student."
        return False, f"Error: {e}"
    finally:
        cursor.close()
        conn.close()


# ============================================
# DELETE — Remove a student
# ============================================
def delete_student(student_id):
    """Delete a student by ID. Returns (success, message)."""
    conn = get_connection()
    if not conn:
        return False, "Database connection failed."

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return False, f"No student found with ID {student_id}."
        return True, "Student deleted successfully."
    finally:
        cursor.close()
        conn.close()
def get_statistics():
    """Return summary statistics about students."""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)

        # Total + CGPA stats
        cursor.execute("""
            SELECT
                COUNT(*) AS total,
                AVG(cgpa) AS avg_cgpa,
                MAX(cgpa) AS max_cgpa,
                MIN(cgpa) AS min_cgpa
            FROM students
        """)
        summary = cursor.fetchone()

        # Count per branch
        cursor.execute("""
            SELECT branch, COUNT(*) AS count
            FROM students
            GROUP BY branch
            ORDER BY count DESC
        """)
        by_branch = cursor.fetchall()

        # Count per year
        cursor.execute("""
            SELECT year, COUNT(*) AS count
            FROM students
            GROUP BY year
            ORDER BY year
        """)
        by_year = cursor.fetchall()

        return {
            "summary": summary,
            "by_branch": by_branch,
            "by_year": by_year,
        }
    finally:
        cursor.close()
        conn.close()

def get_students_paginated(page=1, per_page=10):
    """Return a page of students + total count."""
    conn = get_connection()
    if not conn:
        return [], 0

    try:
        cursor = conn.cursor(dictionary=True)

        # Total count
        cursor.execute("SELECT COUNT(*) AS total FROM students")
        total = cursor.fetchone()["total"]

        # Page data
        offset = (page - 1) * per_page
        cursor.execute(
            "SELECT * FROM students ORDER BY id LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        students = cursor.fetchall()

        return students, total
    finally:
        cursor.close()
        conn.close()