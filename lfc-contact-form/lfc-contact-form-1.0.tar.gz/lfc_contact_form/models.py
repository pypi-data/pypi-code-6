# django imports
from django import forms
from django.db import models

# django imports
from django.core.mail import send_mail
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# lfc imports
import lfc.utils
from lfc.fields.wysiwyg import WYSIWYGInput
from lfc.models import BaseContent

# lfc_contact_form imports
from lfc_contact_form.forms import ContactForm as DjangoContactForm


class ContactForm(BaseContent):
    """Contact form for LFC.
    """
    text = models.TextField(_(u"Text"), blank=True)
    thank_you_message = models.TextField(blank=True)

    def get_searchable_text(self):
        """Returns the searchable text of the contact form.
        """
        searchable_text = self.title + " " + self.description + " " + self.text
        return lfc.utils.html2text(searchable_text)

    def edit_form(self, **kwargs):
        """Returns the add/edit form of the Blog
        """
        return ContactFormForm(**kwargs)

    def render(self, request):
        """Renders the content of the contact form.

        This adds the form and sent to the RequestContext.
        """
        portal = lfc.utils.get_portal()
        if request.method == "POST":
            form = DjangoContactForm(data=request.POST)
            if form.is_valid():
                sent = True
                message = render_to_string("lfc_contact_form/mail.html", RequestContext(request, {
                    "form": form,
                }))
                send_mail(
                    subject=_("New mail from %s" % portal.title),
                    message=message,
                    from_email=portal.from_email,
                    recipient_list=portal.get_notification_emails()
                )
            else:
                sent = False
        else:
            form = DjangoContactForm()
            sent = False

        self.context["sent"] = sent
        self.context["form"] = form

        return super(ContactForm, self).render(request)


class ContactFormForm(forms.ModelForm):
    """The add/edit form of the ContactForm content object.
    """
    class Meta:
        model = ContactForm
        fields = ("title", "display_title", "slug", "description", "text", "thank_you_message")

    def __init__(self, *args, **kwargs):
        super(ContactFormForm, self).__init__(*args, **kwargs)
        self.fields["text"].widget = WYSIWYGInput()
        self.fields["thank_you_message"].widget = WYSIWYGInput()
