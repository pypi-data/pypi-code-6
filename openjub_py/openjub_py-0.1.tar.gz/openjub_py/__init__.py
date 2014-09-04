import urllib
import json
import requests

class Client():
  """A Client for the OpenJUB-API.

  :param token: Token to use for authentication.
  :param app_id: App Id to be used only when using authentication.
  :param server: The Address of the OpenJUB server to use. Must include protocol, port and ending slash.
  """

  allFields = ["firstName", "lastName", "eid", "type", "email", "username", "major", "country", "description"]
  """ All possible fields that are availablw to the server. """

  def __init__(self, token, app_id = None, server = "http://open.jacobs-cs.club/"):
    """Constructor. """
    self.token = token
    self.server = server
    self.app_id = app_id
  def __request__(self, end_point, get_params = None, post_params = None):
    """Makes a generic request to the server.

    :param end_point: Endpoint to request on the server
    :param get_params: GET Parameters for the request.
    :param post_params: POST Parameters for the request.
    :returns: JSON-response to the request.
    """
    if get_params == None:
      get_params = {}
    url = self.server + end_point + "/?" + urllib.urlencode(get_params)
    headers = {"Authorization": "Bearer "+self.token}
    if post_params == None:
      res = requests.get(url, data=json.dumps(post_params), headers=headers)
    else:
      res = requests.post(url, data=json.dumps(post_params), headers=headers)

    return json.loads(res.text)
  def user(self, q, limit = 10, skip = 0, fields = None):
    """The /user endpoint.

    :param q: Query to filter users
    :param limit: Number of elements on one page
    :param skip: Number of elements on one page
    :param fields: List of Fields to return. Defaults to all fields.
    :returns: JSON-response to the request.
    """
    if fields == None:
      fields = Client.allFields

    return self.__request__("user", get_params = {"q": q, "limit": str(limit), "skip": str(skip), "fields": ",".join(fields)})

  def user_autocomplete(self, q, limit = 10, skip = 0, fields = None):
    """The /user/autocomplete endpoint.

    :param account: Account to look for.
    :param fields: List of Fields to return. Defaults to all fields.
    :returns: JSON-response to the request.
    """

    if fields == None:
      fields = Client.allFields

    return self.__request__("user/autocomplete", get_params = {"q": q, "limit": str(limit), "skip": str(skip), "fields": ",".join(fields)})

  def user_account(self, account, fields = None):
    """The /user/:account endpoint.

    :param account: Account to look for.
    :param fields: List of Fields to return. Defaults to all fields.
    :returns: JSON-response to the request.
    """
    if fields == None:
      fields = Client.allFields

    return self.__request__("user/"+account, get_params = {"fields": ",".join(fields)})
  def user_eid(self, eid, fields = None):
    """The /user/eid/:eid endpoint.

    :param eid: eid to look for.
    :param fields: List of Fields to return. Defaults to all fields.
    :returns: JSON-response to the request.
    """
    if fields == None:
      fields = Client.allFields

    return self.__request__("user/eid/"+eid, get_params = {"fields": ",".join(fields)})
