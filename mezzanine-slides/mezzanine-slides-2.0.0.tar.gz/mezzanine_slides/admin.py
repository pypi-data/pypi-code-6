from django.conf import settings

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.forms.admin import FormAdmin
from mezzanine.galleries.admin import GalleryAdmin

from .models import Slide


class SlideInline(TabularDynamicInlineAdmin):
    model = Slide


PageAdmin.inlines += (SlideInline,)
FormAdmin.inlines += (SlideInline,)
GalleryAdmin.inlines += (SlideInline,)


if "cartridge.shop" in settings.INSTALLED_APPS:
    from cartridge.shop.admin import CategoryAdmin
    CategoryAdmin += (SlideInline,)

