from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from Blinker import Namespace

# initalize db extension without configuring
db = SQLAlchemy()
flask_bcrypt = Bcrypt()

timeline_signals = Namespace()
user_followed = timeline_signals.signal('user-followed')
from signal_handlers import connect_handlers
connect_handlers()


def create_app(config=None):
	app = Flask(__name__)

	if config is not None:
		app.config.from_object(config)

	# add db and bcrypt to app
	db.init_app(app)
	flask_bcrypt.init_app(app)

	return app