from . import db 
from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user

auth= Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email= request.form.get('email')
        password= request.form.get('password')

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist!", category='error')
    
    return render_template("login.html", user=current_user)


@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    if request.method ==  'POST':
        email= request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        confirmPassword= request.form.get('confirmPassword')

        user= User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist", category='error')
        elif len(email)<4:
            flash("Email should be greater than 3 characters", category='error')
        elif len(firstName)<2:
            flash("FirstNmae should be greater than 1 characters", category='error')
        elif password != confirmPassword:
            flash("Password should matchb the confirm password", category='error')
        elif len(password)<5:
            flash('Password should be greater than 4 characters', category='error')
        else:
            new_user = User(email=email, firstName = firstName, password= generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


