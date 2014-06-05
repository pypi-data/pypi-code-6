__import__("pkg_resources").declare_namespace(__name__)

import os
import sys
import time
import signal
import psutil
import logging

logger = logging.getLogger(__name__)
EXTENSION = '.exe' if os.name == 'nt' else ''


def is_in_bindir(pathname, getcwd, bin_abspath):
    if os.path.isabs(pathname) and os.path.dirname(pathname) == bin_abspath:
        return True
    if not os.path.isabs(pathname) and os.path.join(getcwd, os.path.dirname(pathname)) == bin_abspath:
        return True


def log_process(process):
    logger.debug("found {!r}".format(process))
    logger.debug("exe {!r}".format(process.exe()))
    logger.debug("cmdline {!r}".format(process.cmdline()))
    logger.debug("getcwd() {!r}".format(process.getcwd()))


def need_to_kill_process(bin_abspath, ignore_list, process):
    log_process(process)
    if process.pid == os.getpid():
        logger.debug("this is me")
        return False
    if os.name == "nt" and process.exe().endswith("buildout.exe"):
        logger.debug("assuming is my child buildout, there's no getppid() on Windows")
        return False
    else:
        for pathname in [[process.exe()], process.cmdline()[:1], process.cmdline()[1:2]]:
            if pathname and os.path.basename(pathname[0]).replace(EXTENSION, '') in ignore_list:
                logger.debug("ignoring this one")
                return False
            if pathname and is_in_bindir(pathname[0], process.getcwd(), bin_abspath):
                return True
    return False


def get_processes(bin_dirpath, ignore_list):
    processes = []
    bin_abspath = os.path.abspath(bin_dirpath)
    logger.debug("looking for processes in {!r}".format(bin_abspath))
    for process in psutil.process_iter():
        try:
            if need_to_kill_process(bin_abspath, ignore_list, process):
                processes.append(process)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            logger.debug("skipping {!r}".format(process))
    return processes


def kill_process(process):
    try:
        logger.info("killing {!r}".format(process))
        process.kill()
    except psutil.NoSuchProcess:
        logger.info("process already dead")
    except:
        logger.exception("kill process failed")


def close_application(bin_dirpath, ignore_list=()):
    logger.debug("sys.executable: {!r}".format(sys.executable))
    logger.debug("sys.argv: {!r}".format(sys.argv))
    for process in get_processes(bin_dirpath, ignore_list):
        kill_process(process)
    time.sleep(1)


class CloseApplication(object):
    def __init__(self, buildout, name, options):
        super(CloseApplication, self).__init__()
        self.buildout = buildout
        self.name = name
        self.options = options

    def close_application(self):
        bin_dirpath = os.path.join(self.buildout.get("buildout").get("directory"), "bin")
        ignore_list = self.options.get("ignore-list", '').split()
        close_application(bin_dirpath, ignore_list)
        return []

    def update(self):
        return self.close_application()

    def install(self):
        return self.close_application()

