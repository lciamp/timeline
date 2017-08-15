import datetime
from application import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from ..posts.models import Post

__all__ = ['follower', 'User']

followers = db.Table('followers',
	db.Column('follower_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True))

class User(db.Model):

	id = db.Column(db.Integer(), primary_key=True)

	email = db.Column(db.String(255), unique=True)

	username = db.Column(db.String(40), unique=True)

	_password = db.Column('password', db.String(60))

	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

	followed = db.relationship('User',
		secondary=followers,
		primaryjoin=(id==followers.c.follower_id),
		secondaryjoin=(id==followers.c.user_id),
		backref=db.backref('followers', lazy='dynamic'),
		lazy='dynamic')

	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self._password = password


	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def password(self, password):
		self._password = flask_bcrypt.generate_password_hash(password)

	def __repr__(self):
		return "<User %r>" % self.username

	def is_authenticated(self):
		"""All our registered users are authenticated."""
		return True

	def is_active(self):
		"""All our users are active."""
		return True

	def is_anonymous(self):
		"""We don't have anonymous users; always False"""
		return False

	def get_id(self):
		"""Get the user ID."""
		return unicode(self.id)	

	def unfollow(self, user):
		if not self.is_following(user):
			return False

		self.followed.remove(user)
		return self

	def follow(self, user):
		if self.is_following(user):
			return False

		self.followed.append(user)
		return self

	def is_following(self, user):
		followed = self.followed.filter(followers.c.user_id == user.id)
		return followed > 0

	def newsfeed(self):
		"""
		return all posts from users followed by the current user,
		in decending cronological order
		"""
		join_condition = followers.c.user_id == Post.user_id
		filter_condition = followers.c.follower_id == self.id
		ordering = Post.created_on.desc()

		return Post.query.join(followers, (join_condition)).filter(filter_condition).order_by(ordering)






























