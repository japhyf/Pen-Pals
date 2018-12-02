import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

app = Blueprint('main-site', __name__, url_prefix='/main-site')

@app.route('/index')
def test_route():
    user_details = {
        'name': 'John',
        'email': 'john@doe.com'
    }

    return render_template('index.html', user=user_details)
