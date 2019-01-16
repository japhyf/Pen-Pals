import os

from flask import Flask, redirect, url_for
from flask_mail import Mail, Message


def create_app(test_config=None):
    # create and configure the app
    mail = Mail()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config.update(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='penpalsmessenger@gmail.com',
        MAIL_PASSWORD='CE96IZXHQA3p'
    )

    mail.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    @app.route('/')
    def start():
        return redirect(url_for('auth.start_page'))

    @app.route('/porn')
    def send():
        try:
            msg = Message("someone visited the porn page :/", sender="12345ere6789@gmail.com", recipients=["nickfrog11@gmail.com"])
            msg.body = "u little fuck"
            msg.add_recipient("aaebrahi@ucsc.edu")
            msg.add_recipient("cdixonfe@ucsc.edu")
            msg.add_recipient("jfrolick@ucsc.edu")
            msg.add_recipient("thaygood@ucsc.edu")
            msg.add_recipient("hbquique@gmail.com")

            mail.send(msg)
            return 'Mail sent'


        except Exception as e:
            return str(e)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import main
    app.register_blueprint(main.bp)

    return app
