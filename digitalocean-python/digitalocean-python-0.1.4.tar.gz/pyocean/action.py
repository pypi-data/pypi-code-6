# encoding: utf-8

from .base import Resource, ResourceIterator


class Action(Resource):
    """This class represents an Action.

    Actions are records of events that have occured on the resources
    in your account (creating droplet, rebooting droplet, etc).

    """

    def __init__(self, attrs={}):
        super(Action, self).__init__(attrs)

    def create(self, *args, **kwargs):
        raise AttributeError("'Action' object has no attribute 'create'.")

    def destroy(self, *args, **kwargs):
        raise AttributeError("'Action' object has no attribute 'create'.")

    def __str__(self):
        return "<Action '%s' (%s)>" % (self.type, self.status)


class ActionIterator(ResourceIterator):
    """This class is the container for the Action objects.
    """

    def __init__(self, droplet_id=None):
        super(ActionIterator, self).__init__()
        if droplet_id:
            self._resource = 'droplets/%s/actions' % droplet_id
