
class SSHKey( object ):
  def __init__( self, dict={} ):
    for attr in dict.keys(): setattr( self, attr, dict[attr] )



  def details( self ):
    details = ""
    for key in self.__dict__.keys():
      details = details+"%s: %s\n" % ( key, self.__dict__.get(key) )
    details = details+"===============================================================\n"
    return details


    