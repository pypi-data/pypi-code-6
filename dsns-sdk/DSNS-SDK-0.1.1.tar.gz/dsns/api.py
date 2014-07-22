"""
main api handler to process various api request
"""
from dsns.services import ChannelAPIService, SubscriptionAPIService
from dsns.services import PublishAPIService


class DSNS(object):
    """
    Main dsns app handlers that handles api
    like channel, subscription
    Usage:
        >>dsns = DSNS(**params)
        # to list all channels
        >>dsns.channel.list(params)
        # to create channel
        >>dsns.channel.create(params)
    """
    __channel_api = ChannelAPIService
    __subscription_api = SubscriptionAPIService
    __publish_api = PublishAPIService

    def __init__(self, **kwargs):
        self.params = kwargs

    @property
    def channel(self):
        """
        instance of channel api
        """
        if DSNS.__channel_api:
            return DSNS.__channel_api(**self.params)

    @property
    def subscription(self):
        """
        instance of subscription api
        """
        if DSNS.__subscription_api:
            return DSNS.__subscription_api(**self.params)

    @property
    def publisher(self):
        """
        instance of publish api
        """
        if DSNS.__publish_api:
            return DSNS.__publish_api(**self.params)
