#!/usr/bin/python
# -*- coding: utf-8 -*-


''' usage: pysed [-h] [-v] [-p] [-l] [-r] [-i]

Utility that parses and transforms text

optional arguments:
  -h, --help     : show this help message and exit
  -v, --version  : print version and exit
  -p, --print    : print text
                   e extract/, c chars/, s sum/
  -l, --lines    : print lines
                   'N', '[N-N]', '*, all'
  -r, --replace  : replace text
                   m max(N)/, u upper */, l lower */, /color
  -i, --insert   : insert text
                   m max(N)/, /color

N = Number, {Options}/, 'Pattern'
color = red, green, blue, cyan, yellow, magenta

'''

import re
import os
import sys
import platform


__prog__ = 'pysed'
__author__ = "dslackw"
__version__ = "0.1.8"
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"


if platform.system() == 'Linux':
    path = os.getcwd() + '/'

elif platform.system() == 'Windows':
    path = os.getcwd() + '\/'


def colors(color):
    '''Print colors'''

    paint = {
        'red': '\x1b[31m',
        'green': '\x1b[32m',
        'yellow': '\x1b[33m',
        'blue': '\x1b[34m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'default': '\x1b[0m'
    }

    return paint[color]


def get_from_arg(arg):
    '''Get any string before char /'''

    result = []
    for char in arg:
        result.append(char)
        if char == '/':
            break

    return ''.join(result).replace('/', '')


def get_from_arg_reverse(arg):
    '''Get any string after char /'''

    i = 0
    result = []
    for char in range(len(arg)):
        i -= 1
        result.append(arg[i])
        if arg[i] == '/':
            break

    return ''.join(result[::-1]).replace('/', '')


def get_nums(text):
    '''Grep numbers from a string'''

    nums = '0123456789'

    result = []
    for t in text:
        for n in nums:
            if n == t:
                result.append(n)

    return ''.join(result)


def findall(argX, read):
    '''Find text from string'''

    try:

        find_text = re.findall(argX, read)

        if find_text == []:
            find_text == ''

    except re.error:
        find_text = ''

    return find_text


def open_file_for_read(file):
    '''Open files for read only'''

    file = open(path + file, 'r')
    read = file.read()
    file.close()

    return read


def open_file_for_read_and_write(file):
    '''Open files for read and write'''

    return open(path + file, 'r+')


def write_to_file(file, result):
    '''Write results to a file'''

    file.seek(0)
    file.truncate()
    file.write(result)
    file.close()


def replace(read, arg2, arg3, options_1, options_2):
    '''Replace text with new'''

    nums = get_nums(options_1)
    options_1 = options_1.replace(nums, '')

    if nums == '':
        nums = 0

    find_text = findall(arg2, read)

    if options_2 in ['red', 'green', 'yellow', 'cyan', 'blue', 'magenta']:
        color = colors(options_2)
        default = colors('default')
    else:
        color = ''
        default = ''

    result = read
    for text in set(find_text):
        if options_1 == 'm=' or options_1 == 'max=':
            result = read.replace(text, color + arg3 + default,
                                  int(nums))

        elif options_1 == 'u' or options_1 == 'upper':
            result = read.replace(text,
                                  color + arg3.upper() + default)

        elif options_1 == 'u=*' or options_1 == 'upper=*':
            result = color + read.upper() + default

        elif options_1 == 'l' or options_1 == 'lower':
            result = read.replace(text,
                                  color + arg3.lower() + default)

        elif options_1 == 'l=*' or options_1 == 'lower=*':
            result = color + read.lower() + default

        else:
            result = result.replace(text, color + arg3 + default)

    return result


def append(read, arg2, arg3, options_1, options_2):
    '''Insert new text'''

    nums = get_nums(options_1)
    options_1 = options_1.replace(nums, '')

    if nums == '':
        nums = 0

    find_text = findall(arg2, read)

    if options_2 in ['red', 'green', 'yellow', 'cyan', 'blue', 'magenta']:
        color = colors(options_2)
        default = colors('default')
    else:
        color = ''
        default = ''

    result = read
    for text in set(find_text):
        if options_1 == 'm=' or options_1 == 'max=':
            result = read.replace(text,
                                  text + color + arg3 + default,
                                  int(nums))

        else:
            result = result.replace(text,
                                    text + color + arg3 + default)
    return result


def linesx(read, argX):
    '''Print lines'''

    result = []

    options_1 = get_from_arg(argX)
    argX = argX.replace(options_1 + '/', '', 1)
    step = get_nums(options_1)
    options_1 = options_1.replace(step, '')

    if step == '' or step == '0':
        step = 1

    for line in read.splitlines():
        result.append(line)

    if argX == '*' or argX == 'all':
        if options_1 == 'step=':
            for line in range(0, len(result), int(step)):
                print result[line]
            sys.exit()
        else:
            for line in range(len(result)):
                print result[line]
            sys.exit()

    elif argX.startswith('[') and argX.endswith(']'):
        argX = argX.replace('[', '', 1)
        argX = argX.replace(']', '', 1)

        line_nums = argX.replace('-', '\n').split()

        if len(line_nums) < 2 or int(
                line_nums[1]) >= len(result):
            sys.exit()

        else:

            try:
                for n in range(int(line_nums[0]),
                               int(line_nums[1]) + 1):
                    print result[int(n)]
                sys.exit()
            except ValueError:
                sys.exit()

    else:

        try:
            line_nums = argX.replace(',', '\n').split()

            for num in line_nums:
                if int(num) >= len(result):
                    pass
                else:
                    print result[int(num)]
            sys.exit()
        except ValueError:
            sys.exit()


def print_text(file, arg0, arg1, arg2, arg3):
    '''Print all results before
    any changes save in a file'''

    result = []

    options_1 = get_from_arg(arg2)
    arg2 = arg2.replace(options_1 + '/', '', 1)

    options_2 = get_from_arg_reverse(arg3)
    arg3 = arg3.replace('/' + options_2, '', 1)

    try:
        read = open_file_for_read(file)
        if arg0 == '-p' or arg0 == '--print':

            options_1 = get_from_arg(arg1)
            arg1 = arg1.replace(options_1 + '/', '', 1)
            find_text = findall(arg1, read)

            if options_1 == 's' or options_1 == 'sum':

                words = read.split()
                chars = ''.join(words)
                for lines in range(len(read.splitlines())):
                    pass
                print '%d lines' % (lines)
                print '%d characters' % len(chars)
                print '%d words' % len(words)
                print '%d blanks' % (len(read) - len(chars))
                sys.exit()

            if options_1 == 'c' or options_1 == 'chars':

                print 'find %d --> \'%s\'' % (
                    len(find_text), arg1)
                sys.exit()

            if options_1 == 'e' or options_1 == 'extract':

                print ' '.join(find_text)
                sys.exit()

            else:

                print read,
                sys.exit()

        elif arg0 == '-l' or arg0 == '--lines':
            result = linesx(read, arg1)

        elif arg0 == '-r' or arg0 == '--replace':
            result = replace(read, arg2, arg3, options_1, options_2)

        elif arg0 == '-i' or arg0 == '--insert':
            result = append(read, arg2, arg3, options_1, options_2)

        else:

            arguments_error(arg0, '')

        if result != []:
            print result,

    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def write_replace_text(file, arg1, arg2):
    '''Replace the text and save changes to the file'''

    result = []

    options_1 = get_from_arg(arg1)
    arg1 = arg1.replace(options_1 + '/', '', 1)

    try:
        file = open_file_for_read_and_write(file)
        read = file.read()
        result = replace(read, arg1, arg2, options_1, '')

        if result != []:
            write_to_file(file, result)

    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def write_append_text(file, arg1, arg2):
    '''Insert text and save changes to the file'''

    result = []

    options_1 = get_from_arg(arg1)
    arg1 = arg1.replace(options_1 + '/', '', 1)

    try:

        file = open_file_for_read_and_write(file)
        read = file.read()
        result = append(read, arg1, arg2, options_1, '')

        if result != []:
            write_to_file(file, result)

    except IOError:
        print ("%s: can't read %s: No such file or directory"
               % (__prog__, file))


def version():
    '''Print version, license and email'''

    print ('version :'), __version__
    print ('License :'), __license__
    print ('Email   :'), __email__


def arguments_view():
    '''Print arguments options'''

    print ('usage: pysed [-h] [-v] [-p] [-l] [-r] [-i]\n')
    print ('Utility that parses and transforms text\n')
    print ('optional arguments:')
    print ('  -h, --help     : show this help message and exit')
    print ('  -v, --version  : print version and exit')
    print ('  -p, --print    : print text')
    print ('                   e extract/, c chars/, s sum/')
    print ('  -l, --lines    : print lines')
    print ('                   \'N\', \'[N-N]\', \'step=N/*, all\'')
    print ('  -r, --replace  : replace text')
    print ('                   m max=N/, u upper=*/, l lower=*/, /color')
    print ('  -i, --insert   : insert text')
    print ('                   m max=N/, /color\n')
    print ('N = Number, {Options}/, \'Pattern\'')
    print ('color = red, green, blue, cyan, yellow, magenta')


def arguments_error(arg0, argx):
    '''Print errors arguments'''

    print ('usage: %s [-h] [-v] [-p] [-l] [-r] [-i]\n' % __prog__)

    if arg0 == '':
        print ('%s: error: argument: expected one argument' % __prog__)

    elif arg0 in ['-p', '--print',
                  '-l', '--lines',
                  '-r', '--replace',
                  '-i', '--insert']:
        print ('%s: argument %s: expected at least one argument'
               % (__prog__, arg0))

    else:
        print ('%s: error: unrecognized arguments: %s %s'
               % (__prog__, arg0, ' '.join(argx)))


def main():

    arg = sys.argv
    arg.pop(0)

    if len(arg) == 2:
        file = arg[1]

    elif len(arg) == 3:
        file = arg[2]

    elif len(arg) == 4:
        file = arg[3]

    elif len(arg) == 5:
        file = arg[4]

    if len(arg) == 0:
        arguments_error('', '')

    elif (len(arg) == 1 and arg[0] == '-h' or len(arg) == 1
          and arg[0] == '--help'):
        arguments_view()

    elif (len(arg) == 1 and arg[0] == '-v' or len(arg) == 1 and
          arg[0] == '--version'):
        version()

    elif (len(arg) == 2 and arg[0] == '-p' or len(arg) == 2 and
          arg[0] == '--print'):
        print_text(file, arg[0], '', '', '')

    elif (len(arg) == 3 and arg[0] == '-p' or len(arg) == 3 and
          arg[0] == '--print'):
        print_text(file, arg[0], arg[1], '', '')

    elif (len(arg) == 5 and arg[1] == '-p' or len(arg) == 5 and
          arg[1] == '--print'):
        print_text(file, arg[0], arg[1], arg[2], arg[3])

    elif (len(arg) == 3 and arg[0] == '-l' or len(arg) == 3 and
          arg[0] == '--lines'):
        print_text(file, arg[0], arg[1], '', '')

    elif (len(arg) == 4 and arg[0] == '-r' or len(arg) == 4 and
          arg[0] == '--replace'):
        write_replace_text(file, arg[1], arg[2])

    elif (len(arg) == 4 and arg[0] == '-i' or len(arg) == 4 and
          arg[0] == '--insert'):
        write_append_text(file, arg[1], arg[2])

    elif not any(
            [len(arg) == 1 and arg[0] == '-p', len(arg) == 1 and arg[0] == '--print',
             len(arg) == 1 and arg[0] == '-l', len(arg) == 1 and arg[0] == '--lines',
             len(arg) == 1 and arg[0] == '-r', len(arg) == 1 and arg[0] == '--replace',
             len(arg) == 1 and arg[0] == '-i', len(arg) == 1 and arg[0] == '--insert', ]):
        arguments_error(arg[0], arg[1:])

    else:
        arguments_error(arg[0], arg[1:])

if __name__ == '__main__':
    main()
