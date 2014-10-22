from oak import Hub


class oakify(object):
    """

    """

    @classmethod
    def model(cls, **kwargs):
        """

        """
        def wrapper(klass):
            Hub.register_model(klass, **kwargs)
            return klass

        return wrapper

    @classmethod
    def view(cls, **kwargs):
        """

        """
        def wrapper(klass):
            Hub.register_view(klass, **kwargs)
            return klass

        return wrapper
