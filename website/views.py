import os
from flask import Blueprint, app, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from .forms import NoteForm, LoginForm, ContactForm
from . import db
import json
from flask_mail import Mail, Message
from flask import session

views = Blueprint('views', __name__)

# Initialize Flask-Mail
mail = Mail()

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/my_notes', methods=['GET', 'POST'])
@login_required
def my_notes():
    login_form = LoginForm()
    add_note_form = NoteForm()
    if request.method == 'POST':
        note = request.form.get("note")

        if len(note) < 1:
            flash("Your note is too short", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Your note is added!", category='success')

    # Fetch all notes for the current user
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("my_notes.html", user=current_user, login_form=login_form, add_note_form=add_note_form, notes=user_notes)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    contact_form = ContactForm()
    if request.method == 'POST':
        if contact_form.validate_on_submit():
            name = contact_form.name.data
            email = contact_form.email.data
            message = contact_form.message.data

            # Prepare email to send to the admin
            msg = Message("Contact Form Submission",
                          sender=email,
                          recipients=["admin@example.com"])  # Replace with the admin's email address
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)
            
            flash("Your message has been sent! We will get back to you soon.", category='success')
            return redirect(url_for('views.contact'))
        else:
            flash("Please correct the errors in the form.", category='error')

    return render_template("contact.html", contact_form=contact_form)

@views.route('/delete-note/<int:id>', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get(id)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash("Your note is deleted!", category='error')
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@views.route('/share-note/<int:note_id>', methods=['GET'])
def share_note_view(note_id):
    note = Note.query.get(note_id)
    if note:
        user = User.query.get(note.user_id)
        session['shared_note'] = True
        db.session.commit()
        session['shared_note_id'] = note.id
        return render_template("shared_note.html", note=note, user=user)
    else:
        flash("Note not found!", category='error')
        return redirect(url_for('views.my_notes'))

@views.route('/home', methods=['GET'])
@login_required
def home_page():
    session.pop('shared_note', None)  # Remove the shared_note flag when user navigates to home
    return render_template("home.html", user=current_user)


from flask import Blueprint
from flask_mail import Message
from . import mail  

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/send-email')
def send_email():
    name = request.form.get('name')
    sender_email = request.form.get('email')
    message_content = request.form.get('message')
    
    if not name or not sender_email or not message_content:
        return jsonify({'error': 'All fields are required!'}), 400
    
    msg = Message(
        'Contact Form Submission',
        sender=sender_email,
        recipients=[os.environ.get('MAIL_USERNAME')]  # Replace with your recipient email
    )
    msg.body = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message_content}"
    mail.send(msg)
    
    return 'Email sent!'

@views.route('/note/<int:note_id>')
@login_required
def note_detail(note_id):
    # Fetch the note by ID
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    return render_template('note_detail.html', note=note)
