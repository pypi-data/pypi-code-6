# you can run these tests with:
#   python tests.py
#
import os
import unittest
from numpy import sqrt, NaN, isnan, nan

from pandas import Series, DataFrame
import pandas as pd

# add the parent directory to the path so the montepylib directory can be found
os.sys.path.append(os.path.dirname(os.path.abspath('.')))
from montepylib.sim import Simulator
from montepylib.utils import assert_data_equal
import montepylib.extend # add .command() to DataFrame, useful while creating tests

# define some simple versions we'll use across lots of tests
fruit_per_tree = DataFrame([['Farm A','apple',200,30.0],
                                 ['Farm A','pear',50,7.5],
                                 ['Farm B','apple',160,24],
                                 ], 
                                columns=['farm','fruit','mean','sd'])
price_per_fruit = DataFrame([['apple',.9,.1],
                                 ['pear',1.04,.2],
                                 ], 
                                columns=['fruit','mean','sd'])
cost_per_fruit = DataFrame([['apple',.4,.1],
                                 ['pear',.5,.2],
                                 ], 
                                columns=['fruit','mean','sd'])


class TestSimulation(unittest.TestCase):

    def setUp(self):
        # define some more complex inputs
        self.fruit_per_tree = DataFrame([['Farm A','apple','Granny Smith',200,30.0],
                                         ['Farm A','apple','Jonathon',150,22.5],
                                         ['Farm A','pear','Nashi',50,7.5],
                                         ['Farm B','apple','Granny Smith',160,24],
                                         ['Farm B','apple','Jonathon',120,18],
                                         ], 
                                        columns=['farm','fruit','variety','mean','sd'])
        self.fixed_costs = DataFrame([['Farm A',30000],
                                         ['Head Office',60000],
                                         ], 
                                        columns=['farm','value'])
        self.exponential_costs = DataFrame([['Farm A',100],
                                         ['Farm B',600],
                                         ], 
                                        columns=['farm','scale'])
        self.price_per_fruit = DataFrame([['apple','Granny Smith',.9,.1],
                                         ['apple','Jonathon',.95,.1],
                                         ['pear','Nashi',1.04,.2],
                                         ], 
                                        columns=['fruit','variety','mean','sd'])

    def test_sim_normal(self):
        N = 30
        mc = Simulator('iter')
        sim = mc.sim_from_params(N, self.fruit_per_tree, 'val')
        # is it the right length?
        self.assertEqual(len(sim), N*len(self.fruit_per_tree))
        # does it have the 'val' and 'iter' columns?
        self.assertTrue('val' in sim.columns)
        self.assertTrue('iter' in sim.columns)
        # are there N iterations?
        self.assertEqual(len(sim.groupby('iter').mean()), N)
        # is the mean approximately right?
        keys = [col for col in sim.columns if col not in ['val','iter']]
        bounds = self.fruit_per_tree.set_index(keys)
        bounds['lower'] = bounds['mean'] - 5*bounds['sd']/sqrt(N)
        bounds['upper'] = bounds['mean'] + 5*bounds['sd']/sqrt(N)
        sim_means = sim.groupby(keys).mean()
        self.assertTrue(all(sim_means['val'] < bounds['upper']))
        self.assertTrue(all(sim_means['val'] > bounds['lower']))
        # are the parameter columns removed?
        self.assertFalse('mean' in sim.columns)
        self.assertFalse('sd' in sim.columns)

    def test_sim_single_value(self):
        N = 10
        mc = Simulator('iter')
        sim = mc.sim_from_params(N, self.fixed_costs, 'val')
        # is it the right length?
        self.assertEqual(len(sim), N*len(self.fixed_costs))
        # does it have the 'val' and 'iter' columns?
        self.assertTrue('val' in sim.columns)
        self.assertTrue('iter' in sim.columns)
        # are there N iterations?
        self.assertEqual(len(sim.groupby('iter').mean()), N)
        # are the values all constant? (ie same mean, 0 sd)
        keys = [col for col in sim.columns if col not in ['val','iter']]
        self.assertTrue(all(sim.groupby(keys).mean()['val']==self.fixed_costs.set_index(keys)['value']))
        self.assertTrue(all(sim.groupby(keys).std()['val']==0))

    def test_sim_exponential(self):
        N = 400
        mc = Simulator('iter')
        mc.add_dist(params=['scale'], dist='exponential', base_case='scale', low_case=lambda x: x.scale/2, high_case=lambda x:x.scale*1.5)
        sim = mc.sim_from_params(N, self.exponential_costs, 'val')
        # is it the right length?
        self.assertEqual(len(sim), N*len(self.exponential_costs))
        # does it have the 'val' and 'iter' columns?
        self.assertTrue('val' in sim.columns)
        self.assertTrue('iter' in sim.columns)
        # are there N iterations?
        self.assertEqual(len(sim.groupby('iter').mean()), N)
        # is the mean approximately right?
        keys = [col for col in sim.columns if col not in ['val','iter']]
        bounds = self.exponential_costs.set_index(keys)
        bounds['lower'] = bounds['scale'] - 5*bounds['scale']/sqrt(N)
        bounds['upper'] = bounds['scale'] + 5*bounds['scale']/sqrt(N)
        sim_means = sim.groupby(keys).mean()
        self.assertTrue(all(sim_means['val'] < bounds['upper']))
        self.assertTrue(all(sim_means['val'] > bounds['lower']))

    def test_sim_normal_base_case(self):
        N = 0
        mc = Simulator('iter', base_case_name='base')
        sim = mc.sim_from_params(N, self.fruit_per_tree, 'val')
        # is it the right length?
        self.assertEqual(len(sim), len(self.fruit_per_tree))
        # does it have the 'val' and 'iter' columns?
        self.assertTrue('val' in sim.columns)
        self.assertTrue('iter' in sim.columns)
        # are the iterations labelled properly?
        self.assertTrue(all(sim['iter']=='base'))
        # is the base case equal to the mean?
        self.assertTrue(all(sim['val'] == self.fruit_per_tree['mean']))
        # are the parameter columns removed?
        self.assertFalse('mean' in sim.columns)
        self.assertFalse('sd' in sim.columns)

    def test_sim_normal_high_low(self):
        N = -1
        mc = Simulator('iter', base_case_name='base', low_prefix='low ', high_prefix='high ')
        sim = mc.sim_from_params(N, self.fruit_per_tree, 'volume')
        #print sim
        # is it the right length? each original row should now be 3 (low/base/high cases)
        self.assertEqual(len(sim), len(self.fruit_per_tree)*3)
        # does it have the 'volume' and 'volume case' columns?
        self.assertTrue('volume' in sim.columns)
        self.assertTrue('volume case' in sim.columns)
        # are the iterations labelled properly?
        #self.assertTrue(all(sim['iter']=='base'))
        # is the base case equal to the mean?
        #self.assertTrue(all(sim['val'] == self.fruit_per_tree['mean']))
        # are the parameter columns removed?
        self.assertFalse('mean' in sim.columns)
        self.assertFalse('sd' in sim.columns)



