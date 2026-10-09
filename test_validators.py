from validators import *

print(validate_name("Anjali Biradar"))     # (True, 'Anjali Biradar')
print(validate_name(""))                    # (False, 'Name cannot be empty.')
print(validate_name("A"))                   # (False, 'Name must be between...')
print(validate_email("anjali@x.com"))       # (True, 'anjali@x.com')
print(validate_email("not-an-email"))       # (False, 'Invalid email format.')
print(validate_year("3"))                   # (True, 3)
print(validate_year("10"))                  # (False, 'Year must be between...')
print(validate_branch("cse"))               # (True, 'CSE')
print(validate_branch("xyz"))               # (False, 'Branch must be one of...')
print(validate_cgpa("8.567"))               # (True, 8.57)
print(validate_cgpa("15"))                  # (False, 'CGPA must be between...')