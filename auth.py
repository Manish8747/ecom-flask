from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models import db, User
from flask_jwt_extended import create_access_token # type: ignore
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, template_folder='templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("User already exists!", "warning")
            return redirect(url_for('auth.register'))

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Invalid username or password!", "danger")
            return redirect(url_for('auth.login'))

        # Create JWT token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

        # Store JWT token in session
        session['access_token'] = access_token

        flash(f"Welcome {username}!", "success")
        return redirect(url_for('home'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('access_token', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))
