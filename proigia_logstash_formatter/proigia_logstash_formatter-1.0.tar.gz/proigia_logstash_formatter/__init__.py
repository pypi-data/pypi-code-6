"""This module will implement a formattor for logstash v1 format."""
import json

import logstash_formatter

# Needed for Formatter Patch
import datetime
import traceback as tb


class ProigiaLogstashFormatter(logstash_formatter.LogstashFormatterV1):

    """\

    Version fo the logstash formatter to output the log messages in json.

    This formatter will convert the incoming log message in a json format
    that can be used by logstash.
    This version fixes some of the issues found in the original version.

    """

    def format(self, record):
        """\

        Override the format function.

        For the most part a copy from the original except some
        additional handling to get the message right iso msg.

        """
        fields = record.__dict__.copy()

        # Custom addition start
        if isinstance(record.msg, dict):
            fields.update(record.msg)
            fields.pop('msg')
            msg = ""
        else:
            msg = record.getMessage()

        if 'msg' in fields:
            fields.pop('msg')

        if 'message' in fields:
            fields.pop('message')

        if 'args' in fields:
            fields.pop('args')

        # Custom addition end

        if 'exc_info' in fields:
            if fields['exc_info']:
                formatted = tb.format_exception(*fields['exc_info'])
                fields['exception'] = formatted
            fields.pop('exc_info')

        if 'exc_text' in fields and not fields['exc_text']:
            fields.pop('exc_text')

        now = datetime.datetime.utcnow()
        base_log = {'@timestamp': now.strftime("%Y-%m-%dT%H:%M:%S") +
                    ".%03d" % (now.microsecond / 1000) + "Z",
                    '@version': 1,
                    'source_host': self.source_host,
                    # Custom addition start
                    'message': msg
                    # Custom addition end
                    }
        base_log.update(fields)

        logr = self.defaults.copy()
        logr.update(base_log)

        json_dict = json.dumps(logr, default=self.json_default,
                               cls=self.json_cls)

        return json_dict
