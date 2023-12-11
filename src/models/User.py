from src.exceptions.LibraryException import LibraryException


class User:
    def __init__(self, user_id=None, first_name=None, last_name=None, username=None
                 , password=None, email=None, contact=None, active=None, role=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.contact = contact
        self.active = active
        self.role = role

    def validate(self, opt=None):

        if opt == 'EDIT':
            if self.user_id is None:
                raise LibraryException("userId must be non-null", "IVD_OPN", 400)
        if opt == 'ADD':
            if self.password is None:
                raise LibraryException("password must be non-null", "IVD_OPN", 400)

        if any(value is None for value in [self.first_name, self.last_name, self.username,
                                           self.email, self.contact, self.active, self.role]):
            raise LibraryException("All fields must be non-null", "IVD_OPN", 400)

        if self.active not in [True, False] or self.role not in ["USER", "ADMIN"]:
            raise LibraryException("Invalid Input", "IVD_IN", 400)
