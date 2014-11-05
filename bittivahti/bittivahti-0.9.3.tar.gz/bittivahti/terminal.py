import curses
import time
import signal
from datetime import datetime

from .bittivahti import Bittivahti

bitti = Bittivahti()


class TimedOutException(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimedOutException()

signal.signal(signal.SIGALRM, _timeout_handler)
IN_TIMEOUT = -1


def main(update_delay=3):
    try:
        curses.wrapper(loop, update_delay)
    except KeyboardInterrupt:
        pass



def loop(screen, update_delay):
    redraw(screen)
    #print('Please wait. The display is updated every {sleep:.0f} seconds.'
    #         .format(sleep=sleep))
    #print('Starting up...')

    # Main loop
    y, x = screen.getmaxyx()
    while True:
        try:
            signal.alarm(int(update_delay))
            in_char = screen.getch()  # Input
            signal.alarm(0)
        except TimedOutException:
            in_char = IN_TIMEOUT

        # Handle resize
        resized = curses.is_term_resized(y, x)
        if resized is True:
            y, x = screen.getmaxyx()
            screen.clear()
            curses.resizeterm(y, x)
            redraw(screen)

        if in_char in [ord(' '), IN_TIMEOUT]:
            redraw(screen)
        elif in_char is ord('q'):
            raise SystemExit()
        else:
            pass  # ignore

def redraw(screen):
    bitti.update_state()
    display_lines = bitti.format_data()
    screen.clear()
    #screen.immedok(True)
    screen.border(0)
    screen.refresh()
    title = "bittivahti 0.93 (press q to quit)"
    title_label = curses.newwin(1, len(title)+1, 0, 2)
    title_label.immedok(True)
    title_label.addstr(title)

    content_box = curses.newwin(20, 80, 2, 2)
    content_box.immedok(True)
    content_box.addstr("\n".join(display_lines))

    cur_time = "{now}".format(now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    time_box = curses.newwin(1, len(cur_time)+1, 0, 80-len(cur_time)+1)
    time_box.immedok(True)
    time_box.addstr(cur_time)
