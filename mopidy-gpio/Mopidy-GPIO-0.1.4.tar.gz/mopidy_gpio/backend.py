from __future__ import unicode_literals
from mopidy import backend
import logging

import pykka
logger = logging.getLogger(__name__)

class GPIOBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(GPIOBackend, self).__init__()
        self.audio = audio

	def on_start(self):
        logger.info('Mopidy uses GPIO')
        logger.debug('Starting GPIO')
		
    def on_receive(self, message):
	    logger.info('GPIO: on_receive started')
        action = message['action']
        if action == 'set_volume':
            value = message['value']
            if value < 0:
                value = 0
            elif value > 100:
                value = 100
            self.audio.set_volume(value)
