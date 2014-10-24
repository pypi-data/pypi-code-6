import pytest

from optional import fixture_optional


@fixture_optional
@pytest.fixture(params=[-1,0,1,2,3,4,5])
def number(request):
    return request.param


def test_power(number):
    """
        py.test.exclude(number,0)
    """
    assert number**2 >= number

def test_sqrt(number):
    """
        py.test.exclude(number,-1)
    """
    assert pow(number,0.5) <= number