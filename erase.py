import sqlite3
import os

DB_PATH = "transcripts.db"

# Confirm before deleting
confirm = input(f"Are you sure you want to erase all data in {DB_PATH}? Type YES to confirm: ")
if confirm != "YES":
    print("Operation canceled.")
    exit()

# Check if DB exists
if not os.path.exists(DB_PATH):
    print(f"{DB_PATH} does not exist.")
    exit()

# Connect and clear table
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

try:
    c.execute("DELETE FROM transcripts")
    conn.commit()
    print("✅ All records have been erased from the database.")
except sqlite3.Error as e:
    print("Error:", e)
finally:
    conn.close()
