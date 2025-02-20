from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import app, db, bcrypt
from models import User
from forms import RegistrationForm, LoginForm

@app.route("/coming_soon")
def coming_soon():
    return render_template('ComingSoon.html')

@app.route("/landing")
def landing():
    return render_template('MovieFlix.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return render_template('login.html', form=form)
    else:
        print("Form validation failed")
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", 'danger')
                    print(f"Error in {field}: {error}")
    return render_template('login.html', form=form)

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('landing'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
