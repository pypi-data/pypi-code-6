from base import BaseCommand
from base import CommandError
from tabulate import tabulate
import os, fcntl, termios, struct, os

# http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def terminal_size():
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

class BoardCommand(BaseCommand):
    name = 'board'

    def __init__(self, client, rcfile):
        super(BoardCommand, self).__init__(client, rcfile)

    def help(self):
        print 'List of board subcommands'
        print '------------'
        print 'kanc board - show board of current project' 
        print ''
    
    def action(self, subcmd, args):
        board_id = self.rcfile.get('currentProject')
        board = self.client.get_board(board_id)

        header = []
        rows = []
        max_tasks = 0
        for col in board:
            header.append(col['title'])
            if max_tasks < len(col['tasks']):
                max_tasks = len(col['tasks'])
        
        tw, th = terminal_size()
        title_size = tw / len(header) - 4
        
        for i in range(max_tasks):
            row = []
            for c in range(len(board)):
                if i < len(board[c]['tasks']):
                    t = board[c]['tasks'][i]
                    title ='{:>03}. {}'.format(t['id'], t['title'])
                    if len(title) > title_size:
                        title = title[:title_size - 3] + '...'
                    row.append(title)
                else:
                    row.append('')
            rows.append(row)

        print tabulate(rows, headers=header, tablefmt='orgtbl')

