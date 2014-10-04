import re

FRAME = re.compile(r'.* ([0-9]+)/ *([0-9]+) .*')
def parse_mplayer(stdout_line):
    match = re.match(FRAME, stdout_line)
    left = match.group(1)
    right = match.group(2)
    if left != right:
        raise ValueError('I don\'t know what to do with this line:\n"%s"' % stdout_line)
    else:
        return int(left)
