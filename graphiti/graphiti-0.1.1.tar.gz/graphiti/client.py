import os
from logging import getLogger
from select import select
from struct import pack
from socket import error, socket, AF_INET, SOCK_STREAM, IPPROTO_TCP, TCP_NODELAY, SO_KEEPALIVE, SHUT_RDWR

if os.name != "nt":
    from socket import TCP_KEEPINTVL
from math import expm1, log1p, ceil
from time import time
from threading import Thread, RLock, Event

try:
    from cPickle import dumps, HIGHEST_PROTOCOL
except ImportError:
    from pickle import dumps, HIGHEST_PROTOCOL


def dot_path(*parts):
    return ".".join(map(str, parts))


def normalize_path(path):
    if isinstance(path, (list, tuple)):
        path = dot_path(*path)
    return path



class Client(object):

    MESSAGES_LIMIT_TO_SEND = 6000
    MAX_SEND_TIMEOUT = 60  # in seconds
    STATS_LOG_INTERVAL = 60
    FAILS_LOG_INTERVAL = 60

    @staticmethod
    def _make_socket(address, timeout=0.001):
        new_socket = socket(AF_INET, SOCK_STREAM)
        new_socket.setblocking(True)
        new_socket.settimeout(timeout)
        new_socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, True)
        if os.name != 'nt':
            new_socket.setsockopt(IPPROTO_TCP, SO_KEEPALIVE, True)
            new_socket.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 1)
        new_socket.connect(address)

        return new_socket

    @staticmethod
    def _close_socket(sock):
        if sock:
            sock.shutdown(SHUT_RDWR)
            sock.close()

    def __init__(self, host, port=2004, connection_timeout=1.0, send_timeout=1, worker_sleep=0.1, logger=None):
        """
        Async client for graphite/carbon.

        :param host: carbon host
        :param port: carbon pickle receiver port, by default 2004 is used
        :param connection_timeout: Connection timeout in seconds
        :param send_timeout: Interval between sending metrics to carbon
        :param worker_sleep: sleeping interval for worker thread which sends metrics
        :param logger: Logger object. By default the logging will be graphiti.client logger
        """
        self.messages = []
        self.messages_lock = RLock()
        self.last_sent = time()

        self.address = (host, port)
        self.connection_timeout = connection_timeout
        self.connection_pool = []
        self.send_timeout = send_timeout
        self.failed_send_attempts = 0
        self.next_time_to_log_fail = None
        self.max_failed_send_attempts = int(ceil(log1p(self.MAX_SEND_TIMEOUT)))
        self.stop_background_worker = Event()

        self.worker_sleep = worker_sleep
        self.logger = logger or getLogger("graphiti.client")
        self.background_worker = Thread(target=self._worker_loop, name="GraphitiSender")
        self.background_worker.daemon = True
        self.background_worker.start()

    def __del__(self):
        self.stop()

    def stop(self):
        self.flush(ignore_error=True)
        self.stop_background_worker.set()
        self.background_worker.join()
        for sock in self.connection_pool:
            self._close_socket(sock)
        self.connection_pool = []

    def send(self, path, value, timestamp=None):
        if timestamp is None:
            timestamp = time()
        path = normalize_path(path)
        if not isinstance(value, (int, long, float)):
            raise Exception("Invalid value for %s: %s (%s)" % (path, value, type(value)))
        with self.messages_lock:
            self.messages.append((path, (timestamp, value)))

    def batch(self, iterable):
        for item in iterable:
            self.send(*item)

    def flush(self, timeout=None, ignore_error=False):
        with self.messages_lock:
            if timeout is not None:
                timeout = abs(timeout)
                start_time = time()
                while time() - start_time < timeout and self.messages:
                    self._send()
            else:
                while self.messages:
                    success = self._send()
                    if not success and ignore_error:
                        break

    def _send(self):
        if not self.messages:
            return True

        with self.messages_lock:
            #noinspection PyBroadException
            try:
                messages = dumps(self.messages[:self.MESSAGES_LIMIT_TO_SEND], HIGHEST_PROTOCOL)
                self._send_message(pack("!L", len(messages)) + messages)
                self.messages = self.messages[self.MESSAGES_LIMIT_TO_SEND:]
                if self.failed_send_attempts:
                    self.logger.info("Connection to carbon is restored")
                self.failed_send_attempts = 0
                self.next_time_to_log_fail = None
            except Exception as exc:
                if not self.next_time_to_log_fail or time() >= self.next_time_to_log_fail:
                    if isinstance(exc, error):
                        self.logger.warning("Socket error during send to carbon", exc_info=True)
                    else:
                        self.logger.exception("Error during send to carbon: %s", exc)
                    self.next_time_to_log_fail = time() + self.FAILS_LOG_INTERVAL
                self.failed_send_attempts += 1
                return False
            return True

    def _worker_loop(self):
        next_log_time = time()
        while True:
            if self.stop_background_worker.wait(self.worker_sleep):
                return

            have_enough_messages = len(self.messages) >= self.MESSAGES_LIMIT_TO_SEND
            failed_attempts = min(self.max_failed_send_attempts, self.failed_send_attempts)
            it_is_a_time = (self.send_timeout + expm1(failed_attempts) + self.last_sent) > time()

            if time() >= next_log_time:
                self.logger.info("Sender status: %s messages in buffer, failed attempts: %d",
                                 len(self.messages), self.failed_send_attempts)
                next_log_time = time() + self.STATS_LOG_INTERVAL

            if have_enough_messages or it_is_a_time:
                self._send()
                self.last_sent = time()

    def _send_message(self, message):
        if self.connection_pool:
            _, writables, problems = select([], self.connection_pool, self.connection_pool, self.worker_sleep)
        else:
            writables = problems = []

        for problem in problems:
            self._close_socket(problem)

        self.connection_pool = writables
        socket_to_use = None
        try:
            if writables:
                socket_to_use = self.connection_pool.pop()
            else:
                socket_to_use = self._make_socket(self.address, self.connection_timeout)

            socket_to_use.sendall(message)
            # This looks as excess but actually it is the work around a bug in Gevent 1.0
            # Gevent easily puts data into socket even if it was closed before. SO_KEEPALIVE, low SO_SNDBUF
            # would not work but requesting of peername is ok, it raises an error with ERRNO 117, Transport
            # is not accessible. The question, why it cannot raise it on a socket_to_use.send.
            #
            # And this is crucial to invoke this method AFTER sending ALL the data because it checks a socket state
            # only after that.
            socket_to_use.getpeername()
        except error:
            self._close_socket(socket_to_use)
            raise

        self.connection_pool.append(socket_to_use)
