import httpretty
from sure import expect

from retain import Retaincc


@httpretty.activate
def test_create_user():
    httpretty.register_uri(
        httpretty.POST, "https://app.retain.cc/api/v1/users",
        body='{"user_id": 10}',
        content_type="application/json")

    response = Retaincc.create_user(user_id=10)
    expect(response).to.equal({'user_id': 10})


@httpretty.activate
def test_get_user():
    httpretty.register_uri(
        httpretty.GET, "https://app.retain.cc/api/v1/users?user_id=10",
        body='{"user_id": 10}',
        content_type="application/json")

    response = Retaincc.get_user(user_id=10)
    expect(response).to.equal({'user_id': 10})


@httpretty.activate
def test_update_user():
    httpretty.register_uri(
        httpretty.PUT, "https://app.retain.cc/api/v1/users",
        body='{"user_id": 10}',
        content_type="application/json")

    response = Retaincc.update_user(user_id=10)
    expect(response).to.equal({'user_id': 10})


@httpretty.activate
def test_delete_user():
    httpretty.register_uri(
        httpretty.DELETE, "https://app.retain.cc/api/v1/users?user_id=10",
        body='true',
        content_type="application/json")

    response = Retaincc.delete_user(user_id=10)
    expect(response).to.equal(True)
