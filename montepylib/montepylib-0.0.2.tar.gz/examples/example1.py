import os

from pandas import Series, DataFrame
import pandas as pd
#import matplotlib.pyplot as plt
#from prettyplotlib import plt

# add the parent directory to the path so the montepylib directory can be found
os.sys.path.append(os.path.dirname(os.path.abspath('.')))
import montepylib
from montepylib.io import excel_table_pos
from montepylib.manip import unpivot_int_cols, cross_merge
from montepylib.sim import Simulator
import montepylib.extend

import numpy as np

def read_data(data_path = 'data'):
    # Read num_trees, e.g.:
    #      farm  fruit       variety  num trees
    # 0  Farm A  apple  Granny Smith        100
    # 1  Farm A  apple      Jonathon        200
    # 2  Farm A   pear         Nashi         50
    # 3  Farm B  apple  Granny Smith        200
    # 4  Farm B  apple      Jonathon        400
    num_trees = pd.read_csv(os.path.join(data_path,'numTrees.csv'), comment='#', skipinitialspace=True)
    # To read from Excel worksheet, use:
    # (_, skiprows, _, skip_footer) = table_position('ABC Fruit Farms.xlsx', 'Sheet1', 'Number of trees')
    # num_trees_xl = pd.read_excel('ABC Fruit Farms.xlsx', 'Sheet1', skiprows=skiprows, skip_footer=skip_footer, header=0 )
    # num_trees_xl = pd.read_excel('ABC Fruit Farms.xlsx', 'Sheet1', skiprows=5, skip_footer=68, header=0 )
    # num_trees_xl = num_trees_xl.dropna(axis=1, how='all').fillna(method='ffill')
    # num_trees_xl.rename(columns=lambda x: x.lower(), inplace=True)
    # num_trees_xl.rename(columns={'number of trees':'num trees'}, inplace=True)


    # Read ann_mean_fruit_per_tree, e.g.:
    #      farm  fruit       variety  2014  2015  2016  2017
    # 0  Farm A  apple  Granny Smith   200   220   240   250
    # 1  Farm A  apple      Jonathon   150   175   200   225
    # 2  Farm A   pear         Nashi    50    55    60    60
    # 3  Farm B  apple  Granny Smith   160   180   200   220
    # 4  Farm B  apple      Jonathon   120   150   180   200
    ann_mean_fruit_per_tree = pd.read_csv(os.path.join(data_path,'meanFruitPerTree.csv'), comment='#', skipinitialspace=True)

    # Read SD of fruit_per_tree (a single value = fraction of the mean), e.g.:
    #      sd
    # 0  0.15
    sd_fruit_per_tree = pd.read_csv(os.path.join(data_path,'sdFruitPerTree.csv'), comment='#', skipinitialspace=True)
    sd_fruit_per_tree = sd_fruit_per_tree['sd'][0] # pull out the value, e.g. 0.15

    # Convert mean and sd dataframes to a single dataframe, fruit_per_tree, e.g.:
    #       farm  fruit       variety  year  mean     sd
    # 0   Farm A  apple  Granny Smith  2014   200  30.00
    # 1   Farm A  apple      Jonathon  2014   150  22.50
    # 2   Farm A   pear         Nashi  2014    50   7.50
    # 3   Farm B  apple  Granny Smith  2014   160  24.00
    # 4   Farm B  apple      Jonathon  2014   120  18.00
    # 5   Farm A  apple  Granny Smith  2015   220  33.00
    # 6   Farm A  apple      Jonathon  2015   175  26.25
    # 7   Farm A   pear         Nashi  2015    55   8.25
    # 8   Farm B  apple  Granny Smith  2015   180  27.00
    # 9   Farm B  apple      Jonathon  2015   150  22.50
    # ...
    fruit_per_tree = unpivot_int_cols(ann_mean_fruit_per_tree, 'year', 'mean')
    fruit_per_tree['sd'] = sd_fruit_per_tree * fruit_per_tree['mean']

    # Read ann_fixed_costs, e.g.:
    #           farm   2014   2015   2016   2017
    # 0       Farm A  30000  30000  30000  30000
    # 1  Head office  60000  60000  60000  60000
    ann_fixed_costs = pd.read_csv(os.path.join(data_path,'fixedCosts.csv'), comment='#', skipinitialspace=True)
    # And convert years to rows
    fixed_cost = unpivot_int_cols(ann_fixed_costs, 'year', 'value')  # value => single-valued

    # Read ann_var_costs_per_fruit, e.g.:
    #      farm  fruit  2014  2015  2016  2017
    # 0  Farm A  apple  0.15  0.15  0.15  0.15
    # 1  Farm A   pear  0.20  0.20  0.20  0.20
    # 2  Farm B  apple  0.18  0.18  0.18  0.18
    ann_var_costs_per_fruit = pd.read_csv(os.path.join(data_path,'varCostsPerFruit.csv'), comment='#', skipinitialspace=True)
    # And convert years to rows
    cost_per_fruit = unpivot_int_cols(ann_var_costs_per_fruit, 'year', 'cost per fruit')

    # Read ann_mean_revenue_per_fruit, e.g.:
    #    fruit       variety  2014  2015  2016  2017
    # 0  apple  Granny Smith  0.90  0.94  0.97  1.01
    # 1  apple      Jonathon  0.95  0.99  1.03  1.07
    # 2   pear         Nashi  1.00  1.04  1.08  1.12
    ann_mean_revenue_per_fruit = pd.read_csv(os.path.join(data_path,'meanRevenuePerFruit.csv'), comment='#', skipinitialspace=True)

    # Read SD of revenue per fruit (a single value = fraction of the mean), e.g.:
    #      sd
    # 0  0.20
    sd_revenue_per_fruit = pd.read_csv(os.path.join(data_path,'sdRevenuePerFruit.csv'), comment='#', skipinitialspace=True)
    sd_revenue_per_fruit = sd_revenue_per_fruit['sd'][0] # pull out the value, e.g. 0.15

    # Convert years to rows and add SD column
    revenue_per_fruit = unpivot_int_cols(ann_mean_revenue_per_fruit, 'year', 'mean')
    revenue_per_fruit['sd'] = sd_revenue_per_fruit * revenue_per_fruit['mean']

    return {'num_trees': num_trees, 
            'fruit_per_tree': fruit_per_tree, 
            'fixed_cost': fixed_cost,
            'cost_per_fruit': cost_per_fruit,
            'revenue_per_fruit': revenue_per_fruit,
            }



