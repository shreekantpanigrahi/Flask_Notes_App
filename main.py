from website import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.models import User

app=create_app()
if __name__=='__main__':
    app.run(debug=True)

# In your main Flask application file (e.g., main.py)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Import your models here
@app.cli.command("show_users")
def show_users():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, First Name: {user.firstName}")
