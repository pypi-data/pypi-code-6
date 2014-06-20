from abacus.util import resturl


def test_simple_restrul():
    assert resturl('/games/:id') == r'/games(?:/(\d+))?$'


def test_nested_resturl():
    assert resturl(
        '/games/:id/replies/:id') == r'/games/(\d+)/replies(?:/(\d+))?$'


def test_more_nested_resturl():
    assert resturl('/a/:id/b/:id/c/:id') == r'/a/(\d+)/b/(\d+)/c(?:/(\d+))?$'
