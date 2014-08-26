from django.conf import settings

__all__ = (
    'TemplateNameResolverMixin',
)

_default_separators = None
def default_separators():
    global _default_separators
    if not _default_separators:
        try:
            _default_separators = settings.template_suffix_separators
        except AttributeError:
            _default_separators = ('-',)
    return _default_separators

_default_extensions = None
def default_extensions():
    global _default_extensions
    if not _default_extensions:
        try:
            _default_extensions = settings.template_extensions
        except AttributeError:
            _default_extensions = ('html',)
    return _default_extensions

class TemplateNameResolverMixin(object):
    """
    Overrides get template name.
    """
    
    template_suffixes = ('',)
    template_suffix_separators = default_separators()
    template_extensions = default_extensions()

    def __template_name_parts(self):
        for suffix in self.template_suffixes:
            for separator in self.template_suffix_separators:
                for extension in self.template_extensions:
                    yield suffix, separator, extension

    def __format_template_name(self, suffix, separator, extension):
        args = (
            self.model._meta.app_label,
            self.model._meta.model_name,
            (separator + suffix if suffix else ""),
            extension,
        )
        name = '%s/%s%s.%s' % args
        return name

    def __template_names(self):
        """
        Generator function that resolves template names.
        """
        for suffix, separator, extension in self.__template_name_parts():
            yield self.__format_template_name(suffix, separator, extension)

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]
        template_names = list(self.__template_names())
        return template_names
