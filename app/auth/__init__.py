from werkzeug.security import generate_password_hash
from app.auth.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import db
from app.db.models import User


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    loginform = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('simple_pages.about'))
    if loginform.validate_on_submit():
        user = User.query.filter_by(email=loginform.email.data).first()
        if user is None or not user.check_password(loginform.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        else:
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Welcome!', 'success')
            return redirect(url_for('simple_pages.about'))
    return render_template('login.html', form=loginform)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    registerform = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('simple_pages.about'))
    if registerform.validate_on_submit():
        user = User.query.filter_by(email=registerform.email.data).first()
        if user is None:
            user = User(email=registerform.email.data, password=generate_password_hash(registerform.password.data))
            db.session.add(user)
            db.session.commit()
            if user.id == 1:
                user.is_admin = 1
                db.session.add(user)
                db.session.commit()
            flash('Thank you for registering!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('This email is already registered.')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=registerform)

