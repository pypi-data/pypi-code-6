# -*- coding: utf-8 -*-

from api import ApiTwip
from twipy import version
from adapter import Adapter, CliAdapter
import keys
import re

COMMAND_HELP_TEXT = """Command helps\n
ht:\tGets the user's timeline
v:\tPrints the version
h:\tPrints help commands
u:\tWrite u <text> to update your status
rp:\tWrite rp <id_number> <text> to reply a status. The <id_number> has to be between 0 and 19
\tDon't forget to include the user name with the '@'
m:\tGet your mentions, included RT
rt:\tRetweet a tweet with rt <id_number>. The <id_number> has to be between 0 and 19
dm:\tWrite dm @<screen_name> <text>. Don't forget to write the "@"
fv:\tWrite fv to get your favorite tweets or add one to your list with fv <id_number>
q:\tExits
"""

COMMAND_TIMELINE = ['ht']
COMMAND_VERSION = ['v']
COMMAND_EXIT = ['q']
COMMAND_HELP = ['h']
COMMAND_UPDATE = ['u']
COMMAND_REPLY = ['rp']
COMMAND_MENTIONS = ['m']
COMMAND_RT = ['rt']
COMMAND_DM = ['dm']
COMMAND_FV = ['fv']

REG_EXP_COMMAND_RP = '[^0-9]{1,2}'


class Command():

    def __init__(self):
        self._command = None
        self._api = ApiTwip(keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
        self._adapter = Adapter()
        self._timeline = None

    def dispatch(self, command):
        self._command = command

        if self._command in COMMAND_TIMELINE:
            content = self._api.get_home_time_line()  # pragma: no cover
            if content:
                self._timeline = self._adapter.create_timeline_object(content)  # pragma: no cover

                cli_adapter = CliAdapter(self._timeline)  # pragma: no cover
                cli_adapter.get_statuses()  # pragma: no cover

        elif self._command in COMMAND_VERSION:
            print version  # pragma: no cover

        elif self._command in COMMAND_EXIT:
            pass  # pragma: no cover

        elif self._command in COMMAND_HELP:
            print COMMAND_HELP_TEXT  # pragma: no cover

        elif self._command in COMMAND_MENTIONS:
            content = self._api.get_mentions()  # pragma: no cover

            if content:
                self._timeline = self._adapter.create_timeline_object(content)  # pragma: no cover

                cli_adapter = CliAdapter(self._timeline)  # pragma: no cover
                cli_adapter.get_statuses()

        elif len(self._command) > 2:
            com = self._command[:2].strip()
            text = self._command[2:].strip()
            self._send_info(com, text)

        else:
            print COMMAND_HELP_TEXT

    def _send_info(self, com, text):
        if com in COMMAND_UPDATE:
            self._api.update_status(text)

        elif com in COMMAND_REPLY:
            if not self._timeline:
                print 'Timeline is empty. Execute first "ht" or "m" command'
                return

            cli_adapter = CliAdapter(self._timeline)

            c_id = text[:2].strip()
            text = text[2:]
            if not reg_exp_only_numbers(c_id):
                print 'Bad reply id. Only numbers between 0 and 19'
                return

            c_id = int(c_id)
            if c_id < 0 or c_id > 19:
                print 'Bad reply id. Range: 0..19'
                return

            status = cli_adapter.get_status_from_id(c_id)
            self._api.update_status(text=text, reply_to=status.id_str)

        elif com in COMMAND_RT:
            c_id = self._command[2:].strip()

            if not reg_exp_only_numbers(c_id):
                print 'Bad tweet id. Range 0..19'
                return

            if not self._timeline:
                print 'Timeline is empty. Execute first "ht" or "m" command'
                return

            c_id = int(c_id)
            if c_id < 0 or c_id > 19:
                print 'Bad reply id. Range: 0..19'
                return

            cli_adapter = CliAdapter(self._timeline)
            status = cli_adapter.get_status_from_id(c_id)
            self._api.retweet(tweet_id=status.id_str)

        elif com in COMMAND_FV:
            if not self._timeline:
                print 'Timeline is empty. Execute first "ht" or "m" command'
                return

            cli_adapter = CliAdapter(self._timeline)
            c_id = text[:2].strip()
            text = text[2:]
            if not reg_exp_only_numbers(c_id):
                print 'Bad favorite id. Only numbers between 0 and 19'
                return

            c_id = int(c_id)
            if c_id < 0 or c_id > 19:
                print 'Bad favorite id. Range: 0..19'
                return

            status = cli_adapter.get_status_from_id(c_id)
            self._api.create_fav(tweet_id=status.id_str)

        elif com in COMMAND_DM:
            temp_text = text.split(' ')

            if len(temp_text) < 2:
                print 'Ups! Something wrong with the dm command. Did you write the @<screen user name> and the <text>?'
                return

            if -1 == temp_text[0].find('@') or len(temp_text[0]) < 2:
                print 'I don\'t know who I will send the message. Please add the "@" to the twitter user name'
                return

            screen_name = temp_text[0].strip()
            screen_name = screen_name[1:]
            text = text[len(screen_name)+1:].strip()

            self._api.send_direct_message(text=text, screen_name=screen_name)


def reg_exp_only_numbers(n):
    r = re.findall(REG_EXP_COMMAND_RP, n)
    if r:
        return False
    return True
