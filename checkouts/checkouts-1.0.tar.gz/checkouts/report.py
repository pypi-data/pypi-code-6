import os
import sys
import subprocess
import threading

base_mods = set([k.split('.')[0] for k in sys.modules.keys()])

def shell_out(cmd):
    pipe = subprocess.PIPE
    proc = subprocess.Popen(
            cmd.split(), cwd=moddir, stdout=pipe, stderr=pipe)
    return proc.stdout.read().strip()

os_mod_dir = os.path.dirname(os.__file__)
for mod_name in base_mods:
    mod = sys.modules[mod_name]
    if hasattr(mod, '__file__'):
        moddir = os.path.dirname(mod.__file__)
        if not moddir.startswith(os_mod_dir):
            revision = shell_out('git rev-parse HEAD')
            if revision:
                branch = shell_out('git rev-parse --abbrev-ref HEAD')
                msg = "%s (%s) %s"
                msg %= os.path.abspath(moddir), branch, revision
                print msg

def autodestruct():
    nm = 'checkouts.report'
    if nm in sys.modules:
        del sys.modules[nm]

t = threading.Timer(1.0, autodestruct, args=[], kwargs={})
t.start()
