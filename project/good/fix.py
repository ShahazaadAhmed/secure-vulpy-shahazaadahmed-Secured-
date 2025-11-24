import sqlite3, os
db = os.path.join("D:/p&ps/Secure_web/CA-2/app/project/bad/db_users.sqlite")
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
conn.commit()
print("rows affected:", conn.total_changes)
conn.close()