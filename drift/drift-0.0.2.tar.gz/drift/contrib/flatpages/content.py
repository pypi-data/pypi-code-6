from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe

from drift import content
from .models import Flatpage


class FlatpageContent(content.ModelContent):
    contenteditable = ('title', 'content')

    def get_new_url(self):
        return reverse_lazy('new_flatpage')

    def get_edit_url(self):
        if self.instance is not None:
            return reverse_lazy('edit_flatpage', args=[self.instance.url])
        return None


content.system.register(Flatpage, FlatpageContent)
