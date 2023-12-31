from src.dao.database import db
from src.models.User import User


class UserDao:
    TABLE_NAME = "users"
    GET_ALL_USER_QUERY = ("SELECT user_id, firstname, lastname, username, password, email,contact, active, role, "
                          "updated_at, due FROM ") + TABLE_NAME + (
        " WHERE active=true ORDER BY updated_at DESC LIMIT :limit "
        "OFFSET :offset")

    ADD_USER_QUERY = "INSERT INTO " + TABLE_NAME + (" (firstname, lastname, username, password, email, "
                                                    "contact, active, role) VALUES (:firstname, :lastname, "
                                                    ":username, :password, :email, :contact, :active, :role)")

    DELETE_USER_QUERY = "UPDATE " + TABLE_NAME + " SET active=:active WHERE user_id=:user_id"

    GET_USER_BY_ID_QUERY = ("SELECT user_id, firstname, lastname, username, password, email,contact, active, role, "
                            "updated_at, due FROM ") + TABLE_NAME + " WHERE user_id=:user_id"

    UPDATE_USER_QUERY = (f"UPDATE {TABLE_NAME} SET firstname=:first_name, lastname=:last_name, username=:username, "
                         "email=:email, contact=:contact, active=:active, role=:role "
                         "WHERE user_id=:user_id")

    ADD_DUE_QUERY = "UPDATE " + TABLE_NAME + " SET due=:due WHERE user_id=:user_id"

    SEARCH_ALL_USER_QUERY = ("SELECT user_id, firstname, lastname, username, password, email,contact, active, role,"
                             "updated_at, due FROM ") + TABLE_NAME + (
        " WHERE active=true and (CAST(user_id AS TEXT) LIKE :userId OR LOWER(username) LIKE LOWER(:userName) OR LOWER("
        "CONCAT(""firstname, ' ', lastname)) LIKE LOWER(:name))  ORDER BY updated_at DESC LIMIT :limit "
        "OFFSET :offset ")

    def get_by_username(self, username):
        return db.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE username = ?", username)

    def get_userBy_id(self, user_id):
        result = db.execute(self.GET_USER_BY_ID_QUERY, user_id=user_id)
        return result[0] if result else None

    def get_all_users_db(self, offset, limit):
        return db.execute(self.GET_ALL_USER_QUERY, offset=offset, limit=limit)

    def add_user_in_db(self, user: User):
        db.execute(
            self.ADD_USER_QUERY,
            firstname=user.first_name,
            lastname=user.last_name,
            username=user.username,
            password=user.password,
            email=user.email,
            contact=user.contact,
            active=user.active,
            role=user.role
        )

    def remove_user_from_db(self, user_id):
        db.execute(self.DELETE_USER_QUERY, active=False, user_id=user_id)

    def updateUser(self, user):
        db.execute(self.UPDATE_USER_QUERY,
                   first_name=user.first_name,
                   last_name=user.last_name,
                   username=user.username,
                   email=user.email,
                   contact=user.contact,
                   active=user.active,
                   role=user.role,
                   user_id=user.user_id
                   )

    def updateDue(self, due, user_id):
        db.execute(self.ADD_DUE_QUERY, due=due, user_id=user_id)

    def searchUsers(self, value, offset=0, limit=0):
        return db.execute(self.SEARCH_ALL_USER_QUERY, userId=value, userName=value, name=value, offset=offset,
                          limit=limit)
