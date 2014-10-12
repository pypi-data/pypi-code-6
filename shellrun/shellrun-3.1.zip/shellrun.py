#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Run commands through system shell

Author:  anatoly techtonik <techtonik@gmail.com>
License: Public Domain

Recipe 1 (run, let output pass):

    from shellrun import run
    if run('ls -la').success:
        print('Done.')

Recipe 2 (capture):

    from shellrun import run_capture

    res = run_capture('ls -la')
    if res.success:
        print(res.output)
    else:
        print("Error %s" % res.retcode)

Recipe 3 (capture, but return 3 last lines only):

    from shellrun import run_capture_limited

    res = run_capture_limited('ls -la & false', maxlines=3)
    if not res.success:
        print("Something is not right, retcode %s:" % res.retcode)
        print("  ...")
        print(res.output)

Roadmap:
 [ ] run command string through system shell
   [x] output immediately visible on the screen (run)
   [x] catch the output if needed (run_capture)
     [ ] catch and output simultaneously asap
   [ ] catch stderr and stdout separately
         >>> run("something with 1 line on stdout and 2 on stderr")
         1 line
         2 on stderr
   [x] show last three lines of output on error in example

 [ ] Python 3 compatibility
   [ ] automatically decode output from binary to unicode
       (make sure there is no unnecessary exceptions)
   [ ] provide option to skip automatic decoding

 [ ] buffer overflow protection
   [x] reader in separate thread
   [*] avoid MemoryError when process writes too much
       by providing limited size queue
     [x] line queue
     [ ] binary buffer

   [ ] avoid deadlocks when app waits for stdin input
       and Python process waits for its stdout output
       (asynchronous subprocess)

 [ ] timeout for deadlock protection

 [ ] tests


History:
  3.1 (2014-10-12)
    - bugfix: run_capture() stderr merge didn't work

  3.0 (2014-08-04)
    + new function
        run_capture_limited(command, maxlines=20000)

  2.0 (2014-07-21)
    * changed API
      - run_capture(command) returns stdout + stderr
        combined in result.output

  1.1 (2014-07-20)
    - bugfix: result.command was always empty

  1.0 (2014-01-01)
    * changed API
       -run(command, combine_stderr=True)
       +run(command)
       +run_capture(command)
    * changed return object


Credits:
  Nick Coghlan for constructive discussion
  Kenny, Jason L for SCons Parts works 
  python-ideas for the feedback
  Fabric folks for the example of intuitive API

Inspired by Fabric API:
    http://docs.fabfile.org/en/1.4.2/api/core/operations.html#fabric.operations.run
  and this thread:
    https://groups.google.com/d/topic/python-ideas/u42aZZnrs8A/discussion
  and shell_command's:
    http://pypi.python.org/pypi/shell_command
    https://github.com/robgleeson/shell_command
  and envoy:
    https://github.com/kennethreitz/envoy

Notes:

  Every process in Linux and Windows (thanks to C legacy) communicates
  through three streams (called 'standard streams'). Sometimes these
  streams can be closed, but by default the process model is this:

                ┌───────────┐
    stdin  o───>│  Process  │>───o  stdout
                │           │>───o  stderr
                └───────────┘
"""

__version__ = '3.1'
__license__ = 'Public Domain'


import subprocess

"""
subprocess behaviour when shell=True

1. no exceptions are raised if command is not found
2. there is no reliable way to distinguish between
   command not found and error during execution

