from src.service.BookService import BookService
from src.models.Book import Book
from flask import render_template, redirect, request, url_for, session, Blueprint, jsonify

from src.utils.libraryUtils import login_required

book_service = BookService()

book_controller = Blueprint('book', __name__)


@book_controller.route('/getAllBooks', methods=['GET'])
@login_required
def get_all_books():
    offset = int(request.args.get('offset', 0))
    books = (book_service.
             get_all_books(offset, 10))
    return render_template('book.html', books=books)


@book_controller.route('/addBook', methods=['POST'])
def add_book():
    book_data = request.json
    book = Book(
        book_id = 0,
        title=book_data.get('title'),
        author_name=book_data.get('authorName'),
        category=book_data.get('category'),
        available=book_data.get('available'),
        total_quantity=book_data.get('totalQuantity'),
        lib_section=book_data.get('libSection'),
        active=book_data.get('active')
    )
    book.validate()
    book_service.add_book(book)
    return jsonify({"message": "Book added successfully"})


@book_controller.route('/deleteBook/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book_service.delete_book(book_id)
    return jsonify({"message": "Book deleted successfully"})


@book_controller.route('/updateBook', methods=['PUT'])
def update_book():
    book_data = request.json
    book = Book(
        book_id=book_data.get('bookId'),
        title=book_data.get('title'),
        author_name=book_data.get('authorName'),
        category=book_data.get('category'),
        available=book_data.get('available'),
        total_quantity=book_data.get('totalQuantity'),
        lib_section=book_data.get('libSection'),
        active=book_data.get('active')
    )
    book.validate()
    book_service.update_book(book)
    return jsonify({"message": "Book updated successfully"})


@book_controller.route('/getBookById/<int:book_id>')
def getBookById(book_id):
    book=book_service.getBookById(book_id)
    book_dict = {key: getattr(book, key) for key in vars(book)}

    return jsonify(book_dict)


@book_controller.route('/searchBook')
def search_books():
    offset = request.args.get('offset', 0)
    value = request.args.get('value', None)
    value = value.strip()

    if value == '""' or value is None:
        return book_service.get_all_books()

    return book_service.search_Books(value, offset, 10)

