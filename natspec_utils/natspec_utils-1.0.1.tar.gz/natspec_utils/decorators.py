class TextSyntax():
    def __init__(self, pattern, types=[], return_type=None):
        pass

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped_f