import json
import base64

COOKIE_NAME = "vulpy_session"
MAX_AGE = 60 * 60 * 24  # 1 day

def create(response, session_dict):
    """Store ENTIRE session (username, role, _csrf) in cookie."""
    try:
        encoded = base64.b64encode(json.dumps(session_dict).encode()).decode()
        response.set_cookie(
            COOKIE_NAME,
            encoded,
            httponly=True,
            samesite='Lax',
            max_age=MAX_AGE
        )
    except Exception as e:
        print("SESSION CREATE ERROR:", e)
    return response


def load(request):
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return {}
    try:
        decoded = base64.b64decode(cookie).decode()
        return json.loads(decoded)
    except Exception:
        return {}


def destroy(response):
    response.set_cookie(COOKIE_NAME, '', expires=0, httponly=True, samesite='Lax')
    return response
