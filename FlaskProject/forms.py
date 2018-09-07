from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField

# from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError#, url

from FlaskProject.models import User

class PostForm(Form):
	title = StringField('title', validators=[DataRequired()])
	text = StringField('text')
	# link = URLField('link', validators=[url()])



class LoginForm(Form):
	username = StringField('Username:', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')


class SignupForm(Form):
	username = StringField('Username', 
		validators=[
			DataRequired(), 
			Length(3,80), 
			Regexp('^[A-Za-z0-9_]{3,}$', message='Username consist of numbers, letters, and underscores.')])
	password = PasswordField('Password', 
		validators=[
		DataRequired(),
		EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', 
		validators=[DataRequired()])

	def validate_username(self, username_field):
		if User.query.filter_by(username=username_field.data).first():
			raise ValidationError('This username is already taken.')