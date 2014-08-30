# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 15:14:18 2014

@author: jukka

SliderApp demo. Update data based on slider positions which are saved to
self.sliders[n].value(), where n = slider number.

"""

import sys
from PyQt4.QtGui import QApplication
from mplgbw.fancysliders import SliderApp
import numpy as np

class MyApp(SliderApp):

    def initialize_app(self):
        """Create 4 x 4 grid of plots and 3 line plots for each subplot."""

        # Create axes
        self.ax = np.zeros((4, 4), dtype=object)
        self.plots = np.zeros((4, 4, 3), dtype=object)
        plot_num = 1
        for i in range(4):
            for j in range(4):
                ax = self.ax[i, j] = self.fig.add_subplot(4, 4, plot_num)
                ax.tick_params(axis='both', which='major', labelsize=6)
                ax.tick_params(axis='both', which='minor', labelsize=6)
                ax.set_xlim(0, 10)
                ax.set_ylim(-10, 10)
                for k in range(3):
                    self.plots[i, j, k], = ax.plot([], [], animated=True)
                plot_num += 1

        self.fig.subplots_adjust(wspace=0.2, hspace=0.2)
        self.fig.tight_layout()

    def update_plots(self):
        """When sliders are moved, update data to plots."""
        x = np.linspace(0, 10, 20)
        for i in range(4):
            for j in range(4):
                for k in range(3):
                    y = np.sin(i*x*self.sliders[k].value() + j) + k + self.sliders[k].value()/10.0
                    self.plots[i, j, k].set_data(x, y)
                    self.ax[i, j].draw_artist(self.plots[i, j, k])

def main():
    app = QApplication(sys.argv)
    form = MyApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()