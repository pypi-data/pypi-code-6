from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django import dispatch
from django.contrib.sites.models import Site

from rest_framework.authtoken.models import Token

from threebot.models import Workflow
from threebot.models import Worker
from threebot.models import ParameterList


@python_2_unicode_compatible
class Hook(models.Model):
    slug = models.SlugField(max_length=255)
    user = models.CharField(max_length=255, blank=True, null=True)
    repo = models.CharField(max_length=255, blank=True, null=True)
    secret = models.CharField(max_length=255, blank=True, null=True)
    workflow = models.ForeignKey(Workflow)
    worker = models.ForeignKey(Worker)
    param_list = models.ForeignKey(ParameterList)

    def get_hook_url(self):
        return "%d-%d-%d-%s" % (self.workflow.id, self.worker.id, self.param_list.id, self.slug)

    def __str__(self):
        return "%s (%d)" % (self.get_hook_url(), self.pk)

    def make_full_url(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return "https://%s/hooks/%s/%s-%s-%s/" % (Site.objects.get_current().domain, token, self.workflow.id, self.worker.id, self.param_list.id)

    class Meta():
        verbose_name = _("Hook")
        verbose_name_plural = _("Hooks")
        db_table = 'threebot_hook'
        unique_together = ("workflow", "worker", "param_list")


class HookSignal(dispatch.Signal):
    pass

pre_hook_signal = HookSignal()
post_hook_signal = HookSignal()
