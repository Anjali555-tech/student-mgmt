from student_dao import (
    add_student, get_all_students, get_student_by_id,
    search_students, update_student, delete_student
)


def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_table(students):
    """Pretty print a list of student dicts."""
    if not students:
        print("  (No students found)")
        return

    print(f"\n  {'ID':<5} {'Name':<22} {'Email':<28} {'Branch':<8} {'Yr':<4} {'CGPA':<6}")
    print("  " + "-" * 80)
    for s in students:
        cgpa = f"{s['cgpa']:.2f}" if s['cgpa'] is not None else "-"
        phone = s['phone'] or "-"
        print(f"  {s['id']:<5} {s['name']:<22} {s['email']:<28} {s['branch']:<8} {s['year']:<4} {cgpa:<6}")
    print(f"\n  Total: {len(students)} student(s)")


def prompt(label, optional=False):
    """Ask for input. If optional, allow blank."""
    marker = " (optional, press Enter to skip)" if optional else ""
    value = input(f"  {label}{marker}: ").strip()
    return value if value else None


# ============================================
# MENU ACTIONS
# ============================================

def action_add():
    print_header("ADD NEW STUDENT")
    name = prompt("Name")
    email = prompt("Email")
    phone = prompt("Phone", optional=True)
    branch = prompt("Branch (CSE/ECE/EEE/MECH/CIVIL/IT/AIML/DS)")
    year = prompt("Year (1-5)")
    cgpa = prompt("CGPA (0-10)", optional=True)

    success, message = add_student(name, email, phone, branch, year, cgpa)
    print(f"\n  {'✅' if success else '❌'} {message}")


def action_view_all():
    print_header("ALL STUDENTS")
    students = get_all_students()
    print_table(students)


def action_search():
    print_header("SEARCH / FILTER")
    print("  Leave blank to skip any filter.\n")
    name = prompt("Name contains", optional=True)
    branch = prompt("Branch", optional=True)
    year = prompt("Year", optional=True)

    students = search_students(name=name, branch=branch, year=year)
    print_table(students)


def action_update():
    print_header("UPDATE STUDENT")
    sid = prompt("Student ID to update")

    student = get_student_by_id(sid)
    if not student:
        print(f"\n  ❌ No student found with ID {sid}.")
        return

    print(f"\n  Current: {student['name']} | {student['email']} | {student['branch']} | Year {student['year']}")
    print("\n  Leave blank to keep current value.\n")

    name = prompt(f"New name [{student['name']}]", optional=True)
    email = prompt(f"New email [{student['email']}]", optional=True)
    phone = prompt(f"New phone [{student['phone']}]", optional=True)
    branch = prompt(f"New branch [{student['branch']}]", optional=True)
    year = prompt(f"New year [{student['year']}]", optional=True)
    cgpa = prompt(f"New CGPA [{student['cgpa']}]", optional=True)

    success, message = update_student(
        sid, name=name, email=email, phone=phone,
        branch=branch, year=year, cgpa=cgpa
    )
    print(f"\n  {'✅' if success else '❌'} {message}")


def action_delete():
    print_header("DELETE STUDENT")
    sid = prompt("Student ID to delete")

    student = get_student_by_id(sid)
    if not student:
        print(f"\n  ❌ No student found with ID {sid}.")
        return

    print(f"\n  About to delete: {student['name']} ({student['email']})")
    confirm = input("  Type 'yes' to confirm: ").strip().lower()
    if confirm != "yes":
        print("\n  ❌ Cancelled.")
        return

    success, message = delete_student(sid)
    print(f"\n  {'✅' if success else '❌'} {message}")


# ============================================
# MAIN MENU LOOP
# ============================================

def main():
    while True:
        print("\n" + "=" * 50)
        print("  🎓 STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search / Filter")
        print("  4. Update Student")
        print("  5. Delete Student")
        print("  6. Exit")
        print("=" * 50)

        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            action_add()
        elif choice == "2":
            action_view_all()
        elif choice == "3":
            action_search()
        elif choice == "4":
            action_update()
        elif choice == "5":
            action_delete()
        elif choice == "6":
            print("\n  👋 Goodbye!\n")
            break
        else:
            print("\n  ❌ Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()