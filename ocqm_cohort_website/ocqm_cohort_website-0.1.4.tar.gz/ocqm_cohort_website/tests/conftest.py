import pytest

from .. import paths


@pytest.yield_fixture()
def temp_directory():
    with paths.temporary_directory() as temp:
        with paths.switch_path(temp):
            yield temp
