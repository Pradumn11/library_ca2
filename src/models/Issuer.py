class Issuer:
    def __init__(self, issuer_id=None, book_id=None, user_id=None, issue_date=None,
                 return_date=None, active=None, days=None):
        self.issuer_id = issuer_id
        self.book_id = book_id
        self.user_id = user_id
        self.issue_date = issue_date
        self.return_date = return_date
        self.active = active
        self.days = days
