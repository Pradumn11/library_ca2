from src.models.Issuer import Issuer
from src.dao.IssuerDao import IssuerDao
from src.service.BookService import BookService
from src.service.UserService import UserService
from src.utils.libraryUtils import *


class IssuerService:

    def _init_(self):
        self.issuerDao = IssuerDao()
        self.bookService = BookService()
        self.userService = UserService()

    def get_All_Issued_Books(self):
        return self.issuerDao.get_issued_books()

    def addIssue(self, issuer: Issuer):
        book = self.bookService.getBookById(issuer.book_id)
        self.userService.get_user_by_id(issuer.user_id)

        check_book_availability(book.available)
        userIssuedBookList = self.issuerDao.get_issued_active_issued_books_by_id(issuer.user_id)
        check_or_raise(
            any(issuedBook['book_id'] == issuer.book_id for issuedBook in userIssuedBookList),
            False, f" {book.title}: Already Issued")
        check_user_book_issued(len(userIssuedBookList))

        issuer.issue_date = get_current_timestamp(DUBLIN_TIMEZONE)
        issuer.return_date = get_return_time(issuer.days, DUBLIN_TIMEZONE)

        num = self.issuerDao.add_issuer_in_db(issuer)
        check_row_change(num)
        book.available -= 1
        self.bookService.update_book(book)

    def returnIssuedBook(self, issuer_id):
        issuerBook = self.issuerDao.getIssuerByIssuerId(issuer_id)[0]
        check_or_raise(issuerBook['active'], True, "Invalid Operation: Already Returned")
        book = self.bookService.getBookById(issuerBook['book_id'])
        print(issuerBook['issue_date'], issuerBook['return_date'])
        user = self.userService.get_user_by_id(issuerBook['user_id'])
        due = check_due(issuerBook['issue_date'], issuerBook['return_date'], issuerBook['days'])
        returned_date = get_current_timestamp(DUBLIN_TIMEZONE)
        check_row_change(self.issuerDao.return_issued_book_in_db(issuer_id, due, returned_date))
        book.available += 1
        self.bookService.update_book(book)
        due = user['due']+due
        self.userService.updateDue(due, issuerBook['user_id'])

    def returnDue(self, due, user_id):
        issuerBook = self.userService.get_user_by_id(user_id)

        if issuerBook['due'] < due:
            raise LibraryException("Returned due should not be more than actual Due", "IVD_OPN", 400)
        issuerBook['due'] -= due
        check_row_change(self.userService.updateDue(issuerBook['due'], user_id))

    def search_Issuers(self, value, offset=0, limit=10):
        return self.issuerDao.searchIssuers(getWildCardWords(value), offset, limit)