the only convention that works is that successful
execution returns 0 exit status (error code)
"""

class Result(object):
    def __init__(self, command=None, retcode=None, output=None):
        self.command = command or ''
        self.retcode = retcode
        self.output = output
        self.success = False
        if retcode == 0:
            self.success = True


def run(command):
    """
    Run `command` through shell and wait for it to complete.
    stdin/stdout/stderr are shared with Python, so the output
    is immediately visible and not captured. Returns Result
    with command, retcode and success attributes.

    - return code
    - no stdout capture
    - no stderr capture
    - no deadlocks or MemoryError
    - stdout, stderr and stdin are shared with Python process

   ┌─────────┐             ┌────────┐                   ┌─────────┐
   │  Parent │>─(stdin)─┬─>│ Python ├─────┬──(stdout)──>│  Parent │
   │(console)│          │  │ script ├─────│┬─(stderr)──>|(console)│
   └─────────┘          │  └────────┘     ││            └─────────┘
                        │  ┌────────────┐ ││
                        └─>│ Subprocess ├─┘│
                           │  (shell)   ├──┘
                           └────────────┘
    """
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    return Result(command=command, retcode=process.returncode)


def run_capture(command):
    """
    Run `command`, wait, capture output into returned Result object.

    - return code
    - stdout and stdout combined capture
    - no deadlocks, but MemoryError at about 500Mb of buffered
      output on Windows (internal Python buffer)
    - stdin is shared with current Python process

    ┌─────────┐ (stdin) ┌─────────────┐     
    │  Parent │>──┬────>│ Python      │
    │(console)│   │     │ script      │
    └─────────┘   │     └───────────^─┘
                  │  ┌────────────┐ │
                  └─>│ Subprocess ├─┤ (buffer: stdout+stderr)
                     │  (shell)   ├─┘
                     └────────────┘
    """
    outpipe = subprocess.PIPE
    errpipe = subprocess.STDOUT
    process = subprocess.Popen(command, shell=True, stdout=outpipe,
                                                    stderr=errpipe)
    output, _ = process.communicate()
    return Result(command=command, retcode=process.returncode, output=output)


def run_capture_limited(command, maxlines=20000):
    """
    Run `command` through a system shell, return last `maxlines`
    as output string in Result object.

    - return code
    - stdout and stdout combined capture
    - no deadlocks
    - no memory errors thanks to limited size FIFO buffer
      (memory error is possible for long output without newlines)
    - stdin is shared with current Python process

    ┌─────────┐ (stdin) ┌─────────────┐            ┌─────────┐
    │  Parent │>──┬────>│ Python      ├─(stdout)──>│  Parent │
    │(console)│   │     │ script      ├─(stderr)──>│(console)│
    └─────────┘   │     └───────────^─┘            └─────────┘
                  │  ┌────────────┐ │
                  └─>│ Subprocess ├─┤ (buffer: stdout+stderr
                     │  (shell)   ├─┘   limited to maxlines)
                     └────────────┘
    """
    """
    [x] start reader thread
      [x] reader: wait for lines
      [x] wait for process to complete
      [x] reader: wait for EOF

    [ ] may not be a binary accurate read, because of \n split
        and reassembly, needs testing
    [ ] buffer size is line limited, test big streams without
        newlines

    [ ] need tests for missing output
      [ ] process finished, pipe closed, did reader thread get
          all the output? when pipe closes? is it possible to
          miss the data?

    [ ] access local buffer from outside
      [ ] show current buffer contents if needed
      [ ] show current line count if needed
    """

    import collections
    import threading

    lines = collections.deque(maxlen=maxlines)
    def reader_thread(stream, lock):
        for line in stream:
            lines.append(line)

    outpipe = subprocess.PIPE
    errpipe = subprocess.STDOUT
    process = subprocess.Popen(command, shell=True, stdout=outpipe,
                                                    stderr=errpipe)
    lock = threading.Lock()
    thread = threading.Thread(target=reader_thread, args=(process.stdout, lock))
    thread.start()

    # With communicate() we get in thread:
    #   ValueError: I/O operation on closed file
    # or in main thread
    #   IOError: close() called during concurrent operation on the same file object.
    #out, _ = process.communicate()

    process.wait()
    thread.join()

    return Result(command=command, retcode=process.returncode, output=''.join(lines))


if __name__ == '__main__':
    print('---[ .success ]---')
    print(run('ls').success)
    print(run('dir').success)

    print('---[ .retcode ]---')
    print(run('ls').retcode)
    print(run('dir').retcode)

    print('---[ capture ]---')
    print(len(run_capture('ls').output))
    print(len(run_capture('dir').output))

    # Test that output is immediately available on the screen
    #run('git clone https://github.com/wesnoth/wesnoth')

    print('---[ limited capture ]---')
    print(run_capture_limited('ls', maxlines=2).output)
    print(run_capture_limited('dir', maxlines=2).output)
