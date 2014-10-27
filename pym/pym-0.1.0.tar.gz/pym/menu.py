"""Console based paged menu module

Author: Mike Bond <mikeb@hitachi-id.com>
Python version: Python 3.x

Requires colorama, ansicolors, and readline.

"""
import os
import sys
import re
import __main__ as main
import readline
from colorama import init, Style
import colors


class Menu():
    """The class for console based menu paging."""

    def __init__(self, title, default, choices):
        """Initialize the menu for console paging. 

        :param str title: The menu title
        :param default: The key value for the default option
        :param dict choices: A dictionary of choices

        """

        self.title = title
        self.default = default
        self.choices = choices
        self.menu_choices = sorted(list(choices.keys()))

        # default configuration
        self.prompt = 'Your choice => '
        self.term_size = os.get_terminal_size()
        self.column_width = self.term_size.columns

        # determine the history filename
        if hasattr(main, '__file__'):
            self.hist_filename = '.history_{}'.format(
                os.path.basename(main.__file__)
            )

        # initialize the default choice
        if self.default and self.choices.get(self.default):
            self._style_default()

        # find the longest choice
        self._find_longest()

        # initialize colorama
        init(autoreset=True)

        # initialize readline support
        if os.path.exists(self.hist_filename):
            readline.read_history_file(self.hist_filename)
        readline.parse_and_bind('tab: complete')

    @staticmethod
    def _sanitize(description):
        """Sanitize the given description, removing ansi codes

        :param str description: The description

        """

        return re.sub('\033\[((?:\d|;)*)([a-zA-Z])', '', description)

    def _style_default(self):
        """Update the style of the default option"""

        # initialize the default choice
        self.choices[self.default] = '{}{}'.format(
            colors.white(self.choices[self.default], style='bold+underline'),
            Style.RESET_ALL
        )

    def _find_longest(self):
        """Find the longest choice"""

        longest = 0
        for choice, value in self.choices.items():
            if len(value) > longest:
                longest = len(value)
        self.column_width = longest + 9

    def choose(self):
        """Display the list of choices"""

        # display parameters
        columns = int(self.term_size.columns / self.column_width)
        if columns == 0:
            columns = 1

        title_lines = self.title is None and 0 or 1
        menu_lines = self.term_size.lines - title_lines - 2

        # remove line for default
        if self.default and self.choices.get(self.default):
            menu_lines -= 1

        start = 0
        match = False
        choice = None

        while not match:
            last = start
            line = 0

            # clear the screen and print the title
            print('{}{}{}'.format(
                os.linesep,
                '=' * self.term_size.columns,
                os.linesep
            ))
            if self.title:
                print(self.title)

            while line < menu_lines and line < len(self.menu_choices):
                output = ''
                # build the output string for multiple columns
                for column in range(0, columns):

                    counter = start + menu_lines * column + line

                    # check if choice exists
                    if counter >= len(self.menu_choices):
                        continue

                    if counter > last:
                        last = counter

                    # existing output string
                    description = self.choices.get(self.menu_choices[counter])

                    # generate the output choice padded to column width
                    next_choice = '{}. {}'.format(
                        str(counter - start + 1).rjust(2),
                        description
                    )
                    width = self.column_width - len(self._sanitize(next_choice))
                    output += '{}{}'.format(
                        next_choice,
                        ' ' * width
                    )

                line += 1
                print(output)

            last = last - start + 1

            # output default choice
            if self.default and self.choices.get(self.default):
                print('Default: {}'.format(self.choices.get(self.default)))

            print('----- <space>Next <->Prev <q>Quit <Q>Quit program -----')
            reply = input('({}-{} of {}) {}'.format(
                start + 1,
                last + start,
                len(self.menu_choices),
                self.prompt
            ))

            # quit the entire program and save history file
            if reply == 'Q':
                readline.write_history_file(self.hist_filename)
                print('Quitting program')
                sys.exit(0)
            elif reply == 'q':
                return None
            elif reply == ' ':
                start += menu_lines * columns
                if start >= len(self.menu_choices):
                    start = 0
            elif reply == '-':
                start -= menu_lines * columns
                if start < 0 and abs(start) <= len(self.menu_choices):
                    start = len(self.menu_choices) - abs(start)
                if start < 0:
                    start = 0
            elif reply == '':
                if self.default:
                    return self.default
            else:
                # check for numerical choice
                try:
                    int_choice = int(reply)
                    if int_choice <= len(self.menu_choices):
                        match = True
                        choice = self.menu_choices[start + int_choice - 1]
                except ValueError:
                    # filter choices and show filtered Menu
                    new_choices = {new_choice: self.choices.get(new_choice)
                                   for new_choice in self.menu_choices
                                   if reply in new_choice}

                    if len(new_choices) == 0:
                        print('No menu items match: {}'.format(reply))
                        input('Press <Enter> to continue...')
                        continue

                    new_pager = Menu(self.title, self.default, new_choices)
                    new_result = new_pager.choose()
                    if new_result:
                        match = True
                        choice = new_result

        return choice

if __name__ == '__main__':

    testing_data = {i: 'Testing {}'.format(i) for i in range(1, 1001)}
    pager = Menu('Make a choice:', 1, testing_data)
    result = pager.choose()

    print('Choice: {} = {}'.format(result, testing_data.get(result)))
