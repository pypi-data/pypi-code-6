"""
signalfd(2) demo, see the manual page of signalfd(2) for the equivalent C-code
"""
from __future__ import print_function
from __future__ import absolute_import

from ctypes import byref
from os import fork, execlp, fdopen, wait, pipe, close, dup2
from signal import SIGINT, SIGQUIT, SIGCHLD, SIGPIPE

from glibc import (
    SIG_BLOCK, SFD_CLOEXEC, EPOLL_CLOEXEC,
    sigset_t, signalfd_siginfo, epoll_event,
    sigemptyset, sigaddset, sigprocmask, signalfd,
    epoll_create1,
)


def main():
    # Block signals so that they aren't handled
    # according to their default dispositions
    ask = sigset_t()
    fdsi = signalfd_siginfo()
    sigemptyset(mask)
    sigaddset(mask, SIGINT)
    sigaddset(mask, SIGQUIT)
    sigaddset(mask, SIGCHLD)
    sigaddset(mask, SIGPIPE)
    sigprocmask(SIG_BLOCK, mask, None)
    # Get a signalfd descriptor
    sfd = signalfd(-1, mask, SFD_CLOEXEC)
    # Get a epoll descriptor
    efd = epoll_create1(EPOLL_CLOEXEC)
    epoll_event ev
    ev.events = EPOLLIN
    ev.data.fd = sfd
    # Create a pipe for stdout
    stdout_read_end, stdout_write_end = pipe()
    # Create a pipe for stderr
    stderr_read_end, stderr_write_end = pipe()
    # Spawn a child process
    pid = fork()
    if pid == 0:
        # Child
        dup2(1, stdout_write_end)
        dup2(2, stderr_write_end)
        close(stdout_read_end)
        close(stderr_read_end)
        close(stdout_write_end)
        close(stderr_write_end)
        # Run dmesg in the child
        execlp("dmesg", "dmesg")
    else:
        # Parent
        close(stdout_write_end)
        close(stderr_write_end)
    with fdopen(sfd, 'rb', 0) as sfd_stream:
        while True:
            # Read the next delivered signal
            sfd_stream.readinto(fdsi)
            if fdsi.ssi_signo == SIGINT:
                print("Got SIGINT")
            elif fdsi.ssi_signo == SIGQUIT:
                print("Got SIGQUIT")
                return
            elif fdsi.ssi_signo == SIGCHLD:
                print("Got SIGCHLD")
                result = wait()
                print("Done waiting!", result)
            elif fdsi.ssi_signo == SIGPIPE:
                print("Got SIGCHLD")
                result = wait()
                print("Done waiting!", result)
            else:
                print("Read unexpected signal")
    close(stdout_read_end)
    close(stderr_read_end)


if __name__ == '__main__':
    main()
