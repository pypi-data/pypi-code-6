'''
ggplot2 Style
=============

'''
from .default import Style

class ggplot2Style(Style):
    '''
    This class is a collection of all painting methods provided by the 
    ggplot2 style of MatPlotTheme.
    
    :param palette: The palette used for coloring.
    '''
        
    def legend(self, ax, *args, **kwargs):
        '''
        Place a legend to the input :class:`matplotlib.axes.Axes` object.
        
        :param ax: The input axes object.
        :param width_scale: The percentage that the width of the axes 
                object will be scaled down to.
        :return: The legend
        
        All additional input parameters are passed to :meth:`~matplotlib.axes.legend`.
        
        .. seealso::
           :meth:`matplotlib.axes.legend` for documentation on valid kwargs.
        '''
        width_scale = kwargs.pop('width_scale', 0.8)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * width_scale, box.height])
        
        kwargs.setdefault('loc', 'center left')
        kwargs.setdefault('bbox_to_anchor', (1, 0.5))
        kwargs.setdefault('frameon', False)
            
        legend = ax.legend(*args, **kwargs)
        
        if not legend:
            raise ValueError("Legend is not generated. Do you add labels "
                             "to the source data?")
            
        texts = legend.texts
        for t in texts:
            t.set_color(self.palette.dark_frame)
        legend.get_title().set_color(self.palette.dark_frame)
        
        return legend
        
    def plot(self, ax, *args, **kwargs):
        '''
        Add a line plot to the input :class:`matplotlib.axes.Axes` object.
        
        :param ax: The input axes object.
        :param reset_color_cycle: Reset the color cycle iterator of lines. Default is ``False``.
        :param grid: Draw the grid line. Default is ``'both'``.
                Value can be ``'both'``, ``'x'``, ``'y'``, and ``None``.
        :return: A list of lines that were added.
        
        A major modification made on the line plot is the change of color
        cycle, which is used to color different lines. :class:`matplotlib.axes.Axes`
        uses an iterable cycle to generate colors for different lines. The
        color cycle is changed by the :class:`~matplottheme.palette.default.Palette`
        employed. ``reset_color_cycle`` can reset the iterable and the color
        for current line will reset to the start of the cycle.
        
        All additional input parameters are passed to :meth:`~matplotlib.axes.plot`.
        
        .. seealso::
           :meth:`matplotlib.axes.plot` for documentation on valid kwargs.
        '''
        grid = kwargs.pop('grid', 'both')
        
        result = Style.plot(self, ax, *args, **kwargs)
        
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.patch.set_facecolor(self.palette.frame_bgcolor)
        ax.grid(axis=grid, color='white', linestyle='-', linewidth=0.5)
        
        return result
