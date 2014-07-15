import re
from flake8_double_quotes import __version__

def check_quotes(logical_line):
    """ Raise lint error when using ' instead of " """
    # if there is no double quote sign
    # there's nothing to do
    if logical_line.find("'") == -1:
        return

    # if it's a comment logical_line ignore it
    if logical_line.strip().startswith('#'):
        return

    # ignore single quotes wrapped in double quotes
    doubles = re.match(r'"(.*)"', logical_line)
    if doubles and logical_line.find("'") != -1:
        return

    single_quotes = logical_line.find("'")
    if single_quotes:
        yield single_quotes + 1, 'Q000 Remove Single quotes'


check_quotes.name = name ='flake8-double-quotes'
check_quotes.version = __version__
