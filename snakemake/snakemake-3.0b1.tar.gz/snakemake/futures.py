
import os
import multiprocessing
import concurrent.futures
from concurrent.futures.process import _ResultItem, _process_worker


def _graceful_process_worker(call_queue, result_queue):
    """Override the default _process_worker from concurrent.futures.
    We ensure here that KeyboardInterrupts lead to silent failures.
    """
    try:
        _process_worker(call_queue, result_queue)
    except KeyboardInterrupt:
        # let the process silently fail in case of a keyboard interrupt
        raise SystemExit()


class ProcessPoolExecutor(concurrent.futures.ProcessPoolExecutor):
    """Override the default ProcessPoolExecutor to gracefully handle KeyboardInterrupts."""
    def _adjust_process_count(self):
        for _ in range(len(self._processes), self._max_workers):
            p = multiprocessing.Process(
                    target=_graceful_process_worker,
                    args=(self._call_queue,
                          self._result_queue))
            p.start()
            self._processes[p.pid] = p
