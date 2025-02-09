from flask import Flask
from models import db
from routes import routes  # Import the blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

# Register the blueprint
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
