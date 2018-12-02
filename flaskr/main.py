import functools
import sys
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
        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        if user is None:
            return redirect(url_for('auth.start_page'))
        user_details = {
            'email': user['email'],
        }
        return render_template('main/search.html', user=user_details)

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
#                'INSERT INTO total_msg (identifier, total_messages) VALUES (, 1)',
#                'ON DUPLICATE KEY UPDATE total_messages = total_messages + 1;',
#            )
#            db.commit()

#            db.execute(
#                'INSERT INTO messages (identifier_msg_nmbr, message, sender) VALUES ("new", "test", "today")'
#            )
#            db.commit()


            user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            user2 = db.execute('SELECT * FROM user WHERE email = ?', ('three@3.com',)).fetchone()


            user_details = {
                'email': user['email'],
                'last': user['last'],
                'first': user['first'],
                'email2': user2['email'],
                'last2': user2['last'],
                'first2': user2['first'],
            }

            concat_users = user_details['email'] + ":" + user_details['email2']

            db.execute(
                'INSERT OR IGNORE INTO total_msg (identifier, total_messages) VALUES (?, ?)', (concat_users, 0,)
#                'INSERT INTO total_msg (identifier, total_messages) VALUES ("fuck", 3) ON DUPLICATE KEY UPDATE total_messages = total_messages + 1;',
#                'ON DUPLICATE KEY UPDATE total_messages = total_messages + 1;', hack['total_messages'] +1
            )
            db.commit()

            hack = db.execute('SELECT * FROM total_msg WHERE identifier = ?', (concat_users,)).fetchone()

            db.execute(
                'INSERT OR REPLACE INTO total_msg (identifier, total_messages) VALUES (?, ?)', (concat_users, hack['total_messages'] +1,)
#                'INSERT INTO total_msg (identifier, total_messages) VALUES ("fuck", 3) ON DUPLICATE KEY UPDATE total_messages = total_messages + 1;',
#                'ON DUPLICATE KEY UPDATE total_messages = total_messages + 1;', hack['total_messages'] +1
            )
            db.commit()

            hack2 = db.execute('SELECT * FROM total_msg WHERE identifier = ?', (concat_users,)).fetchone()
            y = concat_users + str(hack['total_messages'])
            z = "lick2"
            f = user_details['email']

            db.execute(
                'INSERT INTO messages (identifier_msg_nmbr, message, sender) VALUES (?, ?, ?)', (y, z, f,)
            )
            db.commit()

            y = json.dumps(user_details)
            return jsonify(y)

@bp.route('/chatdb')
def chatdb():
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

@bp.route('/livechat')
def livechat():
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    else:
        return render_template('main/livechat.html')

@bp.route('/livechat', methods=('GET', 'POST'))
def livechat_post():
    if request.method == 'POST':
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
            print (request.form['flag'], file=sys.stderr)
            print ('flag 0', file=sys.stderr)

            #the first ajax call for creating the conversation
            otherEmail = request.form['otherEmail']
            reversed = True
            concat_users = user['email'] + ":" + otherEmail
            concat_reverse = otherEmail + ":" + user['email']

            #check to see who started the conversation
            check_dup  = db.execute(
                'SELECT * FROM total_msg WHERE identifier = ?', (concat_reverse,)
            ).fetchone()

            if check_dup is None:
                reversed = False
                db.execute(
                    'INSERT OR IGNORE INTO total_msg (identifier, total_messages) VALUES (?, ?)', (concat_users, 0,)
                )
                db.commit()
            # the second ajax call for entering a message into the database
            if request.form['flag'] == '1':
                #adds 1 to the conversation message count and enters the message
                print ('flag 1', file=sys.stderr)
                if not reversed:
                    hack = db.execute('SELECT * FROM total_msg WHERE identifier = ?', (concat_users,)).fetchone()
                    db.execute(
                        'INSERT OR REPLACE INTO total_msg (identifier, total_messages) VALUES (?, ?)', (concat_users, hack['total_messages'] +1,)
                    )
                    db.commit()
#                    concat_users_msgnumber = concat_users + ":" + str(hack['total_messages'])
                    db.execute(
                        'INSERT INTO messages (id, identifier_msg_nmbr, message, sender) VALUES (?, ?, ?, ?)', (hack['total_messages'], concat_users, request.form['the_message'], user['email'],)
                    )
                    db.commit()
                else:
                    hack2 = db.execute('SELECT * FROM total_msg WHERE identifier = ?', (concat_reverse,)).fetchone()
                    db.execute(
                        'INSERT OR REPLACE INTO total_msg (identifier, total_messages) VALUES (?, ?)', (concat_reverse, hack2['total_messages'] +1,)
                    )
                    db.commit()
#                    concat_reverse_msgnumber = concat_reverse + ":" + str(hack2['total_messages'])
                    db.execute(
                        'INSERT INTO messages (id, identifier_msg_nmbr, message, sender) VALUES (?, ?, ?, ?)', (hack2['total_messages'], concat_reverse, request.form['the_message'], user['email'],)
                    )
                    db.commit()

            if not reversed:
                print ('if', file=sys.stderr)
                chat_history = db.execute(
                    'SELECT * FROM messages WHERE identifier_msg_nmbr = ?', (concat_users,)
                ).fetchall()
        #                print (chat_history, file=sys.stderr)
            else:
                print ('else', file=sys.stderr)
                chat_history = db.execute(
                    'SELECT * FROM messages WHERE identifier_msg_nmbr = ?', (concat_reverse,)
                ).fetchall()
            print (chat_history, file=sys.stderr)
            cursor = db.execute('select * from messages')
            header = [x[0] for x in cursor.description]
            chat_obj = {}
            for row in chat_history:
                chat_obj[row["id"]] = dict(zip(header,row))
                print (chat_obj[row["id"]], file=sys.stderr)
            y = json.dumps(chat_obj)
            #return full list of users to template
            return jsonify(y)

    return render_template('main/livechat.html', chat_history=chat_history)


@bp.route('/create_bio')
def create_bio():
    #check that user is logged in
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    #send all user data to template
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
    #send all user data to template
    return render_template('main/create_bio.html', user=user_details)

@bp.route('/create_bio', methods=('GET', 'POST'))
def create_bio_submit():
    user_id = session.get('user_id')
    db = get_db()
    error = None
    #insert all info entered on create_bio page into database
    if request.method == 'POST':
        genreString = request.form['genres']
        titleString = request.form['titles']
        desc = request.form['desc']
        pic_url = request.form['pic']
        sql = 'UPDATE user SET genres = ?, titles = ?, picture = ?, description = ? WHERE id = ?'
        val = (genreString, titleString, pic_url, desc, user_id)
        db.execute(sql, val)
        db.commit()       
    return render_template('main/db.html')

@bp.route('/search')
def search():
    #check that user is logged in
    user_id = session.get('user_id')
    db = get_db()
    if user_id is None:
        return redirect(url_for('auth.start_page'))
    #send all user data to template
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
    #send all user data to template
    return render_template('main/search.html', user=user_details)

@bp.route('/search', methods=('GET', 'POST'))
def search_results():
    db = get_db()
    error = None
    if request.method == 'POST':
        #find all users with favorite genres matching search genres
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
        #find all users with favorite titles matching search titles
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
        #return full list of users to template
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
