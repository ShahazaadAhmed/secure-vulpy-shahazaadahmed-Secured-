import secrets

def ensure_csrf(session):
    if not session:
        return None
    if '_csrf' not in session or not session.get('_csrf'):
        session['_csrf'] = secrets.token_urlsafe(32)
    return session.get('_csrf')

def validate_csrf(session, token):
    if not session or not token:
        return False
    return session.get('_csrf') == token
