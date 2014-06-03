import os
import sys
import requests
import tarfile
import tempfile
import backstage
from backstage.venue import use_venue
from backstage.venue import Venue

class Act():
    def __init__(self, venue, actname):
        self.venue = venue
        self.actname = actname
        self.acthome = os.path.join(self.venue.VENUE_ROOT, 'acts', actname)
        self.uwsgi_ip = None
        self.uwsgi_port = None
        self.uwsgifile = os.path.join(self.acthome, 'uwsgi.ini')
        if not os.path.exists(self.acthome):
            print 'Act %s does not exist in venue %s' % (self.venue.VENUE_NAME, self.actname)
            raise
        self.get_settings()
        self.uwsgi_linker()
        self.uwsgi_log = self.get_uwsgi_log()

    def get_settings(self):
        syspath = sys.path
        sys.path.insert(0,os.path.join(self.venue.VENUE_ROOT,'acts'))
        exec('from %s import settings' % self.actname)
        sys.path = syspath
        self.settings = settings

    def uwsgi_linker(self, linkmode=None):
        """Links the uwsgi.ini file to the uwsgi emperor's vassals directory
        (set in backstage.backstage_settings UWSGI_VASSALS)
        """
        linkmodes = [None, 'link', 'unlink', 'relink']
        vassal_name = 'backstage-%s-acts-%s.ini' % (self.venue.VENUE_NAME, self.actname)
        self.vassal_file = os.path.join(self.settings.UWSGI_VASSALS, vassal_name)
        if linkmode not in linkmodes:
            return 'Usage: uwsgi_linker <%s>' % (linkmodes)
        if linkmode == None:
            pass
        elif linkmode == 'link':
            os.symlink(self.uwsgifile, self.vassal_file)
            self.get_uwsgi_port()
        elif linkmode == 'unlink':
            os.unlink(self.vassal_file)
            self.uwsgi_port = None
        elif linkmode == 'relink':
            os.unlink(self.vassal_file)
            self.uwsgi_port = None
            os.symlink(self.uwsgifile, self.vassal_file)
            self.get_uwsgi_port()

    def get_uwsgi_log(self):
        fo = open(self.uwsgifile, 'r')
        d = fo.readlines()
        fo.close()
        logfile = None
        for line in d:
            line = line.strip()
            if line[0:9] == 'daemonize':
                logfile = line.split('=')[1]
                return logfile
        return logfile

    def get_uwsgi_port(self):
        from backstage.utils import uwsgi_portsniffer
        ip, port = uwsgi_portsniffer.portsniffer(self.uwsgi_log)
        print 'ip:',ip
        if port is None:
            print "No port.  Try self.uwsgi_linker(linkmode='link')"
            return
        uwsgi_uri = 'http://%s:%s' % (ip, port)
        try:
            h = requests.head(uwsgi_uri)
            if h.status_code == 200:
                self.uwsgi_ip = ip
                self.uwsgi_port = port
                print str(ip), str(port)
            else:
                self.uwsgi_ip = None
                self.uwsgi_port = None
        except:
            raise
            self.uwsgi_ip = None
            self.uwsgi_port = None
            print 'None'
        return


def new_act(venue, actname):
    """create a new Act within a backstage Venue"""
    if isinstance(venue, str):
        try:
            venue = use_venue(venue)
        except:
            venue = None
    if not isinstance(venue, Venue):
        print '%s is not a valid backstage venue' % (venue)
        return None
    actsdir = os.path.join(venue.VENUE_ROOT, 'acts')
    acthome = os.path.join(actsdir, actname)
    if os.path.exists(acthome):
        print 'A folder named %s already exists under %s' % (actname, actsdir)
        return None
    os.mkdir(acthome)
    copy_act_skel(venue, actsdir, actname)
    create_act_uwsgi_file(venue, actsdir, actname)

    act = Act(venue, actname)
    if act:
        s = 'created Backstage Act %s at %s' % (actname, acthome)
        print s
        s = 'using Act %s' % (act)
        print s
    return act

def create_act_uwsgi_file(venue, actsdir, actname):
    """create the uwsgi ini file for a (usually) new Act. This reads in backstage/conf/uwsgi.ini.src
    and substitutes values appropriately."""
    srcfile = os.path.join(os.path.dirname(backstage.__file__),'conf/uwsgi.ini.src')
    with open(srcfile,'r') as f:
        srcdata = f.read()
    outfile = os.path.join(actsdir, actname, 'uwsgi.ini')
    o = open(outfile,'w')
    o.write(srcdata.format(VENUE_ROOT=venue.VENUE_ROOT, VENUE_NAME=venue.VENUE_NAME, ACT_NAME=actname))
    o.close()
    return

def copy_act_skel(venue, actsdir, actname):
    """copy the skeleton files into the Act instance folder"""
    backstage_home = os.path.dirname(os.path.abspath(backstage.__file__))
    act_home = os.path.join(actsdir, actname)
    act_skel = os.path.join(backstage_home,'skel/act')
    #recursive copy via tar
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.close()
    tar_file = tarfile.open(tmpfile.name,'w')
    cwd = os.getcwd()
    os.chdir(act_skel)
    tar_file.add('.')
    os.chdir(cwd)
    tar_file.close()
    tar_file = tarfile.open(tmpfile.name,'r')
    tar_file.extractall(act_home)
    tar_file.close()
    os.remove(tmpfile.name)
