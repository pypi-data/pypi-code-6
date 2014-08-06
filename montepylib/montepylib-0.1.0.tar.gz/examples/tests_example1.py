# you can run these tests with:
#   python tests.py
#
import os
import unittest

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

# if needed, add the parent directory to the path so the montepylib directory can be found
# os.sys.path.append(os.path.dirname(os.path.abspath('.')))
from montepylib.utils import assert_data_equal
import montepylib.extend

import example1


class Test1(unittest.TestCase):

    def setUp(self):
        data_path = 'data'
        # these could be defined in separate input files - not sure which is better
        self.data = example1.read_data()


    def test_sim(self):
        N = 1000
        totals = example1.simulate(self.data, N)
        # check the total num trees, fixed cost for the first 5 iterations
        for i in range(min(N,5)):
            self.assertTrue(all(totals['num trees'].ix[i]==self.data['num_trees']['num trees'].sum()))
            self.assertTrue(all(totals['fixed cost'].ix[i]==self.data['fixed_cost'].groupby('year').sum()['value']))
        # check the total profit is approximately right
        mean_profit_per_year = totals[['profit']].groupby(level='year').mean()
        base_case = example1.simulate(self.data, N=0)
        base_case_profit = base_case[['profit']].reset_index().set_index(['year']).drop('iteration',axis=1)
        rel_diff = abs(mean_profit_per_year - base_case_profit)/base_case_profit
        # assert that these diffs are small.  
        # The SDs are approx 15-20%, so expect rel SEM to be ~ 0.2/sqrt(N). Go out 5 SEMs to be safe.
        self.assertTrue(all(rel_diff < 5 * 0.2/np.sqrt(N)))

    def test_base_case(self):
        totals = example1.simulate(self.data, N=0)
        #print totals.command()  # use this command (added by montepylib.extend) to print out a line like the following
        target = DataFrame([[950., 680., 132500., 0.86, 22400., 4.7, 123400., 90000., 11000.], 
                            [950., 780., 155750., 0.86, 26380., 4.9, 151430., 90000., 35050.], 
                            [950., 880., 179000., 0.86, 30360., 5.08, 180680., 90000., 60320.], 
                            [950., 955., 197000., 0.86, 33420., 5.28, 206800., 90000., 83380.]], 
                            index=pd.MultiIndex.from_tuples([('base case', '{0}'.format(year)) for year in range(2014, 2018)], 
                                                            names=('iteration', 'year')),
                            columns=['num trees', 'fruit per tree', 'volume', 'cost per fruit', 'var cost', 
                                     'revenue per fruit', 'revenue', 'fixed cost', 'profit'])
        assert_data_equal(totals, target)

    def test_high_lows(self):
        totals = example1.simulate(self.data, N=-1)
        target = DataFrame([[0.86, 90000.0, 680.0, 950.0, 123400.0, 4.7, 22400.0, 132500.0, 11000.0],
                            [0.86, 90000.0, 780.0, 950.0, 151430.0, 4.9, 26380.0, 155750.0, 35050.0],
                            [0.86, 90000.0, 880.0, 950.0, 180680.0, 5.08, 30360.0, 179000.0, 60320.0],
                            [0.86, 90000.0, 955.0, 950.0, 206800.0, 5.28, 33420.0, 197000.0, 83380.0],
                            [0.86, 90000.0, 680.0, 950.0, 123400.0, 4.7, 22400.0, 132500.0, 11000.0],
                            [0.86, 90000.0, 780.0, 950.0, 151430.0, 4.9, 26380.0, 155750.0, 35050.0],
                            [0.86, 90000.0, 880.0, 950.0, 180680.0, 5.08, 30360.0, 179000.0, 60320.0],
                            [0.86, 90000.0, 955.0, 950.0, 206800.0, 5.28, 33420.0, 197000.0, 83380.0],
                            [0.86, 90000.0, 680.0, 950.0, 148080.0, 5.64, 22400.0, 132500.0, 35680.0],
                            [0.86, 90000.0, 780.0, 950.0, 181716.0, 5.88, 26380.0, 155750.0, 65336.0],
                            [0.86, 90000.0, 880.0, 950.0, 216816.0, 6.096, 30360.0, 179000.0, 96456.0],
                            [0.86, 90000.0, 955.0, 950.0, 248160.0, 6.336, 33420.0, 197000.0, 124740.0],
                            [0.86, 90000.0, 680.0, 950.0, 123400.0, 4.7, 22400.0, 132500.0, 11000.0],
                            [0.86, 90000.0, 780.0, 950.0, 151430.0, 4.9, 26380.0, 155750.0, 35050.0],
                            [0.86, 90000.0, 880.0, 950.0, 180680.0, 5.08, 30360.0, 179000.0, 60320.0],
                            [0.86, 90000.0, 955.0, 950.0, 206800.0, 5.28, 33420.0, 197000.0, 83380.0],
                            [0.86, 90000.0, 680.0, 950.0, 98720.0, 3.76, 22400.0, 132500.0, -13680.0],
                            [0.86, 90000.0, 780.0, 950.0, 121144.0, 3.92, 26380.0, 155750.0, 4764.0],
                            [0.86, 90000.0, 880.0, 950.0, 144544.0, 4.064, 30360.0, 179000.0, 24184.0],
                            [0.86, 90000.0, 955.0, 950.0, 165440.0, 4.224, 33420.0, 197000.0, 42020.0]],
                            index=pd.MultiIndex.from_tuples([(case_name, '{0}'.format(year)) 
                                        for case_name in ('base case','high fixed cost','high revenue per fruit', 'low fixed cost',
                                                          'low revenue per fruit') 
                                        for year in range(2014, 2018)], 
                            names=[u'iteration', u'year']), 
                            columns=['cost per fruit', 'fixed cost', 'fruit per tree', 'num trees', 'revenue', 'revenue per fruit', 
                                     'var cost', 'volume', 'profit'])
        assert_data_equal(totals, target)

def main():
    unittest.main()

if __name__ == "__main__":# and __package__ is None:
    main()
