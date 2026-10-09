import csv
import io
from flask import Response

from flask import Flask, render_template, request, redirect, url_for, flash
from student_dao import (
    add_student,
    get_all_students,
    get_student_by_id,
    get_students_paginated,
    search_students,
    update_student,
    delete_student,
    get_statistics,
    get_students_paginated,
)

app = Flask(__name__)
app.secret_key = "change-this-to-something-random"


# ---------- HOME: list all students ----------
@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 3

    students, total = get_students_paginated(page=page, per_page=per_page)
    total_pages = (total + per_page - 1) // per_page  # ceil division

    return render_template(
        "index.html",
        students=students,
        page=page,
        total_pages=total_pages,
        total=total,
    )


# ---------- ADD ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        success, message = add_student(
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone") or None,
            branch=request.form.get("branch"),
            year=request.form.get("year"),
            cgpa=request.form.get("cgpa") or None,
        )
        if success:
            flash(message, "success")
            return redirect(url_for("index"))
        else:
            flash(message, "error")

    return render_template("add.html")


# ---------- EDIT ----------
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id):
    student = get_student_by_id(student_id)
    if not student:
        flash(f"No student found with ID {student_id}.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        success, message = update_student(
            student_id,
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone") or None,
            branch=request.form.get("branch"),
            year=request.form.get("year"),
            cgpa=request.form.get("cgpa") or None,
        )
        if success:
            flash(message, "success")
            return redirect(url_for("index"))
        else:
            flash(message, "error")

    return render_template("edit.html", student=student)


# ---------- DELETE ----------
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete(student_id):
    success, message = delete_student(student_id)
    flash(message, "success" if success else "error")
    return redirect(url_for("index"))


# ---------- SEARCH ----------
@app.route("/search")
def search():
    name = request.args.get("name") or None
    branch = request.args.get("branch") or None
    year = request.args.get("year") or None

    results = None
    if any([name, branch, year]):
        results = search_students(name=name, branch=branch, year=year)

    return render_template("search.html", results=results)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    stats = get_statistics()
    return render_template("dashboard.html", stats=stats)

# ---------- EXPORT CSV ----------
@app.route("/export")
def export_csv():
    students = get_all_students()

    # Write to an in-memory text buffer
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(["ID", "Name", "Email", "Phone", "Branch", "Year", "CGPA", "Created At"])

    # Data rows
    for s in students:
        writer.writerow([
            s["id"], s["name"], s["email"], s["phone"] or "",
            s["branch"], s["year"], s["cgpa"] or "", s["created_at"]
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=students.csv"
        }
    )
if __name__ == "__main__":
    app.run(debug=True)