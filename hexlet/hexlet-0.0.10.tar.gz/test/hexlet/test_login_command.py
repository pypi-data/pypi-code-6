import responses
import click, i18n
from click.testing import CliRunner

import hexlet
import hexlet.commands.lesson as lesson
import conftest
import hexlet.routes as routes


@responses.activate
def test_success_login():
    url = routes.api_teacher_check_auth_url()
    responses.add(responses.GET, url, status=200)

    runner = CliRunner()
    #FIXME
    with runner.isolated_filesystem():
        args = ['login', 'a']
        result = runner.invoke(lesson.cli, args)
        assert not result.exception
        assert result.output
        assert result.exit_code == 0

def test_login_with_invalid_credentials(monkeypatch):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=403))

    runner = CliRunner()
    args = ['login', 'a']
    result = runner.invoke(lesson.cli, args)
    assert result.exception
    assert result.output
    assert result.exit_code != 0

def test_login_with_server_error(monkeypatch):
    monkeypatch.setattr("requests.get", conftest.prepare_request_mock(status_code=500))

    runner = CliRunner()
    args = ['login', 'a']
    result = runner.invoke(lesson.cli, args)
    assert result.exception
    assert result.output
    assert result.exit_code != 0
