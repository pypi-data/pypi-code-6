#
# Routines to simulate with DataFrames
#

from numpy import random
from pandas import Series, DataFrame
import pandas as pd

from collections import namedtuple

# dist_params is a list of tuples, with element:
#  0: the parameters to be found in the input table
#  1: distribution name, a string looked up as an attribute of numpy.random
#  2: the parameters to pass on to the distribution, or None if no change
#  3: a processing function which converts input params to distr. params, 
#     or None for no change
#

class BadParamsException(Exception):
    pass

class NoParamsException(Exception):
    pass

_DistType = namedtuple("DistType", "params dist base_case low_case high_case post_params process")

# two helper functions to make it easier to return the base case or special cases
def _field_fn(fieldname):
    return lambda x: x[fieldname]

def _special_case(dist_type, field, x, value_name):
    """
    Eg. add a base case value under the column name 'price' to the DataFrame row x by calling
    _special_case('base_case', sim._dist_types[0], x, 'price')
    The first parameter should be one of 'base_case', 'low_case' or 'high_case'.
    """
    x[value_name] = getattr(dist_type, field)(x)
    return x

def _convertValueToUniform(x):
    x['low'] = x['value']
    x['high'] = x['value']
    return x

class Simulator(object):
    def __init__(self, iter_name='iteration', 
                       base_case_name='base case', 
                       low_prefix='low', 
                       high_prefix='high', 
                       case_suffix='case',
                       sep=' ',
                       use_defaults=True):
        self._dist_types = []
        self.iter_name = iter_name
        self.base_case_name = base_case_name
        self.low_prefix = low_prefix
        self.high_prefix = high_prefix
        self.case_suffix = case_suffix
        self.sep = sep
        if use_defaults:
            self.add_dist(params=['mean', 'sd'], 
                          dist='normal', 
                          base_case='mean', 
                          low_case=lambda x: x['mean']-x['sd'], 
                          high_case=lambda x: x['mean']+x['sd'])
            self.add_dist(params=['min', 'mode', 'max'], 
                          dist='triangular', 
                          base_case=lambda x: (x['min']+x['mode']+x['max'])/3, 
                          low_case='min', 
                          high_case='max')
            self.add_dist(params=['low', 'high'], 
                          dist='uniform', 
                          base_case=lambda x: (x['high']+x['low'])/2, 
                          low_case=lambda x: x['low'], 
                          high_case=lambda x: x['high'])
            self.add_dist(params=['value'], 
                          dist='uniform', 
                          base_case='value',
                          low_case='value',
                          high_case='value',
                          process=_convertValueToUniform,
                          post_params=['low', 'high'])

    def add_dist(self, **kwargs):
        """
        Add a distribution type.
        Base case may be a function or the name of a function under numpy.random, eg. 'normal'.
        Eg.
        >>> sim = Simulator()
        >>> sim.add_dist(params=['scale'], dist='exponential', base_case='scale', low_case=lambda x: x.scale/2, high_case=lambda x:x.scale*1.5)
        """
        # check the required arguments are present and not none
        for required in ['params', 'dist', 'base_case', 'low_case', 'high_case']:
            assert required in kwargs, '{0} is required to add a distribution'.format(required)
            assert kwargs[required] is not None, '{0} can not be None'.format(required)
        # replace any missing args with None
        for field in _DistType._fields:
            if field not in kwargs:
                kwargs[field] = None
        # replace name of a numpy.random function with the function
        if type(kwargs['dist'])==str:
            kwargs['dist'] = getattr(random, kwargs['dist'])
        # replace eg. base_case='mean' with base_case=lambda x: x['mean']
        for function_field in ['base_case', 'low_case', 'high_case']:
            if type(kwargs[function_field])==str:
                # wrap the lambda function in another function so it has the right scope
                kwargs[function_field] =  _field_fn(kwargs[function_field])
        # replace None post_params with params
        if not kwargs['post_params']:
            kwargs['post_params'] = kwargs['params']
        # replace None process function with identity function
        if not kwargs['process']:
            kwargs['process'] = lambda x: x
        # add the distribution type to the master list
        self._dist_types += [_DistType(**kwargs)]

    def merge(self, *args, **kwargs):
        """
        Use in place of pd.merge(df1, df2, how=...), to accommodate the possibility of 
        the 'iterations' being high/low sensitivities. Kwargs are passed on to pd.merge.
        Extends pd.merge by allowing more than 2 dataframes to be merged
        (which it does by calling pd.merge sequentially on pairs, starting at the left).
        Defaults to how='outer', unlike pd.merge.
        Pass error_if_no_cases=True if desired.
        See calc_one_way_sensitivities for more detail.
        """
        if len(args)<2:
            raise TypeError('merge() takes at least two arguments ({0} given)', len(args))
        df = args[0]
        error_if_no_cases = kwargs.pop('error_if_no_cases',False)
        if not 'how' in kwargs:
            kwargs['how'] = 'outer'  # default to outer merge
        for df2 in args[1:]:
            df = pd.merge(df, df2, **kwargs)
        return self.calc_one_way_sensitivities(df, error_if_no_cases)


    def calc_one_way_sensitivities(self, df, error_if_no_cases=False):
        """
        Low and high cases are parameter-specific.
        An outer merge of two cases gives all possible combinations of high, base and low.
        This filters out only the high/low of one with the base of all the others,
        for each one.
        Replaces the 'case' columns with a single iter_name (eg 'iteration') column.
        Eg. 
        >>> fruit_per_tree = DataFrame([['Farm A','apple',200,30.0], ['Farm A','pear',50,7.5], ['Farm B','apple',160,24]], columns=['farm','fruit','mean','sd'])
        >>> price_per_fruit = DataFrame([['apple',.9,.1],['pear',1.04,.2]], columns=['fruit','mean','sd'])
        >>> mc = Simulator(iter_name='iteration', base_case_name='base', low_prefix='low', high_prefix='high', sep=' ')
        >>> sim_vol = mc.sim_from_params(-1, fruit_per_tree, 'volume')
        >>> sim_price = mc.sim_from_params(-1, price_per_fruit, 'price')
        >>> scenarios = pd.merge(sim_vol, sim_price, how='outer')
        >>> print scenarios
              farm  fruit  volume case  volume  price case  price
        0   Farm A  apple   low volume   170.0   low price   0.80
        1   Farm A  apple   low volume   170.0        base   0.90
        2   Farm A  apple   low volume   170.0  high price   1.00
        3   Farm A  apple         base   200.0   low price   0.80
        4   Farm A  apple         base   200.0        base   0.90
        5   Farm A  apple         base   200.0  high price   1.00
        6   Farm A  apple  high volume   230.0   low price   0.80
        7   Farm A  apple  high volume   230.0        base   0.90
        8   Farm A  apple  high volume   230.0  high price   1.00
        9   Farm B  apple   low volume   136.0   low price   0.80
        10  Farm B  apple   low volume   136.0        base   0.90
        11  Farm B  apple   low volume   136.0  high price   1.00
        ...
        >>> sim.calc_one_way_sensitivities(scenarios)
              iteration    farm  fruit  price  volume
        0          base  Farm A  apple   0.90   200.0
        1          base  Farm B  apple   0.90   160.0
        2          base  Farm A   pear   1.04    50.0
        3     low price  Farm A  apple   0.80   200.0
        4     low price  Farm B  apple   0.80   160.0
        5     low price  Farm A   pear   0.84    50.0
        6    high price  Farm A  apple   1.00   200.0
        7    high price  Farm B  apple   1.00   160.0
        8    high price  Farm A   pear   1.24    50.0
        9    low volume  Farm A  apple   0.90   170.0
        10   low volume  Farm B  apple   0.90   136.0
        11   low volume  Farm A   pear   1.04    42.5
        12  high volume  Farm A  apple   0.90   230.0
        13  high volume  Farm B  apple   0.90   184.0
        14  high volume  Farm A   pear   1.04    57.5
        """
        # find the relevant column names, which are those ending with the case_suffix, or the iter_name
        cases = [col for col in df.columns if col.endswith(self.sep+self.case_suffix) or col==self.iter_name]
        if len(cases)<2 and not error_if_no_cases:
            # nothing to do - just return the input dataframe silently
            return df
        x,y = cases[0], cases[1]
        result = self._calc_two_one_way_sensitivities(df, x, y)
        if len(cases)==2:
            return result
        else:
            # if more than 2 cases to bring together, repeat
            return self.calc_one_way_sensitivities(result, error_if_no_cases)

    def _calc_two_one_way_sensitivities(self, df, x, y):
        # if the merged data didn't have data for the first case, it will have NaNs there - find them
        nan_x = (df[x].isnull())
        # look for the base case line in the first case column (x), allowing NaNs
        base_x = (df[x]==self.base_case_name) | nan_x
        # using getattr(d,'startswith', lambda q:False) instead of a simple d.startwith
        # in case d is not a string (eg. can be NaN)
        low_x = df[x].apply(lambda d:getattr(d,'startswith', lambda q:False)(self.low_prefix+self.sep))
        high_x = df[x].apply(lambda d:getattr(d,'startswith', lambda q:False)(self.high_prefix+self.sep))
        nan_y = (df[y].isnull())
        base_y = (df[y]==self.base_case_name) | nan_y
        low_y = df[y].apply(lambda d:getattr(d,'startswith', lambda q:False)(self.low_prefix+self.sep))
        high_y = df[y].apply(lambda d:getattr(d,'startswith', lambda q:False)(self.high_prefix+self.sep))
        # five lines to return: base case for both cases, and hi & low for each of the 2 cases (with base for other).
        z1 = df[base_x & base_y]
        z2 = df[base_x & low_y]
        z3 = df[base_x & high_y]
        z4 = df[base_y & low_x]
        z5 = df[base_y & high_x]
        del z1[x], z2[x], z3[x]
        z1 = z1.rename(columns={y: self.iter_name})
        z1 = z1.fillna({self.iter_name: self.base_case_name}) # in case col y was NaN
        z2 = z2.rename(columns={y: self.iter_name})
        z3 = z3.rename(columns={y: self.iter_name})
        del z4[y], z5[y]
        z4 = z4.rename(columns={x: self.iter_name})
        z5 = z5.rename(columns={x: self.iter_name})
        
        def missing_rows(nan_x, base_y, x, y, low_x, high_x):
            # handle missing cases
            # to pick up the low/hi cases, need to add in the base case value explicitly
            z = DataFrame()
            if nan_x.any():
                # x is missing, so add hi/lo x case to y, using base case values
                z = df[nan_x & base_y]
                del z[x]
                z = z.rename(columns={y: self.iter_name})
                # pull out all the high/low case names from x col
                x_cases = list(set(df[x][low_x | high_x]))
                newcol = x_cases*len(z)
                newcol = [e for e in x_cases for _ in z.iterrows()]
                z = pd.concat([z]*len(x_cases), ignore_index=True)
                # depends on concat returning each piece in order
                z[self.iter_name] = newcol
            return z

        zx = missing_rows(nan_x, base_y, x, y, low_x, high_x)
        zy = missing_rows(nan_y, base_x, y, x, low_y, high_y)
        # stitch the results back together
        length = len(z1)+len(zx)+len(zy)+len(z2)+len(z3)+len(z4)+len(z5)
        result = pd.concat([z1,zx,zy,z2,z3,z4,z5]).set_index([range(length)])
        return result

    def _which_dist(self, df):
        """
        Check which distribution the dataframe df is, based on the parameters given.
        Returns the dist_type named tuple.
        """
        dists = [dist_type for dist_type in self._dist_types if all([param in df for param in dist_type.params])]
        if len(dists)!=1:
            if dists:
                raise BadParamsException(u'Parameters are ambiguous: {0}.'.format([dist.params for dist in dists]))
            else:
                raise NoParamsException(u'No parameters passed for any known distribution.')
        return dists[0]

    
    def _sim_row(self, row, size, dist_type, value_name):
        """
        Supply a row in a DataFrame with columns matching parameter names, 
        and a number of values to simulate (size).
        row can be either a DataFrame or a Series.
        Supply the distribution type from _dist_types.
        Returns a DataFrame of simulated values, with simulated column named value_name
        (iteration number is the index)

        Eg.
        >>> print row  # a Series
        fruit               apple
        min                     4
        mode                    6
        max                     7
        Name: 0, dtype: object
        >>> print sim._sim_row(row, 3, sim._dist_types[1], 'apples')
             apples
        0  4.348717
        1  5.519316
        2  6.881625
        """
        return pd.DataFrame(dist_type.dist(*[dist_type.process(row)[param] for param in dist_type.post_params], 
                                           size=size), columns=[value_name])

    def _calc_high_low(self, row, dist_type, value_name):
        """
        Supply a row in a DataFrame with columns matching parameter names, 
        row can be either a DataFrame or a Series.
        Supply the distribution type from _dist_types.
        Returns a DataFrame of low, base_case and high values in a column named value_name

        Eg.
        >>> print row  # a Series
        fruit               apple
        min                     4
        mode                    6
        max                     7
        Name: 0, dtype: object
        >>> print sim._calc_high_low(row, sim._dist_types[1], 'apples')
                       apples
        low apples          4
        base case    5.666667
        high apples         7
        """
        return pd.DataFrame([dist_type.low_case(row).iloc[0], dist_type.base_case(row).iloc[0], dist_type.high_case(row).iloc[0]], 
                            columns=[value_name], index=[self.sep.join([self.low_prefix,value_name]),
                                                         self.base_case_name,
                                                         self.sep.join([self.high_prefix,value_name])])

        
    def sim_from_params(self, size, df, value_name='value', groupby_cols=None):
        """
        Run through every row of the supplied DataFrame df, 
        which should have columns matching a distribution's parameter names (eg. 'mean', 'sd').
        Return a DataFrame with 'size' simulation iterations in the value_name column,
        numbered under a column named self.iter_name.
        If size==0, return the base case.
        If size==-1, return low, base and high cases. 
                     Places the case name in a "{value} case" column, not iter_name.

        Eg:
        >>> print x
             farm  fruit       variety  num trees  min  mode  max
        0  Farm A  apple  Granny Smith        100    4     6    7
        1  Farm A  apple      Jonathon        200    4     7    9
        2  Farm A   pear         Nashi         50    2     6   10
        >>> print sim.sim_from_params(2, x)
             farm  fruit  iteration max min mode num trees     value       variety
        0  Farm A  apple          0   7   4    6       100  5.504104  Granny Smith
        1  Farm A  apple          1   7   4    6       100  5.466288  Granny Smith
        0  Farm A  apple          0   9   4    7       200  5.709649      Jonathon
        1  Farm A  apple          1   9   4    7       200  6.722766      Jonathon
        0  Farm A   pear          0  10   2    6        50  7.346312         Nashi
        1  Farm A   pear          1  10   2    6        50  4.775222         Nashi
        """
        dist_type = self._which_dist(df)
        if not groupby_cols:
            # get a list of all the non-param columns to group by
            groupby_cols = [col for col in df.columns if col not in dist_type.params]
        if size>0:
            out = df.groupby(groupby_cols).apply(self._sim_row, size, dist_type, value_name)
            # TODO: currently inserting iteration column name here - is there a better way?
            out = out.reset_index().rename(columns={'level_{0}'.format(len(groupby_cols)): self.iter_name})
        if size==0:
            out = df.apply(lambda x: _special_case(dist_type, 'base_case', x, value_name), axis=1)
            out[self.iter_name] = self.base_case_name
            # in this case, the parameters are still present - delete them
            for col in dist_type.params:
                del out[col]
        if size==-1:
            out = df.groupby(groupby_cols).apply(self._calc_high_low, dist_type, value_name)
            out = out.reset_index().rename(columns={'level_{0}'.format(len(groupby_cols)): self.sep.join([value_name, self.case_suffix])})
        return out

