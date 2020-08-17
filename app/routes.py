from flask import render_template, redirect, session, request, url_for, flash
from app import app, db
from app.forms import LoginForm, EditorForm
from app.models import User, Post, Tag
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=1).order_by(Post.timestamp.desc()).paginate(
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
    if not current_user.is_authenticated and not post.published:
        return redirect(url_for('index'))

    title = post.title
    return render_template('post.html', post=post, title=title)

@app.route('/editor/<slug>', methods=['GET', 'POST'])
@app.route('/editor/', methods=['GET', 'POST'])
@login_required
def editor(slug=None, action=None):

    obj = Post.query.filter_by(slug=slug).first()
    form = EditorForm(obj=obj)
    form.tags.choices = [(tag.tag, tag.tag) for tag in Tag.query.order_by('tag')]

    if form.validate_on_submit():
        if slug:
            post = obj
        else:
            post = Post()

        post.title = form.title.data
        post.body = form.body.data
        post.author = current_user.get_id()
        for tag in form.tags.data:
            t = Tag.query.filter_by(tag=tag).first()
            post.tags.append(t)

        if slug and post.published:
            flash('Published edited post')
        elif slug and not post.published:
            flash('Saved edited post as draft')
        elif not slug and post.published:
            flash('Published new post')
        elif not slug and not post.published:
            flash('Saved new post as draft')

        post.save()
        slug = post.slug
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post', slug=slug))
    return render_template('editor.html', title='Editor', form=form)


@app.route('/publish/<slug>')
@login_required
def publish(slug):
    post = Post.query.filter_by(slug=slug).first()
    post.published = not post.published

    if post.published:
        flash('Published draft')
    else:
        flash('Post withdrawn')

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('post', slug=slug))
