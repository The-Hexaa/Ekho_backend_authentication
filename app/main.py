from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from flask import request, current_app
from .models import User
from . import db, mail
from flask import jsonify


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the API!'})


@main.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'You are already logged in!'})

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email or Password missing!'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.email_verified:
        return jsonify({'error': 'Please verify your email address before logging in.'}), 401

    login_user(user)
    return jsonify({'message': 'Login successful!'})


@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email or Password missing!'}), 400

    if not email.endswith('@thehexaa.com'):
        return jsonify({'error': 'Please enter a valid @thehexaa.com email address!'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists.'}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    send_verification_email(user)
    return jsonify({'message': 'Registration successful! A confirmation email has been sent.'})


def send_verification_email(user):
    token = user.generate_verification_token()
    verification_link = url_for('main.confirm_email', token=token, _external=True)
    msg = Message('Confirm Your Email Address', sender=current_app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'Please click the following link to verify your email address: {verification_link}'
    mail.send(msg)

def confirm_email(token):
    user = User.verify_verification_token(token)
    if user is None:
        return jsonify({'error': 'The confirmation link is invalid or has expired.'}), 400

    user.email_verified = True
    db.session.commit()
    return jsonify({'message': 'Email verified successfully!'})

@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'})



    