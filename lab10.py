# This file will run our GUI application

import configparser
import sys
import UI
from PyQt4 import QtGui
from PyQt4 import QtCore


if __name__ == "__main__":
    config = configparser.RawConfigParser()

    app = QtGui.QApplication(sys.argv)
    gui = UI.UI(configuration=config)
    gui.show()
    app.exec_()
