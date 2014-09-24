"""
Layout representation.
"""
from __future__ import unicode_literals

from pygments.token import Token
from ..renderer import Screen, Size, Point, Char

from .menus import PopupCompletionMenu
from .prompt import DefaultPrompt
from .margins import LeftMargin

__all__ = (
    'Layout',
)


class Layout(object):
    """
    Default prompt class.
    """
    #: Menu class for autocompletions. This can be `None`
    completion_menu = PopupCompletionMenu()

    #: What to show before the actual input.
    before_input = DefaultPrompt()
    after_input = None

    left_margin = LeftMargin()
    left_margin_width = 2

    top_toolbars = []
    bottom_toolbars = []

    #: Processors for transforming the tokens received from the `Code` object.
    #: (This can be used for displaying password input as '*' or for
    #: highlighting mismatches of brackets in case of Python input.)
    input_processors = []  # XXX: rename to something else !!!!!

    def __init__(self, cli_ref):
        self._cli_ref = cli_ref
        self.reset()

    def reset(self):
        #: Vertical scrolling position of the main content.
        self.vertical_scroll = 0

    @property
    def cli(self):
        """
        The :class:`CommandLineInterface` instance.
        """
        return self._cli_ref()

    @property
    def line(self):
        """
        The main :class:`Line` instance.
        """
        return self.cli.line

    def get_input_tokens(self):
        tokens = list(self.line.create_code().get_tokens())

        for p in self.input_processors:
            tokens = p.process_tokens(tokens)

        return tokens

    def get_highlighted_characters(self):
        """
        Return a dictionary that maps the index of input string characters to
        their Token in case of highlighting.
        """
        highlighted_characters = {}

        # In case of incremental search, highlight all matches.
        if self.line.isearch_state:
            for index in self.line.document.find_all(self.line.isearch_state.isearch_text):
                if index == self.line.cursor_position:
                    token = Token.IncrementalSearchMatch.Current
                else:
                    token = Token.IncrementalSearchMatch

                highlighted_characters.update({
                    x: token for x in range(index, index + len(self.line.isearch_state.isearch_text))
                })

        # In case of selection, highlight all matches.
        selection_range = self.line.document.selection_range()
        if selection_range:
            from_, to = selection_range

            for i in range(from_, to):
                highlighted_characters[i] = Token.SelectedText

        return highlighted_characters

    def _write_input(self, screen, highlight=True):
        # Get tokens
        # Note: we add the space character at the end, because that's where
        #       the cursor can also be.
        input_tokens = self.get_input_tokens() + [(Token, ' ')]

        # 'Explode' tokens in characters.
        input_tokens = [(token, c) for token, text in input_tokens for c in text]

        # Apply highlighting.
        if highlight:
            highlighted_characters = self.get_highlighted_characters()

            for index, token in highlighted_characters.items():
                input_tokens[index] = (token, input_tokens[index][1])

        for index, (token, c) in enumerate(input_tokens):
            # Insert char.
            screen.write_char(c, token,
                              string_index=index,
                              set_cursor_position=(index == self.line.cursor_position))

    def write_input_scrolled(self, screen, write_content, accept_or_abort=False,
                             min_height=1, top_margin=0, bottom_margin=0):
        """
        Write visible part of the input to the screen. (Scroll if the input is
        too large.)

        :return: Cursor row position after the scroll region.
        """
        # Make sure that `min_height` is in the 0..max_height interval.
        min_height = min(min_height, screen.size.rows)
        min_height = max(0, min_height)
        min_height -= (top_margin+ bottom_margin)

        left_margin_width = self.left_margin.width
        # Write to a temp screen first. (Later, we will copy the visible region
        # of this screen to the real screen.)
        temp_screen = Screen(Size(columns=screen.size.columns - left_margin_width,
                                  rows=screen.size.rows))
        write_content(temp_screen)

        # Determine the maximum height.
        max_height = screen.size.rows - bottom_margin - top_margin

        # Scroll.
        if True:
            # Scroll back if we scrolled to much and there's still space at the top.
            if self.vertical_scroll > temp_screen.current_height - max_height:
                self.vertical_scroll = max(0, temp_screen.current_height - max_height)

            # Scroll up if cursor is before visible part.
            if self.vertical_scroll > temp_screen.cursor_position.y:
                self.vertical_scroll = temp_screen.cursor_position.y

            # Scroll down if cursor is after visible part.
            if self.vertical_scroll <= temp_screen.cursor_position.y - max_height:
                self.vertical_scroll = (temp_screen.cursor_position.y + 1) - max_height

            # Scroll down if we need space for the menu.
            if self.need_to_show_completion_menu():
                menu_size = self.completion_menu.get_height(self.line.complete_state)
                if temp_screen.cursor_position.y - self.vertical_scroll >= max_height - menu_size:
                    self.vertical_scroll = (temp_screen.cursor_position.y + 1) - (max_height - menu_size)

        # Now copy the region we need to the real screen.
        y = 0
        for y in range(0, min(max_height, temp_screen.current_height - self.vertical_scroll)):
            # Write line numbers. (XXX: not correct in case of line wraps!!!)
            screen._y = y + top_margin
            screen._x = 0
            self.left_margin.write(self.cli, screen, y + self.vertical_scroll)

            # Write line content.
            for x in range(0, temp_screen.size.columns):
                screen._buffer[y + top_margin][x + left_margin_width] = temp_screen._buffer[y + self.vertical_scroll][x]

        screen.cursor_position = Point(y=temp_screen.cursor_position.y - self.vertical_scroll + top_margin,
                                       x=temp_screen.cursor_position.x + left_margin_width)

        y_after_input = y + top_margin

        # Show completion menu.
        if not accept_or_abort and self.need_to_show_completion_menu():
            y, x = temp_screen._cursor_mappings[self.line.complete_state.original_document.cursor_position]
            self.completion_menu.write(screen, (y - self.vertical_scroll + top_margin, x + left_margin_width), self.line.complete_state)

        return_value = max([min_height + top_margin, screen.current_height])

        # Fill up with tildes.
        if not accept_or_abort:
            y = y_after_input + 1
            max_ = max([min_height, screen.current_height]) + top_margin
            while y < max_:
                screen.write_at_pos(y, 1, Char('~', Token.Layout.Tilde))
                y += 1

        return return_value

    def need_to_show_completion_menu(self):
        return self.completion_menu and self.line.complete_state

    def write_to_screen(self, screen, min_available_height, accept=False, abort=False):
        """
        Render the prompt to a `Screen` instance.

        :param screen: The :class:`Screen` class into which we write the output.
        :param min_available_height: The space (amount of rows) available from
                                     the top of the prompt, until the bottom of
                                     the terminal. We don't have to use them,
                                     but we can.
        """
        # Filter on visible toolbars.
        top_toolbars = [b for b in self.top_toolbars if b.is_visible(self.cli, screen)]
        bottom_toolbars = [b for b in self.bottom_toolbars if b.is_visible(self.cli, screen)]

        # Write top toolbars.
        for i, t in enumerate(top_toolbars):
            screen._y, screen._x = i, 0
            t.write(self.cli, screen)

        # Write actual content.
        def write_content(scr):
            if self.before_input is not None:
                self.before_input.write(self.cli, scr)

            self._write_input(scr, highlight=not (accept or abort))

            if self.after_input is not None:
                self.after_input.write(self.cli, scr)

        y = self.write_input_scrolled(screen,
                                      write_content,
                                      accept_or_abort=(accept or abort),
                                      min_height=min_available_height,
                                      top_margin=len(top_toolbars),
                                      bottom_margin=len(bottom_toolbars))

        # Write bottom toolbars.
        for i, t in enumerate(bottom_toolbars):
            screen._y, screen._x = y + i, 0
            t.write(self.cli, screen)
