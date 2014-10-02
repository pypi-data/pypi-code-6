import collections
from classymq.registry import RegistryBase

__author__ = 'gdoermann'

class EventRegistry(RegistryBase):

    def __init__(self, *args, **kwds):
        RegistryBase.__init__(self, *args, **kwds)
        self.cataloged = False

    def event_name(self, event):
        if isinstance(event, basestring):
            return event
        else:
            return event.NAME

    def register(self, event, *args, **kwargs):
        super(EventRegistry, self).register(event.NAME, event)

    def unregister(self, event):
        super(EventRegistry, self).unregister(self.event_name(event))

    def is_registered(self, event):
        return super(EventRegistry, self).is_registered(self.event_name(event))

    def get(self, event):
        return self.reg.get(self.event_name(event))

    def set(self, key, event):
        if not key:
            key = event.NAME
        self.reg[key] = event

    def autodiscover(self):
        if self.cataloged:
            return
        exec('from classymq.event.events *')
        self.cataloged = True

    def sorted(self):
        sitems = self.items()
        sitems.sort()
        d = collections.OrderedDict(sitems)
        return d

    def reconstruct(self, d):
        name = d.get('event__name', None)
        if not name:
            return None
        klass = self.get(name)
        return klass(**d)

registry = EventRegistry()
