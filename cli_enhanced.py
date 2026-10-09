import csv
from datetime import datetime
from colorama import init, Fore, Style

from student_dao import (
    add_student, get_all_students, get_student_by_id,
    search_students, update_student, delete_student
)

# Initialize colorama (auto-resets colors on Windows)
init(autoreset=True)

# -------- Color shortcuts --------
OK = Fore.GREEN + "✅" + Style.RESET_ALL
ERR = Fore.RED + "❌" + Style.RESET_ALL
WARN = Fore.YELLOW + "⚠️ " + Style.RESET_ALL
INFO = Fore.CYAN + "ℹ️ " + Style.RESET_ALL

C_HEADER = Fore.CYAN + Style.BRIGHT
C_TITLE = Fore.MAGENTA + Style.BRIGHT
C_DIM = Style.DIM
C_ID = Fore.YELLOW
C_NAME = Fore.WHITE + Style.BRIGHT
C_BRANCH = Fore.GREEN
C_CGPA = Fore.CYAN


def print_header(title):
    print(f"\n{C_HEADER}{'=' * 55}")
    print(f"  {title}")
    print(f"{'=' * 55}{Style.RESET_ALL}")


def print_table(students):
    if not students:
        print(f"  {WARN}No students found.")
        return

    print(f"\n  {C_HEADER}{'ID':<5}{'Name':<22}{'Email':<28}{'Branch':<8}{'Yr':<4}{'CGPA':<6}{Style.RESET_ALL}")
    print(f"  {C_DIM}{'-' * 78}{Style.RESET_ALL}")

    for s in students:
        cgpa = f"{s['cgpa']:.2f}" if s['cgpa'] is not None else "—"
        print(
            f"  {C_ID}{s['id']:<5}{Style.RESET_ALL}"
            f"{C_NAME}{s['name']:<22}{Style.RESET_ALL}"
            f"{s['email']:<28}"
            f"{C_BRANCH}{s['branch']:<8}{Style.RESET_ALL}"
            f"{s['year']:<4}"
            f"{C_CGPA}{cgpa:<6}{Style.RESET_ALL}"
        )
    print(f"\n  {INFO}Total: {len(students)} student(s)")


def prompt(label, optional=False):
    marker = f" {C_DIM}(Enter to skip){Style.RESET_ALL}" if optional else ""
    value = input(f"  {Fore.YELLOW}{label}{Style.RESET_ALL}{marker}: ").strip()
    return value if value else None


# ---------- Actions ----------

def action_add():
    print_header("ADD NEW STUDENT")
    name = prompt("Name")
    email = prompt("Email")
    phone = prompt("Phone", optional=True)
    branch = prompt("Branch (CSE/ECE/EEE/MECH/CIVIL/IT/AIML/DS)")
    year = prompt("Year (1-5)")
    cgpa = prompt("CGPA (0-10)", optional=True)

    success, message = add_student(name, email, phone, branch, year, cgpa)
    print(f"\n  {OK if success else ERR} {message}")


def action_view_all():
    print_header("ALL STUDENTS")
    print_table(get_all_students())


def action_search():
    print_header("SEARCH / FILTER")
    print(f"  {INFO}Leave blank to skip any filter.\n")
    name = prompt("Name contains", optional=True)
    branch = prompt("Branch", optional=True)
    year = prompt("Year", optional=True)
    print_table(search_students(name=name, branch=branch, year=year))


def action_update():
    print_header("UPDATE STUDENT")
    sid = prompt("Student ID")
    student = get_student_by_id(sid)
    if not student:
        print(f"\n  {ERR} No student found with ID {sid}.")
        return

    print(f"\n  {INFO}Current: {C_NAME}{student['name']}{Style.RESET_ALL} | "
          f"{student['branch']} | Year {student['year']}")
    print(f"  {INFO}Leave blank to keep current value.\n")

    name = prompt(f"New name [{student['name']}]", optional=True)
    email = prompt(f"New email [{student['email']}]", optional=True)
    phone = prompt(f"New phone [{student['phone']}]", optional=True)
    branch = prompt(f"New branch [{student['branch']}]", optional=True)
    year = prompt(f"New year [{student['year']}]", optional=True)
    cgpa = prompt(f"New CGPA [{student['cgpa']}]", optional=True)

    success, message = update_student(sid, name=name, email=email, phone=phone,
                                       branch=branch, year=year, cgpa=cgpa)
    print(f"\n  {OK if success else ERR} {message}")


