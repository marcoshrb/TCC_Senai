class IncorrectInstanceException(Exception):
    def __init__(self, received, expected):
        message = f"Received type {received}, expected type {expected}"
        super().__init__(message)
        self.message = message