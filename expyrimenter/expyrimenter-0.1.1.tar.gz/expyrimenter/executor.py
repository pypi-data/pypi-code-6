from concurrent.futures import ThreadPoolExecutor
from . import Config
import concurrent.futures
import logging
from subprocess import CalledProcessError


class Executor:
    def __init__(s, max_workers=None):
        if max_workers is None:
            max_workers = int(Config('workers').get('max'))

        s._executor = ThreadPoolExecutor(max_workers)
        s._future_runnables = {}  # for submitted runnables
        s._function_titles = {}     # for submitted functions
        s.results = []
        s._log = logging.getLogger('executor')

    def run_function(s, function, title=None, *args, **kwargs):
        """Submits a function to be run in parallel.

        If you only want to submit a function, use this method.
        It is not mandatory to call wait() or shutdown() later.
        """
        future = s._executor.submit(function, *args, **kwargs)
        s._function_titles[future] = title
        future.add_done_callback(s._done_function)

        return future

    def run(s, runnable, *args, **kwargs):
        """Submits Runnable objects to the PoolExector.

        Using Runnable objects, you have more control and verbosity.
        Useful when things go wrong (we know it always happens).
        If you are in a hurry, submit a function using :py:func:`run_fn`.
        """
        future = s._executor.submit(runnable.run, *args, **kwargs)
        s._future_runnables[future] = runnable
        future.add_done_callback(s._done_runnable)

        return future

    def _done_function(s, future):
        title = s._function_titles[future]
        s._done(future, title)
        del s._function_titles[future]

    def _done_runnable(s, future):
        runnable = s._future_runnables[future]
        title = runnable.title
        s._done(future, title)
        del s._future_runnables[future]

    def _done(s, future, title):
        if title is None:
            title = 'no given title'
        result = None

        ex = future.exception()
        if ex is None:
            s._log.debug('success:%s' % title)
            result = future.result()
        else:
            if type(ex) is CalledProcessError:
                msg = 'CalledProcessError:'
                if title != ex.cmd:
                    msg += '\n\tTitle   : %s' % title
                msg += '\n\tCmd     : %s' % ex.cmd
                msg += '\n\tReturned: %s' % ex.returncode
                msg += '\n\tOutput  : %s' % ex.output
                result = ex.output
            else:
                msg = 'exception:%s:%s' % (title, ex)
            s._log.error(msg)

        s.results.append(result)

    def wait(s):
        futures = list(s._future_runnables.keys())
        futures += list(s._function_titles.keys())

        concurrent.futures.wait(futures)

    def shutdown(s):
        s._executor.shutdown()
        s._future_runnables.clear()
        s._function_titles.clear()
        del s.results[:]
