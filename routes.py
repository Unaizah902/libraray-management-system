from flask import Blueprint, render_template, redirect, url_for
from models import db, Book, User
from flask_login import login_required, current_user

# Create a blueprint instead of using app directly
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)


@routes.route('/borrow/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if not book.is_borrowed:
        book.is_borrowed = True
        book.borrower_id = current_user.id
        db.session.commit()
    return redirect(url_for('routes.home'))  # Update to 'routes.home'


@routes.route('/return/<int:book_id>')
@login_required
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.is_borrowed and book.borrower_id == current_user.id:
        book.is_borrowed = False
        book.borrower_id = None
        db.session.commit()
    return redirect(url_for('routes.home'))  # Update to 'routes.home'
