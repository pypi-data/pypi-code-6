pytest_plugins = "kotti"

import os
import shutil

from pytest import fixture
from yurl import URL


class mocktransaction(object):
    def __init__(self, status):
        self.status = status


@fixture
def transactionmockup(monkeypatch):

    testtransaction = mocktransaction("Committing")
    monkeypatch.setattr(
        "transaction.get",
        lambda: testtransaction)


@fixture
def tmpdir(request):
    def rmdir():
        shutil.rmtree("/tmp/kotti_filestore")
    request.addfinalizer(rmdir)
    os.makedirs("/tmp/kotti_filestore", mode=0777)


@fixture
def filestore(tmpdir):
    from kotti_filestore import filestore
    return filestore(URL("foo:///tmp/kotti_filestore/"))
