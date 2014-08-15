__author__ = 'colin'
'''
Created on Jul 29, 2014

@author: "Colin Manning"
'''
import sys
import getopt
import logging.handlers
import signal

from pf3.fs.FileSystemMonitor import FileSystemMonitor

#Global definitions

__pf3_version__ = "3.0.1"

fileSystemMonitor = None
webService = None
framework = None

def close_down(signal, frame):
    print('printflow2 is shutting down')
    if fileSystemMonitor is not None:
        fileSystemMonitor.stop()

    sys.exit(0)

def main():
    global __pf3_version__
    global fileSystemMonitor
    global webService
    global framework
    help_text = 'usage:\n pf3 -c <configfile> -w <workgroup> -l <logfile>\n pf3 -v'
    workgroupConfigFile = None
    configFile = None
    workgroupRunFile = None
    logFile = None
    logger = None
    framework = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"vhc:w:r:l:",["version", "configfile=", "workgroup=", "runfile=", "logfile="])

    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ("-v", "--version"):
            print(('PrintFlow 3 File System Monitor Version:',__pf3_version__))
            sys.exit()
        elif opt in ("-c", "--configfile"):
            configFile = arg
        elif opt in ("-w", "--workgroup"):
            workgroupConfigFile = arg
        elif opt in ("-r", "--runfile"):
            workgroupRunFile = arg
        elif opt in ("-l", "--logfile"):
            assert isinstance(arg, object)
            logFile = arg

    if configFile is not None and workgroupConfigFile and workgroupRunFile  is not None:
        # setup logging
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('printflow2')
        handler = logging.handlers.TimedRotatingFileHandler(logFile, when='midnight')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # disable default logging (INFO level) from 'requests' module

        # Ok, let's go
        # First start listeners in particular the FileSystemMonitor
        # Once NooshMonitor start is called, that's it, as it sits in an infinite loop checking Noosh

        print(('Running PrintFlow 3 File System Monitor Version:',__pf3_version__))
        fileSystemMonitor = FileSystemMonitor(workgroupConfigFile, workgroupRunFile)
        if fileSystemMonitor.is_ready():
            fileSystemMonitor.scanFolders()
            fileSystemMonitor.start()

        close_down()
    else:
        print("Invalid call to PrintFlow 3 File System Monitor")
        print(help_text)



signal.signal(signal.SIGINT, close_down)
signal.signal(signal.SIGTERM, close_down)

if __name__ == "__main__":
    main()
