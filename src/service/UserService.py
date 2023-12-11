from psycopg2 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from src.dao.UserDao import UserDao
from src.exceptions.LibraryException import LibraryException
from src.models.User import User
from src.utils.libraryUtils import *
from typing import List


class UserService:
    def __init__(self):
        self.user_dao = UserDao()

    def check_user_creds(self, username, password):

        user = self.user_dao.get_by_username(username)
        if user:
            if user and check_password_hash(user[0]["password"], password):
                return user
            else:
                return None, "Invalid password"
        return None, "Invalid username"

    def get_user_by_id(self, user_id):
        user = self.user_dao.get_userBy_id(user_id)
        if not user:
            raise LibraryException("User Not Exists", "NOT_EXISTS", 400)
        return user

    def get_all_users(self, offset, limit) -> List[User]:
        return self.user_dao.get_all_users_db(offset, limit)

    def add_user(self, user: User) -> None:
        try:
            num = self.user_dao.add_user_in_db(user)
            check_row_change(num)

        except ValueError as e:
            error_message = str(e)
            checkUniqueAndThrow(error_message)

    def remove_user(self, user_id: int) -> None:
        self.user_dao.get_userBy_id(user_id)
        check_row_change(self.user_dao.remove_user_from_db(user_id))

    def update_user(self, user: User):
        self.user_dao.get_userBy_id(user.user_id)
        try:
            num = self.user_dao.updateUser(user)
            check_row_change(num)
        except ValueError as e:
            error_message = str(e)
            checkUniqueAndThrow(error_message)

    def updateDue(self, due, user_id):
        self.user_dao.get_userBy_id(user_id)
        check_row_change(self.user_dao.updateDue(due, user_id))

    def searchUsers(self, value, offset=0, limit=10):
        return self.user_dao.searchUsers(getWildCardWords(value), offset, limit)

    def getHashedPassword(self, password):
        return generate_password_hash(password, method='pbkdf2:sha256')
