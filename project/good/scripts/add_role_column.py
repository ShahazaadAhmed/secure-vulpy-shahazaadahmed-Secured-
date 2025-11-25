#!/usr/bin/env python3
import sqlite3
import os
DB_PATH = os.path.join("D:/p&ps/Secure_web/CA-2/Sapp/project/bad/db_users.sqlite")

def main():
    if not os.path.exists(DB_PATH):
        print("DB not found at", DB_PATH)
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
        conn.commit()
        print("Added role column.")
    except Exception as e:
        print("Role column may already exist or error:", e)
    try:
        cur.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
        conn.commit()
    except Exception as e:
        print("Update step error:", e)
    conn.close()

if __name__ == '__main__':
    main()
