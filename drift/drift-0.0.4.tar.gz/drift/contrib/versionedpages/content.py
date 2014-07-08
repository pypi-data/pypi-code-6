from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe

from drift import content

from .models import Page


class PageHistoryPanel(content.ContentPanelBase):
    def get_header(self):
        return mark_safe(
            u'<button class="btn btn-xs toggle_content_history">History '
            '<i class="fa fa-chevron-down"></i></button>'
        )

    def get_panel_template_name(self):
        return 'versionedpages/_history_panel.html'


class PageContent(content.ModelContent):
    name = "Versioned Web Page"
    contenteditable = ('title',)
    exclude = ('is_published', 'published', 'published_version')
    prepopulated_fields = {'url': 'title'}

    panels = (PageHistoryPanel,)

    def get_form_initial_data(self, request):
        if request is not None and request.user.is_authenticated():
            return dict(owner=request.user)
        else:
            return None

    def get_new_url(self):
        return reverse_lazy('new_versioned_page')

    def get_edit_url(self):
        if self.instance is not None:
            return reverse_lazy('edit_versioned_page', args=[self.instance.url])
        return None


content.system.register(Page, PageContent)
