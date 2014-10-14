'''
Easily format figures to match the publication requirements of an academic journal. 
Figure settings can be determined using the defaults provided in the 'journals' module,
which currently supports the following journals: 
    * Proceedings of the Royal Society B (use key 'ProcRoySocB')
    * Public Library of Science One (use key 'PLOSONE')
    * Deep Sea Research II (use key 'DSRII')
    * Marine Ecology Progress Series (use key 'MEPS')
    * Journal of Experimental Biology (use key 'JEB')
    * Proceedings of the National Academy of Sciences, USA (use key 'PNAS')
    * Ecology Letters (use key 'EcolLett')
For journals not in the above list, custom settings can be provided by creating a module 
on the python path containing a dictionary named 'journals' with the following structure::
    journals = {'some_journal': {'key1': value, 'key2': value},
                'another_journal': {'key1': value, 'key2': value}}
where 'some_journal' is the identifying name of an academic journal (e.g. 'Nature') and
'key1', 'key2' correspond either to valid keys for matplotlib.rcParams (for example the
font name and size) or to one of 'column_width', 'gutter_width', 'max_height' or 'units'. 
Each of these non-rcParams keys except for 'max_height' is required. For an example of 
this kind of dictionary, see the module 'journals' in this package. Definitions of valid 
keys to rcParams can be found at <http://matplotlib.org/users/customizing.html>. 
The non-rcParams keys are:
    * column_width (required) - the maximum width a figure is allowed to be while still 
      fitting withing a single column.
    * gutter_width (required) - the width of the gutter (space between columns). This can 
      usually be found by comparing the maximum width that a journal allows for a single-
      column figure with the maximum width of a 2-column figure. For example, PLoS One
      allows a 1-column figure to be 83 mm in width and a 2-column figure to be 173.5 mm,
      meaning that the gutter width (173.5 - 83*2) must be 7.5 mm wide.
    * max_height (optional) - the maximum height a figure is allowed to be while fitting 
      on a single page (i.e. the page height).
    * units (required) - the units in which the above are reported. Can be one of 'mm', 
      'cm', 'inch', or 'pts'

Created on Oct 10, 2014

@author: gdelraye
'''

from matplotlib import rcParams
import importlib
import warnings
import copy

