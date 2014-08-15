
"""
  Not listed in /images response?
  Ubuntu 14.04 x64    id 5141286
  Ubuntu 14.04 x32    id 5142677
  Ubuntu 12.04.5 x64  id 5588928
  Ubuntu 12.04.5 x32  id 5588929
  Ubuntu 10.04 x64    id 5566812
  Ubuntu 10.04 x32    id 5566684
"""

import sys
from .Api import Api
from .Region import Region

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



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details



class Snapshot( Image ):
  """
    Although a seperate class name is not needed, it just seems
    appropriate to refer to droplet snapshots as "snapshots" and
    not just "images". Maybe I'm wrong.
  """
  def __init__( self, token="", id="", dict={}, api=None ):
    super(Snapshot, self).__init__( token, id, dict, api )



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details


    
