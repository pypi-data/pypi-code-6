


class DataTable(object):
    def __init__(self, request, model, query, columns):
        self.request = request
        self.model = model
        self.query = query
        self.columns = columns

    def run(self):
        pass