import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import os
import psycopg2


def get_db():
    # if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row
    DATABASE_URL = ""
    if 'DATABASE_URL' not in os.environ:
        DATABASE_URL = "postgres://yhivuemwhsfpyt:1c8e44328f627ec543f0e73aa3d1f85cff71f430058a9a1afaefe27aadaba626@ec2-54-243-228-140.compute-1.amazonaws.com:5432/d8i90ik7u70tbv"
    else:
        DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn
    # return g.db

def get_db_conn():
    DATABASE_URL = "postgres://yhivuemwhsfpyt:1c8e44328f627ec543f0e73aa3d1f85cff71f430058a9a1afaefe27aadaba626@ec2-54-243-228-140.compute-1.amazonaws.com:5432/d8i90ik7u70tbv"
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    # with current_app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
    db.execute("""CREATE TABLE "user" (id SERIAL PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,first TEXT,last TEXT,address_line1 TEXT,address_line2 TEXT,username TEXT,description TEXT,genres TEXT,titles TEXT,birthdate TEXT,penpal INTEGER, /*penpal = 0 if not interested, 1 if open to it, 2 if wants to pen pal */picture TEXT);""")
#     db.execute("""INSERT INTO x (email, password, first, last) VALUES ('dog', 'man', 'hi', 'asdf');""")
#     click.echo(db.execute(
#                 """SELECT * FROM x WHERE email = 'dog';"""
#             ).fetchone())


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
