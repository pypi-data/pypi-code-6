from __future__ import print_function

from fuf import ActionSet

def test_realworld():
    # Create a simple action set
    action = ActionSet()


    # Full decorator
    # Nothing is gathered implicitly
    @action("help", "List command help")
    def action_help(*args):
        "List command help"
        if args:
            for arg in args:
                if arg in action:
                    print("{0.name}:\t{0.helpmsg}".format(action[arg]))
        else:
            print("Available commands:", ", ".join(a for a in action))


    # Partially applied
    # The name is specified, but the help is pulled from the docstring
    @action("verify")
    def action_verify():
        "Confirm access"
        print("Authentication valid")


    # Implicit
    # The name of the command and the help are pulled from
    # the function name and docstring
    @action
    def say(*args):
        "Say a message"
        print(" ".join(args))


def test_basic():
    action = ActionSet()

    @action
    def add(x, y):
        return float(x)+float(y)

    @action
    def sub(x, y):
        return float(x)-float(y)

    assert action.perform("sub 2 5") == -3, "Basic subtraction failed"

def test_env():
    action = ActionSet()

    @action
    def add(data, x):
        return data["x"] + int(x)

    data = {}
    data["x"] = 10
    assert action.perform("add 5", data) == 15, "Environment failed"
    data["x"] = 5
    assert action.perform("add 5", data) == 10, "Environment updating failed"
