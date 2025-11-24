import json
import base64

def create(response, username):
    session = {'username': username}
    cookie_val = base64.b64encode(json.dumps(session).encode()).decode('ascii')
    response.set_cookie('vulpy_session', cookie_val, httponly=True, samesite='Lax')
    return response

def load(request):
    session = {}
    cookie = request.cookies.get('vulpy_session')
    if not cookie:
        return session
    try:
        decoded = base64.b64decode(cookie)
        if not decoded:
            return session
        session = json.loads(decoded.decode('utf-8'))
    except Exception:
        return {}
    return session

def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0, httponly=True, samesite='Lax')
    return response
