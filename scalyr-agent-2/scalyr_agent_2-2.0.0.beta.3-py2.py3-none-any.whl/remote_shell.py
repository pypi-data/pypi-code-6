# This code was based on a post at http://www.shysecurity.com/posts/Remote%20Interactive%20Python by
# kelson@shysecurity.com.
#
# This is used to enable remote interaction with the python process for remote debugging.  It should
# be used with extreme care since there is no security in the connection model right now.

import sys
import socket
import contextlib

import scalyr_agent.scalyr_logging as scalyr_logging

from scalyr_agent.util import StoppableThread

log = scalyr_logging.getLogger(__name__)

@contextlib.contextmanager
def std_redirector(stdin, stdout, stderr):
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = stdin, stdout, stderr
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds

class socketWrapper():
    def __init__(self, s): self.s = s
    def read(self, len):
        while True:
            try:
                return self.s.recv(len)
            except socket.timeout:
                continue
            except socket.error, e:
                if e.errno == 35:
                    continue
                raise e
    def write(self, str):  return self.s.send(str)
    def readline(self):
        data = ''
        while True:
            try:
                iota = self.read(1)
            except socket.timeout:
                continue
            if not iota: break
            else: data += iota
            if iota in '\n': break
        return data

def ishell(local=None, banner='interactive shell'):
    import code
    local = dict(globals(),**local) if local else globals()
    code.interact(banner,local=local)

def linkup(local,link,banner):
    import traceback
    link = socketWrapper(link)
    banner += '\nStack Trace\n'
    banner += '----------------------------------------\n'
    banner += ''.join(traceback.format_stack()[:-2])
    banner += '----------------------------------------\n'
    with std_redirector(link,link,link):
        ishell(local,banner)


class DebugServer(StoppableThread):
    def __init__(self, local=None, host='127.0.0.1', port=2000):
        self.__server_socket = None
        self.__connections = []
        self.__local = local
        self.__host = host
        self.__port = port
        StoppableThread.__init__(self, 'debug server thread')

    def run(self):
        while self._run_state.is_running():
            if self.__server_socket is None:
                self.__setup_server_socket()

            session = self.__accept_connection()
            if session is not None:
                self.__connections.append(session)
                session.start()

            # Clean up any connections that have been closed.
            if len(self.__connections) > 0:
                remaining_connections = []
                for connection in self.__connections:
                    if connection.isAlive():
                        remaining_connections.append(connection)
                    else:
                        connection.join(1)
                self.__connections = remaining_connections

    def __accept_connection(self):
        if self.__server_socket is None:
            return None

        try:
            client, addr = self.__server_socket.accept()
            return DebugConnection(self.__local, client, self.__host, self.__port)
        except socket.timeout:
            return None
        except Exception:
            log.exception('Failure while accepting new debug connection.  Resetting socket')
            self.__close_socket()
        return None

    def __setup_server_socket(self):
        if self.__server_socket is not None:
            return

        try:
            self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server_socket.settimeout(1)
            self.__server_socket.bind((self.__host, self.__port))
            self.__server_socket.listen(5)
        except Exception:
            log.exception('Failure while accepting new debug connection.  Resetting socket')
            self.__close_socket()

    def __close_socket(self):
        if self.__server_socket is not None:
            try:
                self.__server_socket.shutdown(socket.SHUT_RDWR)
                self.__server_socket = None
            except Exception:
                self.__server_socket = None


class DebugConnection(StoppableThread):
    def __init__(self, local, client_connection, host, port):
        self.__local = local
        self.__client_connection = client_connection
        self.__host = host
        self.__port = port
        StoppableThread.__init__(self, 'Debug connection thread')

    def run(self):
        linkup(self.__local, self.__client_connection,'connected to %s:%d' % (self.__host, self.__port))

def start_server(local=None, host='127.0.0.1', port=2000):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host,port))
        server.listen()
        while True:
            client,addr = server.accept()
            linkup(local,client,'connected to %s:%d'%(host,port))
            client.shutdown(socket.SHUT_RDWR)
        server.shutdown(socket.SHUT_RDWR)
    except Exception:
        log.exception('Remote debugging server failed')

def listen(local=None, host='127.0.0.1', port=2000):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host,port))
        server.listen(1)
        log.warn('Hi there 1')
        client,addr = server.accept()
        log.warn('Hi there 2')
        linkup(local,client,'connected to %s:%d'%(host,port))
        client.shutdown(socket.SHUT_RDWR)
        server.shutdown(socket.SHUT_RDWR)
    except:
        log.exception('Failed to listen')


def connect(local=None, host='127.0.0.1', port=2000):
    link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    link.connect((host,port))
    linkup(local,link,'connected to %s:%d'%(host,port))
    link.shutdown(socket.SHUT_RDWR)
