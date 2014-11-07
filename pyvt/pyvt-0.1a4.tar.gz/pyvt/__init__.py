"""
    This is a modified version of the virustotal2 python pacakge for VirusTotal.
    (https://github.com/Phillipmartin/virustotal2)
    This package supports python3 only and is targeted towards private API key users.
"""

import threading
from itertools import zip_longest
import os
import urllib.parse
import re
import time
import configparser
import requests
from ._version import __version__


class API(object):

    def __init__(self, api_key_file, api_key=None, limit_per_min=3000):

        confpath = os.path.expanduser(api_key_file)

        if not os.path.exists(confpath):
            raise FileExistsError('Could not find API KEY file! Please provide file or provide the api key as input')

        config = configparser.RawConfigParser()
        config.read(confpath)
        key = config.get('vt', 'apikey')

        if not api_key is None:
            key = api_key

        self.api_key = key
        self._urls_per_retrieve = 4
        self._hashes_per_retrieve = 4
        self._ips_per_retrieve = 1
        self._domains_per_retrieve = 1
        self._urls_per_scan = 4
        self._hashes_per_scan = 25
        self._files_per_scan = 1
        self.limits = []
        self.limit_lock = threading.Lock()
        self.limit_per_min = limit_per_min

    @staticmethod
    def _grouped(iterable, n):
        """
        take a list of items and return a list of groups of size n.
        :param n: the size of the groups to return
        """
        args = [iter(iterable)] * n
        return [[e for e in t if not e is None] for t in zip_longest(*args, fillvalue=None)]

    def _limit_call_handler(self):
        """
        Ensure we don't exceed the N requests a minute limit by leveraging a thread lock
        """
        #acquire a lock on our threading.Lock() object
        with self.limit_lock:
            #if we have no configured limit, exit.  the lock releases based on scope
            if self.limit_per_min <= 0:
                return

            now = time.time()
            #self.limits is a list of query times + 60 seconds.  In essence it is a list of times
            #that queries time out of the 60 second query window.

            #this check expires any limits that have passed
            self.limits = [l for l in self.limits if l > now]
            #and we tack on the current query
            self.limits.append(now + 60)

            #if we have more than our limit of queries (and remember, we call this before we actually
            #execute a query) we sleep until the oldest query on the list (element 0 because we append
            #new queries) times out.  We don't worry about cleanup because next time this routine runs
            #it will clean itself up.
            if len(self.limits) >= self.limit_per_min:
                time.sleep(self.limits[0] - now)

    def _whatis(self, thing):
        """
        Categorizes the thing it gets passed into one of the items VT supports
        Returns a sting representation of the type of parameter passed in. \n
        :param thing: a parameter to identify. this can be a list of string or a string
        :return: a string representing the identified type of the input thing. If the input thing is a list the
         first element of the list is used to identify.
        """
        #per the API, bulk requests must be of the same type
        #ignore that you can intersperse scan IDs and hashes for now
        #...although, does that actually matter given the API semantics?
        if isinstance(thing, list):
            thing = thing[0]

        #implied failure case, thing is neither a list or a file, so we assume string
        if not isinstance(thing, str):
            return "%s" % API_Constants.UNKNOWN

        if os.path.isfile(thing):
            if thing.endswith(".base64"):
                    return API_Constants.BASE64
            else:
                return API_Constants.FILE_NAME

        elif API_Constants.HASH_RE.match(thing):
            return API_Constants.HASH

        elif API_Constants.IP_RE.match(thing):
            return API_Constants.IP

        elif API_Constants.DOMAIN_RE.match(thing):
            return API_Constants.DOMAIN

        elif API_Constants.SCAN_ID_RE.match(thing):
            return API_Constants.SCANID

        elif urllib.parse.urlparse(thing).scheme:
            return API_Constants.URL

        else:
            return API_Constants.UNKNOWN

    def _get_query(self, query, params):
        """
        Submit a GET request to the VT API
        :param query: The query (see https://www.virustotal.com/en/documentation/private-api/ for types of queries)
        :param params: parameters of the query
        :return: JSON formatted response from the API
        """
        if not "apikey" in params:
            params["apikey"] = self.api_key

        response = requests.get(query, params=params)
        return response.json()

    def _post_query(self, query, params):
        """
        Submit a POST request to the VT API
        :param query: The query (see https://www.virustotal.com/en/documentation/private-api/ for types of queries)
        :param params: parameters of the query
        :return: JSON formatted response from the API
        """
        if not "apikey" in params:
            params["apikey"] = self.api_key

        response = requests.post(query, data=params)
        return response.json()

    def retrieve(self, thing, thing_type=None):
        """
        Retrieve a report from VirusTotal based on a hash, IP, domain, file or URL or ScanID.  NOTE: URLs must include the scheme
         (e.g. http://)\n

        :param thing: a file name on the local system, a URL or list of URLs,
                      an IP or list of IPs, a domain or list of domains, a hash or list of hashes
        :param thing_type: Optional, a hint to the function as to what you are sending it
        :return: Returns a a dictionary with thing as key and the API json response as the value
                If thing was a list of things to query the results will be a dictionary with every thing in the list
                as a key
        :raises TypeError: if it gets something other than a URL, IP domain, hash or ScanID
        :raises TypeError: if VirusTotal returns something we can't parse.
        """
        #trust the user-supplied type over the automatic identification
        thing_id = self._whatis(thing)
        if thing_type is None:
            thing_type = thing_id

        query_parameters = {}

        # Query API for URL(s)
        if thing_type == API_Constants.URL:  # Get the scan results for a given URL or list of URLs.
            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_URL_REPORT
            if not isinstance(thing, list):
                thing = [thing]
            grouped_urls = self._grouped(thing, self._urls_per_retrieve)  # break list of URLS down to API limits
            results = {}

            for group in grouped_urls:
                query_parameters = {"resource": "\n".join([url for url in group])}
                self._limit_call_handler()
                try:
                    response = self._post_query(query, query_parameters)
                except:
                    raise TypeError

                # If we get a list of URLs that has N urls and N mod '_url_per_retrieve' is 1
                # for example  [url, url, url], when limit is 2, the last query will not return a list
                if not isinstance(response, list):
                    response = [response]

                for index, scanid in enumerate(group):
                    results[scanid] = response[index]

            result = results

        # Query API for domain(s)
        elif thing_type == API_Constants.DOMAIN:

            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_DOMAIN_REPORT
            if not isinstance(thing, list):
                thing = [thing]
            results = {}
            for domain in thing:
                query_parameters["domain"] = domain
                self._limit_call_handler()
                response = self._get_query(query, query_parameters)
                results[domain] = response

            result = results

        # Query API for IP(s)
        elif thing_type == API_Constants.IP:

            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_IP_REPORT

            if not isinstance(thing, list):
                thing = [thing]

            results = {}
            for ip in thing:
                query_parameters["ip"] = ip
                self._limit_call_handler()
                try:
                    response = self._get_query(query, query_parameters)
                except:
                    raise TypeError
                results[ip] = response

            result = results

        # Query API for HASH, bulk HASH queries not possible
        elif thing_type == API_Constants.HASH:

            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_FILE_REPORT

            results = {}
            if not isinstance(thing, list):
                thing = [thing]
            query_parameters["resource"] = ", ".join(thing)
            self._limit_call_handler()
            response = self._get_query(query, query_parameters)

            if not isinstance(response, list):
                response = [response]

            for index, hash in enumerate(thing):
                results[hash] = response[index]
            result = results

        elif thing_type == "scanid":
            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_GET_URL_REPORT
            if not isinstance(thing, list):
                thing = [thing]
            results = {}

            for scanid in thing:
                query_parameters["resource"] = scanid
                self._limit_call_handler()
                try:
                    response = self._post_query(query, query_parameters)
                except:
                    raise TypeError
                results[scanid] = response

            result = results
        else:
            raise TypeError("Unimplemented '%s'." % thing_type)

        return result

    def scan(self, thing, thing_type=None, blocking=False):
        """
        \nScan a single or list of URLs, or Domains\n
        NOTE: URLs must include the scheme (http:// or https://)\n
        NOTE: For a single domain or list of domains this method will automatically append an 'http://' to the \n
        beginningof the domain(s)\n

        :param thing: a URL or list of URLs,
                      a domain or list of domains
        :param thing_type: Optional, a hint to the function as to what you are sending it
        :param blocking: Default is False, it set to True will cause the function to block until all scan results can be
                        retrieved from virus total and the results returned
        :return: If blocking is False will return a dictionary with the thing as key and the ScanID as the value.
                 These scan results can be later retrieved with the the API's retrieve method by providing the ScanID(s).
                 If blocking if True will return a dictionary with the thing as key and the Scan result as the value.
        :raises TypeError: if it gets something other than a URL or domain or list of either
        :raises TypeError: if VirusTotal returns something we can't parse.
        """
        thing_id = self._whatis(thing)
        if thing_type is None:
            thing_type = thing_id

        query_parameters = {}
        result = {}

        if thing_type == API_Constants.URL:  # Get the scan results for a given URL or list of URLs.
            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_SUBMIT_URL_SCAN
            if not isinstance(thing, list):
                thing = [thing]

            pending_results = {}
            for url in thing:
                query_parameters["url"] = url
                self._limit_call_handler()
                try:
                    response = self._post_query(query, query_parameters)
                    pending_results[url] = response['scan_id']
                except:
                    raise TypeError

            result = pending_results
            if blocking:
                results = {}
                done = 0
                pending = len(pending_results)
                while done < pending:
                    url, scan_id = pending_results.popitem()
                    response = self.retrieve(scan_id)
                    if response[scan_id]['response_code'] == 1:
                        results[url] = response[scan_id]
                        done += 1
                    else:
                        pending_results[url] = scan_id
                result = results

        elif thing_type == API_Constants.DOMAIN:
            query = API_Constants.CONST_API_URL + API_Constants.API_ACTION_SUBMIT_URL_SCAN
            if not isinstance(thing, list):
                thing = [thing]

            thing = ['http://%s' % a for a in thing]
            pending_results = {}

            for url in thing:
                query_parameters["url"] = url
                self._limit_call_handler()
                try:
                    response = self._post_query(query, query_parameters)
                    pending_results[url] = response['scan_id']
                except:
                    raise TypeError

            result = pending_results
            if blocking:
                results = {}
                done = 0
                pending = len(pending_results)
                while done < pending:
                    url, scan_id = pending_results.popitem()
                    response = self.retrieve(scan_id)
                    if response[scan_id]['response_code'] == 1:
                        results[url] = response[scan_id]
                        done += 1
                    else:
                        pending_results[url] = scan_id
                result = results

        else:
            raise TypeError("Unimplemented! for '%s'." % thing_type)
        return result


class API_Constants:
    #Regular expressions used internally to match the type of query sent to the virus total API
    SCAN_ID_RE = re.compile(r"^[a-fA-F0-9]{64}-[0-9]{10}$")
    IP_RE = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    HASH_RE = re.compile(r"^([1234567890abcdef]{32,32}|[1234567890abcdef]{40,40}|[1234567890abcdef]{64,64})$")
    DOMAIN_RE = re.compile(r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$")

    #Constants used to identify the type of query sent to the virus total API
    BASE64 = "base64"
    SCANID = "scanid"
    DOMAIN = "domain"
    IP = "ip"
    HASH = "hash"
    URL = "url"
    FILE_NAME = "file_name"
    UNKNOWN = "unknown"

    CONST_API_URL = "https://www.virustotal.com/vtapi/v2/"
    API_ACTION_GET_URL_REPORT = "url/report"
    API_ACTION_GET_IP_REPORT = "ip-address/report"
    API_ACTION_GET_DOMAIN_REPORT = "domain/report"
    API_ACTION_GET_FILE_REPORT = "file/report"
    API_ACTION_SUBMIT_URL_SCAN = "url/scan"
