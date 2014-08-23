import random
import os

import pyfiglet
import colorama as c

ITEMS = [
    'Boneless Pork Tenderloin',
    'Boneless Top Round Roast',
    'Split Chicken Breast',
    'Tilapia Fillets',
    'Krakus Polish Ham',
    'Chicken Salad With Fruit',
    'Personal Size Watermelon',
    'Golden Ripe Pineapples',
    'Juicy Cantalopes',
    'Kraft Salad Dressing',
    'Langers Cranberry 100% Juice', # Plus
    'Pasta Sale Elbows Farfalle',
    'Tri Color Primavera',
    'Viva Paper Towels',
    'OREO Cookies',
    'Split Top White Bread',
    'Minute Maid Drinks',
    'Lindy\'s Italian Ice',
    'Blueberry Pie',
    '4% Off Your Purchase',
]

COLORS = [
    c.Fore.CYAN,
    c.Fore.YELLOW,
    c.Fore.MAGENTA,
    c.Fore.WHITE,
]

def item():
    if random.randint(0,7) > 0:
        item_string = random.choice(ITEMS)
        split = item_string.split()
    else:
        split = ['pirateship', '< 3', 'Market', 'Basket']
    if len(split) == 2:
        word = [split[0], split[0], split[1], split[1]]
        colors = [COLORS[0], COLORS[0], COLORS[1], COLORS[1]]
    elif len(split) == 3:
        word = split + [split[2]]
        colors = [COLORS[0], COLORS[1], COLORS[2], COLORS[2]]
    elif len(split) == 4:
        word = split
        colors = COLORS
    else:
        return None
    return zip(colors, word)

def main():
    f = pyfiglet.Figlet()

    words = None
    prevwords = None
    try:
        os.system("clear") 
        print('Press enter to advance the pretty words.')
        while True:
            prevwords = words
            words = item()
            if words == None or prevwords == words:
                continue
            f.setFont(font = random.choice(f.getFonts()))
            for color, word in words:
                _ = input()
                os.system("clear") 
                print(6 * '\n')
                print(color + f.renderText(word))
    except KeyboardInterrupt:
        pass
