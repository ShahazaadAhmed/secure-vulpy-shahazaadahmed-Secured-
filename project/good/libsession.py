import json
import base64

COOKIE_NAME = "vulpy_session"
MAX_AGE = 60 * 60 * 24

def create(response, username):
    session = {'username': username}
    cookie_val = base64.b64encode(json.dumps(session).encode()).decode('ascii')
    response.set_cookie(COOKIE_NAME, cookie_val, httponly=True, samesite='Lax', max_age=MAX_AGE)
    return response

def load(request):
    session = {}
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return session
    try:
        decoded = base64.b64decode(cookie)
        if not decoded:
            return {}
        session = json.loads(decoded.decode('utf-8'))
    except Exception:
        return {}
    return session

def destroy(response):
    response.set_cookie(COOKIE_NAME, '', expires=0, httponly=True, samesite='Lax')
    return response