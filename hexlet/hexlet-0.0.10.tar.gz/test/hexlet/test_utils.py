from hexlet import utils
import sys
import conftest


def test_new_version_available(monkeypatch):
    funcs = conftest.get_update_test_funcs("myproject", "1.1.0", "1.1.1")
    if sys.version_info > (3, 0):
        monkeypatch.setattr("xmlrpc.client.ServerProxy", funcs["get_new_ver_func"])
    else:
        monkeypatch.setattr("xmlrpclib.ServerProxy", funcs["get_new_ver_func"])
    monkeypatch.setattr("pip.get_installed_distributions", funcs["get_curr_ver_func"])

    res = utils.look_for_new_version("myproject")
    assert res == (True, "1.1.0", "1.1.1")


def test_new_version_not_available(monkeypatch):
    funcs = conftest.get_update_test_funcs("myproject", "1.1.0", "1.1.0")
    if sys.version_info > (3, 0):
        monkeypatch.setattr("xmlrpc.client.ServerProxy", funcs["get_new_ver_func"])
    else:
        monkeypatch.setattr("xmlrpclib.ServerProxy", funcs["get_new_ver_func"])
    monkeypatch.setattr("pip.get_installed_distributions", funcs["get_curr_ver_func"])

    res = utils.look_for_new_version("myproject")
    assert res == (False, "1.1.0", "1.1.0")


def test_new_version_failure(monkeypatch):
    funcs = conftest.get_update_test_funcs("myproject", "1.1.0", "1.1.0", True)
    if sys.version_info > (3, 0):
        monkeypatch.setattr("xmlrpc.client.ServerProxy", funcs["get_new_ver_func"])
    else:
        monkeypatch.setattr("xmlrpclib.ServerProxy", funcs["get_new_ver_func"])
    monkeypatch.setattr("pip.get_installed_distributions", funcs["get_curr_ver_func"])

    res = utils.look_for_new_version("myproject")
    assert res == (False, "1.1.0", "")


def test_build_key_value():
    d = {'a': {'b': 3, 'c': 2, 'd': [1, 2]}, 'x': ['1', '2', '3']}
    expected = {
        "a[b]": 3,
        "a[c]": 2,
        "a[d][0]": 1,
        "a[d][1]": 2,
        "x[0]": "1",
        "x[1]": "2",
        "x[2]": "3"
    }

    assert expected == utils.build_key_value(d)
