# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from pyrate.services import mailchimp

from .utils import get_language_for_code
from .forms import SubscriptionPluginForm
from .models import SubscriptionPlugin


ERROR_MESSAGES = {
    104: _('Invalid API-Key'),
    200: _('The selected list does not exist.'),
    214: _('You are already subscribed to our list.'),
    230: _('You are already subscribed to our list.'),
}


class SubscriptionView(FormView):

    form_class = SubscriptionPluginForm
    template_name = 'aldryn_mailchimp/subscription.html'

    def form_valid(self, form):
        h = mailchimp.MailchimpPyrate(settings.MAILCHIMP_API_KEY)
        plugin = get_object_or_404(SubscriptionPlugin, pk=form.cleaned_data['plugin_id'])

        merge_vars = None
        if plugin.assign_language:
            language = get_language_for_code(self.request.LANGUAGE_CODE)
            if language:
                merge_vars = {'mc_language': language}

        try:
            h.subscribe_to_list(list_id=plugin.list_id, user_email=form.cleaned_data['email'], merge_vars=merge_vars)
        except Exception, e:
            if hasattr(e, 'code') and e.code in ERROR_MESSAGES:
                message = ERROR_MESSAGES.get(e.code)
            else:
                message = _(u'Oops, something must have gone wrong. Please try again later.')
            messages.error(self.request, message)
        else:
            messages.success(self.request, _(u'You have successfully subscribed to our mailing list.'))
        return redirect(form.cleaned_data['redirect_url'])
