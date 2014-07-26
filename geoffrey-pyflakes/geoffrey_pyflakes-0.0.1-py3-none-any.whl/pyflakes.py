import logging
import asyncio

from geoffrey import plugin
from geoffrey.data import EventType
from geoffrey.subscription import subscription
from geoffrey.utils import execute


class PyFlakes(plugin.GeoffreyPlugin):
    """
    pyflakes plugin.

    """
    @staticmethod
    def message_to_highlight(message):
        return {"start_line": message['line'],
                "start_char": 0,
                "end_line": message['line'],
                "end_char": 0,
                "text": message['message'],
                "link": "",
                "type": "error"}

    @subscription
    def modified_files(self, event):
        """
        Subscription criteria.

        """
        return (self.project.name == event.project and
                event.plugin == "filecontent" and
                event.key.endswith('.py') and
                event.type in (EventType.created, EventType.modified))

    @subscription
    def deleted_files(self, event):
        """
        Files deleted or moved.

        """
        return (event.project == self.project.name and
                event.plugin == "filesystem" and
                event.fs_event in ('deleted', 'moved'))

    @asyncio.coroutine
    def removed_files_remove_errors(self, events:"deleted_files") -> plugin.Task:
        while True:
            event = yield from events.get()
            state = self.new_state(key=event.key)
            yield from self.hub.put(state)

    @asyncio.coroutine
    def run_pyflakes(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        pyflakes_path = self.config.get(self._section_name, "pyflakes_path")
        while True:
            event = yield from events.get()

            exitcode, stdout, stderr = yield from execute(
                pyflakes_path, event.key, stdin=event.raw)

            lines = []
            for line in stdout.decode('utf-8').splitlines():
                file, linenum, message = [l.strip()
                                          for l in line.split(':', 2)]
                lines.append({'line': linenum, 'message': message})

            state = self.new_state(key=event.key,
                                   lines=lines,
                                   exitcode=exitcode)

            yield from self.hub.put(state)

            # Highlight content_type
            highlights = []
            for message in lines:
                highlights.append(self.message_to_highlight(message))

            if highlights:
                hl_state = self.new_state(content_type="highlight", key=event.key,
                                      highlights=highlights)
            else:
                hl_state = self.new_state(content_type="highlight", key=event.key)

            yield from self.hub.put(hl_state)
