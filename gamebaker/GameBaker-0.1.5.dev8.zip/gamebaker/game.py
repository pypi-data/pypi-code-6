"""
Contains functions used in the ``game.py`` file of a project.
"""

import sys
from os.path import join
from operator import attrgetter

import pygame
from pygame.locals import *

from gamebaker import classes, constants


def get_events(blueprints):
    """
    Return all the events that have been defined in any ``Blueprint``.
    
    Events that haven't been defined will not be called to save time.
    ``blueprints`` should be the module containing the game's blueprints.
    """
    events = set()
    for variable in vars(blueprints).values():
        try:
            if issubclass(variable, blueprints.Blueprint) and variable != blueprints.Blueprint:
                print(variable)                
                for key, value in vars(variable).items():
                    if callable(value):
                        events.add(key)
        except TypeError:
            continue
    
    return events & classes.events

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
        
def key_method_args(key):
    """
    Return the method name used by blueprints to refer to a Pygame key event, and possibly arguments to be passed to a relevant Blueprint instance's event.
    """
    if key in constants.key_constants1:
        return (constants.key_constants1[key],)
    else:
        for group in constants.key_constants2:
            if key in group:
                method_name = constants.key_constants2[group]
                if method_name == "key_letter":
                    print((method_name, chr(key),))
                    return (method_name, chr(key),)
                elif method_name == "key_numberpad":
                    return (method_name, key-256,)       # pygame.K_KPx -> x
                elif method_name == "key_number":
                    return (method_name, key-48,)        # pygame.K_x -> x
                elif method_name == "key_function":
                    return (method_name, key-281,)       # pygame.K_Fx -> x
                else:
                    return (method_name,)
        else:
            return ("key_unknown",)
        
def main(events, views, objects, settings, blueprints):
    """
    Set up the game and run the game loop.
    """
    
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

    pygame.init()
    
    while True:
        key_press_events = set()
        key_release_events = set()
        key_held_events = set()
        mouse_events = set()
        
        blueprints.variables.mouse_x, blueprints.variables.mouse_y = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                method_name = key_method_args(event.key)[0]
                if method_name + "_release" in events:
                    key_release_events.add(method_name)
                    if event.key + "_held" in key_held_events:
                        key_held_events.discard(method_name)
            elif event.type == pygame.KEYDOWN:
                method_name = key_method_args(event.key)[0]
                if method_name + "_press" in events:
                    key_press_events.add(method_name)
                if method_name + "_held" in events:
                    key_held_events.add(method_name)
            
        # Call begin_tick event for all active instances
        active_instances = [i for i in objects if any(v.get_active(i) for v in views)]
        active_instances.sort(key=attrgetter("draw_depth"), reverse=True)
        draw_objects(active_instances, views, window)
        for instance in active_instances:
            instance.tick()
            for method in key_press_events:
                if len(method) == 1:
                    getattr(instance, method[0] + "_press")()
                else:
                    getattr(instance, method[0] + "_press")(method[1])
            for method in key_release_events:
                if len(method) == 1:
                    getattr(instance, method[0] + "_release")()
                else:
                    getattr(instance, method[0] + "_release")(method[1])
            for method in key_held_events:
                if len(method) == 1:
                    getattr(instance, method[0] + "_held")()
                else:
                    print(method)
                    getattr(instance, method[0] + "_held")(method[1])
            
        # set the caption
        if game_version.build_type != "r":    # r for release
            window_caption = "{} - {} - {} fps".format(game_name, game_version, game_clock.get_fps())
            pygame.display.set_caption(window_caption)
        
        pygame.display.flip()    
        
        game_clock.tick(game_speed)