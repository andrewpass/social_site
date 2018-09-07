#! /user/bin/env python

from FlaskProject import app, db
from FlaskProject.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
	db.create_all()
	db.session.add(User(username="andrew", password='asdf'))
	db.session.add(User(username="stephanie", password='asdf'))
	db.session.commit()
	print('Initialized the database')

@manager.command
def dropdb():
	if prompt_bool("Are you sure? You'll lose all of your data"):
		db.drop_all()
		print('Dropped the database')

if __name__ == '__main__':
	manager.run()