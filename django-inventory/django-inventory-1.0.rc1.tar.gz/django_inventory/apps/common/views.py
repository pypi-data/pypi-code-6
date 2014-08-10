from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'main/about.html'


def password_change_done(request):
    messages.success(request, _(u'Your password has been successfully changed.'))
    return redirect('home')
