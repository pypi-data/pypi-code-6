# Copyright 2014, Scalyr, Inc.
#
# A ScalyrMonitor which retrieves a specified URL and records the response status and body.

import re
import httplib
import urllib2
import cookielib

from scalyr_agent.scalyr_monitor import ScalyrMonitor


first_line_pattern = re.compile('[^\r\n]+')


# Redirect handler that doesn't follow any redirects
class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response

    https_response = http_response


# UrlMonitor implementation
class UrlMonitor(ScalyrMonitor):
    """A Scalyr agent monitor which retrieves a specified URL and records the response status and body.
    """

    def _initialize(self):
        # Fetch and validate our configuration options.
        # Note that we do NOT currently validate the URL. It would be reasonable to check
        # for valid syntax here, but we should not check that the domain name exists, as an
        # external change (e.g. misconfigured DNS server) could then prevent the agent from
        # starting up.
        self.url = self._config.get("url")
        self.timeout = self._config.get("timeout", 10)
        self.max_characters = self._config.get("max_characters", 200)
        self.log_all_lines = self._config.get("log_all_lines", False)

        # Verify that the timeout value is reasonable
        try:
            float(self.timeout)
        except ValueError:
            raise Exception("timeout (%s) is not a number" % (self.timeout))
            
        if self.timeout < 0 or self.timeout > 30:
            raise Exception("invalid timeout %d; must be in the range 0 to 30" % (self.timeout))

        # Verify that the max_characters value is reasonable
        try:
            int(self. max_characters)
        except ValueError:
            raise Exception("max_characters (%s) is not a number" % (self. max_characters))
            
        if self.max_characters < 0 or self. max_characters > 10000:
            raise Exception("invalid max_characters %d; must be in the range 0 to 1000" % (self. max_characters))

        extract_expression = self._config.get("extract", "")
        if extract_expression:
            self.extractor = re.compile(extract_expression)
            
            # Verify that the extract expression contains a matching group, i.e. a parenthesized clause.
            # We perform a quick-and-dirty test here, which will work for most regular expressions.
            # If we miss a bad expression, it will result in a stack trace being logged when the monitor
            # executes.
            if extract_expression.find("(") < 0:
                raise Exception("extract expression [%s] must contain a matching group" % (extract_expression))
        else:
            self.extractor = None

    def gather_sample(self):
        response = None

        try:
            opener = urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            response = opener.open(self.url, None, self.timeout)
        except urllib2.HTTPError, e:
            self._logger.error("HTTPError retrieving %s: %s" % (self.url, e))
            return
        except urllib2.URLError, e:
            self._logger.error("URLError retrieving %s: %s" % (self.url, e))
            return

        response_body = response.read()
        if self.extractor is not None:
            match = self.extractor.search(response_body)
            if match is not None:
                response_body = match.group(1)

        if self.log_all_lines:
            s = response_body
        else:
            first_line = first_line_pattern.search(response_body)
            s = ''
            if first_line is not None:
                s = first_line.group().strip()

        if len(s) > self.max_characters:
            s = s[:self.max_characters] + "...";
        self._logger.emit_value('response', s, extra_fields={'url': self.url, 'status': response.getcode(), 'length': len(response_body)})

