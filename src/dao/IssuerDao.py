from src.dao.database import db
from src.exceptions.LibraryException import LibraryException


class IssuerDao:
    TABLE_NAME = "issuer"
    ADD_ISSUER_QUERY = (
            "INSERT INTO " + TABLE_NAME +
            " (book_id, user_id, issue_date, return_date, active,days) " +
            "VALUES (:bookId, :userId, :issueDate, :returnDate, :active, :days)"
    )

    RETURN_BOOK_QUERY = "UPDATE " + TABLE_NAME + (" SET active=:active, due=:due, return_date=:return_date WHERE "
                                                  "issuer_id=:issuerId")

    GET_ISSUER_INFO = (
            "SELECT issuer.issuer_id, " +
            "issuer.book_id, " +
            "issuer.user_id, " +
            "issuer.updated_at, " +
            "books.title AS book_title, " +
            "CONCAT(users.firstname, ' ', users.lastname) AS fullname, " +
            "to_char(issuer.issue_date, 'DD Mon YYYY, HH:MI AM') AS issue_date , " +
            "to_char(issuer.return_date, 'DD Mon YYYY, HH:MI AM') AS return_date, " +
            "issuer.active, issuer.days, issuer.due " +
            "FROM public.issuer " +
            "JOIN " +
            "public.books ON issuer.book_id = books.book_id " +
            "JOIN " +
            "public.users ON issuer.user_id = users.user_id"
    )

    def add_issuer_in_db(self, issuer):
        db.execute(self.ADD_ISSUER_QUERY,
                   bookId=issuer.book_id,
                   userId=issuer.user_id,
                   issueDate=issuer.issue_date,
                   returnDate=issuer.return_date,
                   days=issuer.days,
                   active=issuer.active
                   )

    def return_issued_book_in_db(self, issuer_id, due, return_date):
        db.execute(self.RETURN_BOOK_QUERY, active=False, issuerId=issuer_id, due=due, return_date=return_date)

    def get_issued_books(self):
        return db.execute(self.GET_ISSUER_INFO + " ORDER BY issuer.updated_at DESC")

    def get_issued_active_issued_books_by_id(self, user_id: int):
        allIssuedBookList = self.getUserAllBooks(user_id)
        userBookList = [issue for issue in allIssuedBookList if issue['active'] == True]
        return userBookList

    def getUserAllBooks(self, user_id):
        return db.execute(self.GET_ISSUER_INFO + " WHERE issuer.user_id = :user_id ORDER BY issuer.updated_at DESC", user_id=user_id)

    def getIssuerByIssuerId(self, issuer_id: int):
        issuerBook = db.execute(self.GET_ISSUER_INFO + " WHERE issuer.issuer_id = :issuer_id ", issuer_id=issuer_id)
        if not issuerBook:
            raise LibraryException("Invalid Issuer Id", "NOT_EXISTS", 400)
        return issuerBook

    def searchIssuers(self, value, offset=0, limit=10):
        return db.execute(self.GET_ISSUER_INFO + " WHERE (LOWER(books.title) LIKE LOWER(:book_title) OR LOWER(CONCAT("
                                                 "users.firstname, ' ', users.lastname)) LIKE LOWER(:name)) ORDER "
                                                 "BY issuer.updated_at DESC", book_title=value, name=value)

    def searchIssuersByUser(self, value, user_id, offset=0, limit=10):
        return db.execute(self.GET_ISSUER_INFO + " WHERE (LOWER(books.title) LIKE LOWER(:book_title) OR LOWER(CONCAT("
                                                 "users.firstname, ' ', users.lastname)) LIKE LOWER(:name)) AND "
                                                 "issuer.user_id=:user_id ORDER "
                                                 "BY issuer.updated_at DESC", book_title=value, name=value, user_id=user_id)