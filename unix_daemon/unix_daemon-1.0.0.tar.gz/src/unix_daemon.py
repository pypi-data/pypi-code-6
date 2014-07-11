# -*- coding: utf-8 -*-
'''
daemon module emulating BSD Daemon(3)

Copyright 2014 Yoshida Shin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import errno


__all__ = ['daemon']


def daemon(nochdir=False, noclose=False):
    r''' Make process daemon and start to run in the background.

    If argument `nochdir' is False, this process changes the calling process's
    current working directory to the root directory ("/");
    otherwise, the current working directory is left unchanged.
    The Default of nochdir is False.

    If  argument `noclose' is False, this function close file descriptors 0, 1
    and 2 and redirect them to /dev/null. Even if some of them are closed, this
    function open these file descriptors and redirect to /dev/null if noclose
    is False.
    The defult value of noclose is False.

    This function returns the pid of new process.

    This function calls os.fork() internally to detach tty safely.
    Be careful to call this function when two or more than two python threads
    are running.

    Normary, file descriptors 0, 1 and 2 are correspond to stdin, stdout and
    stderr. However, even if any of these file discriptors refer to something
    else, they will still be closed when argument `noclose' is False.

    It is a good idea to call this function before creating any threads and
    before opening any files or sockets.
    '''

    # 1st fork
    pid = os.fork()
    if pid != 0:
        os.waitpid(pid, os.P_WAIT)
        os._exit(0)

    # 2nd fork
    os.setsid()
    if os.fork() != 0:
        os._exit(0)

    # daemon process
    # ch '/'
    if not nochdir:
        os.chdir('/')

    if not noclose:
        # Close stdin, stdout and stderr
        for fd in range(3):
            try:
                os.close(fd)
            except OSError as e:
                if e.errno == errno.EBADF:
                    # Do nothing if the descriptor has already closed.
                    pass
                else:
                    raise

        # Redirect stdin to /dev/null
        os.open(os.devnull, os.O_RDONLY)

        # Redirect stdout to /dev/null
        os.open(os.devnull, os.O_WRONLY)

        # Redirect stderr to /dev/null
        os.dup(1)

    return os.getpid()
