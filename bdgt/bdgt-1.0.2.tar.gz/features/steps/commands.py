import string

from behave import then, when
from nose.tools import ok_


@when('I run "{command}"')
def step_run_command(context, command):
    context.cmd_output = context.cmd_line.run(command)


@then('the command output should contain')
def step_output_contains(context):
    output = context.cmd_output.strip()
    ok_(context.text in output)


@then('the command output should equal')
def step_output_equals(context):
    output = context.cmd_output.strip()
    output = ''.join([c for c in output if c in string.printable])
    ok_(context.text == output)
