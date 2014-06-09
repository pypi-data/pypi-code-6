
import sys, os, time
import os.path
import subprocess, shlex

class ServiceSetting():
    def __init__(self,
                config=None,name='django',
                exe="/usr/local/bin/gunicorn"):
        self.name=name
        self.gunicorn_exe=exe

    @property
    def pidfile_num(self):
        if os.path.exists( self.pidfile ):
            return open( self.pidfile).read().strip()
        else:
            return ""

    @property
    def pidfile(self):
        return "/var/gunicorn/%s.pid" % self.name



def start_gunicorn(p):
    pidfile = p.pidfile
    pidpath = os.path.dirname( pidfile )
    if not os.path.exists( pidpath ):
        os.makedirs( pidpath )

    if os.path.exists( pidfile ):
        pid = p.pidfile_num
        print( "last run still running(%s) please try 'stop' first"%pid )
        return

    command="{exe} --config {config} wsgi".format(
        **dict( config=p.config, pid=pidfile, exe=p.gunicorn_exe
          ) )
    #print( command )
    os.system(  command )
    wait_count = 5
    wait_interval = 1
    for i in xrange( wait_count ):
        pid = p.pidfile_num
        if pid:
            print( "Start success(%s)"%p.pidfile_num )
            break
        time.sleep( wait_interval )
    if not p.pidfile_num:
        print( "Start fail" )

    #args = shlex.split( command )
    #subprocess.call( args )
    #os.spawnl( os.P_NOWAIT, command )

def stop_gunicorn( p ):
    pidfile = p.pidfile
    if not os.path.exists( pidfile ):
        print( "%s on gunicorn not running" % p.name )
        return
    pid = p.pidfile_num
    stop_try_count = 5
    stop_try_wait = 5
    for i in xrange( stop_try_count ):
        if os.path.exists( "/proc/%s" % pid ):
            try:
                os.kill( int(pid), 15 )
            except Exception as e:
                print( "try terminate %s error: %s"%( pid, str(e ) ) )
        else:
            print( "%s on gunicorn is stoped"% p.name )
            try:
                os.remove( pidfile )
            except Exception as e:
                print( str( e ) )
            break

        time.sleep( 5 )
    if os.path.exists( "/proc/%s" % pid ):
        print( "Error: couldn't stop '%s'" )

def stat_gunicorn( p ):
    pidfile = p.pidfile
    if not os.path.exists( pidfile ):
        print( "%s on gunicorn not running" % p.name )
    else:
        pid = p.pidfile_num
        print( "%s on gunicorn running( %s )" %( p.name, pid ) )
        if not os.path.exists( "/proc/%s" % pid ):
            print( " but not found instance" )


def gunicorn_service( p ):
    pass
    if sys.argv[1] == "start":
        start_gunicorn( p )
    elif sys.argv[1] == "stop":
        stop_gunicorn( p )
    elif sys.argv[1] == "restart":
        start_gunicorn( p )
        stop_gunicorn( p )
    elif sys.argv[1] == "stat":
        stat_gunicorn( p )
    else:
       print "use arguemnt start| stop| restart| stat"

