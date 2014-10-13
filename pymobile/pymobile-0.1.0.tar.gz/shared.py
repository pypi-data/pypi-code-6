from threading import Event, Thread, RLock
import logging
import uuid

# shared variables for workers and webserver
stop = Event()  # signal to stop workers.
lock = RLock()  # lock the shared-module if needed.

state = {}  # dict for storing worker status.


  #
# # # workers:  Use this to start and stop threads. add threads with
  #             the worker-decorator: @shared.worker
# # #
class Workers(object):
    def __init__(self):
        # list of workers registered with @shared.worker
        self.workers = []
        
    def append(self, worker):
        self.workers.append(worker)

    def start(self):
        for worker in self.workers:
            logging.info('started worker {}'.format(worker.name))
            worker.start()

    def stop(self):
        global stop
        stop.set()
        for worker in self.workers:
            logging.info('stopped worker {}'.format(worker.name))
            worker.join()

workers = Workers()


# decorator for appending a function to worker-pool
def worker(workerfunc):
    workers.append(Thread(target=workerfunc, name=workerfunc.__name__))


  #
# # #  session:  Use this for user-login.
  #
class Session(object):
    def __init__(self):
        self._sid = lambda: None  # override with webframework request get cookie function
        self._registersid = lambda sid: None  # override with webframework response set cookie function
        self._session = dict()

    @property
    def sid(self):
        _sid = self._sid()
        if not _sid in self._session:
            _sid = uuid.uuid4().hex
            self._registersid(_sid)
            self._session[_sid] = dict()
        return _sid
    
    def __getitem__(self, attr):
        return self._session[self.sid].get(attr, None)
    
    def __setitem__(self, attr, val):
        self._session[self.sid][attr] = val
        
    def __delitem__(self, attr, val):
        del self._session[self.sid][attr]
        
    def items(self):
        return self._session[self.sid].items()
    
    def get(self, item, default):
        return self._session[self.sid].get(item, default)

    def get_from(self, sid, item, default):
        if sid in self._session:
            return self._session[sid].get(item, default)
        else:
            return default

session = Session()


try:
    from localshared import *
except ImportError:
    pass

# add your shared project-related stuff here
