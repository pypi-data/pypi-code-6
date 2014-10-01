"""
Views
"""
from django.views.generic import TemplateView

class StaticPageView(TemplateView):
    page_map = None
    browse_map = True
    
    def get_context_data(self, **kwargs):
        context = super(StaticPageView, self).get_context_data(**kwargs)
        if self.browse_map and self.page_map:
            context.update({
                'page_map': self.page_map,
            })
        return context
    
