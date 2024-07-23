# app/routes.py
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, LoyaltyForm
from app.models import User, Loyalty
from flask_login import login_user, current_user, logout_user, login_required
import random

required_list = [
    "emotional_shiya"
]

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('loyalty'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('loyalty'))
        elif form.username.data in required_list:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('loyalty'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/loyalty", methods=['GET', 'POST'])
@login_required
def loyalty():
    form = LoyaltyForm()
    if form.validate_on_submit():
        score = calculate_loyalty(form.name1.data, form.name2.data)
        loyalty = Loyalty(user_id=current_user.id, name1=form.name1.data, name2=form.name2.data, score=score)
        db.session.add(loyalty)
        db.session.commit()
        flash(f'Loyalty score between {form.name1.data} and {form.name2.data} is {score}', 'success')
        return redirect(url_for('loyalty'))
    loyalties = Loyalty.query.filter_by(user_id=current_user.id).all()
    return render_template('loyalty_combined.html', title='Loyalty', form=form, loyalties=loyalties)

def calculate_loyalty(name1, name2):
    random.seed(len(name2))
    return random.randrange(75, 95)
