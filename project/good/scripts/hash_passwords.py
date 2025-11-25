#!/usr/bin/env python3
import sqlite3, os
import bcrypt

DB = os.path.join("D:/p&ps/Secure_web/CA-2/app/project/bad/db_users.sqlite")

def is_bcrypt(s):
    try:
        return isinstance(s, str) and s.startswith("$2")
    except Exception:
        return False

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("SELECT username, password FROM users")
rows = cur.fetchall()
updated = 0
for username, password in rows:
    if password is None:
        continue
    if not is_bcrypt(password):
        new_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cur.execute("UPDATE users SET password = ? WHERE username = ?", (new_hash, username))
        updated += 1
conn.commit()
conn.close()
print("Applied bcrypt to %d users" % updated)