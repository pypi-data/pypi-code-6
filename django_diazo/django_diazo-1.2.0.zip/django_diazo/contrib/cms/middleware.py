from cms.constants import RIGHT
from cms.toolbar.items import TemplateItem
from django_diazo.utils import check_themes_enabled


class DjangoCmsDiazoMiddleware(object):
    """
    Django CMS 3 add-on
    """

    def process_request(self, request):
        """
        Add Django CMS 3 on/off switch to toolbar
        """
        if request.user.is_staff:
            if 'theme_on' in request.GET and not request.session.get('django_diazo_theme_enabled', False):
                request.session['django_diazo_theme_enabled'] = True
            if 'theme_off' in request.GET and request.session.get('django_diazo_theme_enabled', True):
                request.session['django_diazo_theme_enabled'] = False
        if hasattr(request, 'toolbar'):
            request.toolbar.add_item(
                TemplateItem(
                    "cms/toolbar/items/on_off.html",
                    extra_context={
                        'request': request,
                        'diazo_enabled': check_themes_enabled(request),
                    },
                    side=RIGHT,
                ),
                len(request.toolbar.right_items),
            )
