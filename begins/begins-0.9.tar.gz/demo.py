import begin
import logging

@begin.start(auto_convert=True)
@begin.logging
def run(host='127.0.0.1', port=8080, noop=False):
    if noop:
        return
    logging.debug("%s:%d", host, port)
