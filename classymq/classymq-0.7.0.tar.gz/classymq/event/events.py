import json
from uuid import uuid4
from classymq.utils import AttrDict

__author__ = 'gdoermann'


class BaseEvent(AttrDict):
    NAME = ''
    def __init__(self, *args, **kwargs):
        """
        The sender is defined by its CONSUMER you may pass in a consumer object or a the log_header_dict
        information about a consumer. The log header contains a uuid which can be used to route the
         response back to the correct consumer.
        """
        super(BaseEvent, self).__init__(*args, **kwargs)
        if not self.get('event_name', None):
            self.event_name = self.NAME.format(**kwargs)
        self.event_uuid = str(uuid4())
        self.update(kwargs)

    def routing_key(self, *args, **kwargs):
        return self.event_name

    def __str__(self):
        return json.dumps(self)

class BaseResponse(BaseEvent):
    def __init__(self, request, *args, **kwargs):
        super(BaseResponse, self).__init__(request.consumer, *args, **kwargs)
        self.request = request

class ModelEvent(BaseEvent):
    NAME = '{action}.{model}.{pk}'
    ACTION = ''
    def __init__(self, model, pk, *args, **kwargs):
        kwargs['pk'] = pk
        kwargs['model'] = model
        if not kwargs.has_key('action'):
            kwargs['action'] = self.ACTION
        super(ModelEvent, self).__init__(*args, **kwargs)


class CreationEvent(ModelEvent):
    ACTION = 'creation'

class ActivationEvent(ModelEvent):
    ACTION = 'activation'

    def __init__(self, model, pk, active=True, *args, **kwargs):
        super(ActivationEvent, self).__init__(model, pk, *args, **kwargs)
        self.active = active

class UpdateEvent(ModelEvent):
    ACTION = 'update'

    def __init__(self, model, pk, *args, **kwargs):
        super(UpdateEvent, self).__init__(model, pk, *args, **kwargs)
