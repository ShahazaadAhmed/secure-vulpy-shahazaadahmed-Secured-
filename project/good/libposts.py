#!/usr/bin/env python3

import sqlite3
import html
from typing import List, Dict, Any, Optional

DB = "db_posts.sqlite"
MAX_POST_LENGTH = 5000


def get_posts(username: Optional[str]) -> List[Dict[str, Any]]:
    query = "SELECT * FROM posts"
    params = ()
    if username:
        query += " WHERE username = ?"
        params = (username,)
    query += " ORDER BY date DESC"

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

    return [dict(row) for row in rows]


def post(username: str, text: str) -> bool:
    if not username or not text:
        return False
    sanitized = html.escape(text)
    if len(sanitized) > MAX_POST_LENGTH:
        sanitized = sanitized[:MAX_POST_LENGTH]

    try:
        with sqlite3.connect(DB) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO posts (username, text, date) VALUES (?, ?, DateTime('now'))",
                (username, sanitized),
            )
            conn.commit()
        return True
    except Exception:
        return False