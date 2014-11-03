from django.conf import settings
from django.core.exceptions import ValidationError


__all__ = ['validate_url_keyword']


_default_keywords = ('new', 'edit', 'delete')


_keywords = getattr(settings, 'URL_KEYWORDS', _default_keywords)


def validate_url_keyword(value):
    """
    Validates that `value` is not one of the "keywords" to be used in
    URL design for this project.
    """
    if value in _keywords:
        raise ValidationError("Identifier cannot be \"%s\"" % value)
