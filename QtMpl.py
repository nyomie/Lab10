# This file contain MatPlab Library

from PyQt4 import QtGui
import matplotlib
import matplotlib.dates
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class QtMpl(FigureCanvasQTAgg):
    """
    This class will draw figure of the data
    """
    def __init__(self, parent):

        self.fig = matplotlib.figure.Figure()
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        self.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%m/%d/%Y'))
        self.axes.xaxis.set_major_locator(matplotlib.dates.DayLocator())

        FigureCanvasQTAgg.setSizePolicy(self,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def addLine(self, x, y, title):
        self.axes.plot_date(x, y, '-', label = title)
        self.axes.legend()
        self.fig.canvas.draw()
        self.fig.autofmt_xdate()
        return
