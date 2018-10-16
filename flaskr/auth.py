import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#handles register and login on the start page
@bp.route('/start_page', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        db = get_db()
        error = None
        #if the register button is clicked load the register inputs
        if request.form["button"]=="Register":
            regEmail = request.form['regEmail']
            regPassword = request.form['regPassword']	
            if not regEmail:
                return redirect(url_for('auth.noRegUser'))
            elif not regPassword:
                return redirect(url_for('auth.noRegPass'))
            elif db.execute(
                'SELECT id FROM user WHERE email = ?', (regEmail,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(regEmail)
            
            if error is None:
                db.execute(
                    'INSERT INTO user (email, password) VALUES (?, ?)',
                    (regEmail, generate_password_hash(regPassword))
                )
                db.commit()
                user = db.execute(
                    'SELECT * FROM user WHERE email = ?', (regEmail,)
                ).fetchone()
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('auth.index'))
            flash(error)
        #else if the login button is clicked load the login inputs
        else:
            loginEmail = request.form['loginEmail']
            loginPassword = request.form['loginPassword']
            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (loginEmail,)
            ).fetchone()

            if user is None:
                error = 'Incorrect email.'
            elif not check_password_hash(user['password'], loginPassword):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('auth.index'))
 
            flash(error)

    return render_template('auth/start_page.html')

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
    return redirect(url_for('auth.start_page'))
    
	
@bp.route('/index')
def index():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    user_details = {      
		'email': user['email'],
    }

    return render_template('main-site/index.html', user=user_details)
	
@bp.route('/start_page')
def start_page():
    user_id = session.get('user_id')
    if user_id is not None:
        return redirect(url_for('auth.index'))
    else:
        return render_template('auth/start_page.html')

