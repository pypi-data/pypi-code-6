from __future__ import unicode_literals

import logging
import pykka

from mopidy import backend
from .manager import GPIOManager

logger = logging.getLogger(__name__)

class GPIOBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(GPIOBackend, self).__init__()
        self.audio = audio
        self.manager = GPIOManager(self, config)
		
    def on_start(self):
        logger.info('Mopidy uses GPIO')
		
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

    def mute(self):
        logger.info('GPIO: mute started')
        #self.audio.set_mute(True)
        self.audio.prepare_change()
        self.audio.set_uri("http://somafm.com/groovesalad.pls")
        self.audio.start_playback()