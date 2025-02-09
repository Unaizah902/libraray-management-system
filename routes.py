from models import Book
from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# Create a blueprint instead of using app directly
routes = Blueprint('routes', __name__)


@routes.route('/')
@login_required
def home():
    search_query = request.args.get('q', '')
    if search_query:
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    else:
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


@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Get email from form
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('routes.signup'))

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for('routes.signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for('routes.login'))

    return render_template('signup.html')


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('routes.home'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')


@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('routes.login'))
