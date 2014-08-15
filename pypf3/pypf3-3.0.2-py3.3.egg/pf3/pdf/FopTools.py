import logging
import traceback
import subprocess

COMMASPACE = ', '

class FopTools():

    fop_exec = None
    fop_config = None
    noosh_monitor = None

    def __init__(self,fop_exec, fop_config):
        self.logger = logging.getLogger('pf3')
        self.fop_exec = fop_exec
        self.fop_config = fop_config

