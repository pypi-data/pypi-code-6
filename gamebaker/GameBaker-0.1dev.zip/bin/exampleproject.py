from os import makedirs

with open("levels.py", "w") as f:
    f.write("""from gamebaker.classes import Level, View
from blueprints import *

levels = [Level([Square() for _ in range(700)],
[View(0, 0, 720, 480, 160, 0, 0)])]""")

with open("blueprints.py", "w") as f:
    f.write("""from gamebaker.classes import Blueprint, Sprite
from random import randint

class Square(Blueprint):
    sprite = Sprite("square.png")
    def __init__(self):
        x = randint(20, 700)
        y = randint(20, 460)
        super().__init__(x, y)
        
    def tick(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)
        super().tick()
        
    def key_up_press(self):
        self.yspeed -= 1
        
    def key_down_press(self):
        self.yspeed += 1""")
    
with open("settings.py", "w") as f:
    f.write("""from gamebaker.classes import Settings, Version
settings = Settings(window_width=720, window_height=480)""")
    
with open("game.py", "w") as f:
    f.write("""from gamebaker import game
import blueprints
from settings import settings
from levels import levels

views, objects = game.load_level(levels, 0)
events = game.get_events(blueprints)
game.main(events, views, objects, settings)
""")
    
makedirs("images")