import re
import sys
import logging
import asyncio

from collections import defaultdict

from geoffrey import plugin
from geoffrey.utils import execute, slugify
from geoffrey.subscription import subscription


def num_message(message):
    """ Parse messages containing a number and a message """

    split_message = message.split(maxsplit=1)
    return (int(split_message[0]), split_message[1][1:-1])


PARSE_INDEX = {'unpack': num_message,
               'unpack_dir': num_message,
               'setup.py': num_message,
               'install': num_message,
               'generated_files': num_message,
               'INSTALLABILITY INDEX (ABSOLUTE)': int,
               'INSTALLABILITY INDEX (RELATIVE)': num_message,
               'required_files': num_message,
               'docstrings': num_message,
               'formatted_docstrings': num_message,
               'formatted_docstrings': num_message,
               'DOCUMENTATION INDEX (ABSOLUTE)': int,
               'DOCUMENTATION INDEX (RELATIVE)': num_message,
               'unit_tested': num_message,
               'pylint': num_message,
               'CODE KWALITEE INDEX (ABSOLUTE)': int,
               'CODE KWALITEE INDEX (RELATIVE)': num_message,
               'OVERALL CHEESECAKE INDEX (ABSOLUTE)': int,
               'OVERALL CHEESECAKE INDEX (RELATIVE)': num_message
              }

LINE_SPLIT = re.compile(r'(.*)\s\.+\s+(.*)')

class CheeseCake(plugin.GeoffreyPlugin):
    """
    cheesecake plugin.

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
                event.plugin == "filesystem" and
                event.key.endswith('.tar.gz'))

    def parse_output(self, output):
        """ Parse CheeseCake output """
        data = defaultdict(list) 
        for line in output.splitlines():
            if line:
                line_string = line.decode(sys.stdout.encoding)
                if line_string[0].isalpha():
                    line_info = LINE_SPLIT.match(line_string).groups()
                    data_key = slugify(line_info[0]).replace('__', '_')
                    data[data_key] = PARSE_INDEX[line_info[0]](line_info[1])
                elif line_string.startswith('['):
                    line_info = line_string.split(']')
                    data[line_info[0][1:]].append(line_info[1].strip())
                    
        return data

    @asyncio.coroutine
    def run_cheesecake(self, events:"modified_files") -> plugin.Task:
        """
        Main plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        cheesecake_path = self.config.get(self._section_name, "cheesecake_path")

        while True:
            event = yield from events.get()
            filename = event.key

            exitcode, stdout, stderr = yield from execute(cheesecake_path, '-v', '-p', filename)

            data = self.parse_output(stdout)
            self.log.debug("Event received in plugin `cheesecake`")

            state = self.new_state(key=filename, **data)

            yield from self.hub.put(state)
