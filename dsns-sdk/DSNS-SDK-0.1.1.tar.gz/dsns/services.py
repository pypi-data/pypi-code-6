from __future__ import absolute_import

import json

from dsns.connection import BaseConnection


class ChannelAPIService(BaseConnection):
    """
    Channel service to serve various api endpoints
    """
    def __init__(self, **kwargs):
        self.config.resp_format = 'json'
        super(ChannelAPIService, self).__init__(**kwargs)

    def policy(self):
        """
        Description:
            returns default policy for the channel
        returns:
            instance of response formator class
            can be used like:
                response_dict: r.response_dict()
                status_code = r.get_status_code()
        """
        self.config.uri = '/channel/api/policy/'
        return self.execute()

    def list_all(self):
        """
        listing of channels
        """
        self.config.uri = '/channel/api/list/'
        return self.execute()

    def create(self, data, create=True):
        """
        method is being used to create channel
        data:
            {
              "name": "<channel name(unique)>",
              "display_name": "<channel display name>",
              "priority": "<channel priority>"
            }
        """
        self.config.uri = '/channel/api/create/'
        self.method = "POST"
        response = self.execute(data=data)
        if response.get_status_code() == 200:
            from dsns.models import Channel
            resp_dict = response.response_dict()
            r = resp_dict['info']
            channel_drn = r.get(
                "channel_drn", None)
            data.update(**{"channel_drn": channel_drn})
            if create:
                Channel.objects.get_or_create(
                    name=data["name"], channel_drn=data["channel_drn"],
                    defaults=data)
        return response

    def get_by_channel_drn(self, drn):
        """
        get the channel details
        channel_drn:
            channel drn to get the channel
        """
        self.config.uri = "/channel/api/detail/{drn}/".format(drn=drn)
        return self.execute()

    def update_details(self, drn, data):
        """
        method is being used to update details
        of channel
        data:
            {
              "display_name": <display name>,
              "priority": <priority>,
              "policy": <valid json policy>
            }
        """
        self.config.uri = "/channel/api/update/{drn}/".format(
            drn=drn)
        self.method = "PUT"
        return self.execute(data=data)


class SubscriptionAPIService(BaseConnection):
    """
    Channel service to serve various api endpoints
    """
    def __init__(self, **kwargs):
        self.config.resp_format = 'json'
        super(SubscriptionAPIService, self).__init__(**kwargs)

    def policy(self):
        """
        listing of channels
        """
        self.config.uri = '/subscription/api/policy/'
        return self.execute()

    def list_all(self, channel_drn):
        """
        listing of all subscription
        against a channel
        """
        self.query_params = {
            "channel_drn": channel_drn}
        self.config.uri = '/subscription/api/list/'
        return self.execute()

    def list_all_active(self, channel_drn):
        """
        listing of all active subscription
        against a channel
        """
        self.query_params = {
            "channel_drn": channel_drn,
            "active": True}
        self.config.uri = '/subscription/api/list/'
        return self.execute()

    def list_all_inactive(self, channel_drn):
        """
        listing of all inactive subscription
        against a channel
        """
        self.query_params = {
            "channel_drn": channel_drn,
            "active": False}
        self.config.uri = '/subscription/api/list/'
        return self.execute()

    def subscribe(self, data):
        """
        method is being used to create subscription
        data:
            {
              "channel_drn": <channel_drn (Mendatory)>,
              "target_drn": <target_drn (Mendatory)>,
              "protocol": <protocol (Mendatory)>,
              "token": <token to validate request to endpoint (Non-Mendatory)>,
              "username": <username (Non-Mendatory)>,
              "password": <password (Non-Mendatory)>
              "endpoint": <endpoint (Non-Mendatory)>
            }
        """
        self.config.uri = '/subscription/api/create/'
        self.method = "POST"
        response = self.execute(data=data)
        if response.get_status_code() == 200:
            from dsns.models import Channel
            resp_dict = response.response_dict()
            try:
                channel = Channel.objects.get(
                    channel_drn=resp_dict['info']['channel_drn'])
                pre_subs = channel.subscriptions
                ids = [int(
                    each.split('#')[0].split('-')[1]) for each in pre_subs]
            except (Channel.DoesNotExist, KeyError, IndexError), e:
                pass
            else:
                sub = resp_dict['info']
                if not sub['id'] in ids:
                    subscription = "id-%s#target_drn-%s#end_point-%s" % (
                        sub['id'], sub['target_drn'], sub['endpoint'])
                    subs = channel.subscriptions
                    subs.append(subscription)
                    channel.subscriptions = subs
                    channel.save()
        return response

    def update_details(self, channel_drn, subs_id, data):
        """
        method is being used to update details
        of channel
        data:
            {
              "endpoint": <display name>,
              "policy": <policy subscriber>,
              "active": <True/False>,
              "token": <token to validate request to endpoint>,
              "username": <username>,
              "password": <password>
            }
        # Incase BasicAuthentication is selected then username
        and password is mendetory to be passed
        """
        if "policy" in data:
            data['policy'] = json.dumps(data['policy'])
        self.query_params = {"channel_drn": channel_drn}
        self.config.uri = "/subscription/api/update/{subs_id}/".format(
            subs_id=subs_id)
        self.method = "PUT"
        return self.execute(data=data)


class PublishAPIService(BaseConnection):
    def __init__(self, **kwargs):
        self.config.resp_format = 'json'
        super(PublishAPIService, self).__init__(**kwargs)

    def publish(self, data):
        """
        method to publish data into channel
        data:
            {
              "channel_drn": "test:2",
              "target_drn": ["1"],
              "message": '{
                "orderId": "ORDER123",
                "suborderId": "OL123",
                "status": "SHIPPED"}',
              "subject": "REST API TEST",
              "meta": {
                "headers": {
                    "X-EBAY-API-DEV-NAME":"6a6d1553-018d-4864-871b",
                "query_params": {"DEVID": "AIQPV12"}
                }}
            }
        """
        self.method = "POST"
        self.config.uri = "/channel/api/publish/"
        if "meta" in data:
            data["meta"] = json.dumps(data["meta"])
        return self.execute(data=data)
