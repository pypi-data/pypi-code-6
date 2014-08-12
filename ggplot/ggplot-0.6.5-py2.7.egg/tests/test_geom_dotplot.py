from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import unittest
from ggplot import *

from . import get_assert_same_ggplot, cleanup
assert_same_ggplot = get_assert_same_ggplot(__file__)

class TestDotPlot(unittest.TestCase):

    @cleaup
    def test_geom_dotplot_hist(self):
        gg = ggplot(aes(x='price'), data=diamonds.head(1000))
        gg += geom_dotplot()
        assert_same_ggplot(gg, 'geom_dotplot_hist')
    
    @cleaup
    def test_geom_dotplot_bar(self):
        gg = ggplot(aes(x='factor(cyl)'), data=mtcars)
        gg += geom_dotplot()
        assert_same_ggplot(gg, 'geom_dotplot_bar')

if __name__ == '__main__':
    unittest.main()
