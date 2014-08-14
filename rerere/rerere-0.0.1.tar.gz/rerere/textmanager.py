# -*- coding: utf-8 -*-
import re


class TextManager:
    def __init__(self, dt):
        self.list = dt.split('\n')
        self.__i = -1
        self.ret = {}

    def move_index_to_same_line(self):
        self.__i -= 1

    def get_current_line(self):
        return self.list[self.__i]

    def get_line_number(self):
        return self.__i

    def set_line_number(self, i):
        self.__i = i

    def search(self, line, pattern):
        pattern = re.compile(pattern)
        return pattern.search(line)

    def execute(self, command_manager, start=0, end=-1):
        self.__i = start - 1
        try:
            commands = command_manager.next()
        except IndexError:
            return self.ret

        while True:
            try:
                self.__i += 1
                if end >= 0 and self.__i >= end:
                    break

                line = self.get_current_line()

                for mindex, command in enumerate(commands):
                    tmp = self.search(line, command.pattern)
                    if tmp:
                        if command.match(tmp):
                            commands = command_manager.next()
                            break
                    else:
                        if command.unmatch():
                            commands = command_manager.next()
                            break
            except IndexError:
                if commands:
                    tmp = False
                    for v in commands:
                        if v.remain():
                            tmp = True
                    if tmp:
                        try:
                            commands = command_manager.next()
                            continue
                        except IndexError:
                            return self.ret
                return self.ret
        return self.ret
