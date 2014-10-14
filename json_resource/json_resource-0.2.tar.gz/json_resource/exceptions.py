import json


class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super(ValidationError, self).__init__(
            json.dumps(dict([('/' + '/'.join(error.path), error.message) for error
                             in self.errors]))
        )


class ResourceNotFound(Exception):
    pass


class ResourceExists(Exception):
    pass



