from functools import partial
from collections import namedtuple

from os.path import isfile, isdir
from os import chdir
from shutil import rmtree

from tengs_cli import actions, logger, settings
from conftest import get_request_mock, json_mock, popen_mock

log = partial(logger, "debug")

def test_login_ok(monkeypatch):
    LoginStruct = namedtuple("LoginStruct", "tengs_api_key github_name")
    args = LoginStruct(tengs_api_key="key", github_name="name")

    monkeypatch.setattr("requests.get", get_request_mock(code=200))
    assert actions.login(args, log)


def test_login_failure(monkeypatch):
    LoginStruct = namedtuple("LoginStruct", "tengs_api_key github_name")
    args = LoginStruct(tengs_api_key="key", github_name="name")

    monkeypatch.setattr("requests.get", get_request_mock(code=500))
    assert not actions.login(args, log)


def test_fetch_ok(monkeypatch):
    LoginStruct = namedtuple("LoginStruct", "tengs_api_key github_name")
    loginArgs = LoginStruct(tengs_api_key="key", github_name="name")

    monkeypatch.setattr("requests.get", get_request_mock(code=200))
    assert actions.login(loginArgs, log)

    if isdir("%s/base_http" % settings.tengs_path):
        rmtree("%s/base_http" % settings.tengs_path)

    monkeypatch.setattr("requests.get", json_mock)
    actions.fetch({}, log)
    assert isfile("%s/base_http/http_parser/file1.txt" % settings.tengs_path)


def test_submit_ok(monkeypatch, capsys):
    chdir("%s/base_http/http_parser" % settings.tengs_path)

    monkeypatch.setattr("subprocess.Popen", popen_mock)
    monkeypatch.setattr("requests.post", get_request_mock(code=201))

    actions.submit({}, log)
    out, _err = capsys.readouterr()
    assert "Exercise has been submitted. Check this one on the site." in out
