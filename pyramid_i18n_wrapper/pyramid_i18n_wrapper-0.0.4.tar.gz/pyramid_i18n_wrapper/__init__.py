from pyramid.i18n import TranslationStringFactory
from pyramid.threadlocal import get_current_request

class LazyTranslationString:
    
    def __init__(self, translation_string_domain=None):
        self.tsd = translation_string_domain
        self.tsf = TranslationStringFactory(translation_string_domain)

    def translate(self, tstring, domain=None, mapping=None):
        localizer = get_current_request().localizer
        if domain is None:
            domain = self.tsd
        return localizer.translate(self.tsf(tstring), domain, mapping)

    def pluralize(self, singular, plural, n, domain=None, mapping=None):
        localizer = get_current_request().localizer
        if domain is None:
            domain = self.tsd
        return localizer.pluralize(
            self.tsf(singular), self.tsf(plural), n, domain, mapping)
