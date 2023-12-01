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
            if user and password == user[0]["password"]:
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
        check_row_change(self.user_dao.add_user_in_db(user))

    def remove_user(self, user_id: int) -> None:
        self.user_dao.get_userBy_id(user_id)
        check_row_change(self.user_dao.remove_user_from_db(user_id))

    def update_user(self, user: User):
        self.user_dao.get_userBy_id(user.user_id)
        check_row_change(self.user_dao.updateUser(user))

    def updateDue(self, due, user_id):
        self.user_dao.get_userBy_id(user_id)
        check_row_change(self.user_dao.updateDue(due, user_id))

    def searchUsers(self, value, offset=0, limit=10):
        return self.user_dao.searchUsers(getWildCardWords(value), offset, limit)
