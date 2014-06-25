"""
DisplayText

Displays a big paragraph of text in terminal, no problems.
"""

import curses
import textwrap

class Display:
    def __init__(self, text, ok_button=None):
        try:
            self.stdscr = curses.initscr()

            self.cur_lines, self.cur_cols = self.stdscr.getmaxyx()
            self.scroll_pos = 0
            self.y_padding = 2  # 1 border char, 1 space
            self.x_padding = 2  # As above
            self.cols = self.cur_cols - self.x_padding
            self.rows = self.cur_lines - self.y_padding
            self.textlines = self.format(text)
            self.button = ok_button
            # Misc setup
            curses.noecho()
            curses.curs_set(0)


            # Create pad with width of term and height of formatted text
            self.pad = curses.newpad(len(self.textlines) + 4, self.cols + 4)

            # Fill pad with text
            for y_value, line in enumerate(self.textlines):
                self.pad.addstr(self.y_padding + y_value - 1, 
                                self.x_padding,
                                line)
        except:
            self.close()
            raise


    def format(self, text):
        paragraphs = []
        formatted_paras = []
        for paragraph in text.split("\n"):
            paragraphs.append(paragraph)

        for para in paragraphs:
            formatted = textwrap.fill(para, self.cols)
            formatted_paras.append(formatted)

        return formatted_paras


    def refresh(self):
        self.stdscr.refresh()
        self.pad.refresh(self.scroll_pos, 0,
                         1, 1,
                         self.rows - 3, self.cols)


    def scroll_up(self):
        if self.scroll_pos > 0:
            self.scroll_pos -= 1
            self.refresh()


    def scroll_down(self):
        if self.scroll_pos < len(self.textlines) - self.rows + 4:
            self.scroll_pos += 1
            self.refresh()


    def close(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()


    def show(self):
        try:
            self.stdscr.border(0)
            self.stdscr.keypad(True)
            if self.button:
                self.stdscr.addstr(self.rows - 1,
                                   (self.cols - len(self.button)) // 2,
                                   self.button,
                                   curses.A_REVERSE)
            while True:
                self.refresh()
                key = self.stdscr.getkey()
                # self.stdscr.addstr(0,0,str(ord(key)))
                if key == "KEY_UP":
                    self.scroll_up()
                elif key == "KEY_DOWN":
                    self.scroll_down()
                else:
                    try:
                        if ord(key) == 10:
                            self.close()
                            break
                    except TypeError:
                        pass
                self.stdscr.refresh()
        except KeyboardInterrupt:
            pass
        finally:
            self.close()

