
class Book:
    def __init__(self, book_id=None, title=None, author_name=None, category=None, available=None,
                 total_quantity=None, lib_section=None, active=None,updated_at=None):
        self.book_id = book_id
        self.title = title
        self.author_name = author_name
        self.category = category
        self.available = available
        self.total_quantity = total_quantity
        self.lib_section = lib_section
        self.active = active
        self.updated_at=updated_at

    def validate(self):
        if any(value is None for value in [self.title, self.author_name, self.category,
                                           self.available, self.total_quantity, self.lib_section, self.active]):
            raise ValueError("All fields must be non-null")
