from .theme import theme


class adhoc_theme(theme):
    def __init__(self, params):
        super(adhoc_theme, self).__init__(complete=False, **params)

        for param, value in params.items():
            if not isinstance(value, list):
                value = str(value)
            self._rcParams[param] = value
