from flask import render_template, redirect, session
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        if password == app.config['ADMIN_KEY']:
            session['editor'] = True
            
    return render_template('login.html', title='Sign In', form=form)
