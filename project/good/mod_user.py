from flask import Blueprint, render_template, redirect, request, g, session, make_response, flash
import libmfa
import libuser
import libsession
import sqlite3
import os
from functools import wraps


def requires_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            uname = None
            try:
                uname = g.session.get('username') if g.get('session') else None
            except Exception:
                uname = None

            if not uname:
                return redirect('/user/login')

            try:
                db_path = os.path.join(os.path.dirname(__file__), 'db_users.sqlite')
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("SELECT role FROM users WHERE username = ?", (uname,))
                row = cur.fetchone()
                conn.close()
                role = row[0] if row and row[0] is not None else 'user'
            except Exception:
                role = 'user'

            if str(role).lower() != str(required_role).lower():
                return make_response("403 Forbidden", 403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


mod_user = Blueprint('mod_user', __name__, template_folder='templates')


@mod_user.route('/login', methods=['GET', 'POST'])
def do_login():

    session.pop('username', None)

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        otp = request.form.get('otp')

        username = libuser.login(username, password)

        if not username:
            flash("Invalid user or password")
            return render_template('user.login.mfa.html')

        if libmfa.mfa_is_enabled(username):
            if not libmfa.mfa_validate(username, otp):
                flash("Invalid OTP")
                return render_template('user.login.mfa.html')
        g.session['username'] = username
        db_path = os.path.join(os.path.dirname(__file__), 'db_users.sqlite')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        g.session['role'] = row[0] if row and row[0] else 'user'
        response = make_response(redirect('/'))
        response = libsession.create(response=response, username=username)
        return response

    return render_template('user.login.mfa.html')


@mod_user.route('/create', methods=['GET', 'POST'])
def do_create():

    session.pop('username', None)

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please, complete username and password")
            return render_template('user.create.html')

        libuser.create(username, password)
        flash("User created. Please login.")
        return redirect('/user/login')

    return render_template('user.create.html')


@mod_user.route('/chpasswd', methods=['GET', 'POST'])
def do_chpasswd():

    if request.method == 'POST':

        password = request.form.get('password')
        password_again = request.form.get('password_again')

        if password != password_again:
            flash("The passwords don't match")
            return render_template('user.chpasswd.html')

        if not libuser.password_complexity(password):
            flash("The password does not meet complexity requirements")
            return render_template('user.chpasswd.html')

        libuser.password_change(g.session['username'], password)
        flash("Password changed")

    return render_template('user.chpasswd.html')