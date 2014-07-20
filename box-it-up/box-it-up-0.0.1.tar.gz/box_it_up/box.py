
# coding: utf8
import sys

# '''Python class for formatting various kinds of table data into an ascii table.'''

POS_NW = 0
POS_N = 1
POS_NE = 2
POS_W = 3
POS_E = 4
POS_SW = 5
POS_S = 6
POS_SE = 7

class Box(object):
    """
    Description:
    Each data cell is surrounded by 6 header chars, 3 footer chars and a left and right char
    Think of cardinal directions on a map

    H - header
    F - footer
    T - top
    B - bottom
    L - left
    M - middle
    R - right

    Example: HLT = HEADER LEFT TOP, etc.

    HLT   HMT   HRT
    HLB   HMB   HRB
          |
    L --- X --- R
          |
    FL    FM    FR

    Table Types (see: Examples/table_types.txt):
    MINIMAL          - asterisks underline column headers, no column dividers, no outline
    SIMPLE (Default) - single line header and column dividers, no outline
    SIMPLE_OUTLINE   - single line header, column dividers & outline
    OUTLINE          - single line header, column dividers & outline (extended ascii connectors)
    OUTLINE_DBL      - double line header, column dividers & outline (extended ascii connectors)

    Tables can be header=True or False


    @TODO:
    * Add a 0 column row counter flag
    * Add 'colspan' type capability
    """

    def __init__(self, header=True, type='OUTLINE'):

        self._box = ''
        self.header = header
        self.box_type = type

        self._types = {
            'MINIMAL': {
                'HLT': ' ', 'HMT': ' ', 'HRT': ' ',
                'HLB': ' ', 'HMB': ' ', 'HRB': ' ',
                'FL': ' ', 'FM': ' ', 'FR': ' ',
                'L': ' ', 'M': ' ', 'R': ' ',
                'HLINE': '*'
            },
            'SIMPLE': {
                'HLT': ' ', 'HMT': ' ', 'HRT': ' ',
                'HLB': '-', 'HMB': '-', 'HRB': '-',
                'FL': '-', 'FM': '-', 'FR': '-',
                'L': ' ', 'M': '|', 'R': ' ',
                'HLINE': '-'
            },
            'SIMPLE_OUTLINE': {
                'HLT': '.', 'HMT': '+', 'HRT': '.',
                'HLB': '+', 'HMB': '+', 'HRB': '+',
                'FL': '+', 'FM': '+', 'FR': '+',
                'L': '|', 'M': '|', 'R': '|',
                'HLINE': '-'
            },
            'OUTLINE': {
                'HLT':'┌', 'HMT':'┬', 'HRT':'┐',
                'HLB':'├', 'HMB':'┼', 'HRB':'┤',
                'FL':'└', 'FM':'┴', 'FR':'┘',
                'L':'│', 'R':'│', 'M':'│',
                'HLINE':'─'
            },
            'OUTLINE_DBL': {
                'HLT': '╔', 'HMT': '╦', 'HRT': '╗',
                'HLB': '╠', 'HMB': '╬', 'HRB': '╣',
                'FL': '╚', 'FM': '╩', 'FR': '╝',
                'L': '║', 'R': '║', 'M': '║',
                'HLINE': '═'
            }
        }


        self._col_orientations = []

    @property
    def box_type(self):
        return self._type

    @box_type.setter
    def box_type(self, type_str):
        self._type = type_str


    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, data):
        """Use box setter only for processing table data (rows x columns) in one fell swoop (vs. row-by-row)"""
        try:
            assert(self.is_tabular(data))
            self._box = data
            self._cols = len(data[0])
            self._rows = len(data)

            # default: left-orientation
            for i in xrange(0, self._rows):
                self._col_orientations.append('<')
            self.max_col_lens = data
        except Exception as e:
            print 'ERROR: Data is NOT tabular! (lists are not of same length)'
            sys.exit()

    @property
    def max_col_lens(self):
        return self._max_col_lens

    @max_col_lens.setter
    def max_col_lens(self, table_data):
        """set the max col length for each column"""
        self._max_col_lens = [max(len(str(x)) for x in line) for line in zip(*table_data)]

    @property
    def box(self):
        return self._box

    @box.setter
    def box(self, data):
        """Use box setter only for processing table data (rows x columns) in one fell swoop (vs. row-by-row)"""
        try:
            assert(self.is_tabular(data))
            self._box = data
            self._cols = len(data[0])
            self._rows = len(data)

            # default: left-orientation
            for i in xrange(0, self._rows):
                self._col_orientations.append('<')
            self.max_col_lens = data
        except Exception as e:
            print 'ERROR: Data is NOT tabular! (lists are not of same length)'
            sys.exit()

    @property
    def max_col_lens(self):
        return self._max_col_lens

    @max_col_lens.setter
    def max_col_lens(self, table_data):
        self._max_col_lens = [max(len(str(x)) for x in line) for line in zip(*table_data)]

    @property
    def col_orientations(self):
        """Returns column orientations as a list - 1 per column"""
        return self._col_orientations

    @col_orientations.setter
    def col_orientations(self, list_orientations):
        """optional parameter: set column orientations in a list
        Note: all columns left-oriented by default
        Example:
        list_orientations = [ '<', '<', '^', '>', '>' ]"""
        self._col_orientations = list_orientations

    def get_frame_row(self, col, LEFT, MID, RIGHT, HLINE):
        """provides top header/footer frame (row) as string"""
        this_row = ''
        if self.is_col_first(col):
            this_row += '\n'
            this_row += self._types[self._type][LEFT]
        else:
            this_row += self._types[self._type][MID]

        # extend HLINE char for length of cell
        this_row += self._types[self._type][HLINE] * (self._max_col_lens[col] + 2)

        if self.is_col_last(col):
            this_row += self._types[self._type][RIGHT]
        return this_row

    def get_data_row(self, col, data):
        """returns data (or header text) row as string"""
        this_row = ''
        data = self.get_cell_formatted(col, data)
        if self.is_col_first(col):
            this_row += '\n'
            if 'OUTLINE' in self._type:
                this_row += self._types[self._type]['L']
            else:
                this_row += ' '
        else:
            this_row += self._types[self._type]['M']

        this_row += str(data)
        if 'OUTLINE' in self._type:
            if self.is_col_last(col):
                this_row += self._types[self._type]['R']
        return this_row

    def get_cell_formatted(self, col, data=''):
        """returns formatted cell with proper spacing, orientation"""

        spacer_len = (self._max_col_lens[col] - len(str(data)))
        spacer = spacer_len * ' '
        if self._col_orientations[col] == '<':
            cell = ' {}{} '.format(data,spacer)
        elif self._col_orientations[col] == '>':
            cell = ' {}{} '.format(spacer,data)
        else:
            spacer_len, remainder = divmod(spacer_len, 2)
            spacer = spacer_len * ' '
            if remainder !=0:
                extra = ' '
            else:
                extra = ''
            cell = ' {}{}{} {}'.format(spacer,data,spacer,extra)

        return cell

    def box_it(self):
        """
        returns box formatted data as string
        To format each column we need a list containing:
        1) max str length of each column
        2) optional:  orientation of each column:
           left <, right >, center ^ (default: left <)
        """
        box = ''

        # header
        if ('OUTLINE' in self._type):
            for col, data in enumerate(self._box[0]):
                box += self.get_frame_row(col,'HLT', 'HMT', 'HRT', 'HLINE')
        for col, data in enumerate(self._box[0]):
            box += self.get_data_row(col, data)
        if (self.header):
            for col, data in enumerate(self._box[0]):
                box += self.get_frame_row(col,'HLB', 'HMB', 'HRB', 'HLINE')

        # data
        for row, row_list in enumerate(self._box[1:]):
            for col, data in enumerate(row_list):
                box += self.get_data_row(col, data)

        # footer
        if 'OUTLINE' in self._type:
            for col, data in enumerate(row_list):
                box += self.get_frame_row(col,'FL', 'FM', 'FR', 'HLINE')
        return box

    def is_tabular(self, data):
        """Checks if data is tabular (each list in list must be of same length)"""
        lengths = [len(x) for x in data]
        return len(set(lengths))==1

    def is_header(self, row_pos):
        return (row_pos == 0)

    def is_col_first(self, col_pos):
        return (col_pos == 0)

    def is_col_last(self, col_pos):
        return (self._cols - 1 == col_pos)

    def is_row_last(self, row_pos):
        return (self._rows - 1 == row_pos)


