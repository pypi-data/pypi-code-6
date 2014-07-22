import subprocess
import os
import tempfile
import StringIO

r_cmd = ['/usr/bin/R']

def _bool(v):
    return "TRUE" if v else "FALSE"

def update(check_built=True, ask=False, lib_loc=os.environ['R_LIBS_USER']):
    sio = StringIO.StringIO()
    r_script = """update.packages(checkBuilt={check_built}, ask={ask}, lib.loc={lib_loc})\n"""
    sio.write(r_script)

    return subprocess.check_call(r_cmd, stdin=sio)

