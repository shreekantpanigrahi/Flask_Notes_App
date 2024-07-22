from website import create_app
from website.models import User
from flask_login import LoginManager,current_user

app=create_app()
login_manager= LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@app.cli.command("show_users")
def show_users():
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, First Name: {user.firstName}")

@app.context_processor
def inject_user():
    return dict(user=current_user)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__=='__main__':
    app.run(debug=True)
