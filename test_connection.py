import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="9900559278",
        database="student_db"
    )
    print("✅ Connected to MySQL successfully!")
    print(f"MySQL version: {conn.get_server_info()}")
    conn.close()
    print("Connection closed.")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")