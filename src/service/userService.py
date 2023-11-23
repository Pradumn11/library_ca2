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
        user = self.user_dao.get_by_id(user_id)[0]
        if not user:
            raise LibraryException("Invalid User Id", "NOT_EXISTS", 400)
        return user

    def get_all_users(self) -> List[User]:
        return self.user_dao.get_all_users_db()

    def add_user(self, user: User) -> None:
        num = self.user_dao.add_user_in_db(user)
        check_row_change(num)

    def remove_user(self, user_id: int) -> None:
        num = self.user_dao.remove_user_from_db(user_id)
        check_row_change(num)

    def update_user(self, user: User):
        num = self.user_dao.updateUser(user)
        check_row_change(num)


