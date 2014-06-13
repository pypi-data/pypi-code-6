import os
import sys
import stat
import backstage
import subprocess

class Venue():
    """A backstage Venue is a specific local install of backstage."""
    def __init__(self, venue_root):
        """Initialize a Backstage Venue instance. Required arguments are the name of the venue and the fullpath of the venue (name included)
        """
        if not os.path.exists(venue_root):
            print 'venue does not exist at %s' % (venue_root)
            raise

        self.VENUE_ROOT = os.path.abspath(venue_root)
        self.VENUE_PATH,self.VENUE_DIRNAME = os.path.split(self.VENUE_ROOT)
        self.VENUE_NAME = self.VENUE_DIRNAME

        #ensure that the venue path is on sys.path
        self.VENUE_PATH in sys.path or sys.path.insert(0,self.VENUE_PATH)
        self.get_settings()

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

    def getallsites(self):
        """ create a dictionary of all sites, from the database """
        self.sites = {}
        self.connect()
        cur = self.conn.cursor()
        q = 'select name,id,domain,alldomains,site_db,gunicorn_port from django_site where id <> 1'
        cur.execute(q)
        results = cur.fetchall()
        for r in results:
            self.sites[r[0]] = {
                'id': r[1],
                'domain': str(r[2]),
                'alldomains': str(r[3]),
                'site_db': str(r[4]),
                'gunicorn_port': r[5]
            }

    def buildallsites(self):
        """ for each site, create and populate (if necessary) """
        try:
            self.sites
        except:
            self.getallsites()
        skel = os.path.join(self.settings.VENUE_ROOT, 'skel/site')
        for s in self.sites:
            site = backstage.Site(s)
            print 'Site:  %s' % (site.sitename)
            site.populate(replace=False)

    def copyskelfile(self, f=None, replace=False):
        """ replace a skel file into all sites """
        if f is None:
            print 'File Name Required.'
            return False
        infile = os.path.join(self.settings.VENUE_ROOT, 'skel/site', f)
        infile += '.src'
        if not os.path.exists(infile):
            print 'source file %s not found' % (infile)
            return False
        try:
            self.sites
        except:
            self.getallsites()
        for s in self.sites:
            site = backstage.Site(s)
            site.copyskelfile(f, replace)

    def dumpsettings(self):
        try:
            outfile = os.path.join(self.VENUE_ROOT,'settings_dump.py')
            of = open(outfile, 'w')
            my_settings = dir(self.settings)
            for my_setting in my_settings:
                s = "%s = my_settings['%s']\n" % (my_setting, my_setting)
                of.write(s)
            of.close()
        except:
            err = 'ERROR dumping settings'
            raise
        return True

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

    def __unicode__(self):
        s = 'Backstage Venue instance %s at %s' % (self.VENUE_NAME, self.VENUE_ROOT)
        return s

def copy_venue_skel(venue_path):
    """Populate a (usually) new backstage venue with the contents of backstage/skel"""
    skeldir = os.path.join(os.path.dirname(backstage.__file__),'skel/venue')
    if not os.path.exists(skeldir):
        s = 'Source skeleton files for backstage venue not found.  This is a system error'
        print s
        raise
    try:
        #Copy the contents of the 'skel' folder into the venue root
        os.system("cp -rpv %s/* %s" % (skeldir, venue_path))

    except:
        s = "ERROR copying the venue skel into %s" % venue_path
        print s
        raise
    return True

def new_venue(venue_name, venue_path, source_ini_file = None):
        """create a new backstage venue with the given name and located at the specified path"""
        venue_path = os.path.abspath(os.path.join(venue_path, venue_name))
        try:
            os.makedirs(venue_path)
        except:
            print 'Error creating venue.'
            raise

        try:
            with open(os.path.join(venue_path, '__init__.py'), 'w'):
                pass
        except:
            err = 'ERROR with init file'
            print err
            raise
        try:
            if source_ini_file is not None:
                pass  #try to copy the file
            fh=open(os.path.join(venue_path, 'backstage.ini'), 'w')
            fh.write('[backstage]\n')
            fh.close()
        except:
            print 'Error with INI file'
            raise

        try:
            copy_venue_skel(venue_path)
        except:
            s = 'Error in copy_venue_skel'
            print s
            raise



        try:
            p = use_venue(venue_path)
        except:
            raise

        p.build_virtualenv()
        s = 'Successfully created Backstage venue %s at %s' % (p.VENUE_NAME, p.VENUE_ROOT)
        print s
        return p

def test_venue_exists(venue_root):
    """Test for the existence of a Backstage venue instance.  Return True or False"""
    if not os.path.exists(venue_root):
        s = 'venue folder at %s does not exist. Terminating' % venue_root
        print s
        return False
    #A file named backstage.ini should exist.  Proves this is a backstage venue.  Right now it is empty
    ini_file = os.path.join(venue_root, 'backstage.ini')
    if not os.path.exists(ini_file):
        s = 'Backstage INI file not found'
        print s
        return False
    return True

def use_venue(venue_root):
    """Use an existing Backstage venue.  Returns the venue instance."""
    exists = test_venue_exists(venue_root)
    if not exists:
        s = 'venue does not exist'
        print s
        raise

    try:
        backstage_venue = Venue(venue_root)
    except:
        raise
    paths = [backstage_venue.VENUE_ROOT, backstage_venue.VENUE_PATH, ]
    for pth in paths:
        if not pth in sys.path:
            sys.path.append(pth)
    try:
        backstage_venue.get_settings()
    except:
        s = 'Could not import settings'
        print s
        raise
    # paramfiles are those with parameterized variables needing to be replaced using the params dict.
    backstage_venue.paramfiles = ['site_settings.py', 'theme_settings.py', 'wsgi.py', 'conf/gunicorn_launcher',
                   'conf/nginx.conf', 'templates/index.html',
                   'conf/supervisor.conf', ]
    # this would be better in a db table
    backstage_venue.themes = ['default', 'default24', 'fluid', 'container', 'hero', ]
    try:
        backstage_venue.connect()
    except:
        s = 'Could not connect to database'
        raise
    s = 'Using Backstage venue %s at %s' % (backstage_venue.VENUE_NAME, backstage_venue.VENUE_ROOT)
    print s
    return backstage_venue


