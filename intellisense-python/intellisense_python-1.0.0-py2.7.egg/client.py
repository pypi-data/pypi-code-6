import collections
import time
from datetime import datetime, timedelta
import json
import logging
import numbers
import threading

from dateutil.tz import tzutc
import requests

from stats import Statistics
from errors import ApiError
from utils import guess_timezone, DatetimeSerializer

import options


logging_enabled = True
logger = logging.getLogger('intellisense')


def log(level, *args, **kwargs):
    if logging_enabled:
        method = getattr(logger, level)
        method(*args, **kwargs)


def package_exception(client, data, e):
    log('warn', 'Intellify request error', exc_info=True)
    client._on_failed_flush(data, e)


def package_response(client, data, response):
    # TODO: reduce the complexity (mccabe)
    if response.status_code == 200 or response.status_code == 201:
        client._on_successful_flush(data, response)
    elif response.status_code == 400:
        content = response.text
        try:
            body = json.loads(content)

            code = 'bad_request'
            message = 'Bad request'

            if 'error' in body:
                error = body.error

                if 'code' in error:
                    code = error['code']

                if 'message' in error:
                    message = error['message']

            client._on_failed_flush(data, ApiError(code, message))

        except Exception:
            client._on_failed_flush(data, ApiError('Bad Request', content))
    else:
        client._on_failed_flush(data,
                                ApiError(response.status_code, response.text))


def request(client, url, data):

    log('debug', 'Request ... with data ' + json.dumps(data))

    if client.host:
        options.host = client.host

    if client.port:
        options.port = client.port

    requestBaseURL = options.host + ':' + options.port

    log('debug', 'BaseURL for IntelliStore is ' + requestBaseURL)
    
    # Separate out describes
    describes = [x for x in data['batch'] if x['__action'] == 'describe']
    log('debug', 'Describes in list =  ' + json.dumps(describes))
    describe_url = requestBaseURL + options.endpoints['describe']
    
    # Separate out measures
    measures = [x for x in data['batch'] if x['__action'] == 'measure']
    log('debug', 'Measures in list =  ' + json.dumps(measures))
    measure_url = requestBaseURL + options.endpoints['measure']

    # Every thing else
    defaults = [x for x in data['batch'] if x['__action'] == 'identify' or x['__action'] == 'alias' or x['__action'] == 'track']
    log('debug', 'Defaults in list =  ' + json.dumps(defaults))

    try:

        response_flag = True

        if len(describes) > 0:
            for describe in describes:
                response_d = requests.put(describe_url,
                                         data=json.dumps(describe, cls=DatetimeSerializer),
                                         headers={'content-type': 'application/json'},
                                         timeout=client.timeout)
                log('debug', 'Finished Intellify describe request. Response = ' + response_d.text)
                package_response(client, describe, response_d)
                response_flag = response_flag and (response_d.status_code == 200 or response_d.status_code == 201)

        if len(measures) > 0:
            for measure in measures:
                response_m = requests.put(measure_url,
                                         data=json.dumps(measure, cls=DatetimeSerializer),
                                         headers={'content-type': 'application/json'},
                                         timeout=client.timeout)
                log('debug', 'Finished Intellify measure request. Response = ' + response_m.text)
                package_response(client, measure, response_m)
                response_flag = response_flag and (response_m.status_code == 200 or response_m.status_code == 201)

        if len(defaults) > 0:
            response = requests.put(url,
                                 data=json.dumps(defaults, cls=DatetimeSerializer),
                                 headers={'content-type': 'application/json'},
                                 timeout=client.timeout)

            log('debug', 'Finished Intellify describe request. Response = ' + response.text)
            package_response(client, data, response)
            response_flag = response_flag and (response.status_code == 200 or response.status_code == 201)

        log('debug', 'Request - response_flag is ' + str(response_flag))

        return response_flag

    except requests.ConnectionError as e:
        package_exception(client, data, e)
    except requests.Timeout as e:
        package_exception(client, data, e)

    return False


