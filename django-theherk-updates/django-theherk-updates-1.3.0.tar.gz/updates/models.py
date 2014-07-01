from django.db import models
from cms.models import CMSPlugin
from django.utils.translation import ugettext_lazy as _


class Update(models.Model):
    """
    Defines a date on which updates were made.
    """
    date = models.DateField(_('Update Date'))

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'update'
        verbose_name_plural = 'updates'
        app_label = 'updates'


class UpdateItem(models.Model):
    """
    Defines one or many items that were updated on a single date.
    """
    update = models.ForeignKey(Update)
    item = models.CharField(_('Update Item'), max_length=256)
    description = models.TextField(
        _('Item Description (Optional)'),
        help_text="This field is optional and should only be used when the description is too long for the sidebar plugin.",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.item

    class Meta:
        verbose_name = 'updateitem'
        verbose_name_plural = 'updateitems'
        app_label = 'updates'


class UpdatesPlugin(CMSPlugin):
    number_to_show = models.IntegerField(
        max_length=10,)

