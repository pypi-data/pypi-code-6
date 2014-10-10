import sys
from inspect import isgeneratorfunction
import traceback
from abc import ABCMeta, abstractmethod
import asyncio
import pygame
from pygame.locals import *

__all__ = ['FrameManager']

EventLoop = asyncio.base_events.BaseEventLoop
Event = pygame.event.Event
Future = asyncio.Future
Surface = pygame.surface.Surface
Clock = pygame.time.Clock


#-----------------------------------------------------------------------
class FrameManager(metaclass=ABCMeta):

    DELAY = pow(2, -10)
    MSPF = 1000 / 60 # 60fps ~ 16.67ms / frame
    __screen = None


    #---------------------------------------------------------------
    # Override
    #

    @abstractmethod
    def build_screen(self) -> Surface:
        pass


    def load(self) -> None:
        pass


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))


    def handle_event(self, event:Event) -> None:
        pass


    def update(self, milliseconds:float) -> None:
        pass


    def quit(self) -> None:
        sys.exit()


    splash = None


    #---------------------------------------------------------------
    # API
    #

    @property
    def screen(self) -> Surface:
        if self.__screen is None:
            self.__screen = self.build_screen()
        return self.__screen


    def init(self) -> None:
        loop = self.loop = asyncio.get_event_loop()

        if self.splash:
            if isgeneratorfunction(self.splash) and isgeneratorfunction(self.load):
                pygame.init()
                loop.run_until_complete(
                    asyncio.wait([self.splash(), self.load()]),
                )

            elif isgeneratorfunction(self.splash):
                loop.run_until_complete(self.splash())
                pygame.init()
                self.load()

            elif isgeneratorfunction(self.load):
                self.splash()
                pygame.init()
                loop.run_until_complete(self.load())

            else:
                self.splash()
                pygame.init()
                self.load()

        else:
            pygame.init()
            self.screen

            if isgeneratorfunction(self.load):
                loop.run_until_complete(self.load())

            else:
                self.load()

        loop.call_soon(self._event_callback)
        loop.call_soon(self._update_callback, Clock())
        loop.call_soon(self._draw_callback, Clock())


    def start(self) -> None:
        loop = self.loop
        try:
            loop.run_forever()
        finally:
            loop.close()
            pygame.quit()


    def reset_screen(self, screen:Surface=None) -> None:
        self.__screen = screen


    @classmethod
    def main(cls):
        self = cls()
        self.init()
        self.start()


    #---------------------------------------------------------------
    # Internals
    #

    def _event_callback(self) -> None:
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            else:
                try:
                    self.handle_event(event)
                except (SystemExit, KeyboardInterrupt):
                    raise
                except:
                    traceback.print_exc()
        self.loop.call_later(self.DELAY, self._event_callback)


    def _update_callback(self, clock:Clock) -> None:
        try:
            self.update(milliseconds=clock.tick())

        except:
            traceback.print_exc()

        else:
            self.loop.call_later(self.DELAY, self._update_callback, clock)


    def _draw_callback(self, clock:Clock) -> None:
        clock.tick()
        try:
            self.draw()
            if self.screen.get_flags() & DOUBLEBUF:
                pygame.display.flip()
            else:
                pygame.display.update()

        except:
            traceback.print_exc()

        else:
            delay = self.MSPF - clock.tick()
            delay = 0 if delay <= 0 else delay
            self.loop.call_later(delay / 1000, self._draw_callback, clock)
