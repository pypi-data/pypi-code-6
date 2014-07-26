import logging
import asyncio

from geoffrey import plugin
from geoffrey.utils import execute, parse_checkstyle
from geoffrey.subscription import subscription


CATEGORIES = {"warning": "Warning",
              "error": "Error"}

class CssLint(plugin.GeoffreyPlugin):
    """
    csslint plugin.

    TODO: Change this class name to FullCamelCase

    """

    @staticmethod
    def message_to_highlight(message):
        return {"start_line": message['line'],
                "start_char": message['column'],
                "end_line": message['line'],
                "end_char": message['column'],
                "text": '{}: {}'.format(
                    CATEGORIES.get(message['severity'], 'Other'),
                    message['message']),
                "link": "",
                "type": CATEGORIES.get(message['severity'], 'error').lower()}

    @subscription
    def modified_files(self, event):
        """
        Subscription criteria.

        Should be used as annotation of plugin.Tasks arguments.
        Can be used multiple times.

        """
        return (self.project.name == event.project and
                event.plugin == "filesystem" and
                event.key.endswith('.css'))

    @asyncio.coroutine
    def run_csslint(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        csslint_path = self.config.get(self._section_name, "csslint_path")
        while True:
            event = yield from events.get()
            self.log.debug("Event received in plugin `csslint`")

            filename = event.key
            exitcode, stdout, stderr = yield from execute(csslint_path, '--format=checkstyle-xml', filename)

            data = parse_checkstyle(stdout)
            if data:
                state = self.new_state(key=filename, data=data)
                highlights = [ self.message_to_highlight(message) for message in data ]
                hl_state = self.new_state(content_type="highlight", key=filename,
                                      highlights=highlights)
            else:
                state = self.new_state(key=filename)
                hl_state = self.new_state(content_type="highlight", key=filename)

            yield from self.hub.put(state)
            yield from self.hub.put(hl_state)
