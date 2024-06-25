from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from flask import request, current_app
from .models import User
from . import db, mail


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html') 


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!', 'info')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        if not email or not password:
            flash('Email or Password missing!', 'danger')
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.email_verified:
                flash('Please verify your email address before logging in.', 'warning')
                return redirect(url_for('main.login'))
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid credentials', 'danger')
    
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in!", 'info')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Check if request is JSON
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        if not email or not password:
            flash('Email or Password missing!', 'danger')
            return redirect(url_for('main.register'))

        if not email.endswith('@thehexaa.com'):
            flash("Please enter a valid @thehexaa.com email address!", 'warning')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists.", 'danger')
            return redirect(url_for('main.register'))

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user)
        flash('A confirmation email has been sent to your email address.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

def send_verification_email(user):
    token = user.generate_verification_token()
    verification_link = url_for('main.confirm_email', token=token, _external=True)
    msg = Message('Confirm Your Email Address', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'Please click the following link to verify your email address: {verification_link}'
    mail.send(msg)

@main.route('/confirm_email/<token>')
def confirm_email(token):
    user = User.verify_verification_token(token)
    if user is None:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('main.login'))
    user.email_verified = True
    db.session.commit()
    flash('Your email has been verified!', 'success')
    return redirect(url_for('main.login'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


    