def simulate_vars(data, simulator, N):
    """
    Simulate and calculate quantities at farm x fruit x variety (x iteration x year) level.
    Returns a dictionary of simulated quantities.
    Eg.:
    >>> data = read_data()
    >>> simulator = Simulator()
    >>> simulate_vars(data, simulator, N=3)
    """
    # >>> sim_fruit_per_tree
    #       fruitPerTree    farm  fruit  iteration       variety  year
    # 0       211.002035  Farm A  apple          0  Granny Smith  2014
    # 1       154.822309  Farm A  apple          1  Granny Smith  2014
    # 2       163.184328  Farm A  apple          2  Granny Smith  2014
    # 3       156.258009  Farm A  apple          0      Jonathon  2014
    # 4       134.456564  Farm A  apple          1      Jonathon  2014
    # ...
    # >>> fixed_cost
    #           farm  year  value
    # 0       Farm A  2014  30000
    # 1  Head office  2014  60000
    # 2       Farm A  2015  30000
    # 3  Head office  2015  60000
    #
    # >>> sim_fixed_cost = sim_from_params(N, fixed_cost, 'fixed cost')
    #            farm  year  iteration  fixed cost
    # 0        Farm A  2014          0       30000
    # 1        Farm A  2014          1       30000
    # 2        Farm A  2015          0       30000
    # 3        Farm A  2015          1       30000
    # 8   Head office  2014          0       60000
    # 9   Head office  2014          1       60000
    # ...
    #
    # >>> sim_revenue_per_fruit
    #    fruit  iteration  revenue per fruit       variety  year
    # 0  apple          0           0.814296  Granny Smith  2014
    # 1  apple          1           0.898954  Granny Smith  2014
    # 2  apple          2           0.933524  Granny Smith  2014
    # 3  apple          0           1.225027      Jonathon  2014
    # 4  apple          1           1.344400      Jonathon  2014
    #
    # >>> sim_fruit
    #      farm  fruit       variety  num trees  fruit per tree  iteration  year    volume  cost per fruit  var cost  
    # 0  Farm A  apple  Granny Smith        100      188.401056          0  2014  18840.11            0.15  2826.016  
    # 1  Farm A  apple  Granny Smith        100      214.079587          1  2014  21407.96            0.15  3211.194  
    # 2  Farm A  apple  Granny Smith        100      239.373178          2  2014  23937.32            0.15  3590.598  
    # 3  Farm A  apple      Jonathon        200      161.186217          0  2014  64474.49            0.15  9671.173  
    # 4  Farm A  apple      Jonathon        200      135.182474          1  2014  54072.99            0.15  8110.948  
    # ...

    sim_fruit_per_tree = simulator.sim_from_params(N, data['fruit_per_tree'], 'fruit per tree')
    sim_fixed_cost = simulator.sim_from_params(N, data['fixed_cost'], 'fixed cost')
    sim_revenue_per_fruit = simulator.sim_from_params(N, data['revenue_per_fruit'], 'revenue per fruit')

    sim_fruit = simulator.merge(data['num_trees'], sim_fruit_per_tree, how='outer')
    sim_fruit['volume'] = sim_fruit['fruit per tree'] * sim_fruit['num trees']
    sim_var_cost = simulator.merge(sim_fruit, data['cost_per_fruit'])
    sim_var_cost['var cost'] = sim_var_cost['volume'] * sim_var_cost['cost per fruit']
    sim_revenue = simulator.merge(sim_revenue_per_fruit, sim_fruit)
    sim_revenue['revenue'] = sim_revenue['volume'] * sim_revenue['revenue per fruit']
    return {'sim_var_cost': sim_var_cost, 
            'sim_revenue': sim_revenue, 
            'sim_fixed_cost': sim_fixed_cost,
            }


