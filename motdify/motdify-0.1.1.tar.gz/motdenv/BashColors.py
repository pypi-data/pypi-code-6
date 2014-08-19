
class BashColors:
    """ Returns some color variables for bash """

    def getVariableTuple(self):

        return [
            ('BASH_BLACK', '\e[0;30m'),
            ('BASH_RED', '\e[0;31m'),
            ('BASH_GREEN', '\e[0;32m'),
            ('BASH_YELLOW', '\e[0;33m'),
            ('BASH_BLUE', '\e[0;34m'),
            ('BASH_PURPLE', '\e[0;35m'),
            ('BASH_CYAN', '\e[0;36m'),
            ('BASH_WHITE', '\e[0;37m'),
            ('BASH_NOCOLOR', '\e[0m')
        ]