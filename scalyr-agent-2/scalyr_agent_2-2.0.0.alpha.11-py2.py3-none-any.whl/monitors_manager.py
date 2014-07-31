# Copyright 2014, Scalyr, Inc.

import inspect
import os
import sys
import threading

from scalyr_agent.agent_status import MonitorManagerStatus
from scalyr_agent.agent_status import MonitorStatus

import scalyr_agent.scalyr_logging as scalyr_logging

log = scalyr_logging.getLogger(__name__)


class MonitorsManager(object):
    def __init__(self, configuration):
        self.__config = configuration
        self.__monitors = configuration.monitors
        self.__running_monitors = []
        self.__lock = threading.Lock()

    def generate_status(self):
        try:
            self.__lock.acquire()
            result = MonitorManagerStatus()

            for monitor in self.__monitors:
                if monitor.isAlive():
                    result.total_alive_monitors += 1

                status = MonitorStatus()
                status.monitor_name = monitor.monitor_name
                status.reported_lines = monitor.reported_lines()
                status.errors = monitor.errors()
                status.is_alive = monitor.isAlive()

                result.monitors_status.append(status)

            return result
        finally:
            self.__lock.release()

    def start(self):
        try:
            for monitor in self.__monitors:
                if monitor.open_metric_log():
                    monitor.start()
                    self.__running_monitors.append(monitor)
        except Exception:
            log.exception('Failed to start the monitors due to an exception')

    def stop(self):
        try:
            for monitor in self.__running_monitors:
                monitor.stop(wait_on_join=False)

            for monitor in self.__running_monitors:
                monitor.stop(join_timeout=1)
                monitor.close_metric_log()
        except Exception:
            log.exception('Failed to stop the monitors due to an exception')

    @staticmethod
    def build_monitor(monitor_config, additional_python_paths):
        # Set up the logs to do the right thing.
        module_name = monitor_config['module']
        monitor_id = monitor_config['id']

        # Augment the PYTHONPATH if requested to locate the module.
        original_path = list(sys.path)

        if additional_python_paths is not None:
            for x in additional_python_paths.split(os.pathsep):
                sys.path.append(x)

        # Load monitor.
        try:
            monitor_class = MonitorsManager.__load_class_from_module(module_name)
        finally:
            # Be sure to reset the PYTHONPATH
            sys.path = original_path

        # Instantiate and initialize it.
        return monitor_class(monitor_config, scalyr_logging.getLogger("%s(%s)" % (module_name, monitor_id)))

    @staticmethod
    def __load_class_from_module(module_name):
        module = __import__(module_name)
        # If this a package name (contains periods) then we have to walk down
        # the subparts to get the actual module we wanted.
        for n in module_name.split(".")[1:]:
            module = getattr(module, n)

        # Now find any class that derives from ScalyrMonitor
        for attr in module.__dict__:
            value = getattr(module, attr)
            if not inspect.isclass(value):
                continue
            if 'ScalyrMonitor' in str(value.__bases__):
                return value

        return None

