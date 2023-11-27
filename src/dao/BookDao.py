from src.dao.database import db
from src.models.Book import Book

TABLE_NAME = "books"


class BookDao:
    FETCH_ALL_BOOKS_QUERY = f"SELECT * FROM {TABLE_NAME} LIMIT :limit OFFSET :offset"

    ADD_BOOK_QUERY = (
        f"INSERT INTO {TABLE_NAME} title, author_name, category, available, total_quantity, lib_section, active) "
        "VALUES (:title, :author_name, :category, :available, :total_quantity, :lib_section, :active)")

    DELETE_BOOK_QUERY = f"UPDATE {TABLE_NAME} SET active=:active WHERE book_id=:book_id"

    UPDATE_BOOK_QUERY = (f"UPDATE {TABLE_NAME} SET title=:title, author_name=:author_name, category=:category, "
                         "available=:available, total_quantity=:total_quantity, lib_section=:lib_section WHERE "
                         "book_id=:book_id")

    GET_BOOK_BY_ID_QUERY = f"SELECT * FROM {TABLE_NAME}  WHERE book_id=:book_id AND active=True"

    def getAllBooks(self, offset=0, limit=0):
        return db.execute(self.FETCH_ALL_BOOKS_QUERY, limit=limit, offset=offset)

    def add_book_in_db(self, title, author_name, category, available, total_quantity, lib_section, active):
        db.execute(self.ADD_BOOK_QUERY, title=title, author_name=author_name, category=category,
                   available=available, total_quantity=total_quantity, lib_section=lib_section, active=active)

    def delete_book(self, book_id):
        db.execute(self.DELETE_BOOK_QUERY, active=False, book_id=book_id)

    def update_book(self, book_id, title, author_name, category, available, total_quantity, lib_section):
        db.execute(self.UPDATE_BOOK_QUERY, title=title, author_name=author_name, category=category,
                   available=available, total_quantity=total_quantity, lib_section=lib_section, book_id=book_id)

    def get_book_by_id(self, book_id):
        book = db.execute(self.GET_BOOK_BY_ID_QUERY, book_id=book_id)
        if book:
            book_object = Book(**book[0])
            return book_object
        return None
