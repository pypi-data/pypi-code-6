import pytest


def group_fixture(f_arg=None, **kwargs):
    def decorator(f):
        fixtures = f()

        @pytest.fixture(params=fixtures)
        def _(request):
            return request.getfuncargvalue(request.param)

        return _
    if f_arg is None:
        return decorator
    else:
        return decorator(f_arg)
