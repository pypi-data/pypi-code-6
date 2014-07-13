from vfd import *

if __name__ == '__main__':
    import argparse
    import curses.ascii
    import atexit
    import os
    import sys
    import termios
    import tty

    parser = argparse.ArgumentParser('python -m vfd')
    parser.add_argument('serial_path', type=str, help='Path to your serial device')
    parser.add_argument('--interactive', action='store_true', default=False, help='Type to the VFD interactively')
    parser.add_argument('--clear', action='store_true', default=False, help='Clear the VFD first')
    args = parser.parse_args()

    def reset_terminal(stdin, old_stdin):
        termios.tcsetattr(stdin, termios.TCSADRAIN, old_stdin)
        print()
        os.system('cls' if os.name=='nt' else 'clear')

    v = VFD(args.serial_path, clear=args.clear).scroll_write()

    if args.interactive:
        stdin = sys.stdin.fileno()
        old_stdin = termios.tcgetattr(stdin)
        atexit.register(reset_terminal, stdin, old_stdin)
        tty.setraw(stdin)

        while True:
            try:
                c = sys.stdin.read(1)
                if ord(c) == curses.ascii.ETX or ord(c) == curses.ascii.EOT:
                    raise KeyboardInterrupt()

                if ord(c) in [curses.ascii.BS, curses.ascii.DEL]:
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
                    v.backspace()
                    v.write(' ')
                    v.backspace()
                else:
                    sys.stdout.write(c)
                    sys.stdout.flush()
                    v.write(c)
            except KeyboardInterrupt:
                break
    else:
        message = sys.stdin.read().rstrip()
        v.write(message)
