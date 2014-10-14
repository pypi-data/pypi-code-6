'''
Dictionary of plot settings for submission to academic journals.
Dictionary keys can include any valid argument to matplotlib.rcParams
as well as 'max_height', the maximum allowable height of a figure (i.e.
the height of a page). Required keys are 'column_width', 'gutter_width'
and 'units', which specify the width of a single column, the width of
the gutter (the margin in between two columns) and the units of the
width measurement (e.g. 'mm'). Values for many of these settings can be 
found in the journal's Author Information page. For example, the 
settings for the Proceedings of the Royal Society B can be found in
<http://rspb.royalsocietypublishing.org/site/misc/preparing-article.xhtml>

Some notes:
    * Absolute minimum linewidth is typically 0.1pt - don't go below this,
      and for prominent lines (e.g. plot lines) use 1 pt.

Created on Oct 10, 2014

@author: gdelraye
'''

journals = {'ProcRoySocB': {'backend': 'pdf',
                            'axes.labelsize': 9,
                            'text.fontsize': 9,
                            'xtick.labelsize': 9,
                            'ytick.labelsize': 9,
                            'legend.pad': 0.1,
                            'legend.fontsize': 9,
                            'lines.markersize': 3,
                            'font.size': 9,
                            'font.family': u'serif',
                            'font.serif': ['Times'],
                            'text.usetex': False,
                            'column_width': 84,
                            'gutter_width': 7,
                            'max_height': 250,
                            'units': 'mm'}, # Proceedings of the Royal Society B
            'DSRII':        {'backend': 'pdf',
                            'axes.labelsize': 9,
                            'text.fontsize': 9,
                            'xtick.labelsize': 9,
                            'ytick.labelsize': 9,
                            'legend.pad': 0.1,
                            'legend.fontsize': 9,
                            'lines.markersize': 3,
                            'font.size': 9,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 90,
                            'gutter_width': 10,
                            'max_height': 240,
                            'units': 'mm'}, # Deep Sea Research II
            'PLOSONE':     {'backend': 'pdf',
                            'axes.labelsize': 9,
                            'text.fontsize': 9,
                            'xtick.labelsize': 9,
                            'ytick.labelsize': 9,
                            'legend.pad': 0.1,
                            'legend.fontsize': 9,
                            'lines.markersize': 3,
                            'font.size': 9,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 83,
                            'gutter_width': 7.5,
                            'max_height': 233.5,
                            'units': 'mm'}, # Public Library of Science One
            'MEPS':        {'backend': 'pdf',
                            'axes.labelsize': 9,
                            'text.fontsize': 9,
                            'xtick.labelsize': 9,
                            'ytick.labelsize': 9,
                            'legend.pad': 0.1,
                            'legend.fontsize': 9,
                            'lines.markersize': 3,
                            'font.size': 9,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 81,
                            'gutter_width': 7,
                            'max_height': 225,
                            'units': 'mm'}, # Marine Ecology Progress Series
            'JEB':         {'backend': 'pdf',
                            'axes.labelsize': 8,
                            'text.fontsize': 8,
                            'xtick.labelsize': 8,
                            'ytick.labelsize': 8,
                            'legend.pad': 0.1,
                            'legend.fontsize': 8,
                            'lines.markersize': 3,
                            'font.size': 8,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 85,
                            'gutter_width': 10,
                            'max_height': 210,
                            'units': 'mm'}, # Journal of Experimental Biology
            'PNAS':        {'backend': 'pdf',
                            'axes.labelsize': 8,
                            'text.fontsize': 8,
                            'xtick.labelsize': 8,
                            'ytick.labelsize': 8,
                            'legend.pad': 0.1,
                            'legend.fontsize': 8,
                            'lines.markersize': 3,
                            'font.size': 8,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 87,
                            'gutter_width': 4,
                            'max_height': 240,
                            'units': 'mm'}, # Proceedings of the National Academy of Sciences, USA
            'EcolLett':    {'backend': 'pdf',
                            'axes.labelsize': 9,
                            'text.fontsize': 9,
                            'xtick.labelsize': 9,
                            'ytick.labelsize': 9,
                            'legend.pad': 0.1,
                            'legend.fontsize': 9,
                            'lines.markersize': 3,
                            'font.size': 9,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 82,
                            'gutter_width': 9,
                            'units': 'mm'}, # Ecology Letters
            'Presentation':{'backend': 'pdf',
                            'axes.labelsize': 18,
                            'text.fontsize': 18,
                            'xtick.labelsize': 18,
                            'ytick.labelsize': 18,
                            'legend.pad': 0.1,
                            'legend.fontsize': 18,
                            'lines.markersize': 3,
                            'font.size': 18,
                            'font.family': u'sans-serif',
                            'font.sans-serif': ['Arial'],
                            'text.usetex': False,
                            'column_width': 5,
                            'gutter_width': 0,
                            'max_height': 7.5,
                            'units': 'inch'}, # Size for presentations slides (e.g. powerpoint)
            }

