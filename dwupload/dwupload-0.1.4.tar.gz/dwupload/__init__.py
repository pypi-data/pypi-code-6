#!/usr/bin/env python
from __future__ import print_function
from watchdog.observers import Observer
from webdav import DemandwareConnection
from handlers import DemandwareWebDavHandler
from cli import process_arguments
import os
import sys
import time
import ConfigParser
import getpass


def main():
    args = process_arguments()
    config_path = os.path.expanduser("~/.dwsettings")

    if not os.path.exists(config_path):
        config_path = os.environ.get('DWUPLOAD_CONFIG_PATH')

    if not config_path:
        config_path = args.config_path

    if not config_path:
        print("No config path was found")
        exit(1)

    if not os.path.exists(config_path):
        print("Config path does not exist")
        exit(1)

    config = ConfigParser.SafeConfigParser()
    config.read(config_path)

    if args.watch_path:
        watch_path = args.watch_path
    elif config.has_option(args.section_name, 'watch_path'):
        watch_path = config.get(args.section_name, 'watch_path')
    else:
        watch_path = os.getcwd()

    dw_settings = {
        'hostname': config.get(args.section_name, 'hostname'),
        'code_version': config.get(args.section_name, 'code_version'),
        'username': config.get(args.section_name, 'username'),
    }

    try:
        dw_settings['password'] = config.get(args.section_name, 'password')
    except ConfigParser.NoOptionError:
        dw_settings['password'] = getpass.getpass()

    event_handler = DemandwareWebDavHandler(watch_path, **dw_settings)

    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()

    conn = DemandwareConnection(**dw_settings)

    if conn.test_connection() == 401:
        print("Test connection failed. Check authentication settings.")
        sys.exit(1)
    if conn.test_connection() == 500:
        print("Server Error. May be a problem with your sandbox.")
        sys.exit(1)

    print("ctrl-c to stop the process")

    print("[watching] {0}".format(watch_path))

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    sys.exit(0)


if __name__ == '__main__':
    main()