import readline
import shlex
import sys

from functools import partial

from .configparser import JSONConfigParser
from .utils import call, command, root, __registry

__prompt = "JSON >>> "
__sort = True
__exit = False


class ValueStore:
    # A crutch to lean on for now.
    '''
    Generic object to store values on, there needs to be a better way to
    bridge the gap between argparse's storing on an object and actually
    wanting a dictionary.
    '''
    def __init__(self):
        self.multi = False
        self.path = root
        self.convert = False

def autocomplete(text, state):
    actions = [c for c in sorted(__registry.keys()) if c.startswith(text)]

    if state > len(actions):
        return None
    return actions[state]

def interpret(action):
    action, *arguments = shlex.split(action)
    args = ValueStore()

    if action == 'shell':
        raise NotImplementedError("Can't spawn shell from inside shell.")

    for idx, item in enumerate(arguments):
        if item.startswith(root):
            args.path = item
        elif any(m in item for m in ['-m', '--multi']):
            args.multi = True
        elif any(o in item for o in ['-o', '--other']):
            args.other = arguments[idx+1]
        elif any(c in item for c in ['-c', '--convert']):
            args.convert = arguments[idx+1]
        elif any(v in item for v in ['-v', '--value']):
            args.value = arguments[idx+1]

    return partial(call, fname=action, source=args)



def run(json):
    global __exit, __prompt

    readline.set_completer_delims("\t")
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    while True:
        action = ""
        
        try:
            line = input("{}".format(__prompt)).strip()
        except KeyboardInterrupt:
            if __exit:
                sys.exit(0)
            else:
                print("Press ^C again to quit. Otherwise run another command.")
                __exit = True
                continue

        if not line:
            continue
        
        try:
            interpret(line)(json=json)
        except (NotImplementedError, TypeError,
                AttributeError, ValueError) as e:
            print(e)

        __exit = False
