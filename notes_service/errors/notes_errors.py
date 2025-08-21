"""Notes Service Error module"""


class NotesException(Exception):
    """Custom NotesException class"""

    def __init__(self, message: str, status_code: int, details: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class NotesDBException(Exception):
    """Custom NotesDBException class"""

    def __init__(self, message: str, status_code: int, details: str):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details
