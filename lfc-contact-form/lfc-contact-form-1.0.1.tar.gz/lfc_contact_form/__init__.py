# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type
from lfc.utils.registration import register_template
from lfc.utils.registration import unregister_template

# lfc_contact_form import
from lfc_contact_form.models import ContactForm

name = _(u"Contact Form")
description = _(u"Contact form for LFC")
version = u"1.0.1"


def install():
    """Installs the lfc_contact_form application.
    """
    # Register Templates
    register_template(name="Contact Form", path="lfc_contact_form/contact_form.html")

    # Register objects
    register_content_type(ContactForm, name="Contact", templates=["Contact Form"], default_template="Contact Form", global_addable=True, workflow="Portal")


def uninstall():
    """Uninstalls the lfc_contact_form application.
    """
    # unregister your stuff here
    unregister_content_type("ContactForm")

    # Unregister template
    unregister_template("Contact Form")
