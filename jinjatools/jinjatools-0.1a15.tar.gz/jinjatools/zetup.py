from path import path as Path

import jinjatools


__path__ = [Path(jinjatools.__path__[0]).abspath().dirname()]

__file__ = __path__[0] / '__init__.py'

with __path__[0]:
    exec(open(__file__).read())
