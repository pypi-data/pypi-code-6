import json
import re
from urlparse import urljoin

import requests
from json_pointer import Pointer
from pytest_bdd import scenario, given, when, then

from .main import app, Message


@scenario('resource.feature', 'Retrieve non-existing message')
def test_retrieve_non_existing():
    pass

@scenario('resource.feature', 'Retrieve existing message')
def test_retrieve():
    pass


@scenario('resource.feature', 'Delete a message')
def test_delete():
    pass


@scenario('resource.feature', 'Get after delete message')
def test_get_after_delete():
    pass


@scenario('resource.feature', 'Delete a non-existing message')
def test_delete_non_existing():
    pass


@scenario('resource.feature', 'PUT a message')
def test_put():
    pass


@scenario('resource.feature', 'PUT a non-existing message')
def test_put_non_existing():
    pass


@scenario('resource.feature', 'PUT an invalid message')
def test_put_invalid_message():
    pass


@scenario('resource.feature', 'PUT an invalid json')
def test_put_invalid_json():
    pass


@scenario('resource.feature', 'POST a message')
def test_post():
    pass


@scenario('resource.feature', 'POST a message that already exists')
def test_post_existing():
    pass


@scenario('resource.feature', 'POST an invalid message')
def test_post_invalid_message():
    pass


@scenario('resource.feature', 'POST an invalid json message')
def test_post_invalid_json():
    pass


@scenario('collection.feature', 'Retrieve all message')
def test_retrieve_all():
    pass


@given('access to the message API')
def context():
    class Context(object):
        pass

    context = Context()
    context.session = requests.session()
    return context


@given(re.compile(r'an existing message: (?P<text>.+)'))
def message(text):
    """
    Store a single test message in the database
    """
    with app.app_context():
        message = Message(
            json.loads(text)
        )

        message.save()


@when(re.compile(r'I insert a message: (?P<text>.+)'))
def message_insert(text):
    message(text)


@when(re.compile('I set the "(?P<header>.+)" header to "(?P<value>.+)"'))
def set_header(context, header, value):
    """ Set the http header `header` to `value`"""
    context.session.headers.update({header: value})


@when(re.compile('I make a (?P<method>.+) request to "(?P<path>(\S+))" with data: (?P<data>.+)'))
def api_request_with_data(api_server, context, method, path, data):
    """ Make a request to `path` using `method`. If this step contains
    text, use that as the body
    """
    func = getattr(context.session, method.lower())

    context.response = func(urljoin(api_server.url, path), data=data)


@when(re.compile('I make a (?P<method>.+) request to "(?P<path>(\S+))"$'))
def api_request(api_server, context, method, path):
    """ Make a request to `path` using `method`.
    """
    api_request_with_data(api_server, context, method, path, None)


@then(re.compile('the response status should be (?P<status>\d+)'))
def status(context, status):
    """ Make sure the response status code is `status`"""
    assert context.response.status_code == int(status)


@then(re.compile('the response data should be: (?P<data>.+)'))
def data(context, data):
    """ Make sure the response body is equal to the text"""
    expected = json.loads(data)
    found = json.loads(context.response.content)
    assert expected == found


@then(re.compile('"(?P<pointer>.+)" should contain "(?P<value>.+)"'))
def contains(context, pointer, value):
    pointer = Pointer(pointer)

    data = json.loads(context.response.content)
    assert value == json.dumps(pointer.get(data))


@then(re.compile('the size of "(?P<pointer>.+)" should be (?P<value>.+)'))
def pointer_size(context, pointer, value):
    pointer = Pointer(pointer)

    data = json.loads(context.response.content)

    assert int(value) == len(pointer.get(data))


@then(re.compile('the "(?P<header>.+)" header should be "(?P<value>.+)"'))
def header(context, header, value):
    """ Make sure the response header `header` is equal to `value`"""
    assert context.response.headers[header] == value


@then(re.compile('the "(?P<relation>.+)" relation should be "(?P<url>.+)"'))
def relation(context, relation, url):
    """Make sure the link relation in the response is equal to `url`"""
    assert context.response.links[relation]['url'] == url
