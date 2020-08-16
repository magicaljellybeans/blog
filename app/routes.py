from flask import render_template, redirect, session, request, url_for, flash
from app import app, db
from app.forms import LoginForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    for item in posts.items:
        if item.body and len(item.body) > app.config['BLURB_LENGTH']:
            item.body = item.body[:app.config['BLURB_LENGTH']] + '...'

    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title='Home', posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    next_url = request.args.get('next')
    if not next_url or url_parse(next_url).netloc != '':
        next_url = url_for('index')
    if form.validate_on_submit():
        user = User()
        password = form.password.data
        if check_password_hash(app.config['ADMIN_KEY'], password):
            login_user(user)
            flash('Logged in as editor')
            return redirect(next_url)
        else:
            flash('Incorrect password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out with great success')
    return redirect(url_for('index'))

@app.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()

    return render_template('post.html', post=post)
