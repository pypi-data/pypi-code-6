import requests

class TinderClient(object):
  TINDER_URL = "https://api.gotinder.com"

  def __init__(self, access_token=None, fb_id=None):
    self.authorize(access_token, fb_id)

  def post_object(self, id, **args):
    return self.request("/" + id)
  
  def set_headers(self):
    headers = {
          "User-Agent" : "Tinder Android Version 2.2.3",
          "os_version" : "16"
        }

    if hasattr(self, 'x_auth_token'):
      headers["X-Auth-Token"] = self.x_auth_token

    return headers 

  def request(self, path, method=None, args=None, post_args=None):
    try:
      response = requests.request(method or "GET", 
                                  self.TINDER_URL + "/" + path, 
                                  params=args,
                                  data=post_args,
                                  headers=self.set_headers())

    except requests.HTTPError as e:
      response = json.loads(e.read())
    
    headers = response.headers
    if 'json' in headers['content-type']:
      result = response.json()

    return result

  def authorize(self, access_token=None, fb_id=None):
    body = self.request('auth', 
                        post_args={'facebook_token': access_token, 'facebook_id': fb_id},
                        method='POST')

    if body and body['token']:
      self.x_auth_token = body['token']
      self.user_id = body['user']['_id']
  
  def get_user(self, user_id):
    return self.request('user/' + user_id,
                        method='GET')

  def get_recs(self, limit):
    return self.request('user/recs',
                        args={'limit': limit},
                        method='GET')

  def like(self, user_id):
    return self.request('like/' + user_id,
                        method='GET')

  def _pass(self, user_id):
    return self.request('pass/' + user_id,
                        method='GET')

  def update_location(self, lat, lon):
    return self.request('user/ping',
                        post_args={'lat': lat, 'lon': lon},
                        method='POST')
    
