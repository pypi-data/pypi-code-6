import asyncio
import logging
import re

from geoffrey import plugin
from geoffrey.data import EventType, datakey
from geoffrey.subscription import subscription
from geoffrey.utils import execute

MSG_TEMPLATE = ('{line}::{column}::{module}::{obj}::{msg}::{msg_id}::'
                '{symbol}::{C}::{category}')

MSG_REGEX = re.compile(('(?P<line>.*?)::(?P<column>.*?)::(?P<module>.*?)::'
             '(?P<obj>.*?)::(?P<msg>.*?)::(?P<msg_id>.*?)::(?P<symbol>.*?)::'
             '(?P<C>.*?)::(?P<category>.*?)'))

SCORE_REGEX = re.compile('Your code has been rated at (?P<score>.*?)/10')

CATEGORIES = {
    'R': 'Refactor',
    'C': 'Convention',
    'W': 'Warning',
    'E': 'Error',
    'F': 'Fatal',
}

CATEGORIES_TYPES = {
    'R': 'info',
    'C': 'info',
    'W': 'warning',
    'E': 'error',
    'F': 'error',
}



class PyLint(plugin.GeoffreyPlugin):
    """
    pylint plugin.

    """
    @staticmethod
    def message_to_highlight(message):
        return {"start_line": message['line'],
                "start_char": message['column'],
                "end_line": message['line'],
                "end_char": message['column'],
                "text": '{}({}): {}'.format(
                    CATEGORIES.get(message['C'], 'Other'),
                    message['msg_id'],
                    message['msg']),
                "link": "",
                "type": CATEGORIES_TYPES.get(message['C'], 'error')}

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
    def run_pylint(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        pylint_path = self.config.get(self._section_name, "pylint_path")
        while True:
            event = yield from events.get()
            filename = event.key

            exitcode, stdout, stderr = yield from execute(
                pylint_path, '--msg-template={}'.format(MSG_TEMPLATE),
                filename)

            output = stdout.decode('utf-8')

            messages = []
            for message in MSG_REGEX.finditer(output):
                values = message.groupdict()
                values['line'] = int(values.get('line', 0))
                values['column'] = int(values.get('column', 0))
                messages.append(values)

            score_match = SCORE_REGEX.search(output)
            if score_match:
                group = score_match.groupdict()
                score = float(group.get('score', 0.0))
            else:
                score = None

            state = self.new_state(key=filename,
                                   messages=messages,
                                   task="run_pylint",
                                   score=score)

            yield from self.hub.put(state)


    @subscription
    def pylint_analysis(self, event):
        """
        When pylint data is generated.

        """
        return (self.project.name == event.project and
                event.plugin == "pylint" and
                event.task == "run_pylint" and
                event.content_type == "data")

    @asyncio.coroutine
    def pylint_highlights(self, events:"pylint_analysis") -> plugin.Task:
        while True:
            event = yield from events.get()
            messages = event.messages or []

            # Highlight content_type
            state_data = {"content_type": "highlights",
                          "key": event.key,
                          "task": "pylint_highlights",
                         }
            highlights = []
            for message in messages:
                highlights.append(self.message_to_highlight(message))

            if highlights:
                state_data['highlights'] = highlights

            state = self.new_state(**state_data)

            yield from self.hub.put(state)

    @asyncio.coroutine
    def pylint_scores(self, events:"pylint_analysis") -> plugin.Task:
        from copy import copy
        while True:
            event = yield from events.get()
            new_score = event.score

            if new_score is None:  # Not removing history
                continue

            last_state = self.hub.get_one_state(datakey(
                key=event.key,
                content_type="data",
                project=self.project.name,
                plugin="pylint",
                task="pylint_scores"))

            if last_state is not None:
                scores = last_state.scores[-50:]
            else:
                scores = []

            scores.append(new_score)

            state = self.new_state(
                key=event.key,
                task="pylint_scores",
                scores=scores)

            yield from self.hub.put(state)
