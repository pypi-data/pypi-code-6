from babel import Locale
from babel.messages import frontend
from .paths import get_locale_path


def compile_catalog(language):
    from distutils.dist import Distribution

    compiler = frontend.compile_catalog(Distribution())
    compiler.initialize_options()
    compiler.directory = get_locale_path()
    compiler.locale = language
    compiler.finalize_options()
    compiler.run()


def get_language_name(language):
    return Locale.parse(language).get_language_name().capitalize()


class Localized(object):
    """ Wraps a dictionary containing localized / non-localized data and offers
    it through attribute access, returning the current language.

    e.g.

        >>> localized = Localized({
            'id': 'cake',
            'name': {
                'en': 'Delicious cake',
                'de': 'Leckerer Kuchen'
            },
            'description': {
                'en': 'You know.. cake!'
            }
        }, languages=['en', 'de'], language='de')

        >>> localized.id
        =>  'cake'

        >>> localized.name
        =>  'Leckerer Kuchen'

        >>> localized.description
        =>  'You know.. cake!'

    If the current language cannot be found, the default language is tried,
    which is the first language from the list of available languages.

    """

    def __init__(self, data, languages, language):
        self.data = data

        self.language = language
        self.languages = languages

        self.default_language = languages[0]

    def localize_dictionary(self, dictionary):
        return dictionary.get(self.language, dictionary[self.default_language])

    def localize_data(self, key):
        if isinstance(self.data[key], dict):
            return self.localize_dictionary(self.data[key])
        else:
            return self.data[key]

    def __getattr__(self, key):
        if key in self.data:
            return self.localize_data(key)

        raise AttributeError
