#!/usr/bin/env python
# encoding: utf-8
import os
import pty
import select
import termios

import pyte


def process_to_screen(argv, stdin=None, width=80, height=24):
    # Fork the process, spliting into a parent and child process.
    # Reading from master_fd gives us the child process's STDOUT and STDERR,
    # and writing goes to the child process's STDIN.
    pid, master_fd = pty.fork()

    if pid == 0:
        # We're in the child process, so fork and replace the current
        # process with the desired one.
        os.execlp(argv[0], *argv)

    # Disable echoing STDIN to STDOUT in the child process. If we don't do
    # this, we'll see duplicate output on STDOUT.
    old_attr = termios.tcgetattr(master_fd)
    old_attr[3] &= ~termios.ECHO
    termios.tcsetattr(master_fd, termios.TCSADRAIN, old_attr)

    # Create a new virtual screen.
    screen = pyte.Screen(width, height)

    # Create a new input stream and associate it with the previously
    # create virtual screen.
    stream = pyte.ByteStream()
    stream.attach(screen)

    read_fds = [master_fd, stdin]
    write_fds = [master_fd] if stdin is not None else []
    while True:
        # Wait for output from the child process.
        rfds, wfds, xfds = select.select(read_fds, write_fds, [])

        if master_fd in rfds:
            try:
                data = os.read(master_fd, 1024)
            except OSError:
                # A weird, docker-only bug that causes the socket to close
                # dirty.
                break

            if not data:
                break

            stream.feed(data)

        if master_fd in wfds and stdin in rfds:
            chunk = stdin.read(1024)
            while chunk:
                # This isn't optimal, we should be keeping chunk outside
                # of the loop and only trying to write() when select() says
                # we can.
                bytes_written = os.write(master_fd, chunk)
                chunk = chunk[bytes_written:]

    os.close(master_fd)
    os.waitpid(pid, 0)[1]

    default_char = screen.default_char
    final_screen = []
    for line in screen.buffer:
        final_line = []
        for char in line:
            # We don't need extended details for a character that's just
            # the default!
            if char == default_char:
                final_line.append(None)
                continue

            # Only save the attributes that are actually different from
            # the default.
            final_line.append({
                k: v
                for k, v in char._asdict().iteritems()
                if getattr(default_char, k) != v
            })

        # If a line is completely blank, we'll just replace the whole
        # thing with a single None.
        final_screen.append(final_line if any(final_line) else None)

    return final_screen
