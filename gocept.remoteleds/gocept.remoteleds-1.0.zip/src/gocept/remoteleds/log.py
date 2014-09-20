import logging

log = logging.getLogger('remoteleds')
ch = logging.StreamHandler()
log.setLevel(logging.INFO)
log.addHandler(ch)
