from django.views import generic

from .base import TemplateNameResolverMixin


__all__ = (
    'CreateView',
    'CreateViewMixin',
    'DetailView',
    'DetailViewMixin',
    'UpdateView',
    'UpdateViewMixin',
    'DeleteView',
    'DeleteViewMixin',
)


class CreateViewMixin(TemplateNameResolverMixin):
    template_suffixes = ('create', 'editing', 'form')   


class CreateView(CreateViewMixin, generic.CreateView):    
    pass


class DetailViewMixin(TemplateNameResolverMixin):
    template_suffixes = ('detail',) 


class DetailView(DetailViewMixin, generic.DetailView):
    pass


class UpdateViewMixin(TemplateNameResolverMixin):
    template_suffixes = ('update', 'editing', 'form')   


class UpdateView(UpdateViewMixin, generic.UpdateView):    
    pass


class DeleteViewMixin(TemplateNameResolverMixin):
    template_suffixes = ('confirm-delete',) 


class DeleteView(DeleteViewMixin, generic.DeleteView):
    pass
