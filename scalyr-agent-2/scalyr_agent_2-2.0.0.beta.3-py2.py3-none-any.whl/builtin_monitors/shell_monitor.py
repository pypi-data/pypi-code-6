# Copyright 2014, Scalyr, Inc.
#
# A ScalyrMonitor which executes a specified shell command and records the output.

import re
import os

from scalyr_agent.scalyr_monitor import ScalyrMonitor


# Pattern that matches the first line of a string
first_line_pattern = re.compile('[^\r\n]+')


# ShellMonitor implementation
class ShellMonitor(ScalyrMonitor):
    """A Scalyr agent monitor which executes a specified shell command, and records the output.
    """

    def _initialize(self):
        # Fetch and validate our configuration options.
        self.command = self._config.get("command", required_field=True)
        self.max_characters = self._config.get("max_characters", default=200, convert_to=int, min_value=0,
                                               max_value=10000)
        self.log_all_lines = self._config.get("log_all_lines", default=False)

        extract_expression = self._config.get("extract", default="")
        if extract_expression:
            self.extractor = re.compile(extract_expression)
            
            # Verify that the extract expression contains a matching group, i.e. a parenthesized clause.
            # We perform a quick-and-dirty test here, which will work for most regular expressions.
            # If we miss a bad expression, it will result in a stack trace being logged when the monitor
            # executes.
            if extract_expression.find("(") < 0:
                raise Exception("extract expression [%s] must contain a matching group" % (extract_expression))
        else:
            self.extractor = None

    def gather_sample(self):
        # Run the command
        command = self.command
        stdin, stdout, stderr = os.popen3(command)
        stdout_text = stdout.read()
        stderr_text = stderr.read()
        stdin.close()
        stdout.close()
        stderr.close()

        output = stderr_text
        if len(stderr_text) > 0 and len(stdout_text) > 0:
            output += "\n"
        output += stdout_text

        # Apply any extraction pattern
        if self.extractor is not None:
            match = self.extractor.search(output)
            if match is not None:
                output = match.group(1)

        # Apply log_all_lines and max_characters, and record the result.
        if self.log_all_lines:
            s = output
        else:
            first_line = first_line_pattern.search(output)
            s = ''
            if first_line is not None:
                s = first_line.group().strip()

        if len(s) > self.max_characters:
            s = s[:self.max_characters] + "..."
        self._logger.emit_value('output', s, extra_fields={'command': self.command, 'length': len(output)})
