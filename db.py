import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---- Configuration ----
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),   # 🔑 Read from .env, not hardcoded
    "database": "student_db"
}


def get_connection():
    """Return a fresh MySQL connection, or None if it fails."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as err:
        print(f"❌ Database connection failed: {err}")
        return None