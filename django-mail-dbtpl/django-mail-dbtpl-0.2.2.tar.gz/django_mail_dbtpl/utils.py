from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template_from_string

from .models import EmailTemplate


class EmailWrapper(EmailMessage):
    """
    Class wrapper over standard class ``django.core.mail.EmailMessage``. Class constructor accepts optional parameters
    ``slug``, ``context``. Returns an object of class ``EmailMessage`` with defined parameter
    ``content_subtype = 'html'`` and filled in the template fields ``subject`` and ``body``.
    """
    content_subtype = 'html'

    def __init__(self, slug, context=None, **kwargs):
        if not context:
            context = Context({})
        elif isinstance(context, dict):
            context = Context(context)
        kw = kwargs.copy()
        email_tpl = EmailTemplate.objects.get(slug=slug)
        subject = get_template_from_string(email_tpl.subject)
        kw['subject'] = subject.render(context)
        body = get_template_from_string(email_tpl.body)
        kw['body'] = body.render(context)
        super(EmailWrapper, self).__init__(**kw)
