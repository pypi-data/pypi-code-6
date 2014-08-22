__all__ = (
    'TemplateNameResolverMixin',
)


class TemplateNameResolverMixin(object):
    """
    Overrides get template name.
    """
    
    template_suffixes = ('',)
    template_suffix_separators = ('-',)
    template_extensions = ('html',)

    def __template_name_parts(self):
        for suffix in self.template_suffixes:
            for separator in self.template_suffix_separators:
                for extension in self.template_extensions:
                    yield suffix, separator, extension

    def __format_template_names(self, suffix, separator, extension):
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
            yield self.__format_template_names(suffix, separator, extension)

    def get_template_names(self):
        if self.template_name is not None:
            return [self.template_name]
        template_names = list(self.__template_names())
        return template_names
