import subprocess
import commands
import signal
import os
import logging

_logger = logging.getLogger(__name__)

TARGET_DIR = 'test/target'
PORT = os.environ.get('MONGO_PORT') or "1234"

def startup(mongo_path=""):
    _logger.info("about to start mongod")
    path = mongo_path or commands.getoutput('which mongod')
    p = subprocess.Popen([path,
        '--port', PORT,
        '--fork',
        '--dbpath', '{0}/db'.format(TARGET_DIR),
        '--logpath', '{0}/mongo.log'.format(TARGET_DIR),
        '--smallfiles',
        '--noprealloc'])
    p.wait()
    _logger.info("mongod started successfully")


def teardown():
    _logger.info("about to stop mongod")
    with open('{0}/db/mongod.lock'.format(TARGET_DIR), 'r') as log_file:
        first_line = log_file.readline()
        pid = int(first_line)
        os.kill(pid, signal.SIGTERM)
        _logger.info("mongodb stopped")
