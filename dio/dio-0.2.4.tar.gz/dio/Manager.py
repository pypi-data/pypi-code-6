
import sys
from .Api import Api
from .Droplet import Droplet
from .Image import Image
from .Domain import Domain
from .Region import Region
from .Size import Size
from .SSHKey import SSHKey
from .Backup import Backup


class Manager( object ):
  def __init__( self, token="", ignore_list=[] ):
    """
      Pass in an array of droplets you would like to ignore.
      This is great when working on a dev droplet and want
      ignore prodection droplets.
    """
    self.api = Api( token )
    self.droplets = []
    self.domains = []
    self.regions = []
    self.sizes = []
    self.images = []
    self.ssh_keys = []
    self.ignore_list = ignore_list

  

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

  

  def __exists( self, droplet_name ):
    """
      Function to check if droplet is already in self.droplets.
    """
    match = False
    if len(self.droplets):
      for d in self.droplets:
        if droplet_name == d.name:
          match = True
          break
    return match



  def get_all_regions( self ):
    data = self.api.call("/regions")
    for dict in data["regions"]:
      region = Region( dict )
      self.regions.append( region )
    return self.regions

 

  def get_all_sizes( self ):
    data = self.api.call("/sizes")
    for dict in data["sizes"]:
      size = Size( dict )
      self.sizes.append( size )
    return self.sizes



  def get_all_droplets( self ):
    """
      Function to return a list of all droplets as well as
      assign them to self.droplets.
    """
    data = self.api.call("/droplets")
    for dict in data["droplets"]:
      if self.__exists( dict["name"] ) == False:
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
    data = self.api.call("/images")
    for dict in data["images"]:
      image = Image( self.api.token, "", dict, self.api )
      if image not in self.images:
        self.images.append( image )
    return self.images



  def get_all_domains( self ):
    data = self.api.call("/domains")
    for dict in data["domains"]:
      domain = domain( self.api.token, "", dict, self.api )
      if domain not in self.domains:
        self.domains.append( domain )
    return self.domains



  def get_all_sshkeys( self ):
    data = self.api.call("/account/keys/")
    for dict in data["ssh_keys"]:
      sshkey = SSHKey( dict )
      if sshkey not in self.ssh_keys:
        self.ssh_keys.append( sshkey )
    return self.ssh_keys



  def create_droplet( self, name, region, size, image,
    backups=False, ipv6=False, private_networking=False ):
    keys = []
    self.get_all_sshkeys()
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



  def delete_droplet( self, droplet ):
    data = droplet.delete()
    self.get_all_droplets()
    return True, data



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      if key != "token":
        details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details


