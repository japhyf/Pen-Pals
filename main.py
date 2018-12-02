import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr import init_db; init_db()

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
        if user is None:
            return redirect(url_for('auth.start_page'))
        user_details = {
            'email': user['email'],
        }
        return render_template('main/search.html', user=user_details)


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
    if user['description'] is None:
        description = ""
    else:
        description = user['description']
    if user['genres'] is None:
        genres = ""
    else:
        genres = user['genres']
    if user['titles'] is None:
        titles = ""
    else:
        titles = user['titles']
    if user['picture'] is None:
        picture = ""
    else:
        picture = user['picture']
    user_details = {
        'first'       : first,
        'last'        : last,
        'email'       : email,
        'address1'    : address_line1,
        'address2'    : address_line2,
        'username'    : username,
        'description' : description,
        'genres'      : genres,
        'titles'      : titles,
        'picture'     : picture
    }
    return render_template('main/create_bio.html', user=user_details)

@bp.route('/create_bio', methods=('GET', 'POST'))
def create_bio_submit():
    user_id = session.get('user_id')
    db = get_db()
    error = None
    if request.method == 'POST':
        #jsonGenres = json.loads(request.form['genres'])
        #jsonTitles = json.loads(request.form['titles'])
        genreString = request.form['genres']
        titleString = request.form['titles']
        desc = request.form['desc']
        pic_url = request.form['pic']
        #genreString = ' '
        #for x in jsonGenres:
        #    genreString += ' '
        #    genreString += jsonGenres[x]
        #titleString = ' '
        #for x in jsonTitles:
        #    titleString += ' '
        #    titleString += jsonTitles[x]
        sql = 'UPDATE user SET genres = ?, titles = ?, picture = ?, description = ? WHERE id = ?'
        val = (genreString, titleString, pic_url, desc, user_id)
        db.execute(sql, val)
        db.commit()

    return render_template('main/db.html')

@bp.route('/search')
def search():
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
    return render_template('main/search.html', user=user_details)

@bp.route('/search', methods=('GET', 'POST'))
def search_results():
    db = get_db()
    error = None
    if request.method == 'POST':
        jsonGenres = json.loads(request.form['genres'])
        genres = []
        for x in jsonGenres:
            genres.append(jsonGenres[x])
        full_users = {}
        for i in genres:
            str = '%' + i + '%'
            users = db.execute(
                'SELECT * FROM user WHERE genres LIKE ?', (str,)
            ).fetchall()
            cursor = db.execute('select * from user')
            header = [x[0] for x in cursor.description]
            users_obj = {}
            for user in users:
                users_obj[user["id"]] = dict(zip(header,user))
            full_users.update(users_obj)
        jsonTitles = json.loads(request.form['titles'])
        titles = []
        for x in jsonTitles:
            titles.append(jsonTitles[x])
        for i in titles:
            str = '%' + i + '%'
            users = db.execute(
                'SELECT * FROM user WHERE titles LIKE ?', (str,)
            ).fetchall()
            cursor = db.execute('select * from user')
            header = [x[0] for x in cursor.description]
            users_obj = {}
            for user in users:
                users_obj[user["id"]] = dict(zip(header,user))
            full_users.update(users_obj)
        y = json.dumps(full_users)
        return jsonify(y)
    return render_template('main/search.html')


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
    if user['description'] is None:
        description = ""
    else:
        description = user['description']
    user_details = {
        'first': first,
        'last': last,
        'email': email,
        'address1': address_line1,
        'address2': address_line2,
        'username': username,
        'description' : description
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
