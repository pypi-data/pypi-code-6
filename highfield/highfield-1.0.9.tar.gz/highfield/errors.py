class ValidationError(Exception):
    def __init__(self, errors, message=None):
        self.message = message
        self.errors = errors
        pass
    pass