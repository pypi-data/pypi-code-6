def wtforms_translation_string_factory(domain):
    class _WTFormsLazyTranslationString:

        def __init__(self, msg):
            from . import LazyTranslationString
            self.msg = msg
            self.lts = LazyTranslationString(domain)

        def __str__(self):
            return self.lts.translate(self.msg)
    return _WTFormsLazyTranslationString
