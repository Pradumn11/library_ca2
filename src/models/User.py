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