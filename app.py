from flask import Flask, render_template, request, redirect, url_for, flash
from student_dao import (
    add_student, get_all_students, get_student_by_id,
    search_students, update_student, delete_student
)

app = Flask(__name__)
app.secret_key = "change-this-to-something-random"  # Needed for flash messages


# ---------- HOME: list all students ----------
@app.route("/")
def index():
    students = get_all_students()
    return render_template("index.html", students=students)


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


if __name__ == "__main__":
    app.run(debug=True)