class Set:
    '''Set matplotlib figure parameters to conform to academic journal requirements, and
    easily specify figure dimensions.
    
    Usage example:
    
    First set the journal you want to submit to::
            publishable = Set('MEPS') # Lets publish in the Marine Ecology Progress Series!
    Then set the dimensions of a particular figure with the line::
        publishable.set_figsize(n_columns = 1, n_rows = 1)
    This will cause the next figure that is drawn to be 1 column wide (81 mm for MEPS) x 1 
    row high (the concept of 'rows' is a little made up, but the default is that one row is
    equal to one column width multiplied by the golden ratio, so in this case 50.1 mm). Once 
    the first figure is drawn, we can set the next figure to be 2 columns wide and 1 row 
    tall and this time set the row height to be equal to the column width::
        publishable.set_figsize(2, 1, aspect_ratio = 1)
    Importantly, plotsettings doesn't just calculate the width of a 2-column figure as two
    times the width of one column, but includes the width of the gutter (the space between
    columns on a page) as well. Therefore, the figure that follows the above line will end
    up being 169 mm wide (2 columns of 81 mm each plus a 7 mm gutter) and 81 mm tall (row
    height = 1*column width).
    '''
    def __init__(self, journal_name, module = 'journals'):
        '''Import a dictionary containing default plot settings for each journal, and
        set them to values appropriate for the indicated journal.
        
        Inputs:
            * journal_name (str) - identifying name of a journal. Must be a valid key 
              for the dictionary 'journals' contained in 'module'
            * module (str) - name of a module in the pythonpath containing the settings
              for each journal. Defaults to the 'journals' module in this package. To
              use an external module (e.g. 'my_journal_settings.py'), input the module
              name without extensions
        Example:
        
        >>> from matplotlib import rcParams
        >>> publishable = Set('DSRII') # Settings for the journal Deep Sea Research II
        >>> rcParams['font.sans-serif'] # Check that rcparams has been changed
        ['Arial']
        '''
        # Get parameter values for the specified journal:
        self.journals = importlib.import_module(module).journals # python module containing a single dict
        params = copy.deepcopy(self.journals[journal_name]) # Find the journal 'journal_name'
        # Remove non-rcParams keywords from 'params':
        self.units = params.pop('units') # e.g. 'mm' or 'cm'
        self.column_width = self._inches(params.pop('column_width'), self.units) # Column width in inches
        self.gutter_width = self._inches(params.pop('gutter_width'), self.units) # Gutter width in inches
        self.max_height = self._inches(params.pop('max_height', float('inf')), self.units) # Page height in inches
        rcParams.update(params) # Change matplotlib rcparams
    
    def set_figsize(self, n_columns, n_rows = 1, aspect_ratio = 0.618):
        '''Set the figure size according to the number of columns and rows that
        the figure should cover. By default, the 'rows' are calculated as a height
        equal to the width of a column times the golden ratio.
        
        Inputs:
            * n_columns (scalar) - number of columns that the figure should cover
            * n_rows (scalar) - number of rows that the figure should cover. The row
              height is defined as the column height multiplied by the aspect
              ratio.
            * aspect_ratio (scalar) - ratio of row height to column width. Defaults
              to the golden ratio (0.618).
        Example:
        
        >>> from matplotlib import rcParams
        >>> publishable = Set('DSRII') # Settings for the journal Deep Sea Research II
        >>> publishable.set_figsize(1, 1, aspect_ratio = 1) # Figure dimensions = column_width x column_width
        >>> height, width = rcParams['figure.figsize'] # Check the figure dimensions
        >>> print '%.3f, %.3f' %(height, width) # Check the figure dimensions
        3.543, 3.543
        >>> publishable.set_figsize(2, 1, 0.5) # Two-columned figure width = 2*column_width + 1*gutter_width
        >>> height, width = rcParams['figure.figsize'] # Check the figure dimensions
        >>> print '%.3f, %.3f' %(height, width) # Check the figure dimensions
        7.480, 1.772
        >>> publishable.set_figsize(2, 3, 1) # This figure is too tall to fit in one page
        Traceback (most recent call last):
        UserWarning: Specified figure height exceeds maximum height. Setting to maximum height instead
        '''
        row_height = self.column_width*aspect_ratio
        figure_height = row_height*n_rows
        if figure_height > self.max_height:
            warnings.warn('Specified figure height exceeds maximum height. Setting to maximum height instead')
            figure_height = self.max_height
        rcParams['figure.figsize'] = (self._calc_width(n_columns), figure_height)
    
    def list_journals(self):
        '''Return a list of all supported journals
        '''
        return self.journals.keys()
    
    def _calc_width(self, n_columns):
        '''Calculate the width of a figure taking into account the number of columns
        and the width of the gutter between them.
        
        Inputs:
            * n_columns (int) - number of columns that the figure should cover
        Returns:
            * The figure width 
        '''
        return n_columns*self.column_width + (n_columns - 1)*self.gutter_width
    
    @staticmethod
    def _inches(length, units = 'mm'):
        '''Convert measurements to inches
        
        Inputs:
            * length (scalar) - dimension to be converted into units
            * units (str) - the units of the dimension. Must be one of mm, cm, inch, or pts
        Returns:
            * length in inches
        Example:
        
        >>> converted = Set._inches(10, 'cm') # Convert 10cm to inches
        >>> print '%.3f' %(converted) # Check the result
        3.937
        '''
        unitconverter={'pts': 1.0/72.0, # Assuming 72 DPI
                       'mm': 0.039370079,
                       'cm': 0.39370079,
                       'inch': 1.0}
        inches = length*unitconverter[units]
        return inches 

if __name__ == '__main__':
    import doctest
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("error", UserWarning)
        doctest.testmod() 