# bad/libuser.py
import os
import sqlite3
import bcrypt

DB = os.path.join(os.path.dirname(__file__), "db_users.sqlite")


def _get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def _is_bcrypt_hash(s):
    return isinstance(s, str) and s.startswith("$2")


def _rehash_if_plain(username, plain_password):
    """
    If password was stored plaintext and matches plain_password, replace it with bcrypt hash.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if not row:
            return
        stored = row["password"]
        if stored is None:
            return
        if not _is_bcrypt_hash(stored) and stored == plain_password:
            new_hash = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()
            cur.execute("UPDATE users SET password = ? WHERE username = ?", (new_hash, username))
            conn.commit()
    finally:
        conn.close()


def login(username, password):
    """
    Returns username on success, False on failure.
    Supports existing plaintext passwords (will re-hash them) and bcrypt-hashed passwords.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT username, password, failures, mfa_enabled, mfa_secret, role FROM users WHERE username = ?",
            (username,),
        )
        user = cur.fetchone()
        if not user:
            return False
        stored = user["password"]
        if stored is None:
            return False

        # If stored password is a bcrypt hash
        if _is_bcrypt_hash(stored):
            try:
                ok = bcrypt.checkpw(password.encode(), stored.encode())
            except Exception:
                ok = False
            if ok:
                return user["username"]
            return False
        else:
            # stored as plaintext (legacy) - compare directly
            if stored == password:
                # re-hash to bcrypt for future
                new_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                try:
                    cur.execute("UPDATE users SET password = ? WHERE username = ?", (new_hash, username))
                    conn.commit()
                except Exception:
                    pass
                return user["username"]
            return False
    finally:
        conn.close()


def create(username, password, role="user"):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password, failures, mfa_enabled, mfa_secret, role) VALUES (?, ?, ?, ?, ?, ?)",
            (username, pw_hash, 0, 0, "", role),
        )
        conn.commit()
    finally:
        conn.close()


def userlist():
    conn = _get_conn()
    try:
        cur = conn.cursor()
        users = cur.execute("SELECT username FROM users").fetchall()
        if not users:
            return []
        return [u["username"] for u in users]
    finally:
        conn.close()


def password_change(username, password):
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = ? WHERE username = ?", (pw_hash, username))
        conn.commit()
        return True
    finally:
        conn.close()


def password_complexity(password):
    return True