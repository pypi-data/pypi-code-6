from django.utils.translation import ugettext_lazy as _
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class FaqHook(CMSApp):
    name = _('FAQs')
    urls = ["faq.urls"]

apphook_pool.register(FaqHook)