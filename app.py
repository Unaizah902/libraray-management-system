from flask import Flask
from flask_login import LoginManager
from routes import *  # Import the blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "routes.login"  # Redirect to login if unauthorized


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Register the blueprint
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
