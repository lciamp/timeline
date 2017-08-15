from flask import Blueprint, render_template, url_for, redirect, flash, g
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

from models import User
from forms import LoginForm, CreateUserForm
from application import db, flask_bcrypt

users = Blueprint('users', __name__, template_folder='templates')

@users.route("/signup", methods=['GET', 'POST'])
def signup():

	form = CreateUserForm()

	if form.validate_on_submit():
		user = User(username=form.username.data,
					email=form.email.data,
					password=form.password.data)

		db.session.add(user)
		db.session.commit()

		login_user(user, remember=True)

		return redirect(url_for(users.index))

	return render_template('users/signup.html', form=form)

@users.route("/", method=['GET'])
def login():

	if hasattr(g, 'user') and g.user.is_authenticated():
		retrun redirect(url_for('users.index'))

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).one()

		if not user or not flask_bcrypt.check_password_hash(user.password, form.password.data)
			flash("User does not exsist.")
			return render_template('users/login', form=form)

		login_user(user, remember=True)
		return redirect(url_for('users.index'))

	return render_template('users/signup.html', form=form)


@users.route("/logout", methods=['GET'])
def logout():
	logout_user()
	return redirect(url_for('users.login'))
