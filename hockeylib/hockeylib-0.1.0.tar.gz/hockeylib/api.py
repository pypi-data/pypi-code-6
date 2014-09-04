import json
import pycurl
import os
import logging

from StringIO import StringIO

__HOCKEY_API_ROOT = "https://rink.hockeyapp.net/api/2/"

def hockey_uri(endpoint):
    return __HOCKEY_API_ROOT+endpoint

def token_header():
    return ["X-HockeyAppToken: {0}".format(os.environ["HOCKEY_API_KEY"])]

def request(endpoint,postdata=None):
    logging.debug("Sending request to {0}".format(endpoint))

    try:
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, hockey_uri(endpoint))
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.HTTPHEADER,token_header())

        if postdata != None:
            c.setopt(c.HTTPPOST, postdata)

        c.perform()
        c.close()

        response = buffer.getvalue()
        logging.debug("Response: {0}".format(response));

        return json.loads(response)
    except pycurl.error:
        logging.error("Pycurl request interrupted")
        return None