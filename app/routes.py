from flask import render_template, redirect, session, request, url_for, flash
from app import app
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


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
