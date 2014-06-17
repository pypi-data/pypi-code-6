import time

import click
import webcolors
from blink1.blink1 import Blink1


@click.command()
@click.option('--on_color', default='white', help='Color to flash on')
@click.option('--off_color', default='black', help='Color to flash off')
@click.option('--duration', default=1, help='Length of each flash cycle in seconds')
@click.option('--repeat', default=5, help='Number of times to flash')
@click.option('--fade', default=0.1, help='Fade time in seconds')
def flash(on_color, off_color, duration, repeat, fade):
    blink1 = Blink1()

    color_on_rgb = webcolors.name_to_rgb(on_color)
    color_off_rgb = webcolors.name_to_rgb(off_color)

    for i in range(0, repeat):
        blink1.fade_to_rgb(fade * 1000, *color_on_rgb)
        time.sleep(duration)
        blink1.fade_to_rgb(fade * 1000, *color_off_rgb)
        time.sleep(duration)

    blink1.fade_to_rgb(fade * 1000, 0, 0, 0)


if __name__ == '__main__':
    flash()