from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PortafolioApp(CMSApp):
    name = _("Portafolio App")  # give your app a name, this is required
    urls = ["linkuxit.portafolio.urls"]  # link your app to url configuration(s)


apphook_pool.register(PortafolioApp)  # register your app
