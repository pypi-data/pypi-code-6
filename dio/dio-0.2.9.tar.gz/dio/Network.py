
class Network( object ):
  def __init__( self, dict={}, ipv=None):
    for attr in dict.keys(): setattr( self, attr, dict[attr] )
    self.ipv = ipv



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      if key != "token":
        details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details


    