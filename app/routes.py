from flask import render_template, redirect, session, request, url_for, flash, Markup
from app import app, db
from app.forms import LoginForm, EditorForm
from app.models import User, Post, Tag
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash
import markdown


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=1).order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    for item in posts.items:
        if item.body and len(item.body) > app.config['BLURB_LENGTH']:
            item.body = item.body[:app.config['BLURB_LENGTH']] + '...'
            item.body = Markup(markdown.markdown(item.body))

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

    post.body = Markup(markdown.markdown(post.body))
    title = post.title
    return render_template('post.html', post=post, title=title)

@app.route('/editor/<slug>', methods=['GET', 'POST'])
@app.route('/editor/', methods=['GET', 'POST'])
@login_required
def editor(slug=None):
    # old post or new post?
    if slug:
        post = Post.query.filter_by(slug=slug).first()
    else:
        post = Post()
    # drafts list
    drafts = Post.query.filter_by(published=False).all()
    # populate form, blank for new post
    form = EditorForm(obj=post)
    # populate tags field
    form.tags.choices = [(tag.id, tag.tag) for tag in Tag.query.order_by('tag')]
    # populate defaults only on GET otherwise user choice overidden
    if request.method == 'GET':
        # declare default (highlighted) tags list
        form.tags.data = []
        # if post has tags, highlight them
        if post.tags:
            for tag in post.tags:
                form.tags.data.append(tag.id)

    if form.validate_on_submit():
        # submission was a delete
        if form.delete.data:
            db.session.delete(post)
            db.session.commit()
            flash('Post Deleted')
            return redirect(url_for('editor'))
        # copy form data into post
        post.title = form.title.data
        post.body = form.body.data
        post.author = current_user.get_id()
        post.published = form.published.data
        # empty tags list then add highlighted choices
        post.tags = []
        for id in form.tags.data:
            t = Tag.query.filter_by(id=id).first()
            post.tags.append(t)
        # add new tags to database and append
        if form.new_tags.data:
            new_tags = form.new_tags.data.split()
            for tag in new_tags:
                name = tag
                tag = Tag()
                tag.tag = name
                post.tags.append(tag)
                db.session.add(tag)
        # allow timestamp updates for drafts being published
        if post.published and form.update.data:
            post.update_time()
        # generate new/updated slug and save for redirection
        post.save()
        slug = post.slug
        # save post
        db.session.add(post)
        db.session.commit()
        # inform user
        if post.published:
            flash('Published Post')
        elif not post.published:
            flash('Unpublished Post')
        return redirect(url_for('post', slug=slug))
    return render_template('editor.html', title='Editor', form=form, drafts=drafts)


@app.route('/publish/<slug>')
@login_required
def publish(slug):
    post = Post.query.filter_by(slug=slug).first()
    post.published = not post.published

    if post.published:
        flash('Published Post')
    else:
        flash('Unpublished Post')

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('post', slug=slug))