def aggregate_cashflows(sims, simulator, discount_rate=None, base_year=None):
    """
    Aggregate up to the iteration x year level.
    Eg.:
    >>> data = read_data()
    >>> simulator = Simulator()
    >>> sims = simulate_vars(data, simulator, N=3)
    >>> aggregate_cashflows(sims, simulator)
    TBC
    """
    cashflows = simulator.merge(sims['sim_var_cost'], sims['sim_revenue'], how='outer')
    agg_cashflows = cashflows.groupby(['farm','year','iteration']).sum().reset_index()
    agg_cashflows = simulator.merge(agg_cashflows, sims['sim_fixed_cost'], how='outer').fillna(0)
    agg_cashflows['profit'] = agg_cashflows['revenue'] - agg_cashflows['fixed cost'] - agg_cashflows['var cost']
    agg_cashflows.drop(['fruit per tree', 'cost per fruit', 'revenue per fruit', 'num trees'], axis=1)
    total_per_iteration = agg_cashflows.groupby(['iteration', 'year']).sum()
    if discount_rate and base_year:
        total_per_iteration = total_per_iteration.reset_index()
        total_per_iteration['discount factor'] = 1/(discount_rate**(total_per_iteration['year'].apply(int)-base_year))
        total_per_iteration['discounted profit'] = total_per_iteration['discount factor'] * total_per_iteration['profit']
        total_per_iteration = total_per_iteration.set_index(['iteration','year'])
    return total_per_iteration

def simulate(data, N, discount_rate=None, base_year=None):
    """
    Package up the simulation and the aggregation, and calculate NPV.
    Given the data from read_data(), run the whole simulation and return total_per_iteration.
    >>> data = read_data()
    >>> total_per_iteration = simulate(data, N=1000)
    """
    simulator = Simulator()
    sims = simulate_vars(data, simulator, N)
    return aggregate_cashflows(sims, simulator, discount_rate, base_year)

def calc_NPVs(total_per_iteration):
    """
    Returns a DataFrame containing one simulated NPV per iteration.
    Expects as argument the output of simulate()
    Plot a histogram of NPV with eg.: 
    >>> calc_NPVs(total_per_iteration).hist(xrot=90)
    """
    return total_per_iteration.reset_index().groupby(['iteration'])[['discounted profit']].sum().rename(columns={'discounted profit':'NPV'})



def sim_output(total_per_iteration, N):
    """
    Example of some stats you can apply to the output of aggregate_cashflows()
    """
    # Display simulation results (N>0)
    print total_per_iteration.xs('2017', level='year').describe(percentile_width=80).T
    print (total_per_iteration.xs('2014', level='year')['profit']<=0).sum()/(N+.0)
    total_per_iteration.xs('2014', level='year')[['profit']].hist(xrot=90);


# to show sensitivities - when N = -1, just:
# print aggregate_cashflows(sims, simulator)

