import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

app = Blueprint('start', __name__, url_prefix='')

@app.route('/')
def start():
    return redirect(url_for('auth.start_page'))
