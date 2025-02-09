from app import app
from models import db, Book, User
from werkzeug.security import generate_password_hash


# Create test data
def seed_data():
    with app.app_context():
        db.create_all()  # Ensure tables exist

        # Add some books
        books = [
            Book(title="Harry Potter and the Sorcerer’s Stone", author="J.K. Rowling"),
            Book(title="The Hobbit", author="J.R.R. Tolkien"),
            Book(title="1984", author="George Orwell"),
            Book(title="To Kill a Mockingbird", author="Harper Lee"),
        ]

        db.session.add_all(books)

        # Add a test user
        test_user = User(username="testuser", email = "test@gmai.com", password=generate_password_hash("password123"))
        db.session.add(test_user)

        db.session.commit()
        print("✅ Sample data added successfully!")


# Run the function
if __name__ == "__main__":
    seed_data()
