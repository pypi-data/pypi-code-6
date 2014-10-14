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
    
In addition, the function panel_labels provides a convenient way of providing panel
labels (e.g. A, B, C) to each subplot axis which ignoring axes that contain only colorbars.

Created on Oct 10, 2014

@author: gdelraye
'''

from matplotlib import pyplot
import importlib
import warnings
import copy
import string

#--- Set figure properties:
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
    def __init__(self, journal_name, module = 'plotsettings.journals'):
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
        pyplot.rcParams.update(params) # Change matplotlib rcparams
    
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
        pyplot.rcParams['figure.figsize'] = (self._calc_width(n_columns), figure_height)
    
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

#--- Generate labels:
def label_generator(case = 'lowercase', prefix = '', suffix = '.'):
    '''Create a generator that iterates through panel labels (e.g. (A), (B), (C) or a., b., c.)
    
    Inputs:
    
        * case (str) - 'uppercase' for capitalized labels and 'lowercase' for uncapitalized
        * prefix (str) - characters to prepend to the label (e.g. to generate labels such as 
          (A) and (B), set prefix to '(' ).
        * suffix (str) - characters to append to the label (e.g. ')' or '.').
    
    Returns
    
        * A generator object
    
    Examples:
    
    >>> capitals = label_generator('uppercase')
    >>> print capitals.next()
    A.
    >>> print capitals.next()
    B.
    >>> lowercase = label_generator('lowercase', '(', ')')
    >>> print lowercase.next()
    (a)
    '''
    choose_type = {'lowercase': string.ascii_lowercase,
                   'uppercase': string.ascii_uppercase}
    label_generator = ('%s%s%s' %(prefix, letter, suffix) for letter in choose_type[case])
    return label_generator

def panel_labels(fig = None, position = 'outside', case = 'lowercase', prefix = '', suffix = '.', 
                 fontweight = 'bold'):
    '''Label figure subplots as panels (e.g. A., B., C. or (a), (b), (c)) while ignoring
    subplot axes that contain only colorbars.
    
    Inputs:
        * fig (object) - a matplotlib figure object. If None, defaults to the currently 
          opened figure
        * position (str) - 'outside' for labels outside of the top left corner of the 
          axes area and 'inside' for labels inside of it. Defaults to outside.
        * case (str) - 'uppercase' for capitalized labels and 'lowercase' for 
          uncapitalized.
        * prefix (str) - characters to be prepended to the label (e.g. '(' )
        * suffix (str) - characters to be appended to the label (e.g. ')' or '.')
        * fontweight (str) - any valid argument to matplotlib.text.Text.set_weight.
          Use 'normal' for plaintext, 'bold' for boldface.
    
    Usage::
    
        fig, (ax) = pyplot.subplots(1, 1) # Create plot
        ax.plot(range(3)) # Plot some stuff
        panel_labels(fig) # Create the lettering
        pyplot.show()
    '''
    if fig == None:
        fig = pyplot.gcf()
    axis_list = fig.get_axes()
    generate_labels = label_generator(case = case, prefix = prefix, suffix = suffix)
    choose_position = {'outside': {'x': -0.05, 'y': 1.15, 'va': 'bottom', 'ha': 'right'},
                       'inside': {'x': 0.05, 'y': 0.90, 'va': 'top', 'ha': 'left'}}
    create_offset = {'outside': (lambda x, y: (-x, 1 + y)), 'inside': (lambda x, y: (x, 1 - y))}
    text_kwargs = choose_position[position]
    for ax in axis_list:
        try:
            ax.rowNum # Colorbar axes don't appear to have a rowNum or colNum
        except AttributeError: # Found a colorbar axis
            pass # Don't label
        else:
            label = generate_labels.next() # Get the next label
            # Average x and y offsets so that the distance (in display coordinates) is the same:
            x_origin, y_origin = ax.transAxes.transform((0, 0)) # Get the display coordinates at the axis origin
            x_display, y_display = ax.transAxes.transform((abs(text_kwargs['x']), 
                                                           abs(1 - text_kwargs['y']))) # offset in display coordinates
            offset = ((x_display - x_origin) + (y_display - y_origin))*0.5 # offset from axis origin
            x_axis, y_axis = ax.transAxes.inverted().transform((offset + x_origin, offset + y_origin)) # Unify offsets
            text_kwargs['x'], text_kwargs['y'] = create_offset[position](x_axis, y_axis) # Convert back to axis coordinates
            # Draw label:
            ax.text(s = label, transform = ax.transAxes, fontweight = fontweight, **text_kwargs)

#--- Test:
if __name__ == '__main__':
    import doctest
    with warnings.catch_warnings(record = True) as w:
        warnings.simplefilter("error", UserWarning)
        doctest.testmod() 