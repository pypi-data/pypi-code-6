# -*- coding: utf-8 -*-

import argparse
import dialog
import sys


class ArgparseActionWrapper(object):
    action_classes = {
        'help': argparse._HelpAction,
        'version': argparse._VersionAction,
        'store': argparse._StoreAction,
        'store_const': argparse._StoreConstAction,
        'store_true': argparse._StoreTrueAction,
        'store_false': argparse._StoreFalseAction,
        'append': argparse._AppendAction,
        'append_const': argparse._AppendConstAction,
        'count': argparse._CountAction,
    }

    def __init__(self, dialog, action):
        self._dialog = dialog
        self._action = action

    def __getattr__(self, name):
        return getattr(self._action, name)

    @property
    def dialog_help(self):
        if self.help and self.option_string:
            return '%s (%s)' % (self.help, self.option_string)
        elif self.help:
            return self.help
        elif self.option_string:
            return self.option_string
        else:
            return self.dest

    @property
    def option_string(self):
        if self.option_strings:
            return self.option_strings[-1]
        return None

    @property
    def max_values(self):
        if self.nargs == '?':
            return 1
        elif isinstance(self.nargs, int):
            return self.nargs
        elif self.nargs in ('*', '+', argparse.REMAINDER):
            return None
        return 1

    @property
    def no_dialog(self):
        return not bool(self._dialog)

    @property
    def is_help(self):
        return self._is_action('help')

    @property
    def is_version(self):
        return self._is_action('version')

    @property
    def is_one_value(self):
        return self._is_action('store') and self.nargs is None and not self.choices

    @property
    def is_multi_value(self):
        return self._is_action('store') and self.nargs is not None and not self.choices

    @property
    def is_one_choice(self):
        return self._is_action('store') and self.choices

    @property
    def is_multi_chocies(self):
        return self._is_action('append') and self.choices

    @property
    def is_flag(self):
        return self._is_action('store_const', 'store_true', 'store_false')

    @property
    def is_count(self):
        return self._is_action('count')

    def _is_action(self, *actions):
        classes = tuple(self.action_classes[action] for action in actions)
        return isinstance(self._action, classes)


class ArgumentParser(argparse.ArgumentParser):
    width = 60

    def __init__(self, *args, **kwds):
        self._should_show_intro = kwds.pop('show_intro', False)
        self._dialog = None  # __init__ calls add_argument which needs this property.
        super(ArgumentParser, self).__init__(*args, **kwds)
        self._dialog = self._create_dialog()

    def _create_dialog(self):
        d = dialog.Dialog()
        d.set_background_title(self.prog)
        return d

    def add_argument(self, *args, **kwds):
        no_dialog = kwds.pop('no_dialog', False)
        argument = super(ArgumentParser, self).add_argument(*args, **kwds)
        argument = ArgparseActionWrapper(None if no_dialog else self._dialog, argument)
        self._actions[-1] = argument
        return argument

    def parse_args(self, args=None):
        if len(sys.argv) == 1:
            args = self.get_args()
        return super(ArgumentParser, self).parse_args(args)

    def get_args(self):
        result = []

        self._show_intro()

        for action in self._actions:
            if action.is_help or action.is_version or action.no_dialog:
                continue
            elif action.is_one_value:
                result.extend(self._get_values_by_dialog(action))
            elif action.is_multi_value:
                result.extend(self._get_values_by_dialog(action))
            elif action.is_one_choice:
                result.extend(self._get_choice_by_dialog(action))
            elif action.is_multi_chocies:
                result.extend(self._get_choices_by_dialog(action))
            elif action.is_flag:
                result.extend(self._get_flag_by_dialog(action))
            elif action.is_count:
                result.extend(self._get_count_by_dialog(action))

        return result

    def _show_intro(self):
        if not self._should_show_intro:
            return

        self._dialog.msgbox(
            'This is wizzard of %s.\nYou can also use command line arguments if you don\'t like wizzards.\n\n%s\n\n%s' % (
                self.prog,
                self.description or '',
                self.epilog or '',
            ),
            height=15,
            width=self.width,
        )

    def _get_values_by_dialog(self, action):
        default = ''
        if isinstance(action.default, str):
            default = action.default

        result = []
        if action.option_string:
            result.append(action.option_string)
        index, max_index = 1, action.max_values

        while True:
            code, answer = self._dialog.inputbox(
                '%s\n\n%d. value (of %s)\nEnd adding entry by button cancel.' % (
                    action.dialog_help,
                    index,
                    max_index or 'unlimited',
                ) if max_index is None or max_index > 1 else action.dialog_help,
                init=default,
                height=12,
                width=self.width,
            )
            if code == self._dialog.OK:
                result.append(answer)
            if code != self._dialog.OK or index == max_index:
                return result

            index += 1

    def _get_choice_by_dialog(self, action):
        code, tag = self._dialog.menu(
            action.dialog_help,
            height=10+len(action.choices),
            menu_height=len(action.choices),
            width=self.width,
            choices=[(str(idx), str(item)) for idx, item in enumerate(action.choices)],
        )
        if code != self._dialog.OK:
            return[]
        return action.option_string, action.choices[int(tag)]

    def _get_choices_by_dialog(self, action):
        code, tags = self._dialog.checklist(
            action.dialog_help,
            height=10+len(action.choices),
            list_height=len(action.choices),
            width=self.width,
            choices=[(str(idx), str(item), False) for idx, item in enumerate(action.choices)],
        )
        if code != self._dialog.OK:
            return[]
        tags = [action.choices[int(tag)] for tag in tags]
        if action.option_string:
            for x in range(len(tags)):
                tags.insert(x*2, action.option_string)
        return tags

    def _get_flag_by_dialog(self, action):
        code = self._dialog.yesno(
            action.dialog_help,
            width=self.width,
        )
        if code != self._dialog.OK:
            return []
        return [action.option_string]

    def _get_count_by_dialog(self, action):
        code, answer = self._dialog.menu(
            action.dialog_help,
            height=15,
            menu_height=5,
            width=self.width,
            choices=[(str(index), ' '.join([action.option_string] * index)) for index in range(1, 6)]
        )
        if code != self._dialog.OK:
            return[]
        return [action.option_string] * int(answer)
