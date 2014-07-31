# Copyright 2014, Scalyr, Inc.

import errno
import httplib
import re
import socket
import time

import scalyr_agent.json_lib as json_lib
import scalyr_agent.scalyr_logging as scalyr_logging

from cStringIO import StringIO
from scalyr_agent.util import Util

log = scalyr_logging.getLogger(__name__)

class ScalyrClientSession(object):
    def __init__(self, server, api_key, quiet=False):

        if not quiet:
            log.info('Using "%s" as address for scalyr servers' % server)
        parsed_server = re.match('^(http://|https://|)([^:]*)(:\d+|)$', server.lower())

        if parsed_server is None:
            raise Exception('Could not parse server address "%s"' % server)

        self.__full_address = server
        self.__host = parsed_server.group(2)
        self.__use_ssl = parsed_server.group(1) == 'https://'

        if parsed_server.group(3) != '':
            self.__port = int(parsed_server.group(3)[1:])
        elif self.__use_ssl:
            self.__port = 443
        else:
            self.__port = 80

        self.__connection = None
        self.__api_key = api_key
        self.__session_id = Util.create_unique_id()

        # The time we created the connection.
        self.__last_connection_creation = None

        # We create a few headers ahead of time so that we don't have to recreate them each time we need them.
        self.__standard_headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'application/json',
        }

    def ping(self):
        return self.add_events([])

    def add_events(self, events, session_attributes=None):

        # TODO:  Break this part out into a generic invokeApi method once we need to support
        # multiple Scalyr service API calls.
        try:
            if self.__connection is None:
                if self.__use_ssl:
                    self.__connection = httplib.HTTPSConnection(self.__host, port=self.__port)
                else:
                    self.__connection = httplib.HTTPConnection(self.__host, port=self.__port)
                self.__connection.connect()
        except socket.error, e:
            if e.errno == errno.ECONNREFUSED:
                return 'connectionRefused'
        except Exception:
            log.exception('Failed to connect to "%s" due to exception', self.__full_address,
                          error_code='connectionFailed')
            return 'connectionFailed'

        body = {
            'token': self.__api_key,
            'events': events,
            'session': self.__session_id,
            'threads': [],
        }

        if session_attributes is not None:
            body['sessionInfo'] = session_attributes

        body_str = json_lib.serialize(body, use_fast_encoding=True)
        try:
            self.__connection.request('POST', '/addEvents', body=body_str,
                                      headers=self.__standard_headers)

            response = self.__connection.getresponse().read()
        except socket.error, e:
            if e.errno == errno.ECONNREFUSED:
                return 'connectionRefused'
        except Exception:
            # TODO: Do not just catch Exception.  Do narrower scope.
            log.exception('Failed to send request due to exception', error_code='requestFailed')
            return 'requestFailed'

        try:
            response_as_json = json_lib.parse(response)
        except Exception:
            # TODO: Do not just catch Exception.  Do narrower scope.  Also, log error here.
            log.exception('Failed to parse response due to exception', error_code='parseResponseFailed')
            return 'parseResponseFailed'

        if 'status' in response_as_json:
            return response_as_json['status']
        else:
            return 'unknownError'

    def send(self, add_events_request):
        current_time = time.time()

        # TODO:  Break this part out into a generic invokeApi method once we need to support
        # multiple Scalyr service API calls.
        response = ''
        try:
            if self.__connection is None:
                if self.__use_ssl:
                    self.__connection = httplib.HTTPSConnection(self.__host, port=self.__port)
                else:
                    self.__connection = httplib.HTTPConnection(self.__host, port=self.__port)
                self.__connection.connect()
                self.__last_connection_creation = current_time
        except Exception:
            log.exception('Failed to connect to "%s" due to exception', self.__full_address,
                          error_code='connectionFailed')
            return 'connectionFailed', 0, ''

        body_str = add_events_request.get_payload()
        try:
            self.__connection.request('POST', '/addEvents', body=body_str,
                                      headers=self.__standard_headers)

            response = self.__connection.getresponse().read()
        except Exception:
            # TODO: Do not just catch Exception.  Do narrower scope.
            self.__close_connection_for_error_if_necessary(current_time)
            log.exception('Failed to send request due to exception', error_code='requestFailed')
            return 'requestFailed', len(body_str), response

        try:
            response_as_json = json_lib.parse(response)
        except Exception:
            # TODO: Do not just catch Exception.  Do narrower scope.  Also, log error here.
            self.__close_connection_for_error_if_necessary(current_time)
            log.exception('Failed to parse response of \'%s\' due to exception',
                          Util.remove_newlines_and_truncate(response, 1000),
                          error_code='parseResponseFailed')
            return 'parseResponseFailed', len(body_str), response

        self.__last_success = current_time

        if 'status' in response_as_json:
            return response_as_json['status'], len(body_str), response
        else:
            return 'unknownError', len(body_str), response

    def close(self):
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

    def __close_connection_for_error_if_necessary(self, current_time):
        if current_time - self.__last_connection_creation > 60:
            log.warn('Closing HTTP connection due to errors.  Will re-open.')
            self.close()

    def add_events_request(self, session_info=None, max_size=1*1024*1024*1024):
        body = {
            'token': self.__api_key,
            'session': self.__session_id,
            'threads': [],
        }

        if session_info is not None:
            body['sessionInfo'] = session_info

        return AddEventsRequest(body, max_size=max_size)


