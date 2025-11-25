import sqlite3
from flask import Blueprint, render_template, redirect, request, g ,make_response
from mod_user import requires_role
import libposts
import libuser

mod_posts = Blueprint('mod_posts', __name__, template_folder='templates')


@mod_posts.route('/')
@mod_posts.route('/<username>')
def do_view(username=None):
    current_user = None
    current_role = None
    try:
        current_user = g.session.get('username') if g.get('session') else None
        current_role = g.session.get('role') if g.get('session') else None
    except Exception:
        current_user = None
        current_role = None
    if not username:
        if current_user:
            username = current_user
        else:
            return redirect('/user/login')
    if username != current_user and (not current_role or str(current_role).lower() != 'admin'):
        return make_response("403 Forbidden", 403)

    posts = libposts.get_posts(username)
    users = libuser.userlist()

    return render_template('posts.view.html', posts=posts, username=username, users=users)

@mod_posts.route('/admin')
@requires_role('admin')
def admin_panel():
    posts = libposts.get_posts(None)
    users = libuser.userlist()
    return render_template('admin.html', posts=posts, users=users)

@mod_posts.route('/', methods=['POST'])
def do_create():

    if 'username' not in g.session:
        return redirect('/user/login')

    if request.method == 'POST':
        
        username = g.session['username']
        text = request.form.get('text')
        # CSRF validation
        token = request.form.get('csrf_token')
        from libcsrf import validate_csrf
        if not validate_csrf(g.session, token):
            return make_response("400 Bad Request - CSRF token missing or invalid", 400)
        libposts.post(username, text)

    return redirect('/')

