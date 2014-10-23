try:
    import pyinotify
except ImportError:
    raise ImportError("The pyneric.fsnotify module requires pyinotify.")

# Check the pyinotify version (must be >= 0.9).
_version = pyinotify.__version__.split('.')
if not (int(_version[0]) > 0 or int(_version[1]) >= 9):
    raise ImportError("The pyneric.fsnotify module requires pyinotify >= 0.9.")
del _version


class FileSystemNotifier(object):

    """Notify the caller of file system changes via a queue using pyinotify.

    The queue must be a Python Queue object (from the queue standard library
    module; Queue module in Python 2).

    Events from the pyinotify library are put onto the queue according to the
    watches the caller configures.  The notifier needs to be started via the
    `start` method to get the events.  The notifier needs to be stopped via the
    `stop` method when the caller would like to stop the events or delete the
    notifier.

    Note that the inotify polling occurs in a separate thread, and one thread
    is created for each FileSystemNotifier instance, so if it is feasible,
    sharing a notifier/queue is recommended for multiple watches.

    """

    def __init__(self, queue):
        self.queue = queue
        def process_func(self, event):
            queue.put(event)
        ProcessEvent = type('ProcessEvent', (pyinotify.ProcessEvent,),
                            dict(process_default=process_func))
        self.watch_manager = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.watch_manager,
                                                   ProcessEvent())

    def __getattr__(self, item):
        proxy_for = self.watch_manager
        if item in ('start', 'stop'):
            proxy_for = self.notifier
        return getattr(proxy_for, item)
