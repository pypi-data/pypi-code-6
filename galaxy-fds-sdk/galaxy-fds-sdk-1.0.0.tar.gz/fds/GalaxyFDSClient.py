import requests
import json

from GalaxyFDSClientException import GalaxyFDSClientException
from fds.auth.Common import Common
from fds.auth.signature.Signer import Signer
from fds.model.AccessControlPolicy import AccessControlPolicy
from fds.model.Permission import AccessControlList, Grant, Grantee, Owner, Permission
from fds.model.SubResource import SubResource


class GalaxyFDSClient:
  HTTP_OK = 200
  HTTP_NOT_FOUND = 404
  APPLICATION_OCTET_STREAM = 'application/octet-stream'

  access_key = ''
  access_secret = ''
  auth = None

  fds_base_uri = Common.DEFAULT_FDS_SERVICE_BASE_URI
  delimiter = "/"

  def __init__(self, access_key, access_secret, uri=None):
    self.access_key = access_key
    self.access_secret = access_secret
    self.auth = Signer(self.access_key, self.access_secret)
    if uri:
      self.fds_base_uri = uri


  def doesBucketExist(self, bucket_name):
    uri = '%s%s' % (self.fds_base_uri, bucket_name)
    response = requests.head(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      return True
    elif response.status_code == self.HTTP_NOT_FOUND:
      return False
    else:
      message = 'Check bucket existence failed,status=%s,reason=%s' % (response.status_code,response.content)
      raise GalaxyFDSClientException(message)

  def listBuckets(self):
    uri = self.fds_base_uri
    response = requests.get(uri, auth=self.auth)
    if response.status_code != self.HTTP_OK:
      message = 'List buckets failed,status=%s,reason=%s' % (response.status_code,response.content)
      raise GalaxyFDSClientException(message)
    elif response.content is not '':
      buckets_list = []
      buckets = json.loads(response.content)['buckets']
      for bucket in buckets:
        buckets_list.append(bucket['name'])
      return buckets_list
    else:
      return []

  def createBucket(self, bucket_name):
    uri = '%s%s' % (self.fds_base_uri, bucket_name)
    response = requests.put(uri, auth=self.auth)
    print response.status_code
    if response.status_code != self.HTTP_OK:
      message = 'Create bucket failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def deleteBucket(self, bucket_name):
    uri = '%s%s' % (self.fds_base_uri, bucket_name)
    response = requests.delete(uri, auth=self.auth)
    if response.status_code != self.HTTP_OK:
      message = 'Delete bucket failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)


  def putObject(self, bucket_name, object_name, content, metadata=None):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.put(uri, data=content, auth=self.auth, headers=metadata)
    if response.status_code != self.HTTP_OK:
      message = 'Put object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def streamPutObject(self, bucket_name, object_name, iterator, metadata=None):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.put(uri, data=iterator, auth=self.auth, headers=metadata)
    if response.status_code != self.HTTP_OK:
      message = 'Put object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)


  def postObject(self, bucket_name, content, metadata=None):
    uri = '%s%s/' % (self.fds_base_uri, bucket_name)
    response = requests.post(uri, data=content, auth=self.auth, headers=metadata)
    if response.status_code != self.HTTP_OK:
      message = 'Post object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def getObject(self, bucket_name, object_name):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.get(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      return response.content
    else:
      message = 'Get object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)


  def streamGetObject(self, bucket_name, object_name, size=5*1024*1024):
    if size <= 0:
      message = 'Stream get object failed, chunk size is=%s' % (size)
      raise GalaxyFDSClientException(message)
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.get(uri, auth=self.auth, stream=True)
    if response.status_code == self.HTTP_OK:
      for chunk in response.iter_content(chunk_size=size):
        if chunk:
          yield chunk
    else:
      message = 'Stream get object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)


  def doesObjectExists(self, bucket_name, object_name):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.head(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      return True
    elif response.status_code == self.HTTP_NOT_FOUND:
      return False
    else:
      message = 'Check object existence failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def deleteObject(self, bucket_name, object_name):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.delete(uri, auth=self.auth)
    if response.status_code != self.HTTP_OK:
      message = 'Delete object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def getObjectSize(self, bucket_name, object_name):
    uri = '%s%s/%s' % (self.fds_base_uri, bucket_name, object_name)
    response = requests.get(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      return response.headers['content-length']
    else:
      message = 'Get object size failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def renameObject(self, bucket_name, src_object_name, dst_object_name):
    # http://files.fds.api.xiaomi.com/python-test-15652193901/test4?renameTo=test4000
    uri = '%s%s/%s?renameTo=%s' % (self.fds_base_uri, bucket_name, src_object_name, dst_object_name)
    response = requests.put(uri, auth=self.auth)
    if response.status_code != self.HTTP_OK:
      message = 'Rename object failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def listObjects(self, bucket_name, prefix=''):
    uri = '%s%s?prefix=%s&delimiter=%s' % (self.fds_base_uri, bucket_name, prefix, self.delimiter)
    response = requests.get(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      objects_list = []
      print response.content
      objects = json.loads(response.content)['objects']
      for object in objects:
        objects_list.append(object['name'])
      return objects_list
    else:
      message = 'List objects failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def listDirectories(self, bucket_name, prefix=''):
    uri = '%s%s?prefix=%s&delimiter=%s' % (self.fds_base_uri, bucket_name, prefix, self.delimiter)
    response = requests.get(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      directories = json.loads(response.content)['commonPrefixes']
      return directories
    else:
      message = 'List directories failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def listDirectoriesAndObjects(self, bucket_name, prefix=''):
    uri = '%s%s?prefix=%s&delimiter=%s' % (self.fds_base_uri, bucket_name, prefix, self.delimiter)
    response = requests.get(uri, auth=self.auth)
    result_list=[]
    if response.status_code == self.HTTP_OK:
      directories = json.loads(response.content)['commonPrefixes']
      objects_list = []
      objects = json.loads(response.content)['objects']
      for object in objects:
        objects_list.append(object['name'])
      result_list.extend(directories+objects_list)
      return result_list
    else:
      message = 'List directories and objects failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def getBucketAcl(self, bucket_name):
    uri = '%s%s?%s' % (self.fds_base_uri, bucket_name, SubResource.ACL)
    response = requests.get(uri, auth=self.auth)
    if response.status_code == self.HTTP_OK:
      print response.content
      acp = AccessControlPolicy.getAccessControlPolicy(json.loads(response.content))
      acl = self.acpToAcl(acp)
      return acl
    else:
      message = 'Get bucket acl failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def setObjectAcl(self, bucket_name, object_name, acl=None):
    uri = '%s%s/%s?%s' % (self.fds_base_uri, bucket_name, object_name, SubResource.ACL)
    print uri
    acp = self.aclToAcp(acl)
    print json.dumps(acp)
    response = requests.put(uri, auth=self.auth, data=json.dumps(acp))
    if response.status_code != self.HTTP_OK:
      message = 'Set object acl failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def getObjectAcl(self, bucket_name, object_name):
    uri = '%s%s/%s?%s' % (self.fds_base_uri, bucket_name, object_name, SubResource.ACL)
    print uri
    response = requests.get(uri, auth=self.auth)
    print response.status_code
    if response.status_code == self.HTTP_OK:
      print response.content
      acp = AccessControlPolicy.getAccessControlPolicy(json.loads(response.content))
      acl = self.acpToAcl(acp)
      return acl
    else:
      message = 'Get object acl failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)

  def acpToAcl(self, acp):
    if acp is not None:
      acl = AccessControlList()
      for k in acp['accessControlList']:
        grantee = k['grantee']
        grant_id = grantee['id']
        permission = k['permission']
        grant = Grant(Grantee(grant_id), permission)
        acl.addGrant(grant)
      return acl
    return ''

  def setBucketAcl(self, bucket_name, acl=None):
    uri = '%s%s?%s' % (self.fds_base_uri, bucket_name, SubResource.ACL)
    acp = self.aclToAcp(acl)
    response = requests.put(uri, auth=self.auth, data=json.dumps(acp))
    if response.status_code != self.HTTP_OK:
      message = 'Set bucket acl failed,status=%s,reason=%s' % (response.status_code, response.content)
      raise GalaxyFDSClientException(message)



  def aclToAcp(self, acl):
    if acl is not None:
      acp = {}
      owner = {}
      owner['id'] = self.access_key
      acp['owner'] = owner
      accessControlList = acl.getGrantList()
      acp['accessControlList'] = accessControlList
      return acp
    return ''




access_key = "5341725076926"
access_secret = "vhlqXBAsWMbRIKZx+UBfPQ=="
bucket_name = "python-test-bucketacl"
object_name = "test333"
content = "1234567"

# access_key = "5731725086326"
# access_secret = "h8TXiEAT0Yh0VFJ5ZIQmlA=="

client = GalaxyFDSClient(access_key, access_secret)
# client.putObject(bucket_name, object_name, content)

objectReadAcl = AccessControlList()
objectReadAcl.addGrant(Grant(Grantee("5555"), Permission.READ))

client.getObject(bucket_name, object_name)

client.setObjectAcl(bucket_name, object_name, objectReadAcl)
#client.getObjectAcl(bucket_name, object_name)
#
print client.getObjectAcl(bucket_name, object_name)