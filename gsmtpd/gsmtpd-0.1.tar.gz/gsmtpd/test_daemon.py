from server import DebuggingServer

ss = DebuggingServer(ssl=True, keyfile='/home/meng/34nmssl/nopasswd_ssl_privatekey.key',
                               certfile='34nm.pem')
ss.serve_forever()