if __name__ == '__main__':

    # box = Box(type='OUTLINE', header=True)

    ####################################
    # TEST DATA - with header labels
    ####################################

    box = Box()
    results = [
        [ 'aaa','bbb','ccc','dddd','eeee'],
        [ 'ffff','gggg','hhh','iiiiiiiiiiiii','jjjjjj'],
        [ 'kk','lllllll','m','nnnnnn','oooooo'],
        [ 'ppppp','qq','rrrr','sssss','t'],
        [ 'u','vvv','ww','xxx','yyyyyyyyyyyyyyyy']
    ]
    box.col_orientations = [ '>', '<', '^', '>', '>']

    box.box = results
    box.box_type = 'MINIMAL'
    print box.box_it()
    box.box_type = 'SIMPLE'
    print box.box_it()
    box.box_type = 'SIMPLE_OUTLINE'
    print box.box_it()
    box.box_type = 'OUTLINE'
    print box.box_it()
    box.box_type = 'OUTLINE_DBL'
    print box.box_it()


    ####################################
    # TEST DATA - with left column labels
    ####################################

    box = Box()
    results = [
        ( 'AVG TEST DURATION', '2s' ),
        ( 'TEST RESULTS', 'PASS: 2, FAIL: 0, ERROR: 3' ),
        ( 'MORE RESULTS', 'Yes!!!' ),
        ( 'EVEN MORE RESULTS', 'No!!!')
    ]
    box.box = results
    box.col_orientations = [ '<', '<' ]
    box.header = False
    box.box_type = 'SIMPLE_OUTLINE'
    print box.box_it()
    box.box_type = 'OUTLINE_DBL'
    print box.box_it()
