import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, __main__, json, Flask
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db, get_db_conn
from flask_mail import Mail, Message

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/start_page')
def start_page():
    return render_template('auth/start_page.html')
  

#handles register and login on the start page
@bp.route('/start_page', methods=('GET', 'POST'))
def register():
    db = get_db()
    curr = db.cursor()
    error = None
    if request.method == 'POST':
        #if the register button is clicked load the register inputs
        if request.form["button"]=="Register":
            regEmail = request.form['regEmail']
            regPassword = request.form['regPassword']
            first = request.form['first']
            last = request.form['last']
            if not regEmail:
                return redirect(url_for('auth.noRegUser'))
            elif not regPassword:
                return redirect(url_for('auth.noRegPass'))
            curr.execute(
                'SELECT * FROM "user" WHERE email = (%s);', (regEmail,)
            )
            if curr.statusmessage != "SELECT 0":
                error = 'User {} is already registered.'.format(regEmail)
            if error is None:
                curr.execute(
                    'INSERT INTO "user" (email, password, first, last) VALUES (%s, %s, %s, %s);',
                    (regEmail, generate_password_hash(regPassword), first, last)
                )
                # db.commit()
                db.commit()
                curr.execute(
                    'SELECT id FROM "user" WHERE email = (%s);', (regEmail,)
                )
                user_id = curr.fetchone()[0]
                print(user_id)
                session.clear()
                session['user_id'] = user_id
                return redirect(url_for('main.create_bio'))
            flash(error)
        #else if the login button is clicked load the login inputs
        elif request.form["button"]=="Login":
            loginEmail = request.form['loginEmail']
            loginPassword = request.form['loginPassword']
            curr.execute(
                'SELECT * FROM "user" WHERE email = (%s);', (loginEmail,)
            )
            user = curr.fetchone()
            #if the input email doesnt exist in our db
            if user is None:
                error = 'Incorrect email.'
                #display this message:
                return "Email address is not in our system"
            
            #if the email exists but the password is wrong
            elif not check_password_hash(user[2], loginPassword):
                error = 'Incorrect password.'
                return "Incorrect password"
            #if there is no error
            if error is None:
                session.clear()
                session['user_id'] = user[0]
                return redirect(url_for('main.home'))

            flash(error)
        #this is to check if email exists on continue button press
        elif request.form["button"]=="continue":
            email = request.form['regEmail']
            user = curr.execute(
                'SELECT * FROM "user" WHERE email = (%s)', (email,)
            )
            #if the input email doesnt exist in our db
            if curr.statusmessage == "SELECT 0":
                return "good"
            else:
                error = 'Incorrect password.'
                return "Email address already exists in our system"
            flash(error)
        
    return render_template('auth/start_page.html')
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        curr = get_db().cursor()
        curr.execute(
            'SELECT * FROM "user" WHERE id = (%s);', (user_id,)
        )
        g.user = curr.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.start_page'))


@bp.route('/db')
def db():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    db = get_db()
    data = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    return render_template('main/db.html', data=data)

@bp.route('/db', methods=('GET', 'POST'))
def update_email():
    user_id = session.get('user_id')
    db = get_db()
    if request.method == 'POST':
        error = None
        #if the register button is clicked load the register inputs
        email = request.form['email']
        sql = 'UPDATE user SET email = ? WHERE id = ?'
        val = (email, user_id)
        db.execute(sql, val)
        db.commit()
        return redirect(url_for('auth.db'))


@bp.route('/start_page_old')
def start_page_old():
    user_id = session.get('user_id')
    if user_id is not None:
        return redirect(url_for('main.home'))
    else:
        return render_template('auth/start_page_old.html')