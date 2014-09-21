import sys
import os
import subprocess

from .process import ManagedProcess

def start_redis(pidfilename, port, data_dir, loglevel="warning",
                data_file='redis.db', save=True,
                stdout=sys.stdout, stderr=sys.stderr):
    base_config = os.path.join(os.path.dirname(__file__), 'redis.conf')
    with open(base_config) as f:
        redisconf = f.read()
    savestr = ''
    if save: savestr = 'save 10 1'
    redisconf = redisconf % {'port' : port,
                             'dbdir' : data_dir,
                             'dbfile' : data_file,
                             'loglevel' : loglevel,
                             'save' : savestr}
    mproc = ManagedProcess(['redis-server', '-'], 'redis', pidfilename,
                           stdout=stdout,
                           stderr=stderr,
                           stdin=subprocess.PIPE
                           )
    mproc.proc.stdin.write(redisconf.encode())
    mproc.proc.stdin.close()
    return mproc
