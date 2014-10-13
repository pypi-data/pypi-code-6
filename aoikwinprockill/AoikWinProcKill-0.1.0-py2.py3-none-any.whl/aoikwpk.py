# coding: utf-8
"""
File ID: 6xf2hFX
"""
from datetime import datetime
import os
import re
import subprocess
import sys
import traceback
    
#/ 6kdcw4S
try:
    from argparse import ArgumentParser
except Exception:
    #/ 5oG802k
    sys.stderr.write(r"""Error:
Importing |argparse| failed.
Make sure your Python 2 version is >=2.7 or Python 3 version is >=3.2
""")
    
    #/ 4nsknxF
    sys.exit(1)

#/ 9aYkG5z
try:
    import win32com.client #@UnresolvedImport
except ImportError:
    #/ 4pMrNGd
    sys.stderr.write(r"""Error:
Importing |win32com| failed.
Please install |pywin32|.
Download is available at http://sourceforge.net/projects/pywin32/files/pywin32/
""")
    
    #/ 3bhQVAS
    sys.exit(1)

#/ 2oJyTo1
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8') #@UndefinedVariable

#/
def stdout_write_bytes(bytes):
    if sys.version_info[0] > 2:
        sys.stdout.buffer.write(bytes)
    else:
        sys.stdout.write(bytes)

#/
def get_traceback_txt():
    #/
    exc_cls, exc_obj, tb_obj = sys.exc_info()
    
    #/
    txt_s = traceback.format_exception(exc_cls, exc_obj, tb_obj)

    #/
    res = ''.join(txt_s)

    return res

def proc_find(matcher, time_diff_min):
    #/
    my_pid = os.getpid()

    #/
    wmi = win32com.client.GetObject('winmgmts:')

    processe_info_s = wmi.InstancesOf('Win32_Process')

    #/
    start_time = datetime.now()
    
    kill_pi_s = []
    ## pi means proc info
    
    for pi in processe_info_s:
        if pi.Commandline and matcher(pi.Commandline):
            #/
            if pi.ProcessId == my_pid:
               continue
            
            #/
            try:
                proc_time_txt = pi.CreationDate[:14]
                
                proc_time_obj = datetime.strptime(proc_time_txt, '%Y%m%d%H%M%S')
            except Exception:
                kill_pi_s.append(pi)
                continue
            
            #/
            time_diff = (start_time - proc_time_obj).total_seconds()
            
            #/
            if time_diff < time_diff_min:
                continue
            
            #/
            kill_pi_s.append(pi)
    
    #/
    return kill_pi_s

def kill_proc(pattern, time_diff_min, force=False, print_only=False):
    #/ 2u0pfDD
    pattern_rec = re.compile(pattern, re.IGNORECASE)
    
    #/ 4n9qMYq
    def matcher(txt, pattern_rec=pattern_rec):
        return bool(pattern_rec.search(txt))
    
    #/ 6rqB506
    kill_pi_s = proc_find(matcher=matcher, time_diff_min=time_diff_min)
    
    #/ 3rPT9g5
    if not kill_pi_s:
        #/ 8fUAFmc
        return
    
    #/ 2ecTNlu
    print('#/ Found processes')
    
    proc_txt_s = []
    
    for kill_pi in kill_pi_s:
        proc_txt_s.append('%s: %s' % (kill_pi.ProcessId, kill_pi.Commandline))
    
    print('\n'.join(proc_txt_s))
        
    #/ 6m1ybe0
    if print_only:
        #/ 7deb7Dd
        return
    
    #/ 2ipQ8iE
    cmd_part_s = [
        'taskkill',
    ]
    
    #/
    if force:
        cmd_part_s.append('/F')
    
    #/
    for kill_pi in kill_pi_s:
        cmd_part_s.append('/PID')
        cmd_part_s.append(str(kill_pi.ProcessId))
    
    #/ 9ojOdU9
    print('\n#/ Run taskkill\n%s' % (' '.join(cmd_part_s),))
    
    proc_obj = subprocess.Popen(cmd_part_s, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #/ 8fldLwL
    print('\n#/ Output')
    
    result = proc_obj.communicate()
    
    stdout_bytes = result[0]
    stderr_bytes = result[1]
    
    if stdout_bytes:
        stdout_write_bytes(stdout_bytes)
        
    if stderr_bytes:
        stdout_write_bytes(stderr_bytes)
        
    #/ 5eHgDgY
    return

def main():
    #/ 5prcNBx
    parser = ArgumentParser(prog='aoikwpk')
    
    parser.add_argument('proc_cmd_regex', metavar='PROC_CMD_REGEX')
    
    parser.add_argument('-f', dest='force', action='store_true', help='kill processes forcibly by adding /F option to taskkill')
    
    parser.add_argument('-i', dest='print_only', action='store_true', help='show info about matched processes but not kill')
    
    parser.add_argument('-t', dest='time_diff_min', type=float, default=3, metavar='N', help='ignore processes that have been created for less than N seconds (3 by default).')
    
    #/ 4naFQG2
    args_obj = parser.parse_args()
    #/ 5irA2NE
    ## Exit here if arguments are incorrect

    #/
    proc_cmd_regex = args_obj.proc_cmd_regex
    
    force = args_obj.force
    
    print_only = args_obj.print_only
    
    time_diff_min = args_obj.time_diff_min
    
    try:
        kill_proc(
            pattern=proc_cmd_regex,
            force=force,
            print_only=print_only,
            time_diff_min=time_diff_min,
        )
    except Exception:
        print('Error:')
        print('---\n{}---'.format(get_traceback_txt()))

if __name__ == '__main__':
    #/ 3o4XKU0
    main()
    