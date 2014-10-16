from base import BaseCommand
from tabulate import tabulate

class BoardCommand(BaseCommand):
    name = 'board'

    def __init__(self, client):
        super(BoardCommand, self).__init__(client)

    def help(self):
        print 'List of board subcommands'
        print '------------'
        print 'kanc board {project_id} - show board' 
        print ''
    
    def action(self, args):
        board_id = 1
        if len(args) > 0:
            board_id = int(args[0])

        board = self.client.get_board(board_id)

        header = []
        rows = []
        max_tasks = 0
        for col in board:
            header.append(col['title'])
            if max_tasks < len(col['tasks']):
                max_tasks = len(col['tasks'])
        for i in range(max_tasks):
            row = []
            for c in range(len(board)):
                if i < len(board[c]['tasks']):
                    t = board[c]['tasks'][i]
                    title ='{:>03}. {}'.format(t['id'], t['title'])
                    if len(title) > 30:
                        title = title[:27] + '...'
                    row.append(title)
                else:
                    row.append('')
            rows.append(row)

        print tabulate(rows, headers=header, tablefmt='orgtbl')

