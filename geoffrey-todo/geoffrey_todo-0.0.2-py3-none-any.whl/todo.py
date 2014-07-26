import logging
import asyncio
import re

from geoffrey import plugin
from geoffrey.data import EventType
from geoffrey.subscription import subscription

TODO_TYPES = ('TODO', 'XXX', 'FIXME')
TODO_RE = re.compile(
    '(?P<type>{}):\s*(?P<text>.*)$'.format('|'.join(TODO_TYPES)),
    flags=re.MULTILINE | re.IGNORECASE)


class Todo(plugin.GeoffreyPlugin):
    """
    todo plugin.

    TODO: Change this class name to FullCamelCase

    """

    @staticmethod
    def message_to_highlight(message):
        return {"start_line": message['line'],
                "start_char": message['row'],
                "end_line": message['line'],
                "end_char": message['row'] + message['length'],
                "text": '{}: {}'.format(
                    message['type'] if message['type'] in TODO_TYPES else 'Other',
                    message['text']),
                "link": "",
                "type": "note"}


    @subscription
    def modified_files(self, event):
        """
        Files modified or created.

        """
        return (event.project == self.project.name and
                event.plugin == "filecontent" and
                event.type in (EventType.created, EventType.modified))

    @subscription
    def deleted_files(self, event):
        """
        Files deleted or moved.

        """
        return (event.project == self.project.name and
                event.plugin == "filesystem" and
                event.fs_event in ('deleted', 'moved'))

    def removed_files_remove_todos(self, events:"deleted_files") -> plugin.Task:
        while True:
            event = yield from events.get()
            state = self.new_state(key=event.key)
            yield from self.hub.put(state)

    @asyncio.coroutine
    def collect_todos(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        while True:
            event = yield from events.get()
            filename = event.key
            content = str(event.content)
            todos = []
            for match in TODO_RE.finditer(content):
                data = match.groupdict()
                start, end = match.span()
                line = content.count('\n', 0, start) + 1
                row = start - content.rfind('\n', 0, start)
                length = end - start
                todos.append(dict(start=start, end=end, line=line, row=row,
                                  text=data['text'], type=data['type'].upper(),
                                  length=length))
            if todos:
                state = self.new_state(key=filename, todos=todos)

                highlights = [ self.message_to_highlight(message) for message in todos ]
                hl_state = self.new_state(content_type="highlight", key=filename,
                                          highlights=highlights)
            else:
                state = self.new_state(key=filename)
                hl_state = self.new_state(content_type="highlight", key=filename)

            yield from self.hub.put(state)

            if hl_state:
                yield from self.hub.put(hl_state)
