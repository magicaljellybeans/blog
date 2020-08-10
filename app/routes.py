from flask import render_template, redirect, session, request, url_for, flash
from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/index'))
    form = LoginForm()
    next_url = request.args.get('next')
    if not next_url or url_parse(next_url).netloc != '':
        next_url = url_for('index')
    if form.validate_on_submit():
        user = User()
        # how do i call a class here? self? should i have a class for a single user? 
        password = form.password.data
        if password == app.config['ADMIN_KEY']:
            login_user(user)
            flash('Logged in as editor')
            return redirect(next_url)
        else:
            flash('Incorrect password')
    return render_template('login.html', title='Sign In', form=form)
