import collections as col
import decorator as de
import pytest
import re




@de.decorator
def fixture_optional(fun, req, *args, **kwargs):
    """ decorator over pytest fixture, which make fixture optional, depending on value of parameters.
        Fixture must be decorated by fixture_optional, to be skipped when criteria not met.

        Criteria a defined in docstring of test function, eg.

        py.test.expect(id_allowed_client,1)
        or
        py.test.exclude(id_allowed_client,1)
    """
    _fname = req.node.name.split("[")[0]
    _doc = req.module.__dict__[_fname].__doc__

    if _doc:
        _reqs = col.defaultdict(list)
        for key,val in re.findall("py.test.expect\((.*?),(.*?)\)",_doc):
            _reqs[key].append(val)

        for key,vals in _reqs.items():
            val = str(req.node.callspec.params[key])
            if p not in vals:
                pytest.skip("skipping {parm}={val}. Not in {allowed!r}".\
                                            format(parm=key,val=val,allowed=vals))

        for key,val in re.findall("py.test.exclude\((.*?),(.*?)\)",_doc):
            if str(req.node.callspec.params[key]) == val:
                pytest.skip("skipping/ignoring {p}={v}".format(p=key,v=val))

    return fun(req,*args,**kwargs)

