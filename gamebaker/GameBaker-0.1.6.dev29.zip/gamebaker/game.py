"""
Contains functions used in the ``game.py`` file of a project.
"""

import sys
from os.path import join
from operator import attrgetter
from time import time

import pygame
from pygame.locals import *

from gamebaker import classes, constants


def get_events(blueprints):
    """
    Return a set of all the events that have been defined in any ``Blueprint``, and a set of all the doubletap events.
    
    Events that haven't been defined will not be called to save time.
    ``blueprints`` should be the module containing the game's blueprints.
    """
    events = set()
    for variable in vars(blueprints).values():
        try:
            if issubclass(variable, blueprints.Blueprint) and variable != blueprints.Blueprint:              
                for key, value in vars(variable).items():
                    if callable(value):
                        events.add(key)
        except TypeError:
            continue
    return (events & classes.events, events & classes.doubletap_events)

def load_level(level_list, number):
    """
    Load a level given a list of ``Level`` objects and an index, and return a tuple of the views and objects of that level.
    """
    views = list(level_list[number].views)
    objects = list(level_list[number].objects)
    objects.sort(key=attrgetter("draw_depth"), reverse=True)
    return (views, objects)
    
def draw_objects(objects, views, window):
    """
    Draw objects to views, and those views to a window.
    """
    window.fill((0, 0, 0))
    for v in views:
        v.surface.fill((0, 0, 0))
        for a in objects:
            v.surface.blit(a.sprite.image, (a.x - v.x, a.y - v.y))
        window.blit(v.surface, (v.screen_x, v.screen_y))
        
        
class EventContainer:
    """
    Represent an event and data pertaining to it.
    """
    def _attrs(self):
        """
        Returns a tuple containing the attributes of an instance used for hashing and equality checking.
        Should be overridden by subclasses.
        """
        return ()
    
    def __eq__(self, other):
        return type(self) == type(other) and all(a == b for a, b in zip(self._attrs(), other._attrs()))

    def __hash__(self):
        return hash(self._attrs())

class KeyEventWithoutData(EventContainer):
    def __init__(self, name):
        self.name = name
        
    def _attrs(self):
        return (self.name,)
        
    def __repr__(self):
        return "KeyEventWithoutData({})".format(repr(self.name))
    
class KeyEventWithData(EventContainer):
    def __init__(self, name, data):
        self.name = name
        self.data = data
        
    def _attrs(self):
        return (self.name, self.data)
        
    def __repr__(self):
        return "KeyEventAndData({}, {})".format(repr(self.name), repr(self.data))
        
class DoubleTapEvent(EventContainer):
    def __init__(self, key_event, time):
        self.key_event = key_event
        self.time = time

    def _attrs(self):
        return (self.key_event, self.time)
        
    def __repr__(self):
        return "DoubleTapEvent({}, {})".format(repr(self.key_event), repr(self.time))
        
def key_method_args(key):
    """
    Return the method name used by blueprints to refer to a Pygame key event, and possibly arguments to be passed to a relevant Blueprint instance's event.
    """
    if key in constants.key_constants1:
        return KeyEventWithoutData(constants.key_constants1[key])
    else:
        for group in constants.key_constants2:
            if key in group:
                method_name = constants.key_constants2[group]
                if method_name == "key_letter":
                    return KeyEventWithData(method_name, chr(key))
                elif method_name == "key_numberpad":
                    return KeyEventWithData(method_name, key-256)       # pygame.K_KPx -> x
                elif method_name == "key_number":
                    return KeyEventWithData(method_name, key-48)        # pygame.K_x -> x
                elif method_name == "key_function":
                    return KeyEventWithData(method_name, key-281)       # pygame.K_Fx -> x
                else:
                    return KeyEventWithoutData(method_name)
        else:
            return KeyEventWithData("key_unknown")

def call_key_method(instance, method, suffix):
    """
    Calls a method on an instance.
    """
    if type(method) == KeyEventWithoutData:
        getattr(instance, method.name + suffix)()
    elif type(method) == KeyEventWithData:
        getattr(instance, method.name + suffix)(method.data)
            
def main(events, views, objects, settings, blueprints):
    """
    Set up the game and run the game loop.
    """
    pygame.init()
    
    events, doubletap_events = events
    
    game_name = settings.game_name
    game_version = settings.game_version
    window_caption = "{} - {}".format(game_name, game_version)
    window_width = settings.window_width
    window_height = settings.window_height
    game_speed = settings.game_speed

    # set up the window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_caption)

    # set up the clock
    game_clock = pygame.time.Clock()
    key_held_events = set()
    key_doubletap_possibles = set()
    
    while True:
        key_doubletap_events = set()
        key_press_events = set()
        key_release_events = set()
        
        mouse_events = set()
        
        blueprints.variables.mouse_x, blueprints.variables.mouse_y = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                method = key_method_args(event.key)
                if method.name + "_release" in events:
                    key_release_events.add(method)
                key_held_events.discard(method)
            elif event.type == pygame.KEYDOWN:
                method = key_method_args(event.key)
                if method.name + "_press" in events:
                    key_press_events.add(method)
                if method.name + "_held" in events:
                    key_held_events.add(method)
                if method.name + "_doubletap" in doubletap_events:
                    t = time()
                    for e in key_doubletap_possibles:
                        if t - e.time <= 0.3:                # if it was less than 0.3 seconds ago
                            key_doubletap_events.add(e.key_event)
                            key_doubletap_possibles.discard(e)
                            break
                    else:
                        key_doubletap_possibles.add(DoubleTapEvent(method, time()))
        
        
        active_instances = [i for i in objects if any(v.get_active(i) for v in views)]
        active_instances.sort(key=attrgetter("draw_depth"), reverse=True)
        draw_objects(active_instances, views, window)
        for instance in active_instances:
            instance.tick()
            for method in key_press_events:
                call_key_method(instance, method, "_press")
            for method in key_release_events:
                call_key_method(instance, method, "_release")
            for method in key_held_events:
                call_key_method(instance, method, "_held")
            for method in key_doubletap_events:
                call_key_method(instance, method, "_doubletap")
                
            for second_instance in active_instances:
                if Blueprint.check_collision(instance, second_instance):
                    instance.collide(second_instance)
            
        # set the caption
        if game_version.build_type != "r":    # r for release
            window_caption = "{} - {} - {} fps".format(game_name, game_version, game_clock.get_fps())
            pygame.display.set_caption(window_caption)
        
        pygame.display.flip()    
        
        game_clock.tick(game_speed)