"""a basic event dispatcher mechanism
"""

import logging
logger = logging.getLogger('EventDispatcher')

class EventDispatcher(type):
    """An event dispatcher
    """
    
    def __init__(cls, name, bases, newattrs):
        """ Magic needed to create a class with EventDispatcher methods,
        and an empty callbacks property """
        super(EventDispatcher, cls).__init__(name, bases, newattrs)
        
        cls.emit_event = EventDispatcher.emit_event
        
        for key, value in EventDispatcher.__dict__.items():
            if not key.startswith('__'):
                setattr(cls, key, value)
        
    def test_callbacks_dict(self):
        if not hasattr(self,'callbacks'):
            self.callbacks = dict()
    
    def add_listener(self, name, callback, *args, **kwargs):
        """Adds an event listener on the instance.
        
        :param name: event name to listen for
        :type name: unicode or str

        :param callback: the callable to fire when the event is emitted
        :type callback: callable
        
        Additionnal args and kwargs are passed to the callback when the event
        is fired
        
        If you want to stop the callback chain, your callback should
        return False. All other return values are discarded.
        """
        self.test_callbacks_dict()
        d = dict(callback=callback, args=args, kwargs=kwargs)
        self.callbacks.setdefault(name, []).append(d)

    def remove_listener(self, name, func):
        """
        Removes a callback from the callback list for the given
        event name.

        :param name: event name to listen for
        :type name: unicode or str
        
        :param func: the function of the callback to unregister
        :type func: method
        """
        self.test_callbacks_dict()
        if self.callbacks.has_key(name):
            callbacks = self.callbacks[name]
            [callbacks.remove(callback) for callback in callbacks if callback['callback'] == func]

    def emit_event(self, name, *args, **kwargs):
        """
        Emit a named event. This will fire all the callbacks registered
        for the named event.

        :param name: event name to listen for
        :type name: unicode or str

        Additionnal args and kwargs are passed to the callbacks (before the one that were passed to add_listener)
        """
        logger.debug("%s: calling %s with %s and %s" % (repr(self), name,
                                                    repr(args), repr(kwargs)))
        self.test_callbacks_dict()
        for cbdict in self.callbacks.get(name, list()):
            handler = cbdict.get('callback')

            listener_args = cbdict.get('args')
            listener_kwargs = cbdict.get('kwargs')

            myargs = list(args)
            myargs.extend(listener_args)
            mykwargs = kwargs
            mykwargs.update(listener_kwargs)

            result = handler(*myargs, **mykwargs)
            
            if result is False:
                break
