import json
from urlparse import urljoin

import requests
from json_pointer import Pointer
from behave import given, when, then

from ..main import app, Message


@given('a message')
def test_message(context):
    """
    Store a single test message in the database
    """
    with app.app_context():
        message = Message(
            json.loads(context.text)
        )

        message.save()


@when('I make a {method} request to "{path}"')
def make_request(context, method, path):
    """ Make a request to `path` using `method`. If this step contains
    text, use that as the body
    """
    func = getattr(requests, method.lower())

    args = {'headers': context.headers}
    if context.text:
        args['data'] = context.text

    context.response = func(
        urljoin(context.url, path),
        **args
    )


@when('I set the "{header}" header to "{value}"')
def set_header(context, header, value):
    """ Set the http header `header` to `value`"""
    context.headers[header] = value


@then('the response status should be {status}')
def status(context, status):
    """ Make sure the response status code is `status`"""
    assert context.response.status_code == int(status)


@then('the response data should be')
def data(context):
    """ Make sure the response body is equal to the text"""
    expected = json.loads(context.text)
    found = json.loads(context.response.content)
    assert expected == found


@then('"{pointer}" should contain "{value}"')
def contains(context, pointer, value):
    pointer = Pointer(pointer)

    data = json.loads(context.response.content)
    assert value == json.dumps(pointer.get(data))


@then('the size of "{pointer}" should be {value}')
def pointer_size(context, pointer, value):
    pointer = Pointer(pointer)

    data = json.loads(context.response.content)

    assert int(value) == len(pointer.get(data))


@then('the "{header}" header should be "{value}"')
def header(context, header, value):
    """ Make sure the response header `header` is equal to `value`"""
    assert context.response.headers[header] == value


@then('the "{relation}" relation should be "{url}"')
def relation(context, relation, url):
    """Make sure the link relation in the response is equal to `url`"""
    assert context.response.links[relation]['url'] == url
