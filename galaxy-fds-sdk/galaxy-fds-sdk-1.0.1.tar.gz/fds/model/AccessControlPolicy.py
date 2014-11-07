class AccessControlPolicy:
  @staticmethod
  def getAccessControlPolicy(response_content):
    if response_content != '':
      acl = {}
      # if 'owner' in response_content.keys():
      #   # print respons_content['owner']
      #   acl['owner'] = response_content['owner']
      if 'accessControlList' in response_content.keys():
        # print 'accessControlList%s' % respons_content['accessControlList']
        acl['accessControlList'] = response_content['accessControlList']
      return acl
    return None

