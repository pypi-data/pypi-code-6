# -*- coding: utf-8 -*-
import os
import time

start = '\033[1;%dm'
end = '\033[0;0m'

width = int(os.popen('stty size', 'r').read().split()[1])


def do_1337():
    while True:
        for j in range(40,48):
            print(start % j + '1337' * (width // 4) + end)


def main():
    while True:
        try:
            time.sleep(2)
            do_1337()
        except KeyboardInterrupt:
            print('Not so easy...')


if __name__ == '__main__':
    main()
