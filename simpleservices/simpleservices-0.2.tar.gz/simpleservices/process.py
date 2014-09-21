import logging
import signal
import atexit
import subprocess
import os
import json
import sys

logger = logging.getLogger(__name__)
registry = {}

class ManagedProcess(object):
    def __init__(self, args, name, pidfilename,
                 stdout=None, stdin=None, stderr=None,
                 kill_old=True):
        self.name = name
        self.pidfilename = pidfilename

        ##pidfilename and name uniquely identify a services
        registry[(self.pidfilename, self.name)] = self

        data = self.read_pidfile()
        pid = data.get(name)

        if pid and kill_old:
            try:
                os.kill(pid, signal.SIGINT)
            except OSError:
                #this is ok, just means process is not running
                pass
        elif pid and not kill_old:
            raise Exception("process %s is running on PID %s" % (name, pid))
        self.closed = True
        try:
            self.proc = subprocess.Popen(args, stdout=stdout, stderr=stderr, stdin=stdin)
        except OSError as error:
            raise OSError(error.errno, "unable to execute: %s" % " ".join(args))

        self.add_to_pidfile()
        self.closed = False

    def read_pidfile(self):
        if not os.path.exists(self.pidfilename):
            data = {}
            return data
        with open(self.pidfilename, "r") as f:
            try:
                data = json.load(f)
            except ValueError as e:
                logger.info("could not read json in %s", self.pidfilename)
                data = {}
        return data

    def add_to_pidfile(self):
        data = self.read_pidfile()
        data[self.name] = self.proc.pid
        with open(self.pidfilename, "w+") as f:
            json.dump(data, f)

    def remove_from_pidfile(self):
        data = self.read_pidfile()
        if self.name in data:
            del data[self.name]
        with open(self.pidfilename, "w+") as f:
            json.dump(data, f)


    def close(self):
        if not self.closed:
            self.proc.send_signal(signal.SIGTERM)
            #self.proc.kill()
            self.proc.communicate()
            self.remove_from_pidfile()
            self.closed = True

def close(pidfile, name):
    proc = registry.pop((pidfile, name))
    proc.close()

def close_all():
    for k,v in registry.iteritems():
        try:
            v.close()
        except Exception as e:
            logger.exception(e)
    registry.clear()

def exit(*args, **kwargs):
    close_all()
    os._exit(0)

def register_shutdown():
    #does this work in windows?
    signal.signal(signal.SIGTERM, exit)
