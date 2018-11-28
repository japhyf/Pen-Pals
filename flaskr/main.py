import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, json, jsonify
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
        db.commit()
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        user_details = {
            'email': user['email'],
        }
        return render_template('main/home.html', user=user_details)

@bp.route('/chathome')
def chat():
    return render_template('main/chathome.html')
    #make sure user is logged in

@bp.route('/chathome', methods=('GET', 'POST'))
def chat_post():
    if request.method == 'POST':
        user_id = session.get('user_id')
        db = get_db()
        if user_id is None:
            return redirect(url_for('auth.start_page'))
        else:

#            db.execute(
#                'INSERT INTO total_msg (identifier, total_messages) VALUES (?, ?)',
#                ("new tst", 1)
#            )
#            db.commit()

            # db.execute(
            #     'INSERT INTO messages (identifier_msg_nmbr, message, sender) VALUES (?, ?, ?)',
            #     ("helo", "k", "heh")
            # )
            # db.commit()


            user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            user2 = db.execute('SELECT * FROM user WHERE email = ?', ('d@d.com',)).fetchone()

           # db.execute('INSERT INTO total_msg (identifier, total_messages) VALUES (user['id']:user2['id'], 1)')

            user_details = {
                'email': user['email'],
                'last': user['last'],
                'first': user['first'],
                'email2': user2['email'],
                'last2': user2['last'],
                'first2': user2['first'],
            }

            test = user_details['email']

            db.execute(
                'INSERT INTO total_msg (identifier, total_messages) VALUES (?,1)', (test)
            )

            db.commit()

            y = json.dumps(user_details)
            return jsonify(y)

@bp.route('/chatdb')
def db():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    tbl1 = db.execute(
        'SELECT * FROM total_msg'
    ).fetchall()
    tbl2 = db.execute(
        'SELECT * FROM messages'
    ).fetchall()
    return render_template('main/chatdb.html', tbl1=tbl1, tbl2=tbl2)

#@bp.route('/chatdb', methods=('GET', 'POST'))
#def update_email():
#    user_id = session.get('user_id')
#    db = get_db()
#    if request.method == 'POST':
#        error = None
        #if the register button is clicked load the register inputs
#        email = request.form['email']
#        sql = 'UPDATE user SET email = ? WHERE id = ?'
#        val = (email, user_id)
#        db.execute(sql, val)
#        db.commit()
#        return redirect(url_for('auth.db'))

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

@bp.route('/create_bio', methods=('GET', 'POST'))
def create_bio_submit():
    user_id = session.get('user_id')
    db = get_db()
    error = None
    if request.method == 'POST':
        jsonGenres = json.loads(request.form['genres'])
        jsonTitles = json.loads(request.form['titles'])
        desc = request.form['desc']
        pic_url = request.form['pic']
        genreString = ' '
        for x in jsonGenres:
            genreString += ' '
            genreString += jsonGenres[x]
        titleString = ' '
        for x in jsonTitles:
            titleString += ' '
            titleString += jsonTitles[x]
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
