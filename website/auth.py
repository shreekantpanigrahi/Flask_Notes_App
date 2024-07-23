from flask_mail import Message, Mail
from . import db 
from flask import Blueprint, app, jsonify, render_template, request, flash, redirect, session, url_for 
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm  # Import the forms
from . import mail
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer 
from flask import current_app

mail = Mail()
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method=='POST':
        email= request.form.get('email')
        password= request.form.get('password')
        if login_form.validate_on_submit(): 
            email = login_form.email.data
            password = login_form.password.data

        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                # Clear the 'shared_note' flag from the session
                session.pop('shared_note', None)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist!", category='error')
    
    return render_template("login.html", user=current_user, login_form=login_form)


@auth.route('/sign_up', methods=['GET','POST'])
def sign_up():
    signup_form = SignupForm()
    if request.method ==  'POST':
        email= request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        confirmPassword= request.form.get('confirmPassword')

        if signup_form.validate_on_submit(): 
            email = signup_form.email.data
            firstName = signup_form.firstName.data
            password = signup_form.password.data
            confirmPassword = signup_form.confirmPassword.data

        user= User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist", category='danger')
        elif len(email)<4:
            flash("Email should be greater than 3 characters", category='danger')
        elif len(firstName)<2:
            flash("FirstNmae should be greater than 1 characters", category='danger')
        elif password != confirmPassword:
            flash("Password should matchb the confirm password", category='danger')
        elif len(password)<5:
            flash('Password should be greater than 4 characters', category='danger')
        else:
            new_user = User(email=email, firstName = firstName, password= generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # Clear the 'shared_note' flag from the session
            session.pop('shared_note', None)

            login_user(new_user, remember=True)
            flash("Account created successfully!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user = current_user, signup_form=signup_form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetPasswordRequestForm()  # Create an instance of the form
    if form.validate_on_submit():  # Check if the form is submitted and valid
        email = form.email.data  # Retrieve the email from the form
        user = User.query.filter_by(email=email).first()  # Query the user by email
        if user:
            send_reset_email(user)  # Send a reset email if user exists
            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('auth.login'))  # Redirect to login page
        else:
            flash('No account found with that email.', 'warning')  # Notify if email not found

    return render_template('reset_request.html', form=form)  # Render the request form


def send_reset_email(user):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user.email, salt='password-reset-salt')
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    form_t = ResetPasswordForm()
    # Correctly retrieve the secret key
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    
    try:
        # Attempt to load the token with an increased expiration time
        email = s.loads(token, salt='password-reset-salt', max_age=7200)  # Set to 2 hours
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('auth.reset_request'))
    except BadSignature as e:
        print(f"Bad signature error: {e}")  # Log the error
        flash('The password reset link is invalid.', 'danger')
        return redirect(url_for('auth.reset_request'))

    # Find user by email
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Invalid email address!', 'danger')
        return redirect(url_for('auth.reset_request'))

    if form_t.validate_on_submit():
        user.password = generate_password_hash(form_t.password.data, method='pbkdf2:sha256')
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form_t=form_t)
