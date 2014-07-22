from django.contrib import admin

from dsns.models import Channel


class ChannelAdmin(admin.ModelAdmin):
    """
    Description:
        model admin class for channels
    """
    model = Channel
    readonly_fields = ('get_channel_drn',)

    def get_channel_drn(self, instance):
        """
        Returns Actual value of channel DRN
        """
        return instance.channel_drn

    get_channel_drn.short_description = "Channel DRN"

admin.site.register(Channel, ChannelAdmin)
# Register your models here.
