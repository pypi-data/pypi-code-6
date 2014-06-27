import os
from django.db import models

class Venue(models.Model):
    """A backstage Venue is a specific local install of backstage."""
    venue_name = models.TextField(max_length=80, primary_key=True)
    venue_path = models.TextField(max_length=255)
    def __init__(self):
        self.venue_root = os.path.abspath(os.path.join(self.venue_path, self.venue_name))
        self.UWSGI_INI = os.path.join(self.VENUE_ROOT, 'backstage-%s-uwsgi.ini' % (self.VENUE_NAME))

    def __init__(self, venue_root):
        """Initialize a Backstage Venue instance. Required arguments are the name of the venue and the fullpath of the venue (name included)
        """
        if not os.path.exists(venue_root):
            print 'venue does not exist at %s' % (venue_root)
            raise

    def get_settings(self):
        """ import the venue's settings.py"""
        try:
            exec_string = 'from %s import settings' % self.VENUE_NAME
            exec(exec_string)
            self.settings = settings
            return True
        except:
            raise

    def connect(self):
        """ connect to the venue database """
        import psycopg2
        try:
            db = self.settings.DATABASES['default']
            string = "dbname=%s host=%s port=%s user=%s " % \
                     (db['NAME'],
                      db['HOST'],
                      db['PORT'],
                      db['USER']
                     )
            self.conn = psycopg2.connect(string)
            return True
        except:
            return False

    def build_virtualenv(self):
        """build the virtual environment for this backstage venue"""
        cwd = os.getcwd()
        venvdir = os.path.join(self.VENUE_ROOT,'venv')
        cmd = '%s/build_virtualenv' % (venvdir)
        st = os.stat(cmd)
        os.chmod(cmd, st.st_mode | stat.S_IEXEC)
        os.chdir(venvdir)
        subprocess.call(cmd)
        os.chdir(cwd)
        return

    def get_uwsgi_port(self):
        self.uwsgi_ip, self.uwsgi_port = uwsgi_portsniffer.get_uwsgi_port(self.UWSGI_INI)
        return

    def reload(self):
        """Reload the Venue, by touching its ini file"""
        try:
            with file(self.UWSGI_INI, 'a'):
                os.utime(self.UWSGI_INI, None)
        except IOError:
            print 'Could not update, permission denied.'
            return
        self.get_uwsgi_port()
        return

    def __unicode__(self):
        s = 'Backstage Venue instance %s at %s' % (self.VENUE_NAME, self.VENUE_ROOT)
        return s




class Act(models.Model):
    act_name = models.TextField(max_length=80)
    venue = models.ForeignKey(Venue)