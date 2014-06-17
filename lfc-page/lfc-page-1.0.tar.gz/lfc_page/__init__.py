# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type

# lfc_page imports
from lfc_page.models import Page

name = "Page"
description = _(u"HTML pages for LFC")


def install():
    """Installs the blog application.
    """
    # Register objects
    register_content_type(
        Page,
        name="Page",
        sub_types=["Page"],
        templates=["Article", "Plain", "Gallery", "Overview"],
        default_template="Article")


def uninstall():
    """Uninstalls the blog application.
    """
    # Unregister content type
    unregister_content_type("Page")
