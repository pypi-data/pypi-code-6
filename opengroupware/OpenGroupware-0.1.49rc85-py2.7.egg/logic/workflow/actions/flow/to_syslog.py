#
# Copyright (c) 2014
#   Adam Tauno Williams <awilliam@whitemice.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE
#
import syslog
from coils.core import CoilsException
from coils.core.logic import ActionCommand

MESSAGE_LEVEL = {
    'emergency': syslog.LOG_EMERG,
    'alert':     syslog.LOG_ALERT,
    'critical':  syslog.LOG_CRIT,
    'error':     syslog.LOG_ERR,
    'warning':   syslog.LOG_WARNING,
    'notice':    syslog.LOG_NOTICE,
    'info':      syslog.LOG_INFO,
    'debug':     syslog.LOG_DEBUG,
}

MESSAGE_FACILITY = {
    'kernel':         syslog.LOG_KERN,
    'user':           syslog.LOG_USER,
    'mail':           syslog.LOG_MAIL,
    'daemon':         syslog.LOG_DAEMON,
    'authentication': syslog.LOG_AUTH,
    'print':          syslog.LOG_LPR,
    'news':           syslog.LOG_NEWS,
    'uucp':           syslog.LOG_UUCP,
    'cron':           syslog.LOG_CRON,
    'syslog':         syslog.LOG_SYSLOG,
    'local0':         syslog.LOG_LOCAL0,
    'local1':         syslog.LOG_LOCAL1,
    'local2':         syslog.LOG_LOCAL2,
    'local3':         syslog.LOG_LOCAL3,
    'local4':         syslog.LOG_LOCAL4,
    'local5':         syslog.LOG_LOCAL5,
    'local6':         syslog.LOG_LOCAL6,
    'local7':         syslog.LOG_LOCAL7,
}


class SysLogMessageAction(ActionCommand):
    __domain__ = "action"
    __operation__ = "send-to-syslog"
    __aliases__ = ['syslog', 'syslogAction', ]
    mode = None

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        syslog.openlog(
            logoption=syslog.LOG_PID,
            facility=self._message_facility,
        )
        syslog.syslog(
            self._message_level,
            self._message_text,
        )
        syslog.closelog()

    def parse_action_parameters(self):

        self._message_text = self.process_label_substitutions(
            self.action_parameters.get('message', '')
        )

        self._message_level = MESSAGE_LEVEL.get(
            self.process_label_substitutions(
                self.action_parameters.get('level', 'info')
            ).lower(),
            None,
        )
        if self._message_level is None:
            raise CoilsException(
                'Unknown message level "{0}" specified for syslogAction'.
                format(
                    self.action_parameters.get('level', None),
                )
            )

        self._message_facility = MESSAGE_FACILITY.get(
            self.process_label_substitutions(
                self.action_parameters.get('facility', 'daemon')
            ).lower(),
            None,
        )
        if self._message_facility is None:
            raise CoilsException(
                'Unknown message facility "{0}" specified for syslogAction'.
                format(
                    self.action_parameters.get('facility', None),
                )
            )

    def do_epilogue(self):
        pass
