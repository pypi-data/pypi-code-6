# -*- coding: utf-8 -*-

"""
Simple boilerplate to create matplotlib-powered QT application.
The hard part here is to understand how blit works.
"""

import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np

class SliderApp(QMainWindow):

    def __init__(self, parent=None, dpi=100, figsize=(12, 12)):
        QMainWindow.__init__(self, parent)
        self.dpi = dpi
        self.figsize = figsize

        self.create_ui()
        self.initialize_app()
        self.canvas.draw()
        self.background = self.canvas.copy_from_bbox(self.fig.bbox)
        self.on_draw()

    def initialize_app(self):
        raise NotImplementedError("You need to provide your own initialize_app.")

    def update_plots(self):
        raise NotImplementedError("You need to provide your own update_plots.")

    def on_draw(self):
        """Update data according to slider positions."""
        self.canvas.restore_region(self.background)
        self.update_plots()
        self.canvas.blit(self.fig.bbox)

    def create_ui(self):
        self.main = QWidget()

        # Create mpl stuff
        self.fig = Figure(figsize=self.figsize, dpi=self.dpi, facecolor='#edecec')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main)
        #self.mpl_toolbar.setStyleSheet("background-color: #edecec")

        # Create sliders
        sliderLayout = QVBoxLayout()
        self.sliders = []
        for i in range(3):
            layout = QVBoxLayout()
            slider_label = QLabel('Slider %i' % i)
            slider = QSlider(Qt.Horizontal)
            slider.setRange(1, 30)
            self.connect(slider, SIGNAL('valueChanged(int)'), self.on_draw)
            slider.setMinimumSize(100, 1)
            layout.addWidget(slider_label)
            layout.addWidget(slider)
            sliderLayout.addLayout(layout)
            self.sliders.append(slider)

        spacer = QSpacerItem(100,100,QSizePolicy.Expanding,QSizePolicy.Expanding)
        sliderLayout.addItem(spacer)

        hbox = QHBoxLayout()
        hbox.addLayout(sliderLayout)
        hbox.addWidget(self.canvas)

        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addLayout(hbox)

        # Create "main" layout
        self.main.setLayout(vbox)
        self.setCentralWidget(self.main)
        self.showMaximized()
