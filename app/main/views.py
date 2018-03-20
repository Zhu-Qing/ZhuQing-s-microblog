from . import main
from .. import db
from datetime import datetime
from flask import render_template,session,redirect,url_for
from flask_login import current_user
from .forms import NameForm,PostForm
from ..models import User,Post,Permission
		
@main.route('/', methods=['GET','POST'])
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and\
			form.validate_on_submit():
		post = Post(body=form.body.data,
					author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('main.index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',
		form = form, posts = posts)
