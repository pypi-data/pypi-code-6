#!python3
def write_files(levels, blueprints, settings, game):
    """
    Write the the text in each argument to the relevant file.
    
    Used when creating projects
    """
    from os import makedirs

    with open("levels.py", "w") as f:
        f.write(levels)

    with open("blueprints.py", "w") as f:
        f.write(blueprints)
        
    with open("settings.py", "w") as f:
        f.write(settings)
        
    with open("game.py", "w") as f:
        f.write(game)
        
    makedirs("images")

if __name__ == "__main__":
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""
                                     A collection of scripts to do with GameBaker.
                                     """,
                                     epilog=textwrap.dedent("""
                                     Commands:
                                         newproject        create a new GameBaker project in the current directory
                                         exampleproject    create an example GameBaker project in the current directory
                                     """)
                                    )
    parser.add_argument("command", help="the command to run")
    args = parser.parse_args()
    command = args.command
    
    if command == "newproject":
        write_files("""from gamebaker.classes import Level, View
    from blueprints import *
    
    levels = [Level([], [View(0, 0, 640, 480, 160, 0, 0)])]""",
    """from gamebaker.classes import Blueprint, Sprite""",
    """from gamebaker.classes import Settings, Version
    settings = Settings(game_name="", game_version=Version(0, 0, 0, "dev", 0),
                        window_width=480, window_height=480,
                        game_speed=60)""",
    """from gamebaker import game
    import blueprints
    from settings import settings
    from levels import levels
    
    views, objects = game.load_level(levels, 0)
    events = game.get_events(blueprints)
    game.main(events, views, objects, settings, blueprints)""")
    elif command == "exampleproject":
        write_files("""from gamebaker.classes import Level, View
    from blueprints import *
    
    levels = [Level([Square() for _ in range(700)],
    [View(0, 0, 720, 480, 160, 0, 0)])]""",
    """from gamebaker.classes import Blueprint, Sprite
    from random import randint
    
    class Square(Blueprint):
        sprite = Sprite("red_square.png")
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
            self.yspeed += 1""",
    """from gamebaker.classes import Settings
    settings = Settings(game_name="Example game", window_width=720, window_height=480)""",
    """from gamebaker import game
    import blueprints
    from settings import settings
    from levels import levels
    
    views, objects = game.load_level(levels, 0)
    events = game.get_events(blueprints)
    game.main(events, views, objects, settings, blueprints)
    """)
        try:
            os.makedirs("images")
        except Exception:
            pass
        import os
        red_square_image = os.path.join(os.path.dirname(os.path.realpath(__file__)), "red_square.png")
        from shutil import copyfile
        copyfile(red_square_image, os.path.join(os.getcwd(), "images", "red_square.png"))
        
    else:
        print("Unknown command!")
    print("Done!")
