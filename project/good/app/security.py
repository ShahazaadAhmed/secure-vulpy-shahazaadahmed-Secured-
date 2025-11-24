from functools import wraps
from flask import session, redirect, url_for, abort

def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role = session.get('role')
            if not role:
                return redirect(url_for('login'))
            if role != required_role:
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator
