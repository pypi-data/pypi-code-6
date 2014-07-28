import logging
logger = logging.getLogger('gsmtpd')
from server import DebuggingServer

class Server(DebuggingServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        logger.debug(peer)
        

ss = Server(('0.0.0.0', 25000))
ss.serve_forever()
