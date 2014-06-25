# Copyright 2014 Christopher Richard Dobbs <christopher.dobbs@evry.com>.
#
# This file is part of the python-fecru library.
#
# python-fecru is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-fecru is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-fecru.  If not, see <http://www.gnu.org/licenses/>.
#  
import json
import requests
import httplib

class FecruServer(object):
    """Fecru server authentication object."""

    def __init__(self, fecru_url, app_name, app_pass):
        self.fecru_url = fecru_url
        self.app_name = app_name
        self.app_pass = app_pass
        self.rest_url = fecru_url.rstrip("/") + "/rest-service/auth-v1/login"
        self.session = requests.Session()

        self.session.auth = requests.auth.HTTPBasicAuth(app_name, app_pass)
#        print str(self.session.auth)
        self.session.headers.update({
            "Content-type": "application/json",
            "Accept": "application/json"
        })


#        self.conn= httplib.HTTPConnection(self.fecru_url)
#        args=urllib.urlencode({'userName':self.usr, 'password':self.psw})
#        headers={'accept':'application/json'}
#        self.conn.request("post", "/rest-service/auth-v1/login", args, headers)
#        r = self.conn.getresponse() 
#        if r.status not in (200, 304):
#            raise Exception("Problems getting a token from codereview. %s %s" % (r.status, r))
#        else:
#            print "connected OK to FECRU!!! %s:%s"%(conn, r)           
#        print "RTN:%s"%self.atlas

        

    def __str__(self):
        return "Crowd Server at %s" % self.crowd_url

    def __repr__(self):
        return "<CrowdServer('%s', '%s', %s')>" % \
            (self.crowd_url, self.app_name, self.app_pass)

    def _get(self, *args, **kwargs):
        """Wrapper around Requests for GET requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.get(*args, **kwargs)
        return req

    def _post(self, *args, **kwargs):
        """Wrapper around Requests for POST requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.post(*args, **kwargs)
        return req

    def _delete(self, *args, **kwargs):
        """Wrapper around Requests for DELETE requests

        Returns:
            Response:
                A Requests Response object
        """
        req = self.session.delete(*args, **kwargs)
        return req

    def auth_ping(self):
        """Test that application can authenticate to Fecru.

        Attempts to authenticate the application user against
        the Fecru server. In order for user authentication to
        work, an application must be able to authenticate.

        Returns:
            bool:
                True if the application authentication succeeded.
        """

        url = self.rest_url + "/non-existent/location"
        response = self._get(url)

        if response.status_code == 401:
            return False
        elif response.status_code == 404:
            return True
        else:
            # An error encountered - problem with the Crowd server?
            return False

    def get_server_info(self):
        """Return server info.

        Args:
            None

        Returns:
            dict:
                Server information data
                

            None: If failure.
        """
#        print "url:%s"%self.fecru_url + "/rest-service-fecru/server-v1"
#        response = self._get(self.fecru_url + "/rest-service-fecru/server-v1?FEAUTH=" +  self.session.auth)
        response = self._get(self.fecru_url + "/rest-service-fecru/server-v1")
#        print dir(response)
#        print response.content
#        print response.text
        
        if not response.ok:
            return None

        return response.content

    def create_repository(self, repo_name, descr, scmurl, scmpath, enabled="false"):
        """Add a new repository

        Args:
            group: Repository name

        Returns:
 
            None: If failed.
        """
        rtnStr="Success"
        
        params = {
            "type" : "SUBVERSION",
            "name" : repo_name,
            "description" : descr,
#            "enabled" : enabled,
            "url" : scmurl,
            "path" : scmpath,
            "username" : "continuum",
            "password" : "ECOoSTFTjxm67w2Uw6nSmOMxvwuj3jh81fE4FwbvLucw91SmvG8UG6j6mNh5Or5"
#            "svn" : {
#                "url" : scmurl,
#                "path" : scmpath,
#                "auth" : {
#                    "username" : "continuum",
#                    "password" : "ECOoSTFTjxm67w2Uw6nSmOMxvwuj3jh81fE4FwbvLucw91SmvG8UG6j6mNh5Or5"
#                    }
            
        }

        response = self._post(self.fecru_url + "/rest-service-fecru/admin/repositories-v1",
                             data=json.dumps(params))
        if not response.ok:
            rtnStr="Error : "+str(response.status_code)
        else:
            rtnStr=rtnStr+" : "+str(response.status_code)
    
        return(rtnStr)

    def check_repository_exists(self, name):
        """List all repositories

        Args:
            limit: page limit

        Returns:
 
            None: If failed.
        """
        params = {
            "name" : name
            }

        print params
        response = self._get(self.fecru_url + "/rest-service-fecru/admin/repositories-v1",data=json.dumps(params))

        print dir(response)
        print response.status_code
        print response.text
        if not response.ok:
            return False

        return(response.text)
    
