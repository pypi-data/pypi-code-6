from mopidy import backend
import logging

import pykka
logger = logging.getLogger(__name__)

class GPIOBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(GPIOBackend, self).__init__()
        self.audio = audio
        logger.debug('GPIO: Backend started')
		
    def on_receive(self, message):
        action = message['action']
        if action == 'set_volume':
            value = message['value']
            if value < 0:
                value = 0
            elif value > 100:
                value = 100
            self.audio.set_volume(value)
