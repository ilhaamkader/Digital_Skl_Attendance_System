import os
import string

import requests
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mail import Mail, Message
from random import *
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import desc

from flask import session
import re
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
import forms

app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.environ.get('MAINTAINENCE_EMAIL')
app.config["MAIL_PASSWORD"] = os.environ.get('MAINTAINENCE_EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# def is_configured():
#     admin_count = db.session.query(Admins).count()
#     return admin_count > 0

def isConfigured():
    pass

@app.route('/')
def index():
    if not is_configured():
        return redirect(url_for('setup'))
    return redirect(url_for('login'))

def generate_username(email, user_type):
    email_prefix = re.split('@', email)[0]

    if user_type == 'admin':
        prefix = 'a'

    elif user_type == 'secretary':
        prefix = 's'

    elif user_type == 'parent':
        prefix = 'p'

    else:
        raise ValueError("Invalid user type")
    
    username = f"{prefix}{email_prefix}"
    return username

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if is_configured():
        return redirect(url_for('login'))
    
    form = forms.Config()

    if form.validate_on_submit():

        email = form.email.data
        raw_password = form.password.data
        username = generate_username(email, 'admin')
        hashed_password = generate_password_hash(raw_password)

        new_admin = Admins(email = email,
                            password = hashed_password,
                              username = username)

        # db.session.add(new_admin)
        # db.session.commit()

        return redirect(url_for('login'))
    return render_template('setup.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = forms.Login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        prefix = username[0]
        user = None

        # if prefix == 'a':
        #     user = Admins.query.filter_by(username=username).first()
        # elif prefix == 's':
        #     user = Secretaries.query.filter_by(username=username).first()
        # elif prefix == 'p':
        #     user = Parents.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = prefix

            if prefix == 'a':
                return redirect(url_for('admin_dashboard'))
            elif prefix == 'p':
                return redirect(url_for('parent_dashboard'))
            elif prefix == 's':
                return redirect(url_for('secretary_dashboard'))
            elif prefix == 'e':
                return redirect(url_for('educator_dashboard'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html', form = form)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_type' in session and session['user_type'] == 'a':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))
    
def generate_password():
    # Specify counts for letters, numbers, and symbols
    Letter_Count = 8  # Example: 8 letters
    Number_Count = 4  # Example: 4 numbers
    Symbol_Count = 2  # Example: 2 symbols

    Password_List = []
    # Generate letters
    for L in range(Letter_Count):
        Password_List.append(choice(string.ascii_letters))
    # Generate numbers
    for N in range(Number_Count):
        Password_List.append(choice(string.digits))
    # Generate symbols
    for S in range(Symbol_Count):
        Password_List.append(choice(string.punctuation))

    # Shuffle the password list
    shuffle(Password_List)

    # Concatenate the characters to form the password
    Randomised_String = ''.join(Password_List)
    return Randomised_String


@app.route('/add_secretary', methods=['GET', 'POST'])
def add_secretary():
    if 'user_type' in session and session['user_type'] == 'a':
        form = AddSecretaryForm()

        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            rsa_id_num = form.rsa_id_num.data
            email = form.email.data
            cell_number = form.cell_number.data

            username = generate_username(email, 'secretary')
            password = generate_password()
            hashed_password = generate_password_hash(password)

            new_secretary = Secretaries(
                first_name=first_name,
                last_name=last_name,
                RSA_id_num=rsa_id_num,
                email=email,
                cell_number=cell_number,
                username=username,
                password=hashed_password
            )

            db.session.add(new_secretary)
            db.session.commit()

            msg = Message(subject="Welcome to the System - Your Account Details",
                          sender='systememail@gmail.com',
                          recipients=[email])
            msg.body = (f"Hello {first_name} {last_name},\n\n"
                        f"Your account has been created. Below are your login details:\n\n"
                        f"Username: {username}\n"
                        f"Password: {password} (Please change this after logging in)\n\n"
                        "Thank you.")
            mail.send(msg)

            flash('Secretary successfully added and email sent.', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('add_secretary.html', form=form)
    else:
        flash("You must be an admin to access this page.", 'danger')
        return redirect(url_for('login'))

@app.route('/add_educator', methods=['GET', 'POST'])
def add_educator():
    if 'user_type' in session and session['user_type'] == 'a':
        form = AddEducatorForm()

        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            rsa_id_num = form.rsa_id_num.data
            email = form.email.data
            cell_number = form.cell_number.data

            username = generate_username(email, 'educator')
            password = generate_password()
            hashed_password = generate_password_hash(password)

            new_educator = Educators(
                first_name=first_name,
                last_name=last_name,
                RSA_id_num=rsa_id_num,
                email=email,
                cell_number=cell_number,
                username=username,
                password=hashed_password
            )

            db.session.add(new_educator)
            db.session.commit()

            msg = Message(subject="Welcome to the System - Your Account Details",
                          sender='systememail@gmail.com',
                          recipients=[email])
            msg.body = (f"Hello {first_name} {last_name},\n\n"
                        f"Your account has been created. Below are your login details:\n\n"
                        f"Username: {username}\n"
                        f"Password: {password} (Please change this after logging in)\n\n"
                        "Thank you.")
            mail.send(msg)

            flash('Educator successfully added and email sent.', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('add_educator.html', form=form)
    else:
        flash("You must be an admin to access this page.", 'danger')
        return redirect(url_for('login'))

@app.route('/manage_profile', methods=['GET', 'POST'])
@login_required
def manage_profile():
    username = current_user.username
    role = None
    user = None

    if username.startswith('a'):
        user = Admin.query.filter_by(username=username).first()
        role = 'admin'
    elif username.startswith('s'):
        user = Secretary.query.filter_by(username=username).first()
        role = 'secretary'
    elif username.startswith('e'):
        user = Educator.query.filter_by(username=username).first()
        role = 'educator'
    elif username.startswith('p'):
        user = Parent.query.filter_by(username=username).first()
        role = 'parent'
    else:
        flash('Invalid user role or username', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':

        if 'change_password' in request.form:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not check_password_hash(user.password, current_password):
                flash("Current password is incorrect", "danger")

            elif new_password != confirm_password:
                flash("New password and confirmation don't match", "danger")

            else:
                user.password = generate_password_hash(new_password)
                flash("Password updated successfully", "success")
                db.session.commit()

        if 'update_mobile' in request.form and role in ['secretary', 'educator', 'parent']:
            new_mobile_number = request.form.get('mobile_number')
            user.mobile_number = new_mobile_number
            flash("Mobile number updated successfully", "success")
            db.session.commit()

        return redirect(url_for('manage_profile'))

    return render_template('manage_profile.html', user=user, role=role)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
