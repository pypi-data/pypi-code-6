"""
Contains classes used by Game Baker.
"""

import os.path
from itertools import chain

import pygame
from pygame.locals import *

from gamebaker import constants

class Blueprint:
    """
    Parent class for developer-defined classes representing game objects.
    Classes inheriting from `Blueprint` should be stored in the `blueprints.py` file of a project.
    
    Class variables:
    
    sprite - a Sprite instance that instances of a Blueprint will be drawn as.
    
    bounding_box_width, bounding_box_height - integers giving the height of the bounding box
                                              of instances of a Blueprint in pixels.
    draw_depth (default value 0) - an integer giving the order instances of a Blueprint will be drawn in
                                   Instances with lower values will be drawn first (behind others).
    
    Example use::
    
        class MetalBlock(Blueprint):
            sprite = Sprite("metal_block.png")
            bounding_box_width = bounding_box_height = 32
        
            def key_up_press(self):
                self.yspeed -= 1
        
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

# events dictionary contains all the inbuilt events.
# used by `get_events` in `game.py`.
events = {"__init__", "tick", "destroy",}
        
def no_op(self):
    pass

for event in ("_press", "_release", "_held"):
    for method_name in chain(constants.key_constants1.values(), constants.key_constants2.values()):
        setattr(Blueprint, method_name + event, no_op)
        events.add(method_name + event)
        
class Sprite:
    """
    Represent an image used in the game.
    
    Example use::
    
        a_blueprint_sprite = Sprite(os.path.join("path", "to", "file"))
    """
    def __init__(self, path_to_file):
        self.image = pygame.image.load(os.path.join("images", path_to_file))
        self.path_to_file = path_to_file
        
    def __repr__(self):
        return "Sprite({})".format(path_to_file)

class View:
    """
    Represent an area of the game world, and its representation on screen.
    By default, only instances within a View (or the active border around one) are treated as existing.
    
    Example use::
    
        View(0, 0, 640, 480, 160, 0, 0)
    """
    def __init__(self, x, y, width, height, active_border, screen_x, screen_y):
        """
        x - initial x position of the View in the game world
        y - initial y game world position
        width - width of the View, both in the game world and on the screen, in pixels
        height - height of the View
        active_border - area around the View in which instances are treated as existing
        screen_x - initial x position of the View on screen
        screen_y - initial y onscreen position
        """
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
        """
        Returns if an instance is within the view.
        """
        return (self.left <= object.x <= self.right) and (self.top <= object.y <= self.bottom)

        
class Level:
    """
    Represent a single level or area within the game.
    
    Levels should be stored in `levels.py`, in a list assigned to `levels`.
    
    Example use::
    
        Level([Player(0, 0), Enemy(0, 0, "red")], [View(0, 0, 320, 320, 0, 0, 0)])
    """
    def __init__(self, objects, views):
        self.objects = objects
        self.views = views
        
class Version:
    """
    Record version numbers of games.

    Version mostly follows the format of the Python version numbers (see the general FAQ):
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
    """
    Store the game settings.
    
    Used in a project's `settings.py`.
    A Settings object should be assigned to the variable `settings` in that file.
    """
    def __init__(self, game_name="", game_version=Version(0, 0, 0, "dev", 0),
                       window_width=480, window_height=480,
                       game_speed=60):
        """
        game_name - the name of the game
        game_version - a Version object containing the current version
        window_width, window_height - the width and height of the game window
        game_speed - the maximum FPS (frames per second) rate
        """
        self.game_name = game_name
        self.game_version = game_version
        self.window_width = window_width
        self.window_height = window_height
        self.game_speed = game_speed