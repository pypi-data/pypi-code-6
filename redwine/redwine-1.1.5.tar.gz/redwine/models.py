from django.db import models
from django.db.models import Count
from django.conf import settings
from django.db.models.signals import post_save
#from django.contrib.auth import get_user_model

class Penalty(models.Model):
    
    to =        models.ForeignKey(settings.AUTH_USER_MODEL, related_name='penalties')
    giver =     models.ForeignKey(settings.AUTH_USER_MODEL, related_name='penaltygiver')
    amount =    models.PositiveIntegerField()
    committee = models.CharField(max_length=60)
    reason =    models.CharField(max_length=100)
    date =      models.DateTimeField(auto_now=True)
    deleted =   models.BooleanField(default=False)
    item =      models.CharField(default="wine", max_length=30)
    item_name = models.CharField(default="vin", max_length=30)
    def __unicode__(self):
        return u'%s - %s' % (self.amount, self.to)
    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'
