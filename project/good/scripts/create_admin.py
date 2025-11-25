import sqlite3, os, sys

DB_PATH = "D:/p&ps/Secure_web/CA-2/Sapp/project/bad/db_users.sqlite"
ADMIN_USER = "admin"
ADMIN_PASS = "galgate1234"
HAS_BCRYPT = False
try:
    import bcrypt
    HAS_BCRYPT = True
except Exception:
    HAS_BCRYPT = False

def get_table_columns(cur, table):
    cur.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cur.fetchall()]

def find_column(columns, names):
    for n in names:
        for c in columns:
            if n.lower() == c.lower() or n.lower() in c.lower():
                return c
    return None

def main():
    if not os.path.exists(DB_PATH):
        print("DB not found at", DB_PATH)
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    table = "users"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    if not cur.fetchone():
        print(f"Table '{table}' not found. Available tables:")
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for r in cur.fetchall():
            print(" ", r[0])
        conn.close()
        sys.exit(1)

    cols = get_table_columns(cur, table)
    print("Detected columns:", cols)

    username_col = find_column(cols, ["username", "user", "login", "email", "name"])
    password_col = find_column(cols, ["password_hash", "password", "passwd", "pw", "pwd"])
    role_col = find_column(cols, ["role"])

    if not username_col:
        print("Could not detect username column. Columns:", cols)
        conn.close()
        sys.exit(1)
    if not password_col:
        print("Could not detect password column. Columns:", cols)
        conn.close()
        sys.exit(1)
    cur.execute(f"SELECT COUNT(*) FROM {table} WHERE {username_col} = ?", (ADMIN_USER,))
    exists = cur.fetchone()[0]
    if exists:
        print("Admin user already exists.")
        conn.close()
        return
    use_hash = False
    if "hash" in password_col.lower() or "pw" in password_col.lower() or "pass" in password_col.lower() and password_col.lower() != "password":
        use_hash = True if HAS_BCRYPT else False
    else:
        use_hash = False

    if use_hash and not HAS_BCRYPT:
        print("bcrypt not installed, but password column seems to expect hashed passwords.")
        print("Install bcrypt (python -m pip install bcrypt) or the script will insert plaintext instead.")
        use_hash = False

    if use_hash:
        pw_hash = bcrypt.hashpw(ADMIN_PASS.encode(), bcrypt.gensalt()).decode()
        insert_pw = pw_hash
        print("Storing bcrypt hash in password column (detected hashed-password column).")
    else:
        insert_pw = ADMIN_PASS
        print("Storing plaintext password in password column (detected plaintext-password column or fallback).")

    insert_cols = [username_col, password_col]
    insert_vals = [ADMIN_USER, insert_pw]
    if role_col:
        insert_cols.append(role_col)
        insert_vals.append("admin")

    placeholders = ",".join(["?"] * len(insert_cols))
    col_list = ",".join(insert_cols)
    try:
        cur.execute(f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})", tuple(insert_vals))
        conn.commit()
        print(f"Admin '{ADMIN_USER}' created with password '{ADMIN_PASS}'.")
        if not role_col:
            print("Warning: 'role' column not found; consider running add_role_column.py")
    except Exception as e:
        print("Insert error:", e)
    conn.close()

if __name__ == '__main__':
    main()