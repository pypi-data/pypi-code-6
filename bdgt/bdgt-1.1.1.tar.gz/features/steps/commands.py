import string

from behave import then, when
from nose.tools import eq_, ok_


@when('I run "{command}"')
def step_run_command(context, command):
    exit_code, output = context.cmd_line.run(command)
    context.cmd_output = output
    context.cmd_exit_code = exit_code


@then('the command output should contain')
def step_output_contains(context):
    output = context.cmd_output.strip()
    ok_(context.text in output)


@then('the command output should equal')
def step_output_equals(context):
    output = context.cmd_output.strip()
    output = ''.join([c for c in output if c in string.printable])
    ok_(context.text == output)


@then('the command exit code should be {exit_code:n}')
def step_exit_code_equals(context, exit_code):
    eq_(context.cmd_exit_code, exit_code)
