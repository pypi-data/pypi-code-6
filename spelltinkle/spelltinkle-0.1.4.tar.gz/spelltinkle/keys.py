keynames = {
    '^a': 'home',
    '^c': 'copy',
    '^d': 'delete',
    '^e': 'end',
    '^f': 'replace',
    '^g': 'code_analysis',
    '^h': 'help',
    '^i': 'tab',
    '^k': 'delete_to_end_of_line',
    '^m': 'enter',
    '^n': ['end', 'enter'],
    '^o': 'open',
    '^p': 'paste',
    '^q': 'quit',
    '^r': 'search_backward',
    '^s': 'search_forward',
    '^u': 'undo',
    '^v': 'view_files',
    '^w': 'write',
    '^z': 'stop',
    '^ ': 'normalize_space',
    'F8': 'jedi',
    'F9': 'complete',
    'F10': 'format'}

doubles = {
    '^x': {'^g': 'game',
           '^k': 'delete_to_end_of_line_again',
           '^u': 'redo',
           '^w': 'write_as',
           '^n': ['home', 'enter', 'up', 'tab'],
           '+': 'upper',
           '-': 'lower'},
    '^b': {'^b': 'mark',
           '^i': 'rectangle_insert',
           '^d': 'rectangle_delete',
           '<': 'dedent',
           '>': 'indent'}}

again = {'delete_to_end_of_line'}

repeat = {'home', 'end'}

typos = {'imoprt': 'import'}

aliases = {'np': 'import numpy as np',
           'plt': 'import matplotlib.pyplot as plt',
           '__m': "if __name__ == '__main__':"}