class FlushThread(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        log('debug', 'Flushing thread running ...')

        self.client._sync_flush()

        log('debug', 'Flushing thread done.')


class Client(object):
    """The Client class is a batching asynchronous python wrapper over the
    Intellify API.

    """

    def __init__(self, secret=None, sensorId='_ERROR_NO_SENSORID_', host='', port='',
                 log_level=logging.INFO, log=True,
                 flush_at=20, flush_after=timedelta(0, 10),
                 async=True, max_queue_size=10000, stats=Statistics(),
                 timeout=10, send=True):
    
        """Create a new instance of a intellisense-python Client

        :param str secret: The Intellify API secret
        :param logging.LOG_LEVEL log_level: The logging log level for the
        client talks to. Use log_level=logging.DEBUG to troubleshoot
        : param bool log: False to turn off logging completely, True by default
        : param int flush_at: Specicies after how many messages the client will
        flush to the server. Use flush_at=1 to disable batching
        : param datetime.timedelta flush_after: Specifies after how much time
        of no flushing that the server will flush. Used in conjunction with
        the flush_at size policy
        : param bool async: True to have the client flush to the server on
        another thread, therefore not blocking code (this is the default).
        False to enable blocking and making the request on the calling thread.
        : param float timeout: Number of seconds before timing out request to
        Intellify
        : param bool send: True to send requests, False to not send. False to
        turn intellisense off (for testing).
        """

        self.secret = secret
        self.sensorId = sensorId
        self.host = host
        self.port = port

        self.queue = collections.deque()
        self.last_flushed = None

        if not log:
            # TODO: logging_enabled is assigned, but not used
            logging_enabled = False
            # effectively disables the logger
            logger.setLevel(logging.CRITICAL)
        else:
            logger.setLevel(log_level)

        self.async = async

        self.max_queue_size = max_queue_size
        self.max_flush_size = 50

        self.flush_at = flush_at
        self.flush_after = flush_after

        self.timeout = timeout

        self.stats = stats

        self.flush_lock = threading.Lock()
        self.flushing_thread = None

        self.send = send

        self.success_callbacks = []
        self.failure_callbacks = []

        self.current_time = lambda: int(round(time.time() * 1000))

    def set_log_level(self, level):
        """Sets the log level for intellisense-python

        :param logging.LOG_LEVEL level: The level at which intellisense-python log
        should talk at
        """
        logger.setLevel(level)

    def _check_for_secret(self):
        if not self.secret:
            raise Exception('Please set intellisense.secret before calling ' +
                            'identify or track.')

    def _coerce_unicode(self, cmplx):
        return unicode(cmplx)

    def _clean_list(self, l):
        return [self._clean(item) for item in l]

    def _clean_dict(self, d):
        data = {}
        for k, v in d.iteritems():
            try:
                data[k] = self._clean(v)
            except TypeError:
                log('warn', 'Dictionary values must be serializeable to ' +
                            'JSON "%s" value %s of type %s is unsupported.'
                            % (k, v, type(v)))
        return data

    def _clean(self, item):
        if isinstance(item, (str, unicode, int, long, float, bool,
                             numbers.Number, datetime)):
            return item
        elif isinstance(item, (set, list, tuple)):
            return self._clean_list(item)
        elif isinstance(item, dict):
            return self._clean_dict(item)
        else:
            return self._coerce_unicode(item)

    def on_success(self, callback):
        """
        Assign a callback to fire after a successful flush

        :param func callback: A callback that will be fired on a flush success
        """
        self.success_callbacks.append(callback)

    def on_failure(self, callback):
        """
        Assign a callback to fire after a failed flush

        :param func callback: A callback that will be fired on a failed flush
        """
        self.failure_callbacks.append(callback)

    def describe(self, entity_type=None, entity_id=None, properties={}, timestamp=None):

        log('debug', 'Client - describe')

        self._check_for_secret()

        if not entity_type:
            raise Exception('Must supply a entity_type.')

        if not entity_id:
            raise Exception('Must supply a entity_id.')

        if properties is not None and not isinstance(properties, dict):
            raise Exception('properties must be a dictionary.')

        if timestamp is None:
            timestamp = self.current_time()
        # elif not isinstance(timestamp, datetime):
        #     raise Exception('Timestamp must be a datetime object.')
        # else:
        #     timestamp = guess_timezone(timestamp)

        action = {'entityId':    entity_id,
                  'type':        entity_type,
                  'properties':  properties,
                  'timestamp':   timestamp,
                  'apiKey':      self.secret,
                  '__action':    'describe',
                  'il_sensorId': self.sensorId}

        if self._enqueue(action):
            self.stats.describes += 1

    def measure(self, action=None, learning_context={}, activity_context={}, timestamp=None):

        log('debug', 'Client - measure')

        self._check_for_secret()

        if not action:
            raise Exception('Must supply an action.')

        if learning_context is not None and not isinstance(learning_context, dict):
            raise Exception('learning_context must be a dictionary.')

        if activity_context is not None and not isinstance(activity_context, dict):
            raise Exception('activity_context must be a dictionary.')

        if timestamp is None:
            timestamp = self.current_time()
        # elif not isinstance(timestamp, datetime):
        #     raise Exception('Timestamp must be a datetime object.')
        # else:
        #     timestamp = guess_timezone(timestamp)

        action = {'action':           action,
                  'learningContext':  learning_context,
                  'activityContext':  activity_context,
                  'timestamp':        timestamp,
                  'apiKey':           self.secret,
                  '__action':         'measure',
                  'il_sensorId':      self.sensorId}

        if self._enqueue(action):
            self.stats.measures += 1


    def identify(self, user_id=None, traits={}, context={}, timestamp=None):
        """Identifying a user ties all of their actions to an id, and
        associates user traits to that id.

        :param str user_id: the user's id after they are logged in. It's the
        same id as which you would recognize a signed-in user in your system.

        : param dict traits: a dictionary with keys like subscriptionPlan or
        age. You only need to record a trait once, no need to send it again.
        Accepted value types are string, boolean, ints,, longs, and
        datetime.datetime.

        : param dict context: An optional dictionary with additional
        information thats related to the visit. Examples are userAgent, and IP
        address of the visitor.

        : param datetime.datetime timestamp: If this event happened in the
        past, the timestamp  can be used to designate when the identification
        happened.  Careful with this one,  if it just happened, leave it None.
        If you do choose to provide a timestamp, make sure it has a timezone.
        """

        self._check_for_secret()

        if not user_id:
            raise Exception('Must supply a user_id.')

        if traits is not None and not isinstance(traits, dict):
            raise Exception('Traits must be a dictionary.')

        if context is not None and not isinstance(context, dict):
            raise Exception('Context must be a dictionary.')

        if timestamp is None:
            timestamp = self.current_time()
        elif not isinstance(timestamp, datetime):
            raise Exception('Timestamp must be a datetime object.')
        else:
            timestamp = guess_timezone(timestamp)

        cleaned_traits = self._clean(traits)

        action = {'userId':      user_id,
                  'traits':      cleaned_traits,
                  'context':     context,
                  'timestamp':   timestamp,
                  '__action':      'identify'}

        context['library'] = 'intellisense-python'

        if self._enqueue(action):
            self.stats.identifies += 1

    def track(self, user_id=None, event=None, properties={}, context={},
              timestamp=None):
        """Whenever a user triggers an event, you'll want to track it.

        :param str user_id:  the user's id after they are logged in. It's the
        same id as which you would recognize a signed-in user in your system.

        :param str event: The event name you are tracking. It is recommended
        that it is in human readable form. For example, "Bought T-Shirt"
        or "Started an exercise"

        :param dict properties: A dictionary with items that describe the
        event in more detail. This argument is optional, but highly recommended
        - you'll find these properties extremely useful later. Accepted value
        types are string, boolean, ints, doubles, longs, and datetime.datetime.

        :param dict context: An optional dictionary with additional information
        thats related to the visit. Examples are userAgent, and IP address
        of the visitor.

        :param datetime.datetime timestamp: If this event happened in the past,
        the timestamp   can be used to designate when the identification
        happened.  Careful with this one,  if it just happened, leave it None.
        If you do choose to provide a timestamp, make sure it has a timezone.

        """

        self._check_for_secret()

        if not user_id:
            raise Exception('Must supply a user_id.')

        if not event:
            raise Exception('Event is a required argument as a non-empty ' +
                            'string.')

        if properties is not None and not isinstance(properties, dict):
            raise Exception('Context must be a dictionary.')

        if context is not None and not isinstance(context, dict):
            raise Exception('Context must be a dictionary.')

        if timestamp is None:
            timestamp = self.current_time()
        elif not isinstance(timestamp, datetime):
            raise Exception('Timestamp must be a datetime.datetime object.')
        else:
            timestamp = guess_timezone(timestamp)

        cleaned_properties = self._clean(properties)

        action = {'userId':       user_id,
                  'event':        event,
                  'context':      context,
                  'properties':   cleaned_properties,
                  'timestamp':    timestamp,
                  '__action':       'track'}

        context['library'] = 'intellisense-python'

        if self._enqueue(action):
            self.stats.tracks += 1

    def alias(self, from_id, to_id, context={}, timestamp=None):
        """Aliases an anonymous user into an identified user

        :param str from_id: the anonymous user's id before they are logged in

        :param str to_id: the identified user's id after they're logged in

        :param dict context: An optional dictionary with additional information
        thats related to the visit. Examples are userAgent, and IP address
        of the visitor.

        :param datetime.datetime timestamp: If this event happened in the past,
        the timestamp   can be used to designate when the identification
        happened.  Careful with this one,  if it just happened, leave it None.
        If you do choose to provide a timestamp, make sure it has a timezone.
        """

        self._check_for_secret()

        if not from_id:
            raise Exception('Must supply a from_id.')

        if not to_id:
            raise Exception('Must supply a to_id.')

        if context is not None and not isinstance(context, dict):
            raise Exception('Context must be a dictionary.')

        if timestamp is None:
            timestamp = self.current_time()
        elif not isinstance(timestamp, datetime):
            raise Exception('Timestamp must be a datetime.datetime object.')
        else:
            timestamp = guess_timezone(timestamp)

        action = {'from':         from_id,
                  'to':           to_id,
                  'context':      context,
                  'timestamp':    timestamp,
                  '__action':       'alias'}

        context['library'] = 'intellisense-python'

        if self._enqueue(action):
            self.stats.aliases += 1

    def _should_flush(self):
        """ Determine whether we should sync """

        full = len(self.queue) >= self.flush_at
        stale = self.last_flushed is None

        if not stale:
            stale = datetime.now() - self.last_flushed > self.flush_after

        return full or stale

    def _enqueue(self, action):

        # if we've disabled sending, just return False
        if not self.send:
            return False

        submitted = False

        if len(self.queue) < self.max_queue_size:
            self.queue.append(action)

            self.stats.submitted += 1

            submitted = True

            log('debug', 'Enqueued ' + action['__action'] + '.')

        else:
            log('warn', 'intellisense-python queue is full')

        if self._should_flush():
            self.flush()

        return submitted

    def _on_successful_flush(self, data, response):
        if 'batch' in data:
            for item in data['batch']:
                self.stats.successful += 1
                for callback in self.success_callbacks:
                    callback(data, response)
        else:
            log('debug', '*** dealing with data ' + json.dumps(data))
            if data['__action'] == 'describe' or data['__action'] == 'measure':
                self.stats.successful += 1
                for callback in self.success_callbacks:
                    callback(data, response)

    def _on_failed_flush(self, data, error):
        if 'batch' in data:
            for item in data['batch']:
                self.stats.failed += 1
                for callback in self.failure_callbacks:
                    callback(data, error)

    def _flush_thread_is_free(self):
        return self.flushing_thread is None \
            or not self.flushing_thread.is_alive()

    def flush(self, async=None):
        """ Forces a flush from the internal queue to the server

        :param bool async: True to block until all messages have been flushed
        """

        flushing = False

        # if the async arg is provided, it overrides the client's settings
        if async is None:
            async = self.async

        if async:
            # We should asynchronously flush on another thread
            with self.flush_lock:

                if self._flush_thread_is_free():

                    log('debug', 'Initiating asynchronous flush ..')

                    self.flushing_thread = FlushThread(self)
                    self.flushing_thread.start()

                    flushing = True

                else:
                    log('debug', 'The flushing thread is still active.')
        else:

            # Flushes on this thread
            log('debug', 'Initiating synchronous flush ..')
            self._sync_flush()
            flushing = True

        if flushing:
            self.last_flushed = datetime.now()
            self.stats.flushes += 1

        return flushing

    def _sync_flush(self):

        log('debug', 'Starting flush ..')

        successful = 0
        failed = 0

        url = options.host + options.endpoints['batch']

        while len(self.queue) > 0:

            batch = []
            for i in range(self.max_flush_size):
                if len(self.queue) == 0:
                    break

                batch.append(self.queue.pop())

            payload = {'batch': batch, 'secret': self.secret}

            if request(self, url, payload):
                successful += len(batch)
            else:
                failed += len(batch)

        log('debug', 'Successfully flushed {0} items [{1} failed].'.
                     format(str(successful), str(failed)))