class AddEventsRequest(object):
    """Used to construct an AddEventsRequest to eventually send.

    This abstraction has two key features.  First, it uses a generally more efficient scheme to build
    up the string to eventually use as the body for an add_events request.  Secondly, it does not require all events
    at construction time.  Instead, you can incrementally add more events before the request is actually sent.  This
    leads to better memory utilization when combined with an abstraction that is incrementally reading events from disk.
    It will also prevent you from exceeding the maximum request size.
    """
    def __init__(self, base_body, max_size=1*1024*1024):
        """Initializes the instance.

        Arguments:
            base_body:  A JsonObject or dict containing the information to send as the body of the add_events
                request, with the exception of the events field.  The events field must not be included because
                it will be added later.  Note, base_body must have some fields set, such as 'ts' which is required
                by the server.
            max_size:  The maximum number of bytes this request can consume when it is serialized to JSON.
        """
        assert len(base_body) > 0, "The base_body object must have some fields defined."
        assert not 'events' in base_body, "The base_body object cannot already have 'events' set."

        # As an optimization, we use a StringIO object to serialize the request.  We also
        # do a little bit of the JSON object assembly by hand.  Specifically, we serialize the request
        # to JSON without the 'events' field, but then delete the last '}' so that we can manually
        # add in the 'events: [ ... ]' ourselves.  This way we can watch the size of the buffer as
        # we build up events.
        string_buffer = StringIO()
        json_lib.serialize(base_body, output=string_buffer, use_fast_encoding=True)

        # Now go back and find the last '}' and delete it so that we can open up the JSON again.
        location = string_buffer.tell()
        while location > 0:
            location -= 1
            string_buffer.seek(location)
            if string_buffer.read(1) == '}':
                break

        # Now look for the first non-white character.  We need to add in a comma after it.
        last_char = None
        while location > 0:
            location -= 1
            string_buffer.seek(location)
            last_char = string_buffer.read(1)
            if not last_char.isspace():
                break

        # If the character happened to a comma, back up over that since we want to write our own comma.
        if location > 0 and last_char == ',':
            location -= 1

        if location < 0:
            raise Exception('Could not locate trailing "}" and non-whitespace in base JSON for add events request')

        # Now chop off everything after the character at the location.
        location += 1
        string_buffer.seek(location)
        string_buffer.truncate()

        # Append the start of our events field.
        string_buffer.write(', events: [')

        # The string that must be append after all of the events to terminate the JSON.
        self.__post_fix = ']}'

        self.__buffer = string_buffer
        self.__max_size = max_size
        self.__current_size = self.__buffer.tell() + len(self.__post_fix)

        self.__events_added = 0

        # If we have finished serializing the body, it is stored here until the close() method is invoked.
        self.__body = None

    def add_event(self, event, timestamp=None):
        """Adds the serialized JSON for event if it does not cause the maximum request size to be exceeded.

        It will automatically add in a 'ts' field to event containing a new timestamp based on the current time
        but ensuring it is greater than any previous timestamp that has been used.

        It is illegal to invoke this method if 'get_payload' has already been invoked.

        Arguments:
            event:  The event object, usually a dict or a JsonObject.
            timestamp:  The timestamp to use for the event.  This should only be used for testing.

        Returns:
            True if the event's serialized JSON was added to the request, or False if that would have resulted
            in the maximum request size being exceeded so it did not.
        """
        start_pos = self.__buffer.tell()
        # If we already added an event before us, then make sure we add in a comma to separate us from the last event.
        if self.__events_added > 0:
            self.__buffer.write(',')

        if timestamp is None:
            timestamp = self.__get_timestamp()

        event['ts'] = str(timestamp)
        json_lib.serialize(event, output=self.__buffer, use_fast_encoding=True)
        size = self.__buffer.tell() - start_pos

        # Check if we exceeded the size, if so chop off what we just added.
        if self.__current_size + size > self.__max_size:
            self.__buffer.truncate(start_pos)
            return False

        self.__current_size += size
        self.__events_added += 1
        return True

    def get_payload(self):
        """Returns the serialized JSON to use as the body for the add_request.

        After this is invoked, no new events can be added via the 'add_event' method.
        """
        if self.__body is None:
            self.__buffer.write(self.__post_fix)
            self.__body = self.__buffer.getvalue()
            self.__buffer.close()
            self.__buffer = None
        return self.__body

    def close(self):
        """Must be invoked after this request is no longer needed.  You may not add events or invoke get_payload
        after this call.
        """
        self.__body = None

    def __get_timestamp(self):
        global __last_time_stamp__

        base_timestamp = long(time.time() * 1000000000L)
        if __last_time_stamp__ is not None and base_timestamp <= __last_time_stamp__:
            base_timestamp = __last_time_stamp__ + 1L
        __last_time_stamp__ = base_timestamp
        return base_timestamp

    def position(self):
        """Returns a position such that if it is passed to 'set_position', all events added since this method was
        invoked are removed."""

        return AddEventsRequest.Position(self.__current_size, self.__events_added, self.__buffer.tell())

    def set_position(self, position):
        """Reverts this object to only contain the events contained by the object when position was invoked to
        get the passed in position.

        Arguments:
            position:  The position token representing the previous state.
        """
        self.__current_size = position.current_size
        self.__events_added = position.events_added
        self.__buffer.truncate(position.buffer_size)

    class Position(object):
        def __init__(self, current_size, events_added, buffer_size):
            self.current_size = current_size
            self.events_added = events_added
            self.buffer_size = buffer_size

__last_time_stamp__ = None