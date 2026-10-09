from student_dao import *

print("--- Add valid student ---")
print(add_student("Ravi Verma", "ravi@x.com", "9998887770", "IT", 2, 7.5))

print("\n--- Add duplicate email (should fail) ---")
print(add_student("Duplicate Guy", "ravi@x.com", "9998887771", "CSE", 1, 6.0))

print("\n--- Add invalid branch (should fail) ---")
print(add_student("Bad Branch", "bad@x.com", "9998887772", "XYZ", 2, 7.0))

print("\n--- Add invalid year (should fail) ---")
print(add_student("Bad Year", "bad2@x.com", "9998887773", "CSE", 99, 7.0))

print("\n--- Search CSE students ---")
for s in search_students(branch="CSE"):
    print(s["id"], s["name"], s["branch"], s["year"])

print("\n--- Search name contains 'an' ---")
for s in search_students(name="an"):
    print(s["id"], s["name"])

print("\n--- Update Ravi's CGPA ---")
print(update_student(6, cgpa=8.0))  # adjust ID if needed

print("\n--- Delete Ravi ---")
print(delete_student(6))  # adjust ID if needed