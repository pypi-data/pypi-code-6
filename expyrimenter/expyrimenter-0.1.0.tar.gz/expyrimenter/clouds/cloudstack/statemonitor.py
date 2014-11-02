from . import API
from multiprocessing import Manager, Process
from time import sleep
import logging
import signal


class StateMonitor:
    _stop = False

    def __init__(self, proxy_states):
        self._logger = logging.getLogger('cloudstack.statemonitor')
        self._logger.info('started')

        self._proxy_states = proxy_states
        self._local_states = {}
        self._api = API()

    def monitor_states(self, interval=5):
        while not StateMonitor._stop:
            self._monitor_states_once()
            sleep(interval)
        self._logger.info('finished')

    @staticmethod
    def stop():
        StateMonitor._stop = True

    def _monitor_states_once(self):
        vms = self._api.listVirtualMachines()['virtualmachine']
        for vm in vms:
            self._update_state(vm['name'], vm['state'])

    def _update_state(self, k, v):
        if v != self._local_states.get(k):
            self._local_states[k] = v
            self._proxy_states[k] = v


def handler(signum, frame):
    StateMonitor.stop()


signal.signal(signal.SIGTERM, handler)


def monitor_states(states):
    sm = StateMonitor(states)
    sm.monitor_states()


# Ensure only one state monitor is running at most
class StateMonitorProcess:
    _mgr, _states, _process = None, None, None

    @staticmethod
    def start():
        if StateMonitorProcess._process is None:
            cls = StateMonitorProcess
            cls._mgr = Manager()
            cls._states = cls._mgr.dict()
            cls._process = Process(target=monitor_states, args=(cls._states,))
            cls._process.start()

    @staticmethod
    def stop():
        if not StateMonitorProcess._process is None:
            cls = StateMonitorProcess
            cls._process.terminate()
            cls._process.join()
            cls._states.clear()
            cls._mgr.shutdown()
            cls._mgr, cls._states, cls._process = None, None, None

    @staticmethod
    def get_states():
        return StateMonitorProcess._states
