from datetime import datetime, timedelta

from vistrails.core.interpreter.job import JobMixin
from vistrails.core.modules.vistrails_module import Module, ModuleError


class TimeMonitor(object):
    def __init__(self, target_time):
        self.time = target_time

    def finished(self):
        return datetime.now() > self.time


class Delay(JobMixin, Module):
    """ Suspends until a mumber of seconds have passed
    """
    _input_ports = [('seconds', '(org.vistrails.vistrails.basic:Float)', True)]

    def getId(self, params):
        return str(params['delay'])

    def readInputs(self):
        if not self.has_input('seconds'):
            raise ModuleError(self, "No time specified")
        return {'delay': self.get_input('seconds')}

    def startJob(self, params):
        # calculate target time
        params['time'] = str(datetime.now() +
                             timedelta(seconds=params['delay']))
        return params

    def getMonitor(self, params):
        return TimeQueue(datetime.strptime(params['time'],
                                           '%Y-%m-%d %H:%M:%S.%f'))

    def finishJob(self, params):
        "not needed"

    def setResults(self, params):
        "not needed"


_modules = [Delay]
