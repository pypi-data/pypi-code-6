#!/usr/bin/env python
# coding: utf-8
# Simple interactive demo
import sys

from ytrans import YTranslator, read_key
from ytrans.utils import to_str, to_unicode

token_trim = lambda token: token.rstrip(" ").lstrip(" ").strip("\n")


def do_show_menu(aux_message=''):
    console.write_line("""
        %s
        c   -- Change the language
        d   -- Detect language
        m   -- Show this menu
        p   -- Get available primary languages
        r   -- Get available translations for a language code
        t   -- Translate content
        q   -- Exit the program
    """ % aux_message)


def do_lang_listing(ytrans):
    console.write_lines(ytrans.get_supported_primaries())


def do_supported_translations_from_lang(ytrans, lang):
    text = console.prompt(
        pre_text="Primary language, leave blank to use '%s" % lang)

    if text:
        lang = text

    results = ytrans.get_supported_translations(lang)
    if not results:
        console.write_line("No translations supported for %s" % lang)
    else:
        console.write_lines(results)


def do_detect_lang(ytrans):
    text = console.prompt(pre_text='Enter text to detect')
    console.write_line(ytrans.detect(text.strip('\n')))


def set_lang(ytrans, current_lang):
    lang_in = console.prompt(
        "\n[Current: %s. Enter language code eg ru:$> " % current_lang)
    if lang_in:
        current_lang = token_trim(lang_in)

    if not ytrans.is_valid_lang(current_lang):
        console.write("%s is an invalid language!" % current_lang)
        return None

    return current_lang


def do_translate(ytrans, lang, lines):
    tokens = [token_trim(token) for token in lines if token]
    console.write("Performing translation")
    translated = ytrans.translate(lang=lang, text_collection=tokens)
    if translated and tokens:
        console.write_line()
        for i, equiv in enumerate(translated):
            console.write_line("%s <=> %s" % (tokens[i], equiv))
            console.write_line()


def do_translation(ytrans, dest_lang):
    console.write_line("* Hit Ctrl-D to process *")
    console.write_line(" separated by 'Enter'")
    console.write("$> ")
    do_translate(ytrans, dest_lang, console.read().split('\n'))


def do_report_invalid_opt(opt_str):
    console.write_line("Invalid option: '%s'" % opt_str)


def do_exit():
    raise KeyboardInterrupt


class Console(object):
    _instance = None

    def __init__(self):
        raise Exception("Console class is Singleton!")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            instance = cls.__new__(cls)
            instance.set_stdin(sys.stdin)
            instance.set_stderr(sys.stderr)
            instance.set_stdout(sys.stdout)
            cls._instance = instance
        return cls._instance

    def set_stdin(self, stdin):
        self._stdin = stdin

    def set_stderr(self, stderr):
        self._stderr = stderr

    def set_stdout(self, stdout):
        self._stdout = stdout

    def write(self, text, *args, **kwargs):
        text = to_str(text)
        return self._stdout.write(text, *args, **kwargs) and self._stdout.flush()

    def write_line(self, text='', *args, **kwargs):
        return self.write("{}\n".format(text), *args, **kwargs)

    def write_lines(self, lines):
        for line in lines:
            self.write_line(line)

    def write_error(self, message):
        message = to_str(message)
        self._stderr.write(message)
        self._stderr.flush()

    def read(self):
        return self._stdin.read()

    def readline(self, strip=True):
        line = self._stdin.readline()
        return line.strip('\n') if strip else line

    def readlines(self):
        return self._stdin.readlines()

    def prompt(self, ps='$>', pre_text=''):
        self.write('%s %s ' % (pre_text, ps))
        return self.readline()


class CommandExecutor(object):
    """
    Register of commands
    """
    def __init__(self):
        self._actions = {}
        self._dependences = {}

    def add_command(self, name, action, *dependence):
        # if name is None register default command
        self._actions[name] = (action, dependence)

    def remove_command(self, name):
        assert name in self._actions,\
            "Command {} not found!".format(name)
        del self._actions[name]

    def set_dependences(self, **kwargs):
        self._dependences.update(kwargs)

    def process_command(self, command):
        items = self._actions.get(command)
        if items is None:
            items = self._actions.get(None)
        assert items is not None, "Invalid command!"

        action, dependence = items
        return action(*self._get_args(dependence))

    def _get_args(self, dependence):
        for d in dependence:
            assert d in self._dependences,\
                "Dependence {} not found!".format(d)
            yield self._dependences[d]


# console interface
console = Console.get_instance()

command_executor = CommandExecutor()
command_executor.add_command('d', do_detect_lang, 'translator')
command_executor.add_command('p', do_lang_listing, 'translator')
command_executor.add_command('r', do_supported_translations_from_lang, 'translator', 'lang')
command_executor.add_command('t', do_translation, 'translator', 'lang')
command_executor.add_command('m', do_show_menu, 'aux_message')
command_executor.add_command('q', do_exit)

# default case
command_executor.add_command(None, do_report_invalid_opt, 'opt_str')


def main():

    api_key = read_key()
    ytrans = YTranslator(api_key)
    lang = 'ru'
    command_executor.set_dependences(translator=ytrans, lang=lang)
    aux_message = "* Hit Ctrl-C to exit *. Target Language: '%s'"
    do_show_menu(aux_message % lang)

    while True:
        try:
            opt_str = console.prompt(pre_text='Enter your option') or '^'
            l_opt_ch = opt_str.lower()[0]
            if l_opt_ch == 'c':
                tmp = set_lang(ytrans, lang)
                if tmp:
                    lang = tmp
                    console.write_line("Language set to '%s'" % lang)
            else:
                command_executor.set_dependences(
                    lang=lang, opt_str=opt_str, aux_message=aux_message % lang)
                command_executor.process_command(l_opt_ch)

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.write_error('%s\n' % e)

    console.write_line("\nBye")


if __name__ == "__main__":
    main()
