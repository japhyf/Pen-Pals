import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        regUsername = request.form['regUsername']
        regPassword = request.form['regPassword']
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']
        db = get_db()
        error = None
        if not loginUsername and not loginPassword:
            if not regUsername:
                return redirect(url_for('auth.noRegUser'))
            elif not regPassword:
                return redirect(url_for('auth.noRegPass'))
            elif db.execute(
                'SELECT id FROM user WHERE username = ?', (regUsername,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(regUsername)
            
            if error is None:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (regUsername, generate_password_hash(regPassword))
                )
                db.commit()
                return redirect(url_for('auth.index'))
            flash(error)
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (loginUsername,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], loginPassword):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('auth.index'))
 
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['loginUsername']
        password = request.form['loginPassword']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
	
@bp.route('/index')
def index():
    return render_template('main-site/index.html')
