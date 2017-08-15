from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):

	username = StringField('username', validators=[validators.DataRequired()])

	password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=6)])

	submit = SubmitField('submit', validators=[validators.DataRequired()])

class CreateUserForm(FlaskForm):

	username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=3, max=40)])

	email = StringField('email', validators=[validators.DataRequired(), validators.Length(min=255)])

	password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=6)])

	submit = SubmitField('submit', validators=[validators.DataRequired()])
	