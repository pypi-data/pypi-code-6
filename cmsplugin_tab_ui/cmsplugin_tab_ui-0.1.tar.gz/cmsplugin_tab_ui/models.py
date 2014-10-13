from django.db import models
from cms.models import CMSPlugin
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from paintstore.fields import ColorPickerField
# Create your models here.

@python_2_unicode_compatible
class TabUiList(CMSPlugin):
    custom_classes = models.CharField(_('custom classes'), max_length=200, blank=True)
    align = models.CharField(max_length=1, default='h',
                              choices=(('v', _('Vertical')), ('h', _('Horizontal')) ) 
                             )    
    
    def __str__(self):
        return _("%s columns") % self.cmsplugin_set.all().count()

@python_2_unicode_compatible
class TabUi(CMSPlugin):
    title = models.CharField(max_length=255)
    title_color = ColorPickerField(blank=True, null=True)
    background_color = ColorPickerField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    