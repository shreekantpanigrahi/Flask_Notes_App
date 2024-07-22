from flask_mail import Message, Mail
from . import db 
from flask import Blueprint, app, jsonify, render_template, request, flash, redirect, session, url_for 
from .models import User 
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import login_user, login_required, logout_user, current_user
from .forms import LoginForm, SignupForm  # Import the forms

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


# @auth.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     data = request.get_json()
#     email = data.get('email')
    
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({'error': 'The email address you specified does not have an account.'}), 400

#     # Generate a token (use itsdangerous for token generation)
#     from itsdangerous import URLSafeTimedSerializer
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     token = serializer.dumps(email, salt='password-reset-salt')

#     # Send email
#     reset_url = url_for('auth.reset_password', token=token, _external=True)
#     msg = Message(
#         'Password Reset Request',
#         sender=app.config['MAIL_USERNAME'],
#         recipients=[email]
#     )
#     msg.body = f'Please click the link to reset your password: {reset_url}'
#     mail.send(msg)

#     return jsonify({'message': 'Password reset email sent!'}), 200

# @auth.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if request.method == 'POST':
#         data = request.form
#         new_password = data.get('new_password')
#         confirm_password = data.get('confirm_password')

#         if not new_password or not confirm_password:
#             flash('Please fill out both fields', 'error')
#             return render_template('setnewpassword.html', token=token)

#         if new_password != confirm_password:
#             flash('Passwords do not match', 'error')
#             return render_template('setnewpassword.html', token=token)

#         from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
#         serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        
#         try:
#             email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
#         except (SignatureExpired, BadSignature):
#             flash('The password reset link is invalid or has expired', 'error')
#             return redirect(url_for('views.login'))

#         user = User.query.filter_by(email=email).first()
#         if user:
#             user.set_password(new_password)
#             db.session.commit()
#             flash('Your password has been updated', 'success')
#             return redirect(url_for('views.login'))
#         else:
#             flash('User does not exist', 'error')
#             return redirect(url_for('views.login'))

#     return render_template('setnewpassword.html', token=token)



