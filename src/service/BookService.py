from src.dao.BookDao import BookDao
from src.models.Book import Book
from src.utils.libraryUtils import check_row_change


class BookService:
    def __init__(self):
        self.book_dao = BookDao()

    def get_all_books(self, offset, limit):
        return self.book_dao.getAllBooks(offset, limit)

    def add_book(self, book: Book):
        num = self.book_dao.add_book_in_db(book.book_id, book.title, book.author_name, book.category, book.available,
                                           book.total_quantity,
                                           book.lib_section)
        check_row_change(num)

    def delete_book(self, book_id):
        num = self.book_dao.delete_book(book_id)
        check_row_change(num)

    def update_book(self, book: Book):
        num = self.book_dao.update_book(book.book_id, book.title, book.author_name, book.category, book.available,
                                        book.total_quantity, book.lib_section)
        check_row_change(num)

    def getBookById(self, book_id):
        book = self.book_dao.get_book_by_id(book_id)
        if not book:
            raise ValueError("Invalid Book Id")
        return book
