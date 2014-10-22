import sys
import time

from click import echo

from pathlib import Path

from .commands import run_commands


_watch_rules = set()


def watch_forever(env, verbose):
    """
    Starts the watcher.  This is the meat driving the ``iron watch`` shell
    command.
    """
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError:
        echo('The watcher requires watchdog to be installed.')
        sys.exit(3)

    class CommandTrigger(FileSystemEventHandler):
        def __init__(self, patterns, cmdname, env, verbose):
            self.patterns = patterns
            self.cmdname = cmdname
            self.env = env
            self.verbose = verbose

        def on_any_event(self, event):
            # Ignore directories
            if event.is_directory:
                return

            # Ignore .DS_Store updates
            src_path = Path(event.src_path)
            if src_path.name == '.DS_Store':
                if self.verbose:
                    echo('Ignoring changes to .DS_Store')
                return

            # Must match pattern
            if not self.patterns or any(src_path.match(pat) for pat in self.patterns):
                echo('>>> Running {}'.format(self.cmdname))
                run_commands([self.cmdname], self.env, self.verbose)
            else:
                if self.verbose:
                    echo('Ignoring {} (does not match any of {})'.format(src_path, self.patterns))

    observer = Observer(timeout=1.7)

    for name, paths, patterns in sorted(_watch_rules):
        handler = CommandTrigger(patterns, name, env, verbose)

        for path in paths:
            patstr = ', '.join(patterns) if patterns else 'any file'
            echo('Will trigger {} when {} changes in {}'.format(name, patstr, path))
            observer.schedule(handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print('Stopping file system watches...')
        observer.stop()
    observer.join()
