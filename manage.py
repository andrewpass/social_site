#! /user/bin/env python

from FlaskProject import app, db
from FlaskProject.models import User, Post, Comment
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
	db.create_all()
	db.session.add(User(username="andrew", password='asdf'))
	db.session.add(User(username="stephanie", password='asdf'))
	db.session.add(Post(user_id="1", title="Test Post 1", text="This is a test post. What do you think about it?"))
	db.session.add(Comment(user_id=2, post_id=1, text="It looks great!"))
	db.session.add(Comment(user_id=1, post_id=1, text="Thank you!"))	
	db.session.commit()
	print('Initialized the database')

@manager.command
def dropdb():
	if prompt_bool("Are you sure? You'll lose all of your data"):
		db.drop_all()
		print('Dropped the database')

@manager.command
def resetdb():
	dropdb()
	initdb()


if __name__ == '__main__':
	manager.run()