class TestBaseCase(unittest.TestCase):

    def test_normal(self):
        N = 0
        mc = Simulator(iter_name='iteration', base_case_name='base case', sep=' ')
        sim_vol = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        cashflow = mc.merge(sim_vol, sim_price)
        cashflow['revenue'] = cashflow['volume'] * cashflow['price']
        target = DataFrame([['Farm A', 'apple', 200, 'base case', 0.9, 180.0], 
                            ['Farm B', 'apple', 160, 'base case', 0.9, 144.0], 
                            ['Farm A', 'pear', 50, 'base case', 1.04, 52.0]], 
                            columns=['farm', 'fruit', 'volume', 'iteration', 'price', 'revenue'])
        assert_data_equal(cashflow, target, index=['farm','fruit','iteration'])



class TestSensitivities(unittest.TestCase):

    def test_2_calc_one_way_sensitivities(self):
        N = -1
        mc = Simulator(iter_name='iteration', base_case_name='base case', low_prefix='low', high_prefix='high', case_suffix='case', sep=' ')
        sim_vol = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        scenarios = pd.merge(sim_vol, sim_price, how='outer')
        #print scenarios
        high_lows = mc.calc_one_way_sensitivities(scenarios)
        target = DataFrame([['Farm A', 'apple', 'base case', 0.9, 200.0], 
                            ['Farm B', 'apple', 'base case', 0.9, 160.0], 
                            ['Farm A', 'pear', 'base case', 1.04, 50.0], 
                            ['Farm A', 'apple', 'low price', 0.8, 200.0], 
                            ['Farm B', 'apple', 'low price', 0.8, 160.0], 
                            ['Farm A', 'pear', 'low price', 0.84, 50.0], 
                            ['Farm A', 'apple', 'high price', 1.0, 200.0], 
                            ['Farm B', 'apple', 'high price', 1.0, 160.0], 
                            ['Farm A', 'pear', 'high price', 1.24, 50.0], 
                            ['Farm A', 'apple', 'low volume', 0.9, 170.0], 
                            ['Farm B', 'apple', 'low volume', 0.9, 136.0], 
                            ['Farm A', 'pear', 'low volume', 1.04, 42.5], 
                            ['Farm A', 'apple', 'high volume', 0.9, 230.0], 
                            ['Farm B', 'apple', 'high volume', 0.9, 184.0], 
                            ['Farm A', 'pear', 'high volume', 1.04, 57.5]], 
                            columns=['farm', 'fruit', 'iteration', 'price', 'volume'])
        assert_data_equal(high_lows, target, index=['iteration','farm','fruit'])
        # test that mc.merge does the same thing
        high_lows2 = mc.merge(sim_vol, sim_price, how='outer')
        assert_data_equal(high_lows2, target, index=['iteration','farm','fruit'])

    def test_3_calc_one_way_sensitivities(self):
        N = -1
        mc = Simulator(iter_name='iteration', base_case_name='base case', low_prefix='low', high_prefix='high', case_suffix='case', sep=' ')
        sim_vol = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        sim_cost = mc.sim_from_params(N, cost_per_fruit, 'cost')
        scenarios = pd.merge(sim_vol, sim_price, how='outer')
        high_lows = mc.calc_one_way_sensitivities(scenarios)
        # now we want to add another case to it:
        scenarios3_seq = pd.merge(high_lows, sim_cost, how='outer')
        # this replicates the high_lows dataframe, with a low cost/base case/high cost column.
        high_lows3_seq = mc.calc_one_way_sensitivities(scenarios3_seq)
        target = DataFrame([[0.4, 'Farm A', 'apple', 'base case', 0.9, 200.0], 
                            [0.4, 'Farm B', 'apple', 'base case', 0.9, 160.0], 
                            [0.5, 'Farm A', 'pear', 'base case', 1.04, 50.0], 
                            [0.3, 'Farm A', 'apple', 'low cost', 0.9, 200.0], 
                            [0.3, 'Farm B', 'apple', 'low cost', 0.9, 160.0], 
                            [0.3, 'Farm A', 'pear', 'low cost', 1.04, 50.0], 
                            [0.5, 'Farm A', 'apple', 'high cost', 0.9, 200.0], 
                            [0.5, 'Farm B', 'apple', 'high cost', 0.9, 160.0], 
                            [0.7, 'Farm A', 'pear', 'high cost', 1.04, 50.0], 
                            [0.4, 'Farm A', 'apple', 'low price', 0.8, 200.0], 
                            [0.4, 'Farm B', 'apple', 'low price', 0.8, 160.0], 
                            [0.4, 'Farm A', 'apple', 'low volume', 0.9, 170.0], 
                            [0.4, 'Farm B', 'apple', 'low volume', 0.9, 136.0], 
                            [0.5, 'Farm A', 'pear', 'low price', 0.84, 50.0], 
                            [0.5, 'Farm A', 'pear', 'low volume', 1.04, 42.5], 
                            [0.4, 'Farm A', 'apple', 'high price', 1.0, 200.0], 
                            [0.4, 'Farm B', 'apple', 'high price', 1.0, 160.0], 
                            [0.4, 'Farm A', 'apple', 'high volume', 0.9, 230.0], 
                            [0.4, 'Farm B', 'apple', 'high volume', 0.9, 184.0], 
                            [0.5, 'Farm A', 'pear', 'high price', 1.24, 50.0], 
                            [0.5, 'Farm A', 'pear', 'high volume', 1.04, 57.5]],
                            columns=['cost', 'farm', 'fruit', 'iteration', 'price', 'volume'])
        assert_data_equal(high_lows3_seq, target, index=['iteration','farm','fruit'])
        scenarios3_at_once = pd.merge(scenarios, sim_cost, how='outer')
        high_lows3_at_once = mc.calc_one_way_sensitivities(scenarios3_at_once)
        assert_data_equal(high_lows3_at_once, target, index=['iteration','farm','fruit'])
        # test that mc.merge does the same thing
        high_lows3_merge = mc.merge(sim_vol, sim_price, sim_cost, how='outer')
        assert_data_equal(high_lows3_merge, target, index=['iteration','farm','fruit'])


    def test_2_calc_one_way_sensitivities_with_one_outer(self):
        # one case has NaNs - check it works
        fruit_per_tree = DataFrame([['Farm A',200,30.0]], columns=['farm','mean','sd'])
        fixed_costs = DataFrame([['Farm A',100,10],['Admin',300,20]], columns=['farm','mean','sd'])
        N = -1
        mc = Simulator(iter_name='iteration', base_case_name='base case', low_prefix='low', high_prefix='high', case_suffix='case', sep=' ')
        sim_vol = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_fixed_cost = mc.sim_from_params(N, fixed_costs, 'fixed cost')
        scenarios = pd.merge(sim_vol, sim_fixed_cost, how='outer')
        # scenarios looks like:
        #       farm  volume case  volume  fixed cost case  fixed cost
        # 0   Farm A   low volume     170   low fixed cost          90
        # 1   Farm A   low volume     170        base case         100
        # 2   Farm A   low volume     170  high fixed cost         110
        # 3   Farm A    base case     200   low fixed cost          90
        # 4   Farm A    base case     200        base case         100
        # 5   Farm A    base case     200  high fixed cost         110
        # 6   Farm A  high volume     230   low fixed cost          90
        # 7   Farm A  high volume     230        base case         100
        # 8   Farm A  high volume     230  high fixed cost         110
        # 9    Admin          NaN     NaN   low fixed cost         280
        # 10   Admin          NaN     NaN        base case         300
        # 11   Admin          NaN     NaN  high fixed cost         320
        high_lows = mc.calc_one_way_sensitivities(scenarios)
        target = DataFrame([['Farm A', 100.0, 'base case', 200.0], 
                            ['Admin', 300.0, 'base case', nan], 
                            ['Admin', 300.0, 'high volume', nan], 
                            ['Admin', 300.0, 'low volume', nan], 
                            ['Farm A', 90.0, 'low fixed cost', 200.0], 
                            ['Admin', 280.0, 'low fixed cost', nan], 
                            ['Farm A', 110.0, 'high fixed cost', 200.0], 
                            ['Admin', 320.0, 'high fixed cost', nan], 
                            ['Farm A', 100.0, 'low volume', 170.0], 
                            ['Farm A', 100.0, 'high volume', 230.0]],
                            columns=['farm', 'fixed cost', 'iteration', 'volume'])
        assert_data_equal(high_lows, target, index=['iteration','farm'])

    def test_2_calc_one_way_sensitivities_with_both_outer(self):
        # both cases have NaNs - check it works
        fruit_per_tree = DataFrame([['Farm A',200,30.0]], columns=['farm','mean','sd'])
        fixed_costs = DataFrame([['Admin',300,20]], columns=['farm','mean','sd'])
        N = -1
        mc = Simulator(iter_name='iteration', base_case_name='base case', low_prefix='low', high_prefix='high', case_suffix='case', sep=' ')
        sim_vol = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_fixed_cost = mc.sim_from_params(N, fixed_costs, 'fixed cost')
        scenarios = pd.merge(sim_vol, sim_fixed_cost, how='outer')
        # scenarios looks like:
        #      farm  volume case  volume  fixed cost case  fixed cost
        # 0  Farm A   low volume     170              NaN         NaN
        # 1  Farm A    base case     200              NaN         NaN
        # 2  Farm A  high volume     230              NaN         NaN
        # 3   Admin          NaN     NaN   low fixed cost         280
        # 4   Admin          NaN     NaN        base case         300
        # 5   Admin          NaN     NaN  high fixed cost         320
        high_lows = mc.calc_one_way_sensitivities(scenarios)
        target = DataFrame([['Farm A', nan, 'base case', 200.0], 
                            ['Admin', 300.0, 'base case', nan], 
                            ['Admin', 300.0, 'high volume', nan], 
                            ['Admin', 300.0, 'low volume', nan], 
                            ['Farm A', nan, 'low fixed cost', 200.0], 
                            ['Farm A', nan, 'high fixed cost', 200.0], 
                            ['Admin', 280.0, 'low fixed cost', nan], 
                            ['Admin', 320.0, 'high fixed cost', nan], 
                            ['Farm A', nan, 'low volume', 170.0], 
                            ['Farm A', nan, 'high volume', 230.0]], 
                            columns=['farm', 'fixed cost', 'iteration', 'volume'])
        assert_data_equal(high_lows, target, index=['iteration','farm'])
        # a more dramatic test is that you can now repeat the outer merge:
        price = DataFrame([['Farm B',50,5]], columns=['farm','mean','sd'])
        sim_price = mc.sim_from_params(N, price, 'price')
        scenarios3 = pd.merge(high_lows, sim_price, how='outer')
        high_lows3 = mc.calc_one_way_sensitivities(scenarios3)
        target3 = DataFrame([['Farm A', nan, 'base case', nan, 200.0],
                            ['Admin', 300.0, 'base case', nan, nan],
                            ['Farm B', nan, 'base case', 50.0, nan],
                            ['Farm B', nan, 'low fixed cost', 50.0, nan],
                            ['Farm B', nan, 'low volume', 50.0, nan],
                            ['Farm B', nan, 'high fixed cost', 50.0, nan],
                            ['Farm B', nan, 'high volume', 50.0, nan],
                            ['Farm A', nan, 'high price', nan, 200.0],
                            ['Admin', 300.0, 'high price', nan, nan],
                            ['Farm A', nan, 'low price', nan, 200.0],
                            ['Admin', 300.0, 'low price', nan, nan],
                            ['Farm B', nan, 'low price', 45.0, nan],
                            ['Farm B', nan, 'high price', 55.0, nan],
                            ['Farm A', nan, 'low fixed cost', nan, 200.0],
                            ['Farm A', nan, 'low volume', nan, 170.0],
                            ['Admin', 300.0, 'low volume', nan, nan],
                            ['Admin', 280.0, 'low fixed cost', nan, nan],
                            ['Farm A', nan, 'high fixed cost', nan, 200.0],
                            ['Farm A', nan, 'high volume', nan, 230.0],
                            ['Admin', 300.0, 'high volume', nan, nan],
                            ['Admin', 320.0, 'high fixed cost', nan, nan]],
                            columns=['farm', 'fixed cost', 'iteration', 'price', 'volume'])        
        assert_data_equal(high_lows3, target3, index=['iteration','farm'])


    def test_sim_merge_on_simple_sim(self):
        N = 4
        fruit_per_tree = DataFrame([['Farm A','apple',200,30.0]], columns=['farm','fruit','mean','sd'])
        price_per_fruit = DataFrame([['apple',1,.2]], columns=['fruit','mean','sd'])
        mc = Simulator('iteration')
        sim_fruit = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        merge1 = pd.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        merge2 = mc.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        self.assertEqual(len(merge1), N)  # because no extra rows are created in this test
        assert_data_equal(merge1, merge2)
        for i in range(N):
            self.assertEqual(merge1.ix['Farm A','apple',i]['price'], sim_price.set_index(['fruit','iteration']).ix['apple',i]['price'])
            self.assertEqual(merge1.ix['Farm A','apple',i]['volume'], 
                             sim_fruit.set_index(['farm','fruit','iteration']).ix['Farm A','apple',i]['volume'])

    def test_sim_merge_with_NaN(self):
        N = 4
        fruit_per_tree = DataFrame([['Farm A','apple',200,30.0]], columns=['farm','fruit','mean','sd'])
        price_per_fruit = DataFrame([['apple',1,.2],['pear',3,.2]], columns=['fruit','mean','sd'])
        mc = Simulator('iteration')
        sim_fruit = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        merge1 = pd.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        merge2 = mc.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        self.assertEqual(len(merge1), N*2)  # because an extra set of rows are created in this test
        assert_data_equal(merge1, merge2)
        for i in range(N):
            self.assertEqual(merge1.ix['Farm A','apple',i]['price'], sim_price.set_index(['fruit','iteration']).ix['apple',i]['price'])
            self.assertEqual(merge1.ix['Farm A','apple',i]['volume'], 
                             sim_fruit.set_index(['farm','fruit','iteration']).ix['Farm A','apple',i]['volume'])

    def test_sim_merge_with_two_farms(self):
        N = 4
        fruit_per_tree = DataFrame([['Farm A','apple',200,30.0],['Farm B','apple',100,10.0]], columns=['farm','fruit','mean','sd'])
        price_per_fruit = DataFrame([['apple',1,.2],['pear',3,.2]], columns=['fruit','mean','sd'])
        mc = Simulator('iteration')
        sim_fruit = mc.sim_from_params(N, fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, price_per_fruit, 'price')
        merge1 = pd.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        merge2 = mc.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','iteration'])
        self.assertEqual(len(merge1), N*3)  # N from Farm A apple, N from farm B apple, and N from nan-farm pear
        assert_data_equal(merge1, merge2)
        for i in range(N):
            self.assertEqual(merge1.ix['Farm A','apple',i]['price'], sim_price.set_index(['fruit','iteration']).ix['apple',i]['price'])
            self.assertEqual(merge1.ix['Farm A','apple',i]['volume'], 
                             sim_fruit.set_index(['farm','fruit','iteration']).ix['Farm A','apple',i]['volume'])

    def test_sim_merge_on_sim_complex(self):
        N = 4
        mc = Simulator('iteration')
        self.fruit_per_tree = DataFrame([['Farm A','apple','Granny Smith',200,30.0],
                                         ['Farm A','apple','Jonathon',150,22.5],
                                         ['Farm A','pear','Nashi',50,7.5],
                                         ['Farm B','apple','Granny Smith',160,24],
                                         ['Farm B','apple','Jonathon',120,18],
                                         ], 
                                        columns=['farm','fruit','variety','mean','sd'])
        self.price_per_fruit = DataFrame([['apple','Granny Smith',.9,.1],
                                         ['apple','Jonathon',.95,.1],
                                         ['pear','Nashi',1.04,.2],
                                         ], 
                                        columns=['fruit','variety','mean','sd'])
        sim_fruit = mc.sim_from_params(N, self.fruit_per_tree, 'volume')
        sim_price = mc.sim_from_params(N, self.price_per_fruit, 'price')
        #print pd.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','variety','iteration']).sort()
        merge1 = pd.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','variety','iteration'])
        merge2 = mc.merge(sim_fruit, sim_price, how='outer').set_index(['farm','fruit','variety','iteration'])
        self.assertEqual(len(merge1), N*5)  # three varieties at Farm A and two at Farm B
        assert_data_equal(merge1, merge2)
        for i in range(N):
            self.assertEqual(merge1.ix['Farm A','apple','Jonathon',i]['price'], 
                             sim_price.set_index(['fruit','variety','iteration']).ix['apple','Jonathon',i]['price'])
            self.assertEqual(merge1.ix['Farm A','apple','Jonathon',i]['volume'], 
                             sim_fruit.set_index(['farm','fruit','variety','iteration']).ix['Farm A','apple','Jonathon',i]['volume'])
        


def main():
    unittest.main()

if __name__ == "__main__":# and __package__ is None:
    main()
