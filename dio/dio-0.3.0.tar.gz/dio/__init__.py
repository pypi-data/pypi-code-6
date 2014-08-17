import sys, os, json, requests, time, datetime, getpass, commands

"""Python API for DigitalOcean v2.0 REST API"""

__version__       = "0.2.0"
__author__        = "Rob Johnson ( http://corndogcomputers.com )"
__author_email__  = "info@corndogcomputers.com"
__copyright__     = "Copyright (c) 2014 Rob Johnson"
__license__       = "\
The MIT License (MIT)\
Copyright (c) 2014 Rob Johnson\
\
Permission is hereby granted, free of charge, to any person obtaining a copy\
of this software and associated documentation files (the \"Software\"), to deal\
in the Software without restriction, including without limitation the rights\
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\
copies of the Software, and to permit persons to whom the Software is\
furnished to do so, subject to the following conditions:\
\
The above copyright notice and this permission notice shall be included in all\
copies or substantial portions of the Software.\
\
THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\
SOFTWARE.\
"





def get_details( object ):
  details = ""
  for key in object.__dict__.keys():
    if key != "token":
      details = details+"%s: %s\n" % ( key, object.__dict__.get(key) )
  return details





class Action( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Api( object ):
  def __init__( self, token="" ):
    if token == "": sys.exit( "NO TOKEN PROVIDED" )
    self.__raw = None
    self.__base_url = "https://api.digitalocean.com/v2"
    self.token      = token
    self.user_agent = "python-digitalocean"
    self.response   = {}
    self.calls      = 0
    self.remaining  = 1
    self.delay      = 5

  def __headers( self ):
    return {
      "Authorization" : "Bearer %s" % self.token,
      "Content-Type": "application/json",
      "User-Agent": self.user_agent
    }

  def __process_action( self, data, path ):
    action = Action( data )
    completed = False
    path = "%s/%s" % (path, action.id)
    while completed == False:
      self.wait( self.delay )
      data = self.__call( path, "GET", {} )
      if data.get("action"):
        action = Action( data["action"] ) 
        completed = (action.status == "completed")
      else:
        completed = True
    return completed, data["action"]

  def __call( self, path, method, params ):
    if self.remaining >= 1:
      url = "%s%s" % ( self.__base_url, path )
      payload = json.dumps(params)

      if method == "GET":
        self.__raw = requests.get(url, params=None,
          headers=self.__headers(), verify=True )

      elif method == "POST":
        self.__raw = requests.post(url, data=payload,
          headers=self.__headers(), verify=True )

      elif method == "DELETE":
        self.__raw = requests.delete(url, data=payload,
          headers=self.__headers(), verify=True )

      if self.__raw.status_code < 204:
        self.response = self.__raw.json()
      elif self.__raw.status_code == 204:
        self.response = self.completed()
      elif self.__raw.status_code >= 400:
        print "ERROR_DETAILS:"
        print "used api calls: %s" % self.calls
        print "remaining api calls: %s" % self.remaining
        print "resource: %s\n" % url
        print "payload: %s\n" % payload
        print "headers: %s" % self.__raw.headers
        print "content: %s" % self.__raw.content
        sys.exit("\n")

      self.remaining = self.__raw.headers['ratelimit-remaining']
      self.calls = self.calls+1
    else:
      sys.exit("API Rate limit exceeded.")

    return self.response

  def call( self, path="", method="GET", params={} ):
    data = None
    data = self.__call( path, method, params )
    if data != None:
      if data.get("action"):
        return self.__process_action( data["action"], path )
    return data

  def wait( self, delay=5 ):
    time.sleep( delay)

  def completed( self ):
    return json.loads(json.dumps({"status" : "completed"}))

  def timestamp( self ):
    return str( datetime.datetime.fromtimestamp(
      int( time.time() ) ).strftime( '%Y-%m-%d-%H%M' )
    )

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Backup( object ):
  def __init__( self, dict, droplet ):
    self.droplet          = droplet
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
    self.snapshots        = 10000

    """ Check the options dict to see if it's for this droplet """
    if self.droplet.name in dict:
      dict = dict[self.droplet.name]

    """ Set the backup options from the dict """
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
    
    """ We're going to assume root for the ssh_user """
    if self.ssh_user == "": self.ssh_user = "root"

    """ Compatibility for single remote_dir option """
    if self.remote_dir != None:
      self.remote_dirs.append( self.remote_dir )

    """ Connect to the droplet via ip address instead of name """
    if self.use_ip: self.route = droplet.ip_address

    """ Set the default backup_dir to $HOME/Droplets """
    if self.backup_dir == "":
      self.backup_dir = "%s/Droplets" % self.home

    """ Set the default backup_dir to $HOME/Droplets/droplet.name """
    if self.droplet.name not in self.backup_dir:
      self.backup_dir = "%s/%s" % ( self.backup_dir, self.droplet.name )

    """ Create the backup_dir if it doesn't exist """
    if not os.path.exists(self.backup_dir):
      os.makedirs(self.backup_dir)

    """ Find the ssh_key path """
    self.ssh_key = self.__find_ssh_key()

    """ Set snapshot_delete if the user specifies a number of snapshots to keep """
    self.snapshot_delete  = ( self.snapshots >=1 and self.snapshots != 10000 )

    """ Start the droplet backup """
    self.__backup()

  def __log( self, msg ):
    """ Log timestamp  """
    ts = "#####[%s]" % self.droplet.api.timestamp()

    """ Log message  """
    msg = '%s %s\n' % ( ts, msg )

    if self.droplet.freshlog == True:
      log = open( self.droplet.log, 'w' )
      self.droplet.freshlog = False
    else:
      log = open( self.droplet.log, 'a' )

    log.writelines( msg )
    log.close()

  def __which(self, program ):
    """ Find bin program path """
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
    """ Programs needed for the backup operations """
    programs = ["ssh", "rsync"]

    """ Check if the programs are installed """
    for program in programs:
      path = self.__which( program )
      if path == None:
        print "%s is not on this system" % program
        return False
    return True

  def __find_ssh_key( self ):
    """ Places to look for the ssh_key """
    this_path = "%s/%s"      % (os.getcwd(), self.ssh_key)
    home_path = "%s/%s"      % (self.home, self.ssh_key)
    ssh_path  = "%s/.ssh/%s" % (self.home, self.ssh_key)

    """ Try to loacate the ssh_key path """
    paths = [ this_path, home_path, ssh_path ]
    for path in paths:
      if os.path.isfile(path):
        return path

  def __options_set( self ):
    """ Make sure that all required options are set """
    options_set = True
    for key in self.__dict__.keys():
      if self.__dict__.get(key) == "":
        options_set = False
        break
    return (self.__bin_checks() and type(self.droplet) == Droplet and options_set)

  def __run_command( self, cmd ):
    """ Return results of running a command """
    return commands.getstatusoutput( cmd )

  def __remote_dir_check( self, ssh_cmd, remote_dir ):
    result = False
    cmd_result = ""
    """ SSH command to check if remote_dir exists """
    cmd = '%s %s@%s [ -d %s ] && echo True || echo False' % ( ssh_cmd, self.ssh_user, self.route, remote_dir )

    """
      We are going to assume that since the local dir exists of the
      remote_dir, that we don't need remote in and check that it exists
      anymore. We'll only do this once on the first rsync of the
      remote_dir.
    """
    local_dir = "%s%s/" % (self.backup_dir, remote_dir)
    if not os.path.exists( local_dir ):
      command, cmd_result = self.__run_command( cmd )
    else:
      command = 0
      cmd_result = "True"

    if "True" in cmd_result:
      """ Create the local_dir of the backup_dir if it doesn't exits """
      local_dir = "%s%s/" % (self.backup_dir, remote_dir)
      if not os.path.exists( local_dir ):
        os.makedirs( local_dir )
      result = True

    return result

  def __rsync( self, ssh_cmd, remote_dir ):
    completed = False
    result = ""
    if self.__remote_dir_check( ssh_cmd, remote_dir ):
      """ SSH option for rsync to use our ssh_key """
      e = '-e "%s"' % ( ssh_cmd )

      """ The rsync args. some of these may need to be removed. """
      args = '-avz --update --exclude "cache" --exclude "wpcf7_captcha" --exclude ".DS_Store"'

      cmd = 'rsync %s %s %s@%s:%s/ %s%s' % ( args, e, self.ssh_user, self.route, remote_dir, self.backup_dir, remote_dir )
      command, result = self.__run_command( cmd )
      completed = ( command == 0 )
    else:
      completed = True
      result = "**%s not exist on %s**" % (remote_dir, self.droplet.name)

    
    if completed == False:
      self.__log( "DROPLET_RSYNC_CMD: _%s_" % cmd )
      self.__log( "DROPLET_RSYNC_COMMAND: _%s_" % command )
      self.__log( "DROPLET_RSYNC_RESULT: _%s_" % result )

    else:
      """ Format the output for markdown. """
      if "\nsent" in result: result = result.replace( "\nsent", "sent")

      """ Remove trailing whitespace """
      result = result.replace(" \n", "\n")

      """ More markdown """
      str = "receiving file list ... done"
      if str in result:
        result = result.replace(str,("**%s**" % str) )

      """ Even more markdown """
      if "done**\nsent" not in result:
        result = result.replace("\n", "\n* ")
        self.__log( "DROPLET_RSYNC: _%s_\n* %s\n" % (remote_dir, result) )

    return completed, result

  def __get_backup_snapshots( self ):
    """
      We're creating a list of droplet snapshots to check
      that only have or template snapshot name in them.
    """
    snapshots = []
    match = "@%s-" % self.droplet.name
    for snapshot in self.droplet.snapshots:
      if match in snapshot.name:
        snapshots.append(snapshot)
    return snapshots

  def __sync( self ):
    completed = False
    result = ""
    if self.__options_set():
      ssh_cmd = 'ssh -oStrictHostKeyChecking=no -i %s' % self.ssh_key

      for remote_dir in self.remote_dirs:
        completed, dir_result = self.__rsync( ssh_cmd, remote_dir )
        if completed: result = result+dir_result
    else:
      result = "MISSING_REMOTE_DIR: %s" % remote_dir
    result = {"id":self.droplet.id,"name":self.droplet.name,"type":"rsync","result":result}
    return completed, result

  def __backup( self ):
    """ Boot the droplet if it's off """
    if self.droplet.status == "off":
      self.droplet.power_on()

    """ Set a start time  for backup operations. """
    self.start = time.time()

    """ Is it time for a snapshot """
    snapshot_hour = ( datetime.datetime.today().hour == self.snapshot_hour )

    """ Set the log file name. """
    self.droplet.log = "%s/%s" % (self.backup_dir, "_backup_log.md")

    """ Clean the log if it's time to create a new snapshot """
    self.droplet.freshlog = snapshot_hour

    """ First log entry """
    self.__log( "DROPLET_BACKUP: _%s_ " % self.droplet.name )

    """ Log the route we are using to connect to the droplet. (ip/name) """
    self.__log( "DROPLET_ROUTE: _%s_ " % self.route )

    """ Run the rsync function """
    completed, result = self.__sync()

    if completed:
      if snapshot_hour:
        """ Set the name of the backup snapshot to be taken. """
        snapshot_name = "@%s-%s" % ( self.droplet.name, self.droplet.api.timestamp() )

        self.__log( "DROPLET_TAKING_SNAPSHOT: _%s_" % snapshot_name )

        """ Take the backup snapshot. """
        completed, result = self.droplet.snapshot( snapshot_name )

        if completed:
          self.__log( "DROPLET_SNAPSHOT_SUCCESS: _%s_" % completed )

          """ Check if we need to delete old snapshots. """
          if self.snapshot_delete == True:

            """ Get a list of backup snapshots only """
            snapshots = self.__get_backup_snapshots()

            """ Get a count of the backup snapshots """
            count = len(snapshots)

            """
              Keep deleting the oldest snapshot, until we have the
              number of snapshots we want to keep.
            """

            while count > self.snapshots:
              """ Delete the first snapshot in the list """
              completed, result = self.droplet.destroy_snapshot( snapshots[0] )

              self.__log( "DROPLET_SNAPSHOT_DELETED: id: _%s_ name: _%s_" % (result["id"], result["name"]) )

              """ Update our backup snapshots list """
              snapshots = self.__get_backup_snapshots()

              """ Update our count """
              count = len(snapshots)
    else:
      """ At this point we don't know, why the rsync failed, so we'll log it. """
      self.__log( "DROPLET_RSYNC_PROBLEM:\n%s" % result )

    """ How long it's taken to backup in rounded seconds """
    backup_time = int((round(( time.time() - self.start ),0)))

    if backup_time > 60:
      """ Let's log pretty minutes """
      backup_time = "time: %s minutes" % int((round((backup_time/60),0)))

    else:
      """ Let's log pretty seconds """
      backup_time = "time: %s seconds" % backup_time

    """ Let the user know how many api calls were used """
    info = "%s - api calls: %s" % (backup_time, self.droplet.api.calls)

    self.__log( "DROPLET_BACKUP_FINISHED: _%s_" % info )
    self.__log( '**=================================**\n' )

    """ We reset this for the next droplet in a for loop """
    self.droplet.api.calls = 1

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Domain( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Droplet( object ):
  def __init__( self, token="", id="", dict={}, api=None, options={} ):
    self.token = token
    self.id = id
    self.load( token, id, dict, api )
    self.path = "/droplets/%s" % self.id
    self.actions_path = "/droplets/%s/actions" % self.id
    self.kernels_path = "/droplets/%s/kernels" % self.id

  @property
  def snapshots(self):
    if hasattr(self, "_snapshots") == False:
      self._snapshots = self.get_snapshots()
    return self._snapshots
  
  @snapshots.setter
  def snapshots(self, value):
    self._snapshots = value

  @property
  def available_kernels(self):
    if hasattr(self, "_available_kernels") == False:
      self._available_kernels = self.get_available_kernels()
    return self._available_kernels
  
  @available_kernels.setter
  def available_kernels(self, value):
    self._available_kernels = value

  def __status( self, status):
    """
      Private function to check the droplet status against
      the desired status. This means that after performing
      an action on the droplet, it will check to make sure
      the droplet.status is equal to the desired status
      befor continuing.
    """
    self.load()
    completed = (self.status == status)
    while completed == False:
      self.api.wait()
      self.load()
      completed = (self.status == status)
    return completed

  def __networks( self ):
    """
      Function to assign network properties to the droplet.
    """
    networks = []
    for key in self.networks:
      arr = self.networks[key]
      for dict in arr:
        nic = Network( dict, ("%s"%key) )
        networks.append( nic )
    self.networks = networks
    for nic in self.networks:
      if nic.ipv == "v4" and nic.type == "public":
        self.ip_address = nic.ip_address
      if nic.ipv == "v4" and nic.type == "private":
        self.private_ip_address = nic.ip_address
      if nic.ipv == "v6" and nic.type == "public":
        self.ipv6_address = nic.ip_address
      if nic.ipv == "v6" and nic.type == "private":
        self.private_ipv6_address = nic.ip_address

  def load( self, token="", id="", dict={}, api=None ):
    if dict == {} and self.token != "" and id != "":
      self.api = Api( self.token )
      dict = self.api.call( "/droplets/%s" % id )["droplet"]
    elif hasattr(self, "api"):
      dict = self.api.call( "/droplets/%s" % self.id )["droplet"]
    elif api != None:
      self.api = api
    else:
      if token == "":
        sys.exit("NO TOKEN PROVIDED")
      sys.exit("NO DROPLET ID PROVIDED")
    if dict != {}:
      for attr in dict.keys(): setattr( self, attr, dict[attr] )
      
      self.kernel     = Kernel( self.kernel )
      self.region     = Region( self.region )
      self.size       = Size( self.size )
      self.image      = Image( self.image )
      self.__networks()
      """
        For now we are going to load the droplet snapshots on
        on droplet creation. (may change this later)
      """

      """
      if hasattr(self, 'snapshots') == False:
        self.snapshots  = self.get_snapshots()
      """

  def reboot( self ):
    if self.status == "off":
      completed, data = self.power_on()
    else:
      completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name}
      )
      completed = self.__status( "active" )
    return completed, data

  def restart( self ):
    """ just because """
    return self.reboot()

  def power_cycle( self ):
    if self.status == "off":
      completed, data = self.power_on()
    else:
      completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name}
      )
      completed = self.__status( "active" )
    return completed, data
  
  def shutdown( self ):
    expected_status = "off"
    if self.status == expected_status:
      completed = True
      data = self.api.completed()
    else:
      completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name}
      )
      completed = self.__status( expected_status )
    return completed, data

  def power_off( self ):
    expected_status = "off"
    if self.status == expected_status:
      completed = True
      data = self.api.completed()
    else:
      completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name}
      )
      completed = self.__status( expected_status )
    return completed, data

  def power_on( self ):
    expected_status = "active"
    if self.status == expected_status:
      completed = True
      data = self.api.completed()
    else:
      completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name}
      )
      completed = self.__status( expected_status )
    return completed, data
  
  def password_reset( self ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name}
    )
    return completed, data
  
  def resize( self, size ):
    self.shutdown()
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "size":size}
    )
    self.power_on()
    return completed, data
  
  def restore( self, image_id ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "image":image_id}
    )
    self.load()
    return completed, data
  
  def rebuild( self, image_id ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "image":image_id}
    )
    self.load()
    return completed, data
  
  def rename( self, new_name ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "name":new_name}
    )
    self.load()
    return completed, data
  
  def change_kernel( self, new_kernel ):
    self.shutdown()
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "name":new_kernel}
    )
    self.power_on()
    return completed, data
  
  def enable_ipv6( self ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name}
    )
    self.load()
    completed = self.__status( "active" )
    return completed, data
  
  def disable_backups( self ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name}
    )
    self.load()
    return completed, data
  
  def enable_private_networking( self ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name}
    )
    return completed, data
  
  def snapshot( self, snapshot_name="" ):
    """
      Create a default snapshot name using a time stamp
    """
    if snapshot_name == "":
      snapshot_name = "%s-%s" % ( self.name, self.api.timestamp() )
    """
      Function to create a snapshot of the droplet. No need
      to power off the droplet first, the function will do
      it for you.
    """
    self.shutdown()
    """
      Creating snapshots take awhile, and can use a lot of api
      calls while checking action status. So we up the api.delay
      to 30 seconds and set it back to it's original value after
      the action is complete.
    """
    delay = self.api.delay
    self.api.delay = 30
    completed, data = self.api.call(
        self.actions_path, "POST",
        {"type":sys._getframe().f_code.co_name,
        "name":snapshot_name}
      )
    """
      When creating snapshots, we also have to wait for the droplet
      to power up, so let's do a check for that befor returning the data.
    """
    self.api.delay = delay
    completed = self.__status( "active" )
    """
      We have snapshots, so let's retrieve them.
    """
    self.get_snapshots()
    data.update({"snapshot_name":snapshot_name})
    return completed, data

  def destroy_snapshot( self, snapshot ):
    """
      destroying the snapshot this way allows us to update the
      droplet.snapshots
    """
    completed, data = snapshot.destroy()
    data.update({"id":snapshot.id, "name":snapshot.name})
    self.load()
    self.get_snapshots()
    return completed, data

  def get_snapshots( self ):
    self.snapshots = []
    for id in self.snapshot_ids:
      data = self.api.call( "/images/%s" % id)["image"]
      snapshot = Snapshot( self.token, "", data, self.api )
      self.snapshots.append( snapshot )
    return self.snapshots

  def get_available_kernels( self ):
    self.available_kernels = []
    data = self.api.call( self.kernels_path)["kernels"]
    for dict in data:
      kernel = Kernel( dict )
      self.available_kernels.append( kernel )
    return self.available_kernels

  def delete( self, prompt=True ):
    """
      After extensivly testing digitalocean's droplet restore function
      to restore a production droplet that was deleted, I decided to
      require user input to delete a droplet. ;-)
      
      However, if you're are really confident, you can bypass the prompt.
      [ YOU HAVE BEEN WARNED!!! ]
    """
    info = {"id":self.id,"name":self.name}
    delete_droplet = False
    if prompt == True:
      droplet_name = "%s" % raw_input("[WARNING] IF YOU ARE SURE YOU WANT TO DELETE %s TYPE THE DROPLET NAME: " % self.name)
      if droplet_name == self.name:
        delete_droplet = True
    else:
      delete_droplet = True

    if delete_droplet == True:
      data = self.api.call(
        self.path, "DELETE", {}
      )
      self.api.wait( 1 )
      params = {"type":sys._getframe().f_code.co_name}
      data.update(info)
      data.update(params)
      completed = ( data["status"] == "completed" )
    else:
      data = {"status":"user_rejected","type":"delete"}
      data.update(info)
      completed = ( data["status"] == "completed" )
    return completed, data

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Image( object ):
  def __init__( self, token="", id="", dict={}, api=None ):
    """
      Image id can also be an image slug such as "ubuntu-14-04-x64".
    """
    self.token = token
    self.id = id
    self.load( token, id, dict, api )
    self.path = "/images/%s" % self.id
    self.actions_path = "/images/%s/actions" % self.id

  def load( self, token="", id="", dict={}, api=None ):
    if dict == {} and self.token != "" and id != "":
      self.api = Api( self.token )
      dict = self.api.call( "/images/%s" % id )["image"]
    elif hasattr(self, "api"):
      dict = self.api.call( "/images/%s" % self.id )["image"]
    elif api != None:
      self.api = api
    elif dict == {} and id == "" and token == "":
      if token == "":
        sys.exit("NO TOKEN PROVIDED")
      sys.exit("NO IMAGE ID PROVIDED")
    if dict != {}:
      for attr in dict.keys(): setattr( self, attr, dict[attr] )

  def destroy( self ):
    params = {"type":sys._getframe().f_code.co_name}
    data = self.api.call(
      self.path, "DELETE",
      params
    )
    self.api.wait( 1 )
    info = {"id":self.id,"name":self.name}
    data.update(info)
    data.update(params)
    completed = ( data["status"] == "completed" )
    return completed, data

  def transfer( self, new_region ):
    completed, data = self.api.call(
      self.actions_path, "POST",
      {"type":sys._getframe().f_code.co_name,
      "region":new_region}
    )
    return completed, data

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Snapshot( Image ):
  """
    Although a seperate class name is not needed, it just seems
    appropriate to refer to droplet snapshots as "snapshots" and
    not just "images". Maybe I'm wrong.
  """
  def __init__( self, token="", id="", dict={}, api=None ):
    super(Snapshot, self).__init__( token, id, dict, api )

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Kernel( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Manager( object ):
  def __init__( self, token="", ignore_list=[] ):
    """
      Pass in an array of droplets you would like to ignore.
      This is great when working on a dev droplet and want
      ignore prodection droplets.
    """
    self.api = Api( token )
    self.ignore_list = ignore_list

  @property
  def droplets(self):
    if hasattr(self, "_droplets") == False:
      self._droplets = self.get_all_droplets()
    return self._droplets
  
  @droplets.setter
  def droplets(self, value):
    self._droplets = value

  @property
  def domains(self):
    if hasattr(self, "_domains") == False:
      self._domains = self.get_all_domains()
    return self._domains
  
  @domains.setter
  def domains(self, value):
    self._domains = value

  @property
  def regions(self):
    if hasattr(self, "_regions") == False:
      self._regions = self.get_all_regions()
    return self._regions
  
  @regions.setter
  def regions(self, value):
    self._regions = value

  @property
  def sizes(self):
    if hasattr(self, "_sizes") == False:
      self._sizes = self.get_all_sizes()
    return self._sizes
  
  @sizes.setter
  def sizes(self, value):
    self._sizes = value

  @property
  def images(self):
    if hasattr(self, "_images") == False:
      self._images = self.get_all_images()
    return self._images
  
  @images.setter
  def images(self, value):
    self._images = value

  @property
  def ssh_keys(self):
    if hasattr(self, "_ssh_keys") == False:
      self._ssh_keys = self.get_all_ssh_keys()
    return self._ssh_keys
  
  @ssh_keys.setter
  def ssh_keys(self, value):
    self._ssh_keys = value

  def __ignore( self, droplet_name="", droplet_id=""  ):
    """
      Function to check if droplet is to be ignored when
      adding droplets to self.droplets.
    """
    match = False
    if len(self.ignore_list):
      for d in self.ignore_list:
        if droplet_name == d or droplet_id == d:
          match = True
          break
    return match

  def get_all_regions( self ):
    self.regions = []
    data = self.api.call("/regions")["regions"]
    for dict in data:
      self.regions.append( Region(dict) )
    return self.regions

  def get_all_sizes( self ):
    self.sizes = []
    data = self.api.call("/sizes")["sizes"]
    for dict in data:
      self.sizes.append( Size( dict ) )
    return self.sizes

  def get_all_droplets( self ):
    """
      Function to return a list of all droplets as well as
      assign them to self.droplets.
    """
    self.droplets = []
    data = self.api.call("/droplets")["droplets"]
    for dict in data:
      if self.__ignore( dict["name"], dict["id"] ) == False:
        droplet = Droplet( self.api.token, "", dict, self.api )
        self.droplets.append( droplet )
    return self.droplets

  def get_all_images( self ):
    """
      Function to return a list of all images as well as
      assign them to self.images. This will get default
      images too.
    """
    self.images = []
    data = self.api.call("/images")
    pages = data["links"]["pages"]["last"].split("=")[-1]
    key, values = data.popitem()
    for page in range(2, int(pages) + 1):
      path = "/images?page=%s" % page
      new_data = self.api.call( path )
      more_values = new_data.values()[0]
      for value in more_values:
        values.append(value)
      data = {}
      data[key] = values
    
    for dict in data["images"]:
      image = Image( self.api.token, "", dict, self.api )
      if image not in self.images:
        self.images.append( image )

    return self.images

  def get_all_domains( self ):
    self.domains = []
    data = self.api.call("/domains")["domains"]
    for dict in data:
      domain = Domain(dict)
      if domain not in self.domains:
        self.domains.append( Domain(dict) )
    return self.domains

  def get_all_ssh_keys( self ):
    self.ssh_keys = []
    data = self.api.call("/account/keys/")["ssh_keys"]
    for dict in data:
      ssh_key = SSHKey(dict)
      if ssh_key not in self.ssh_keys:
        self.ssh_keys.append( SSHKey(dict) )
    return self.ssh_keys

  def find_images( self, query ):
    results = []
    for image in self.images:
      if all( i.lower() in image.name.lower() for i in query ) or all( i.lower() in image.distribution.lower() for i in query ):
        results.append( image )

    return results

  def create_droplet( self, name, region, size, image,
    backups=False, ipv6=False, private_networking=False ):
    keys = []
    self.get_all_ssh_keys()
    for key in self.ssh_keys:
      if key.id not in keys:
        keys.append( key.id )
    params = {
      "name":name, "region":region, "size":size, "image":image,
      "ssh_keys":keys, "backups":backups, "ipv6":ipv6,
      "private_networking":private_networking
      }
    data = self.api.call("/droplets", "POST", params )["droplet"]
    self.get_all_droplets()
    for droplet in self.droplets:
      if droplet.name == name:
        while droplet.status != "active":
          droplet.load()
          self.api.wait( 10 )
    return True, data

  def delete_droplet( self, droplet, prompt=True ):
    completed, data = droplet.delete( prompt )
    self.get_all_droplets()
    return completed, data

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Network( object ):
  def __init__( self, dict={}, ipv=None):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
    self.ipv = ipv

  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Region( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
  
  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class Size( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
  
  @property
  def details(self):
    self._details = get_details(self)
    return self._details





class SSHKey( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys():
      setattr( self, attr, dict[attr] )
  
  @property
  def details(self):
    self._details = get_details(self)
    return self._details




