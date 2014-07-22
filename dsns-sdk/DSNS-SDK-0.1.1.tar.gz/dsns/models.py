from django.db import models
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError

from south.modelsinspector import add_introspection_rules

from requests.exceptions import ConnectionError

from dsns.app_settings import CHANNEL_PRIORITY

from dsns.fields import ListField

from dsns.api import DSNS


add_introspection_rules([], ["^dsns\.fields\.ListField"])


class Channel(models.Model):
    """
    application lavel channels.
    """
    name = models.CharField(
        max_length=256, validators=[validate_slug])
    display_name = models.CharField(
        max_length=256, null=True, blank=True)
    channel_drn = models.CharField(
        max_length=300, null=True, blank=True)
    priority = models.CharField(max_length=6, choices=CHANNEL_PRIORITY)
    subscriptions = ListField(null=True, blank=True)
    create_to_server = models.BooleanField(
        default=True,
        help_text="Uncheck if DSNS server is not connected")

    class Meta:
        unique_together = ("name", "channel_drn")

    def __unicode__(self):
        return "%s:(%s)" % (self.name, self.priority)

    def clean(self, *args, **kwargs):
        if self.create_to_server:
            if not self.channel_drn:
                try:
                    self.create_channel_to_server(*args, **kwargs)
                except (ConnectionError, ValidationError), e:
                    raise ValidationError(e.message)
        super(Channel, self).clean(*args, **kwargs)

    def create_channel_to_server(self, *args, **kwargs):
        """
        function interact with dsns server and
        creates channel
        """
        data = {
            "name": self.name, "display_name": self.display_name,
            "priority": self.priority}
        dsns = DSNS()
        resp = dsns.channel.create(data=data, create=False)
        if not resp.get_status_code() == 200:
            error = resp.response_dict().get(
                "message", "Connection Error with DSNS server")
            raise ValidationError(
                "DSNS server raised error: '%s', "
                " can not create channel" % error)
        r = resp.response_dict()
        self.channel_drn = r.get("info", {}).get("channel_drn", None)
