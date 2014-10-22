from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, DetailView, UpdateView, CreateView, DeleteView, ListView

oak_template_base = 'oak'


class BaseOakView(View):
    """

    """
    oak_enabled = False

    def get_context_data(self, **kwargs):
        context = super(BaseOakView, self).get_context_data(**kwargs)
        context['current_url'] = self.current_url
        context['target_url'] = self.target_url
        return context

    @property
    def current_url(self):
        return self.request.path

    @property
    def target_url(self):
        return (self.request.GET.get('target_url') or self.request.POST.get('target_url')) or ''

    def generate_template_names(self, section):
        assert(section in ['detail', 'create', 'update', 'delete', 'list'], "unknown section")
        template_names = super(BaseOakView, self).get_template_names()
        if self.oak_enabled and hasattr(self, 'model'):
            app_label, model_name = self.model._meta.app_label, self.model._meta.model_name
            template_names.insert(0, '/'.join([app_label, model_name, '%s.html' % section]))
            template_names.append('/'.join([app_label, oak_template_base, '%s.html' % section]))
            template_names.append('/'.join([oak_template_base, '%s.html' % section]))

        return template_names


class ProtectedBaseOakView(BaseOakView):
    """

    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProtectedBaseOakView, self).dispatch(request, *args, **kwargs)


class BaseDetailView(BaseOakView, DetailView):
    """

    """


class BaseUpdateView(ProtectedBaseOakView, UpdateView):
    """

    """
    def get_template_names(self):
        return self.generate_template_names('update')

    def get_success_url(self):
        return reverse_lazy('%s-%s-list' % (self.model._meta.app_label, self.model._meta.model_name))


class BaseCreateView(ProtectedBaseOakView, CreateView):
    """

    """
    def get_template_names(self):
        return self.generate_template_names('create')

    def get_success_url(self):
        return reverse_lazy('%s-%s-list' % (self.model._meta.app_label, self.model._meta.model_name))


class BaseDeleteView(ProtectedBaseOakView, DeleteView):
    """

    """
    def get_template_names(self):
        return self.generate_template_names('delete')

    def get_success_url(self):
        return reverse_lazy('%s-%s-list' % (self.model._meta.app_label, self.model._meta.model_name))


class BaseListView(BaseOakView, ListView):
    """

    """
    def get_template_names(self):
        return self.generate_template_names('list')


class BaseCrudView(object):
    """

    """
    model = None
    fields = None