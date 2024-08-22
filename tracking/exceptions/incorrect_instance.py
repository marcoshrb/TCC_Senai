class IncorrectInstanceException(Exception):
    def __init__(self, received, expected, comment = ''):
        message = f"Received type {received}, expected type {expected}. {comment}"
        super().__init__(message)
        self.message = message