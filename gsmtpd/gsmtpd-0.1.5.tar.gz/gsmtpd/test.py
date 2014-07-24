from server import DebuggingServer
import logging

logging.basicConfig(level=logging.DEBUG)

ss = DebuggingServer(ssl=True, keyfile='/home/meng/Downloads/34nmssl/nopasswd_ssl_privatekey.key',
                    certfile='/home/meng/Downloads/34nmssl/34nm.pem')
ss.serve_forever()