def action_delete():
    print_header("DELETE STUDENT")
    sid = prompt("Student ID")
    student = get_student_by_id(sid)
    if not student:
        print(f"\n  {ERR} No student found with ID {sid}.")
        return

    print(f"\n  {WARN}About to delete: {C_NAME}{student['name']}{Style.RESET_ALL} "
          f"({student['email']})")
    confirm = input(f"  Type {Fore.RED}'yes'{Style.RESET_ALL} to confirm: ").strip().lower()
    if confirm != "yes":
        print(f"\n  {INFO}Cancelled.")
        return

    success, message = delete_student(sid)
    print(f"\n  {OK if success else ERR} {message}")


# ---------- NEW: Statistics ----------

def action_stats():
    print_header("STATISTICS")
    students = get_all_students()
    if not students:
        print(f"  {WARN}No students in the database.")
        return

    total = len(students)
    cgpas = [s["cgpa"] for s in students if s["cgpa"] is not None]
    avg_cgpa = sum(cgpas) / len(cgpas) if cgpas else 0

    # Count per branch
    branches = {}
    for s in students:
        branches[s["branch"]] = branches.get(s["branch"], 0) + 1

    # Count per year
    years = {}
    for s in students:
        years[s["year"]] = years.get(s["year"], 0) + 1

    print(f"\n  {C_HEADER}📊 Overview{Style.RESET_ALL}")
    print(f"  • Total students     : {C_NAME}{total}{Style.RESET_ALL}")
    print(f"  • Average CGPA       : {C_CGPA}{avg_cgpa:.2f}{Style.RESET_ALL}")
    print(f"  • Highest CGPA       : {C_CGPA}{max(cgpas):.2f}{Style.RESET_ALL}" if cgpas else "")
    print(f"  • Lowest CGPA        : {C_CGPA}{min(cgpas):.2f}{Style.RESET_ALL}" if cgpas else "")

    print(f"\n  {C_HEADER}🏫 By Branch{Style.RESET_ALL}")
    for b, count in sorted(branches.items()):
        bar = "█" * count
        print(f"  {C_BRANCH}{b:<8}{Style.RESET_ALL} {bar} {count}")

    print(f"\n  {C_HEADER}📅 By Year{Style.RESET_ALL}")
    for y, count in sorted(years.items()):
        bar = "█" * count
        print(f"  Year {y}   {bar} {count}")


# ---------- NEW: CSV Export ----------

def action_export():
    print_header("EXPORT TO CSV")
    students = get_all_students()
    if not students:
        print(f"  {WARN}No students to export.")
        return

    filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=students[0].keys())
            writer.writeheader()
            writer.writerows(students)
        print(f"\n  {OK} Exported {len(students)} students to:")
        print(f"  {C_NAME}{filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n  {ERR} Export failed: {e}")


# ---------- Main Menu ----------

def main():
    while True:
        print(f"\n{C_TITLE}{'=' * 55}")
        print(f"  🎓 STUDENT MANAGEMENT SYSTEM {C_DIM}v2.0{Style.RESET_ALL}")
        print(f"{C_TITLE}{'=' * 55}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}1{Style.RESET_ALL}. ➕ Add Student")
        print(f"  {Fore.YELLOW}2{Style.RESET_ALL}. 📋 View All Students")
        print(f"  {Fore.YELLOW}3{Style.RESET_ALL}. 🔍 Search / Filter")
        print(f"  {Fore.YELLOW}4{Style.RESET_ALL}. ✏️  Update Student")
        print(f"  {Fore.YELLOW}5{Style.RESET_ALL}. 🗑️  Delete Student")
        print(f"  {Fore.YELLOW}6{Style.RESET_ALL}. 📊 Statistics")
        print(f"  {Fore.YELLOW}7{Style.RESET_ALL}. 💾 Export to CSV")
        print(f"  {Fore.YELLOW}8{Style.RESET_ALL}. 🚪 Exit")
        print(f"{C_TITLE}{'=' * 55}{Style.RESET_ALL}")

        choice = input(f"  {Fore.CYAN}Enter your choice (1-8):{Style.RESET_ALL} ").strip()

        actions = {
            "1": action_add, "2": action_view_all, "3": action_search,
            "4": action_update, "5": action_delete,
            "6": action_stats, "7": action_export,
        }
        if choice in actions:
            actions[choice]()
        elif choice == "8":
            print(f"\n  {OK} Goodbye!\n")
            break
        else:
            print(f"\n  {ERR} Invalid choice. Enter 1-8.")


if __name__ == "__main__":
    main()