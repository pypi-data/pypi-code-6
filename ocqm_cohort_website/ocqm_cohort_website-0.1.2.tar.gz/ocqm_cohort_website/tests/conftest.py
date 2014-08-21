import os
import pytest
import shutil
import tempfile


@pytest.yield_fixture()
def temp_directory():
    temp = tempfile.mkdtemp()
    current = os.getcwd()

    os.chdir(temp)
    yield temp
    os.chdir(current)

    shutil.rmtree(temp)
