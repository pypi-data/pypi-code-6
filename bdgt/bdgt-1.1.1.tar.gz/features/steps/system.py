import os

from behave import given, then
from nose.tools import eq_


@given('a file named "{fname}" with')
def step_create_file(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    if os.path.exists(fname):
        raise ValueError("{} already exists".format(fname))

    with open(fname, 'w') as f:
        f.write(context.text)
    context.test_data_files.append(fname)


@given("a file named '{fname}' doesn't exist")
def step_file_doesnt_exist(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)
    assert not os.path.exists(fname)


@given("a file named '{fname}' exists")
def step_file_exists(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)
    assert os.path.exists(fname)


@then("a file named '{fname}' was created")
def step_a_file_was_created(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    if os.path.exists(fname):
        context.test_data_files.append(fname)
    else:
        assert False


@then("a file named '{fname}' was deleted")
def step_a_file_was_deleted(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    if fname in context.test_data_files:
        context.test_data_files.remove(fname)
    assert not os.path.exists(fname)


@then("the content of the file '{fname}' equals")
def step_file_content_contains(context, fname):
    if '~' in fname:
        fname = os.path.expanduser(fname)

    assert os.path.exists(fname)

    with open(fname, "r") as f:
        data = f.read()

    eq_(data, context.text)
