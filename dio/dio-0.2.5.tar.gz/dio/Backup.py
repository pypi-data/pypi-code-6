
import os, sys, getpass, commands, time, datetime
from .Droplet import Droplet

class Backup( object ):
  def __init__( self, dict, droplet ):
    self.droplet = droplet
    self.route            = self.droplet.name
    self.ssh_user         = ""
    self.ssh_key          = ""
    self.remote_dirs      = []
    self.remote_dir       = None
    self.backup_dir       = ""
    self.use_ip           = False
    self.user             = getpass.getuser()
    self.home             = os.path.expanduser("~")
    self.snapshot_hour    = 25
    self.snapshots_keep   = 1000
    self.snapshot_delete  = False

    if self.droplet.name in dict:
      dict = dict[self.droplet.name]
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )

    """ compat for single remote_dir option """
    if self.remote_dir != None:
      self.remote_dirs.append( self.remote_dir )

    if self.use_ip:
      self.route = droplet.ip_address
    if self.droplet.name not in self.backup_dir:
      self.backup_dir = "%s/%s" % ( self.backup_dir, self.droplet.name )

    if not os.path.exists(self.backup_dir):
      os.makedirs(self.backup_dir)
    self.ssh_key = self.__find_ssh_key()

    self.backup()



  def __which(self, program ):
    def is_exe( fpath ):
      return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split( program )
    if fpath:
      if is_exe(program):
        return program
    else:
      for path in os.environ["PATH"].split( os.pathsep ):
        path = path.strip('"')
        exe_file = os.path.join( path, program )
        if is_exe(exe_file):
          return exe_file

    return None



  def __bin_checks( self ):
    """
      Programs needed for the backup operations
    """
    programs = ["ssh", "rsync"]
    for program in programs:
      path = self.__which( program )
      if path == None:
        print "%s is not on this system" % program
        return False
    return True



  def __find_ssh_key( self ):
    this_path = "%s/%s"      % (os.getcwd(), self.ssh_key)
    home_path = "%s/%s"      % (self.home, self.ssh_key)
    ssh_path  = "%s/.ssh/%s" % (self.home, self.ssh_key)
    paths = [ this_path, home_path, ssh_path ]
    for path in paths:
      if os.path.isfile(path):
        return path



  def __run_command( self, cmd ):
    return commands.getstatusoutput( cmd )



  def __options_set( self ):
    options_set = True
    for key in self.__dict__.keys():
      if self.__dict__.get(key) == "":
        options_set = False
        break
    return (self.__bin_checks() and type(self.droplet) == Droplet and options_set)



  def __remote_dir_check( self, ssh_cmd, remote_dir ):
    cmd = '%s %s@%s [ -d %s ] && echo True || echo False' % ( ssh_cmd, self.ssh_user, self.route, remote_dir )
    command, result = self.__run_command( cmd )
    if "True" in result: result == True
    else:
      self.log( "DROPLET_REMOTE_DIR_CHECK_COMMAND: %s" % command )
      self.log( "DROPLET_REMOTE_DIR_CHECK_RESULT: %s " % result )
    return result



  def __rsync( self, ssh_cmd, remote_dir ):
    local_dir = "%s/%s/" % (self.backup_dir, remote_dir)
    if not os.path.exists( local_dir ):
      os.makedirs( local_dir )

    e = '-e "%s"' % ( ssh_cmd )
    args = '-avz --update --exclude "cache" --exclude "wpcf7_captcha" --exclude ".DS_Store"'
    cmd = 'rsync %s %s %s@%s:%s/ %s/%s' % ( args, e, self.ssh_user, self.route, remote_dir, self.backup_dir, remote_dir )
    command, result = self.__run_command( cmd )
    completed = ( command == 0 )
    
    if completed == False:
      self.log( "DROPLET_RSYNC_CMD: %s" % cmd )
      self.log( "DROPLET_RSYNC_COMMAND: %s" % command )
      self.log( "DROPLET_RSYNC_RESULT: %s" % result )

    return completed, result



  def __backup_snapshots( self ):
    snapshots = []
    match = "@%s-" % self.droplet.name
    for snapshot in self.droplet.snapshots:
      if match in snapshot.name:
        snapshots.append(snapshot)
    return snapshots



  def log( self, msg ):
    ts = "[%s]" % self.droplet.api.timestamp()
    msg = '%s %s\n' % ( ts, msg )
    if self.droplet.freshlog == True:
      f = open( self.droplet.log, 'w' )
    else:
      f = open( self.droplet.log, 'a' )
    f.writelines( msg )
    f.close()



  def backup( self ):

    if self.droplet.status == "off":
      """
        Let's boot that droplet if it's off or else the backup will
        be worthless.
      """
      self.droplet.power_on()
    
    self.start = time.time()
    snapshot_hour = ( datetime.datetime.today().hour == self.snapshot_hour )

    self.droplet.log = "%s/%s" % (self.backup_dir, "_backup_log.txt")
    self.droplet.freshlog = snapshot_hour
    self.log( "DROPLET_BACKUP: %s " % self.droplet.name )
    self.droplet.freshlog = False
    self.log( "DROPLET_ROUTE: %s " % self.route )
    completed, result = self.rsync()
    self.log( "DROPLET_RSYNC_SUCCESS: %s" % completed )
    if completed:
      self.log( "DROPLET_RSYNC_DATA:%s" % result["result"] )

      if snapshot_hour:
        self.log( "DROPLET_TAKING_SNAPSHOT")
        completed, result = self.droplet.snapshot()
        if completed:
          self.log( "DROPLET_SNAPSHOT: %s" % result["snapshot_name"])
          if self.snapshot_delete == True:
            snapshots = self.__backup_snapshots()
            count = len(snapshots)
            while count > self.snapshots_keep:
              completed, result = self.droplet.destroy_snapshot( snapshots[0] )
              self.log( "DROPLET_SNAPSHOT_DELETED: id:%s name:%s" % (result["id"], result["name"]) )
              snapshots = self.__backup_snapshots()
              count = len(snapshots)
    else:
      self.log( "DROPLET_RSYNC_PROBLEM:\n%s" % result )

    backup_time = (round(( time.time() - self.start ),2))
    if backup_time > 60:
      backup_time = "time: %s minutes" % (round((backup_time/60),2))
    else:
      backup_time = "time: %s seconds" % backup_time
    info = "%s - api calls: %s" % (backup_time, self.droplet.api.calls)
    self.log( "DROPLET_BACKUP_FINISHED: %s" % info )
    self.log( '=============================================================\n' )
    self.droplet.api.calls = 1



  def rsync( self ):
    completed = False
    result = ""
    if self.__options_set():
      self.logfile = "%s/_backup_log.txt" % self.backup_dir
      ssh_cmd = 'ssh -oStrictHostKeyChecking=no -i %s' % self.ssh_key

      for remote_dir in self.remote_dirs:
        if self.__remote_dir_check( ssh_cmd, remote_dir ):
          completed, dir_result = self.__rsync( ssh_cmd, remote_dir )
          if completed:
            ts = "[%s]" % self.droplet.api.timestamp()
            result = result+"\n%s DROPLET_REMOTE_DIR: %s\n" % (ts, remote_dir)
            result = result+"%s\n" % dir_result
            pass
    else:
      result = "no rsync preformed"
    result = {"id":self.droplet.id,"name":self.droplet.name,"type":"rsync","result":result}
    return completed, result



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      if key != "token":
        details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details



