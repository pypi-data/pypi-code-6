
import os, sys, getpass, commands, time, math, datetime
from .Droplet import Droplet

class Backup( object ):
  def __init__( self, dict, droplet ):
    self.droplet = droplet
    self.route            = self.droplet.name
    self.ssh_user         = ""
    self.ssh_key          = ""
    self.remote_dir       = ""
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
    completed, result = self.rsync()
    self.log( "DROPLET_RSYNC_SUCCESS: %s" % completed )
    if completed:
      self.log( "DROPLET_RSYNC_DATA:\n%s" % result["result"] )

      if snapshot_hour:
        self.log( "DROPLET_TAKING_SNAPSHOT")
        completed, result = self.droplet.snapshot()
        if completed:
          self.log( "DROPLET_SNAPSHOT: %s" % result["snapshot_name"])
          if self.snapshot_delete == True:
            while len(self.droplet.snapshots) > self.snapshots_keep:
              completed, result = self.droplet.destroy_snapshot( self.droplet.snapshots[0] )
              self.log( "DROPLET_SNAPSHOT_DELETED: id:%s name:%s" % (result["id"], result["name"]) )
    else:
      self.log( "DROPLET_RSYNC_PROBLEM:\n%s" % result )

    backup_time = ( time.time() - self.start )
    backup_time = math.ceil(backup_time*100)/100
    info = "time: %s seconds - api calls: %s" % (backup_time, self.droplet.api.calls)
    self.log( "DROPLET_BACKUP_FINISHED: %s" % info )
    self.log( '=============================================================\n' )
    self.droplet.api.calls = 1



  def rsync( self ):
    completed = False
    result = ""

    options_set = True
    for key in self.__dict__.keys():
      if self.__dict__.get(key) == "":
        options_set = False
        break

    options_set = (self.__bin_checks() and type(self.droplet) == Droplet and options_set)
    if options_set == True:
      self.logfile = "%s/_backup_log.txt" % self.backup_dir

      ssh_cmd = 'ssh -oStrictHostKeyChecking=no -i %s' % self.ssh_key
      e = '-e "%s"' % ( ssh_cmd )
      args = '-avz --update --exclude "cache" --exclude "wpcf7_captcha" --exclude ".DS_Store"'
      rsync = 'rsync %s %s %s@%s:%s/ %s/' % ( args, e, self.ssh_user, self.route, self.remote_dir, self.backup_dir )

      remote_dir_check = '%s %s@%s [ -d %s ] && echo True || echo False' % ( ssh_cmd, self.ssh_user, self.route, self.remote_dir )

      cmd = remote_dir_check
      command, result = commands.getstatusoutput( cmd )
      if "True" in result:
        cmd = rsync
        command, result = commands.getstatusoutput( cmd )
        if command is not 0: completed = False
        else: completed = True
      if completed == False:
        print cmd
        print command
        print result
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



