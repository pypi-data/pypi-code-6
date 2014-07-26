import os
from glob import glob
from hashlib import md5
import asyncio
import logging
import tempfile

from geoffrey import plugin
from geoffrey.data import EventType
from geoffrey.utils import execute
from geoffrey.subscription import subscription

TEMPDIR = tempfile.gettempdir()

class Pyreverse(plugin.GeoffreyPlugin):
    """
    pyreverse plugin.

    TODO: Change this class name to FullCamelCase

    """
    @subscription
    def modified_files(self, event):
        """
        Subscription criteria.

        Should be used as annotation of plugin.Tasks arguments.
        Can be used multiple times.

        """
        return (self.project.name == event.project and
                event.plugin == "filecontent" and
                event.key.endswith('.py') and
                event.type in (EventType.created, EventType.modified))

    @asyncio.coroutine
    def run_pyreverse(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        pyreverse_path = self.config.get(self._section_name, "pyreverse_path")

        while True:
            event = yield from events.get()

            filename = event.key
            dot_id = md5(filename.encode('utf-8')).hexdigest()

            exitcode, stdout, stderr = yield from execute(
                pyreverse_path, '-A', '-o', 'dot', '-p', dot_id, filename,
                cwd=TEMPDIR)

            data = {}
            dotfiles = glob(os.path.join(TEMPDIR, '*_' + dot_id + '*.dot'))
            for dotfile in dotfiles:
                dot_type, _ = os.path.basename(dotfile).split('_', 1)
                with open(dotfile, 'r') as f:
                    data[dot_type] = f.read()
                os.unlink(dotfile)

            state = self.new_state(key=filename, **data)

            yield from self.hub.put(state)
