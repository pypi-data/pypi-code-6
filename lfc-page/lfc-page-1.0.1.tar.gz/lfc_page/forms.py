# django imports
from django import forms

# lfc imports
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.fields.wysiwyg import WYSIWYGInput

# tagging imports
from tagging.forms import TagField

# lfc_page imports
from lfc_page.models import Page


class PageDataForm(forms.ModelForm):
    """Core data form for pages.
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)

    class Meta:
        model = Page
        fields = ("title", "display_title", "slug", "description", "text", "tags")

    def __init__(self, *args, **kwargs):
        super(PageDataForm, self).__init__(*args, **kwargs)
        self.fields["text"].widget = WYSIWYGInput()
