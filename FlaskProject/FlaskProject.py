from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from forms import PostForm

import models

from settings import app, db


def logged_in_user():
	return models.User.query.filter_by(username='andrew').first()


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', new_posts=models.Post.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
	form = PostForm()
	print(form)
	if form.validate_on_submit():
		title = form.title.data
		print(title)
		text = form.text.data
		link = form.link.data
		post = models.Post(user=logged_in_user(), title=title, text=text, link=link)
		db.session.add(post)
		db.session.commit()
		flash("Stored Post: '{}'".format(title))
		return redirect(url_for('index'))
	return render_template('add.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

