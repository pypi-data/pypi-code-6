# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from models import ContactPlugin
from forms import ContactForm


class ContactCMSPlugin(CMSPluginBase):
    model = ContactPlugin
    name = _("Contact Form")
    render_template = "aldryn_contact/contact.html"

    def render(self, context, instance, placeholder):
        request = context['request']

        if request.method == "POST":
            form = ContactForm(request.POST)
            if form.is_valid():
                form.send(instance.site_email)
                context.update({'contact': instance})
                return context
        else:
            form = ContactForm()

        context.update({'contact': instance, 'form': form})
        return context


plugin_pool.register_plugin(ContactCMSPlugin)
