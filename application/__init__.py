from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initalize db extension without configuring
db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config=None):
	app = Flask(__name__)

	if config is not None:
		app.config.from_object(config)

	# add db and bcrypt to app
	db.init_app(app)
	flask_bcrypt.init_app(app)

	return app