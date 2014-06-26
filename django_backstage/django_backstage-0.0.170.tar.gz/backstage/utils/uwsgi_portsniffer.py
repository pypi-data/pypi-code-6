import os
"""uwsgi_portsniffer.py
Use a uwsgi log file to find the bound uwsgi port
Mostly useful for non-root users, as root can query the socket
much easier.
"""

def port_from_lsof(inifile):
    try:
        with open(inifile,'r') as f:
            inidata = f.readlines()
        for l in inidata:
            l = l.strip()
            if l[0:7] == 'pidfile':
                pidfile = l.split('=')[1].strip()
                break
    except IOError:
        err = 'No Such File: %s' % inifile
        print err
        return None
    try:
        with open(pidfile,'r') as f:
            pid = f.readline().strip()
    except IOError:
        err = 'Error getting PID from %s' % (pidfile)
        print err
        return None
    try:
        p1 = Popen(['lsof', '-a', '-p%s' % (pid), '-i4'], stdout=PIPE)
        p2 = Popen(["grep", "LISTEN"], stdin=p1.stdout, stdout=PIPE)
        output = p2.communicate()[0]
        port = output.split()[8]
        print 'OK: %s' % (port)
        return port
    except:
        raise
        return None


def portsniffer(log_file):
    if not os.path.exists(log_file):
        print 'Log file not found: %s' % log_file
        return None
    try:
        fo = open(log_file, 'r')
    except:
        print 'Could not open log file: %s' % log_file
        return None, None

    found_port = None
    found_ip = None
    try:
        for l in fo.readlines():
            if 'bound to TCP address' in l:
                before0, after0 = l.split('address')

                before1, after1 = after0.split('(port')
                before1 = before1.strip()
                ip, port = before1.split(':')
                found_ip = ip
                found_port = port
        fo.close()
    except Exception, e:
        print 'Error scanning log file: %s' % log_file
        print e
        return None, None
    return found_ip, found_port
