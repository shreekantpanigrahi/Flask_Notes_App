import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


csrf = CSRFProtect()
mail = Mail()
db = SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= os.environ.get('SECRET_KEY')
    database_url = os.environ.get('DATABASE_URL', f"sqlite:///{DB_NAME}")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    db.init_app(app)

    # Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'  
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    
    csrf = CSRFProtect(app)
    mail = Mail(app)

    mail.init_app(app)
    csrf.init_app(app)  

    from .views import views
    from .auth import auth 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Note
    create_database(app)

    return app


def create_database(app):
    with app.app_context():
        if not path.exists('website/instance' + DB_NAME):
            db.create_all()
            print('Create Database!')
