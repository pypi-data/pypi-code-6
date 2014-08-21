import os.path
from itertools import chain

import pygame
from pygame.locals import *

from gamebaker import constants

"""
A module various classes and functions for use in Game Baker:

Classes:

Sprite - a class for images
Sound - a class for sound effects to be played in the game - not yet implemented
Music - a class for music to be played in the game - not yet implemented
Blueprint - a class for game objects to inherit from
Background - a class for static background objects
Settings - a class to store the settings for a game
Version - a class to represent version numbers

"""

class Background:
    """
    Class variables:
    sprite - a Sprite instance that instances of the Background will be drawn as.
    draw_depth (default value 0) - an integer giving the order instances of a Background will be drawn as.
    Backgrounds are currently always drawn behind Blueprint instances.
    
    Use a Background for things that don't move or interact with the user.
    This saves time.
    """

class Blueprint:
    """
    Class variables:
    sprite - a Sprite instance that instances of a Blueprint will be drawn as.
    
    bounding_box_width, bounding_box_height - integers giving the height of the bounding box
                                              of instances of a Blueprint in pixels.
    draw_depth (default value 0) - an integer giving the order instances of a Blueprint will be drawn in
                 Lower values mean drawn first.
    
    Example:
    class MetalBlock(Blueprint):
        sprite = Sprite("metal_block.png")
        bounding_box_width = bounding_box_height = 32
        
    MetalBlock(2,7) # creates a MetalBlock instance and adds it to the list of objects
    # This function is all that needs to be called to add a new instances - fire and forget
    # The library will take care of drawing and updating
    """
    sprite = None
    bounding_box_width = None
    bounding_box_height = None
    draw_depth = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xspeed = 0
        self.yspeed = 0

    def tick(self):
        self.x += self.xspeed
        self.y += self.yspeed
        
    def destroy(self):
        pass

events = {"__init__", "tick", "destroy",}
        
def no_op(self):
    pass

for event in ("_press", "_release", "_held"):
    for method_name in chain(constants.key_constants1.values(), constants.key_constants2.values()):
        setattr(Blueprint, method_name + event, no_op)
        events.add(method_name + event)
        
class Controller(Blueprint):
    def __init__(self):
        pass
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
class Sprite:
    def __init__(self, path_to_file):
        self.image = pygame.image.load(os.path.join("images", path_to_file))
        self.path_to_file = path_to_file
        
    def __repr__(self):
        return "Sprite({})".format(path_to_file)
        

class View:
    """
    A view represents an area of the game world, and its representation on screen
    """
    def __init__(self, x, y, width, height, active_border, screen_x, screen_y):
        self.x = x
        self.y = y
        self.active_border = active_border
        self.width = width
        self.height = height
        self.left = x - active_border
        self.top = y - active_border
        self.right = x + width + active_border
        self.bottom = y + height + active_border
        self.screen_x = screen_x
        self.screen_y = screen_y
        
        self.surface = pygame.Surface((self.width, self.height))
        
    def get_active(self, object):
        return (self.left <= object.x <= self.right) and (self.top <= object.y <= self.bottom)

        
class Level:
    def __init__(self, objects, views):
        self.objects = objects
        self.views = views
        
class Version:
    """
    Version is a class for holding version numbers of games

    It mostly follows the format of the Python version numbers (see the general FAQ):
    major.minor.micro

    This is then followed by the build type, which should either be blank, for a release, or one of the following:
    dev(elopment), which precedes
    a(lpha), which precedes
    b(eta), which precedes
    (release) c(andidate), which precedes
    r(elease)

    If the build type is release, then str(version) doesn't show it or the build number.

    The build type suffix is then followed by the build number. This increases automatically each time the project is built.
    """
    def __init__(self, major, minor, micro, build_type=None, build_number=None):
        self.major = int(major)
        self.minor = int(minor)
        self.micro = int(micro)
        self.build_type = build_type if build_type in ("a", "b", "c", "r") else "dev"
        self.build_number = int(build_number) if build_number else 0

    def __str__(self):
        if self.build_type == "r":
            return "{}.{}.{}".format(self.major, self.minor, self.micro)
        else:
            return "{}.{}.{}{}{}".format(self.major, self.minor, self.micro,
                                     self.build_type if self.build_type else "",
                                     self.build_number if self.build_type else "")
        
class Settings:
    def __init__(self, game_name="", game_version=Version(0, 0, 0, "dev", 0),
                       window_width=480, window_height=480,
                       game_speed=60):
        self.game_name = game_name
        self.game_version = game_version
        self.window_width = window_width
        self.window_height = window_height
        self.game_speed = game_speed