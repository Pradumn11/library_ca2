class LibraryException(Exception):
    def __init__(self, message, error_code, http_status):
        self.message = message
        self.error_code = error_code
        self.http_status = http_status
        super().__init__(message)