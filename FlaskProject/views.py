from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_login import login_required, login_user, logout_user, current_user

from FlaskProject import app, db, login_manager
from FlaskProject.forms import PostForm, LoginForm, SignupForm, CommentForm
from FlaskProject.models import User, Post, Comment


# def logged_in_user():
# 	return User.query.filter_by(username='andrew').first()

@login_manager.user_loader
def load_user(userid):
	return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', new_posts=Post.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		text = form.text.data
		post = Post(user=current_user, title=title, text=text)
		db.session.add(post)
		db.session.commit()
		flash("Posted: '{}'".format(title))
		return redirect(url_for('index'))
	return render_template('post_form.html', form=form, title="Add a post")

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	if current_user != post.user:
		abort(403)
	form = PostForm(obj=post)
	if form.validate_on_submit():
		form.populate_obj(post)
		db.session.commit()
		flash("Edited '{}'".format(post.title))
		return redirect(url_for('user', username=current_user.username))
	return render_template('post_form.html', form=form, title="Edit post")

@app.route('/post/<int:post_id>/add', methods=['GET', 'POST'])
@login_required
def add_comment(post_id):
	form = CommentForm()
	if form.validate_on_submit():
		text = form.text.data
		comment = Comment(user=current_user, post_id=post_id, text=text)
		db.session.add(comment)
		db.session.commit()
		flash("Commented: '{}'".format(text))
		return redirect(url_for('post', post_id=post_id))
	return render_template('comment_form.html', form=form, title="Add a post")



@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if current_user != comment.user:
		abort(403)
	form = CommentForm(obj=comment)
	if form.validate_on_submit():
		form.populate_obj(comment)
		db.session.commit()
		flash("Edited '{}'".format(comment.id))
		return redirect(url_for('post', post_id=comment.post_id))
	return render_template('comment_form.html', form=form, title="Edit comment")



@app.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@app.route('/login', methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.get_by_username(form.username.data)
		if user is not None and user.check_password(form.password.data):
			login_user(user, form.remember_me.data)
			flash("Logged in successfully as {}.".format(user.username))
			return redirect(request.args.get('next') or url_for('user', username=user.username))
		flash('Incorrect username or password.')
	return render_template("login.html", form=form)


@app.route('/logout')
def logout():
	logout_user()
	flash("Successfully logged out.")
	return redirect(url_for('index'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Welcome, {}! Please login.'.format(user.username))
		return redirect(url_for('login'))
	return render_template("signup.html", form=form)

@app.route('/post/<post_id>')
def post(post_id):
	post = Post.query.filter_by(id=post_id).first_or_404()
	return render_template('post.html', post=post, new_comments=Comment.newest(post_id=post_id, num=5))






@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

