import os
import time
import logging
import traceback
import socket
import RPi.GPIO as GPIO
import pykka

from mopidy import core

logger = logging.getLogger(__name__)

class GPIOFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(GPIOFrontend, self).__init__()
        self.core = core
		self.backend = pykka.ActorRegistry.get_by_class_name("GPIOBackend")[0]
		self.gpio_manager = GPIOManager(self, config['gpio'])
		logger.info('GPIO: Frontend started')

	def input(self, input_event):
	    logger.info('GPIO: Input Triggered')
        try:
            if input_event['key'] == 'volume_up':
                if input_event['long']:
                    self.repeat()
                else:
                    current = self.core.playback.volume.get()
                    current += 10
                    self.backend.tell({'action': 'set_volume', 'value': current})
            elif input_event['key'] == 'volume_down':
                if input_event['long']:
                    current = 0
                else:
                    current = self.core.playback.volume.get()
                    current -= 10
                self.backend.tell({'action': 'set_volume', 'value': current})
            elif input_event['key'] == 'main' and input_event['long'] and self.menu:
                self.exit_menu()
            else:
                if self.menu:
                    self.main_menu.input(input_event)
                else:
                    self.manage_input(input_event)

        except Exception:
            traceback.print_exc()
			
    def repeat(self):
        if self.menu:
            self.main_menu.repeat()
        else:
            self.speak_current_song(self.core.playback.current_tl_track.get())