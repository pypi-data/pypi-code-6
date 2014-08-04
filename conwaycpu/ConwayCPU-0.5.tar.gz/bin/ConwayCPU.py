#!/usr/bin/env python
"""Conway's Game of Life, drawn to the terminal care of the Blessings lib

A board is represented like this::

    {(x, y): state,
     ...}

...where ``state`` is an int from 0..2 representing a color.

"""
from contextlib import nested
from itertools import chain
from random import randint
from sys import stdout
from sys import argv
from time import sleep, time

from blessings import Terminal
from psutil import cpu_percent
from random import random


def main():
    """Play Conway's Game of Life on the terminal."""
    def die((x, y)):
        """Pretend any out-of-bounds cell is dead."""
        if 0 <= x < width and 0 <= y < height:
            return x, y

    LOAD_FACTOR = 10  # Smaller means more crowded.
    NUDGING_LOAD_FACTOR = LOAD_FACTOR * 3  # Smaller means a bigger nudge.

    term = Terminal()
    width = term.width
    height = term.height
    board = random_board(width - 1, height - 1, LOAD_FACTOR)
    # detector = BoredomDetector()
    cells = cell_strings(term)
    if len(argv) > 1:
        cpu_cap = float(argv[1])
    else:
        cpu_cap = 1
    section_width = width/len(cpu_percent(interval=0.1, percpu=True)) + \
                    len(cpu_percent(interval=0.1, percpu=True))

    with nested(term.fullscreen(), term.hidden_cursor()):
        try:
            while True:
                frame_end = time() + 0.4
                board = next_board(board, section_width,
                    map(lambda X: get_agitation(X, cpu_cap), cpu_percent(interval=0.2, percpu=True)),
                    die)
                # board.update(agitate_board(board, 1 - cpu_percent(interval=0.2)/100))
                draw(board, term, cells)

                # If the pattern is stuck in a loop, give it a nudge:
                # if detector.is_bored_of(board):
                #     board.update(random_board(width - 1,
                #                               height - 1,
                #                               NUDGING_LOAD_FACTOR))
                

                stdout.flush()
                sleep_until(frame_end)
                clear(board, term, height)
        except KeyboardInterrupt:
            pass


def sleep_until(target_time):
    """If the given time (in secs) hasn't passed, sleep until it arrives."""
    now = time()
    if now < target_time:
        sleep(target_time - now)


def cell_strings(term):
    """Return the strings that represent each possible living cell state.

    Return the most colorful ones the terminal supports.

    """
    num_colors = term.number_of_colors
    if num_colors >= 16:
        funcs = term.on_bright_cyan, term.on_bright_cyan, term.on_bright_green, term.on_bright_yellow
    elif num_colors >= 8:
        funcs = term.on_cyan, term.on_cyan, term.on_green, term.on_yellow
    else:
        # For black and white, use the checkerboard cursor from the vt100
        # alternate charset:
        return (term.reverse(' '),
                term.smacs + term.reverse('a') + term.rmacs,
                term.smacs + 'a' + term.rmacs)
    # Wrap spaces in whatever pretty colors we chose:
    return [f(' ') for f in funcs]


def random_board(max_x, max_y, load_factor):
    """Return a random board with given max x and y coords."""
    return dict(((randint(0, max_x), randint(0, max_y)), 0) for _ in
                xrange(int(max_x * max_y / load_factor)))


# def agitate_board(board, factor):
#     # Consider only the neighbors of currently living cells
#     spawn_points = set(chain(*map(neighbors, board)))
#     agitated_board = {}
#     print factor**(factor*100)

#     for point in spawn_points:
#         should_spawn = (factor**(factor*50))/2
#         if should_spawn > random():
#             state = 3
#         else:
#             state = None

#         if state is not None:
#             agitated_board[point] = state

#     return agitated_board


def clear(board, term, height):
    """Clear the droppings of the given board."""
    for y in xrange(height):
        print term.move(y, 0) + term.clear_eol,


def draw(board, term, cells):
    """Draw a board to the terminal."""
    for (x, y), state in board.iteritems():
        with term.location(x, y):
            print cells[state],

def get_agitation(raw_cpu, cap):
    cpu_usage = raw_cpu/100
    capped_cpu = cpu_usage / cap
    if capped_cpu > 1:
        capped_cpu = 1
    # inverse_cpu = 1 - cpu_usage
    agitation = (capped_cpu/1.2)**7
    return agitation

def next_board(board, section_width, agitation_factors, wrap):
    """Given a board, return the board one interation later.

    Adapted from Jack Diedrich's implementation from his 2012 PyCon talk "Stop
    Writing Classes"

    :arg wrap: A callable which takes a point and transforms it, for example
        to wrap to the other edge of the screen. Return None to remove a point.

    """
    new_board = {}

    # We need consider only the points that are alive and their neighbors:
    points_to_recalc = set(board.iterkeys()) | set(chain(*map(neighbors, board)))

    for point in points_to_recalc:
        agitation_factor = agitation_factors[point[0]/section_width]
        count = sum((neigh in board) for neigh in
                    (wrap(n) for n in neighbors(point) if n))
        if point in board:
            if count == 2 or count == 3:
                state = 0 if board[point] < 2 else 2
            else:
                state = None
        else:
            if count == 3:
                state = 1
            elif (count == 2 or count == 4) and agitation_factor > random():
                state = 3
            else:
                state = None

        if state is not None:
            wrapped = wrap(point)
            if wrapped:
                new_board[wrapped] = state

    return new_board


def neighbors((x, y)):
    """Return the (possibly out of bounds) neighbors of a point."""
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1

# class BoredomDetector(object):
#     """Detector of when the simulation gets stuck in a loop"""

#     # Get bored after (at minimum) this many repetitions of a pattern:
#     REPETITIONS = 14

#     # We can detect cyclical patterns of up to this many iterations:
#     PATTERN_LENGTH = 4

#     def __init__(self):
#         # Make is_bored_of() init the state the first time through:
#         self.iteration = self.REPETITIONS * self.PATTERN_LENGTH + 1

#         self.num = self.times = 0

#     def is_bored_of(self, board):
#         """Return whether the simulation is probably in a loop.

#         This is a stochastic guess. Basically, it detects whether the
#         simulation has had the same number of cells a lot lately. May have
#         false positives (like if you just have a screen full of gliders) or
#         take awhile to catch on sometimes. I've even seen it totally miss the
#         boat once. But it's simple and fast.

#         """
#         self.iteration += 1
#         if len(board) == self.num:
#             self.times += 1
#         is_bored = self.times > self.REPETITIONS
#         if self.iteration > self.REPETITIONS * self.PATTERN_LENGTH or is_bored:
#             # A little randomness in case things divide evenly into each other:
#             self.iteration = randint(-2, 0)
#             self.num = len(board)
#             self.times = 0
#         return is_bored


if __name__ == '__main__':
    main()
