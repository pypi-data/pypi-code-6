import logging

# Filters
class NullFilter(logging.Filter):
    """
    Null Filter
    """
    def filter(self, record):
        return False

class QuietUnlessExceptionFilter(logging.Filter):
    def __init__(self):
        self.records = []

    def filter(self, record):
        self.records.append(record)
        return False
