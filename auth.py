from flask import Blueprint, render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        if email and password:
            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('wrong login or password')
                return redirect(url_for('auth.login'))
            else:
                flash(f'logged in {user.name}')
                login_user(user, remember=remember)
                return redirect(url_for('main.index'))
        else:
            flash('Fill all form')
    return render_template('login.html')


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        if email and name and password:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('already exists')
                return redirect(url_for('auth.signup'))
            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('account created!')
            return redirect(url_for('auth.login'))
        else:
            flash('fill all form')
    return render_template('register.html')


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
