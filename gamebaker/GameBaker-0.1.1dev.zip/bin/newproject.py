from os import makedirs

with open("levels.py", "w") as f:
    f.write("""from gamebaker.classes import Level, View
from blueprints import *

levels = [Level([], [View(0, 0, 640, 480, 160, 0, 0)])]""")

with open("blueprints.py", "w") as f:
    f.write("""from gamebaker.classes import Blueprint, Sprite""")
    
with open("settings.py", "w") as f:
    f.write("""from gamebaker.classes import Settings, Version
settings = Settings()""")
    
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