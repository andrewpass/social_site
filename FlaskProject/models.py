from datetime import datetime

from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from FlaskProject import db


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(50), nullable=False)
	text = db.Column(db.String(500))
	# link = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	@staticmethod
	def newest(num):
		return Post.query.order_by(desc(Post.date)).limit(num)



	def __repr__(self):
		return "<Post '{}': '{}'>".format(self.title, self.description)



class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	posts = db.relationship('Post', backref='user', lazy='dynamic')
	password_hash = db.Column(db.String)

	@property
	def password(self):
		raise AttributeError('password: write-only field')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	@staticmethod
	def get_by_username(username):
		return User.query.filter_by(username=username).first()

	def __repr__(self):
		return '<User %r>' % self.username