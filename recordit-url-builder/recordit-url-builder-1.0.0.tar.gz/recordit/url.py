import hashlib
import urllib

class URLBuilder:
    """A simple tool to generate recordit URLs

    Usage:

    from recordit.url import URLBuilder
    # or import recordit.url and use recordit.url.URLBuilder

    url_builder = URLBuilder(
      "f33dd06d1cd1fb6e94504c767e5ccd9d0f7cd039",     # your client ID
      "6d85ffe45dbc37f6e47bc443f6079dc26f61b3df"      # your secret
    )

    url_builder.generate({
        "fps": 12,
        "encode": "none",
        "action_url": "http://example.com/123",
        "callback": "http://example.com/api/123",
        "start_message": "This is the initial message",
        "end_message": "This is the end message",
        "width": 1280,
        "height": 720
    })

    # => recordit:f33dd06d1cd1fb6e94504c767e5ccd9d0f7cd039-565fcfbfe0c2e0c59be5
    9df7b3b73d42f564e6cc?fps=12&encode=none&action_url=http%3A%2F%2Fexample.com%
    2F123&callback=http%3A%2F%2Fexample.com%2Fapi%2F123&start_message=This%20is%
    20the%20initial%20message&end_message=This%20is%20the%20end%20message&width=
    1280&height=720"""

    client_id = None
    secret = None
    protocol = 'recordit'

    def __init__(self, client_id, secret):
        'Initialize the builder with the client ID and secret'

        self.client_id = client_id
        self.secret = secret

    def generate(self, params_dictionary):
        'Main API entry point, receives a dictionary containing the parameters\
                to encode in the URL, returns the actual URL.'

        query_string = self.__queryfy(params_dictionary)
        authenticity_token = self.__sign_request(query_string)

        return "{0}:{1}-{2}{3}".format(URLBuilder.protocol, self.client_id,
                authenticity_token, query_string)


    def __sign_request(self, query_string):
        'Hashes the query string'
        return hashlib.sha1(self.secret + query_string).hexdigest()

    def __queryfy(self, params_dictionary):
        'Given the params dictionary, converts it to a url encoded query string'

        query_list = []

        for key, value in params_dictionary.iteritems():
            sk = urllib.quote(key)
            sv = urllib.quote(str(value))

            query_list.append("{0}={1}".format(sk,sv))

        return "?{0}".format("&".join(query_list))


