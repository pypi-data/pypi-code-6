from django.views import generic

from .base import TemplateNameResolverMixin


__all__ = (
    'ListView',
)


class ListViewMixin(TemplateNameResolverMixin):    
    template_suffixes = ('list',)


class ListView(ListViewMixin, generic.ListView):
    pass
