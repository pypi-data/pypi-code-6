
class Permission:

# The READ permission: when it applies to buckets it means
# allow the grantee to list the objects in the bucket; when
# it applies to objects it means allow the grantee to read
# the object data and metadata.
  READ  = 0x01

# The WRITE permission: when it applies to buckets it means
# allow the grantee to create, overwrite and delete any
# object in the bucket; it is not applicable for objects.
  WRITE = 0x02

# The FULL_CONTROL permission: allows the grantee the READ
# and WRITE permission on the bucket/object.
  FULL_CONTROL = 0xff

  @staticmethod
  def toString(permission):
    if permission is Permission.READ:
      return 'READ'
    elif permission is Permission.WRITE:
      return 'WRITE'
    elif permission is Permission.FULL_CONTROL:
      return 'FULL_CONTROL'
    else:
      return ''

  @staticmethod
  def getValue(permission):
    if permission == 'READ':
      return Permission.READ
    elif permission == 'WRITE':
      return Permission.WRITE
    elif permission == 'FULL_CONTROL':
      return Permission.FULL_CONTROL
    else:
      return 0

class UserGroups:
  ALL_USERS = 'ALL_USERS'
  AUTHENTICATED_USERS = 'AUTHENTICATED_USERS'

class GrantType:
  USER = 'USER'
  GROUP = 'GROUP'

class Grantee(dict):
  def __init__(self, id):
    self.id = id
  @property
  def displayName(self):
    return self['displayName']
  @displayName.setter
  def displayName(self, displayName):
    self['displayName'] = displayName
  @property
  def id(self):
    return self['id']
  @id.setter
  def id(self, id):
    self['id']=id

class Owner:
  def setOwnerFromJason(self, response_content):
    if response_content != '':
      owner = {}
      if 'id' in response_content.keys():
        # print respons_content['owner']
        owner['id'] = response_content['id']
      if 'displayName' in response_content.keys():
        # print 'accessControlList%s' % respons_content['accessControlList']
        owner['displayName'] = response_content['displayName']
      return owner
    return None





class Grant(dict):
  def __init__(self, grantee, permission):
    self.grantee = grantee
    self.type = GrantType.USER
    self.permission = permission
  @property
  def permission(self):
    return self['permission']
  @permission.setter
  def permission(self, permission):
    if type(permission) is not str:
      self['permission'] = Permission.toString(permission)
      self.int_perm = permission
    else:
      self.int_perm = permission
      self['permission'] = Permission.getValue(permission)
  @property
  def grantee(self):
    return self['grantee']
  @grantee.setter
  def grantee(self, grantee):
    self['grantee'] = grantee
  @property
  def type(self):
    return self['type']
  @type.setter
  def type(self, type):
    self['type'] = type

class AccessControlList():
  def __init__(self):
    self.acl = {}
  def addGrant(self, grant):
    self.acl['%s:%s' % (grant.grantee.id, grant.type)] = grant
    # self.acl = grant
  def getGrantList(self):
    grants = []
    for k in self.acl:
      grants.append(self.acl[k])
    return grants





