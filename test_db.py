from db import get_connection

conn = get_connection()
if conn:
    print("✅ db.py works! Connection opened.")
    conn.close()
    print("Closed.")
else:
    print("❌ db.py failed.")