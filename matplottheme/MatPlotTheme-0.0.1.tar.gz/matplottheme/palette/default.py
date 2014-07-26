'''
Default Palette
===============

'''
class Palette(object):
    '''
    This class is a collection of all colors provided by the default 
    palette of MatPlotTheme.
    '''
    
    color_cycle = [
        '#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3',
        '#a6d854', '#ffd92f', '#e5c494', '#b3b3b3',
    ]
    '''
    Defines the color cycle used in all
    :meth:`matplottheme.style.default.Style.plot`,
    :meth:`matplottheme.style.default.Style.bar`, 
    :meth:`matplottheme.style.default.Style.barh` and other methods.
    '''
    
    dark_frame = '#444444'
    '''
    Defines the color of plot frame and labels/texts.
    '''
    
    legend_bgcolor = '#dddddd'
    '''
    Defines the background color of legend
    '''
    
    frame_bgcolor = '#ffffff'
    '''
    Defines the background color of plots.
    '''