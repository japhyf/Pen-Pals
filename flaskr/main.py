import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route('/home')
def home():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    else:
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        user_details = {
            'email': user['email'],
        }
        return render_template('main/home.html', user=user_details)


@bp.route('/create_bio')
def create_bio():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user['first'] is None:
        first = ""
    else:
        first = user['first']
    if user['email'] is None:
        email = ""
    else:
        email = user['email']
    if user['last'] is None:
        last = ""
    else:
        last = user['last']
    if user['address_line1'] is None:
        address_line1 = ""
    else:
        address_line1 = user['address_line1']
    if user['address_line2'] is None:
        address_line2 = ""
    else:
        address_line2 = user['address_line2']
    if user['username'] is None:
        username = ""
    else:
        username = user['username']
    user_details = {
        'first': first,
        'last': last,
        'email': email,
        'address1': address_line1,
        'address2': address_line2,
        'username': username
    }
    return render_template('main/create_bio.html', user=user_details)


@bp.route('/bio')
def bio():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user['first'] is None:
        first = ""
    else:
        first = user['first']
    if user['email'] is None:
        email = ""
    else:
        email = user['email']
    if user['last'] is None:
        last = ""
    else:
        last = user['last']
    if user['address_line1'] is None:
        address_line1 = ""
    else:
        address_line1 = user['address_line1']
    if user['address_line2'] is None:
        address_line2 = ""
    else:
        address_line2 = user['address_line2']
    if user['username'] is None:
        username = ""
    else:
        username = user['username']
    user_details = {
        'first': first,
        'last': last,
        'email': email,
        'address1': address_line1,
        'address2': address_line2,
        'username': username
    }
    return render_template('main/bio.html', user=user_details)


@bp.route('/edit_bio')
def edit_bio():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()
    if user['first'] is None:
        first = ""
    else:
        first = user['first']
    if user['email'] is None:
        email = ""
    else:
        email = user['email']
    if user['last'] is None:
        last = ""
    else:
        last = user['last']
    if user['address_line1'] is None:
        address_line1 = ""
    else:
        address_line1 = user['address_line1']
    if user['address_line2'] is None:
        address_line2 = ""
    else:
        address_line2 = user['address_line2']
    if user['username'] is None:
        username = ""
    else:
        username = user['username']
    user_details = {
        'first': first,
        'last': last,
        'email': email,
        'address1': address_line1,
        'address2': address_line2,
        'username': username
    }
    return render_template('main/edit_bio.html', user=user_details)


@bp.route('/edit_bio', methods=('GET', 'POST'))
def edit_bio_form():
    user_id = session.get('user_id')
    if request.method == 'POST':
        db = get_db()
        error = None
        # if the register button is clicked load the register inputs
        first = request.form['first']
        last = request.form['last']
        email = request.form['email']
        username = request.form['username']
        address1 = request.form['address1']
        address2 = request.form['address2']
        sql = 'UPDATE user SET first = ?, last = ?, email = ?, username = ?, address_line1 = ?, address_line2 = ? WHERE id = ?'
        val = (first, last, email, username, address1, address2, user_id)
        db.execute(sql, val)
        db.commit()
        return redirect(url_for('auth.db'))


@bp.route('/create_bio', methods=('GET', 'POST'))
def create_bio_form():
    user_id = session.get('user_id')
    if request.method == 'POST':
        db = get_db()
        error = None
        # if the register button is clicked load the register inputs
        first = request.form['first']
        last = request.form['last']
        email = request.form['email']
        username = request.form['username']
        address1 = request.form['address1']
        address2 = request.form['address2']
        sql = 'UPDATE user SET first = ?, last = ?, email = ?, username = ?, address_line1 = ?, address_line2 = ? WHERE id = ?'
        val = (first, last, email, username, address1, address2, user_id)
        db.execute(sql, val)
        db.commit()
        return redirect(url_for('auth.db'))
