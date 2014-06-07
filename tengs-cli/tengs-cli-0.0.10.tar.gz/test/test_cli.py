from tengs_cli import cli, actions
import sys

def test_parse_args(monkeypatch):
    monkeypatch.setattr("sys.exit", lambda x: x)
    parser = cli.parse_args(['-h', '--verbose'])
    assert parser.verbose

def test_login_call(monkeypatch, capsys):
    def login_mock(*args, **kwargs):
        print("login called")

    sys.argv = ["abc", "login", "name", "key"]
    monkeypatch.setattr("tengs_cli.actions.login", login_mock)

    cli.main()
    out, _err = capsys.readouterr()

    assert "login called" in out

def test_fetch_call(monkeypatch, capsys):
    def fetch_mock(*args, **kwargs):
        print("fetch called")

    sys.argv = ["abc", "fetch"]
    monkeypatch.setattr("tengs_cli.actions.fetch", fetch_mock)

    cli.main()
    out, _err = capsys.readouterr()

    assert "fetch called" in out

def test_submit_call(monkeypatch, capsys):
    def submit_mock(*args, **kwargs):
        print("submit called")

    sys.argv = ["abc", "submit"]
    monkeypatch.setattr("tengs_cli.actions.submit", submit_mock)

    cli.main()
    out, _err = capsys.readouterr()

    assert "submit called" in out
