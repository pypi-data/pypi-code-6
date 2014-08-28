import code
import readline
import rlcompleter
import sys

frame = sys._getframe(1)
vars = frame.f_globals
vars.update(frame.f_locals)
del(frame)

class debugme: exit = True
vars['debugme'] = debugme()

readline.set_completer(rlcompleter.Completer(vars).complete)
readline.parse_and_bind("tab: complete")
shell = code.InteractiveConsole(vars)
shell.interact()
if vars['debugme'].exit:
    sys.exit(1)
