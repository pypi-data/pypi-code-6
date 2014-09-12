# -*- coding: utf-8 -*-
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import TemplateView, RedirectView

from mailto.models import Mail, UserOptin


class OptoutView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if kwargs.get('hash'):
            try:
                uopt = UserOptin.objects.get(hash=kwargs.get('hash'))
                uopt.optin = False
                uopt.save()
            except ObjectDoesNotExist:
                raise

        return getattr(settings, 'MAILTO_OPTOUT_REDIRECT_URL', '/')


class EditHTML(TemplateView):
    object = None

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('pk'):
            self.object = Mail.objects.get(id=self.kwargs.get('pk'))
        return super(EditHTML, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        template_name = 'mailto/default.html'

        if self.object:
            template_name = self.object.template

        return [template_name, ]

    def get_context_data(self, **kwargs):
        context = super(EditHTML, self).get_context_data(**kwargs)
        if self.object and self.object.html:
            placeholders = json.loads(self.object.html)
            context.update(placeholders)
        return context