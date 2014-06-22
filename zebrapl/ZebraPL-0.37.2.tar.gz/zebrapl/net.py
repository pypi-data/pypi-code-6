import socket
from socket import error as SocketError
from zebrapl.doc import Document
        
class Printer:
    PRINTER_NOT_FOUND = 57
    
    def __init__(self, host, port=9100, timeout=2):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        self.host = host
        self.port = port
        
    def open(self):
        try:
            self.socket.connect((self.host, self.port))
        except Exception, ex:
            raise ConnectionError(ex.errno)
        
    def printdoc(self, doc, darkness=None):
        assert isinstance(doc, Document), AssertionError('Not a document')
        try:
            out = ''
            if not darkness is None:
                out += "~SD" + str(darkness)
            out += doc.tostring()
            self.socket.send(out)
        except SocketError as ex:
            raise ConnectionError(str(ex))
        
    def cancelall(self):
        self.socket.send('~JA')
        
    def close(self):
        try:
            self.socket.close()
        except:
            pass

class ConnectionError(socket.error):
    pass