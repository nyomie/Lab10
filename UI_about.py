# This file will provide code related to UI_about

from PyQt4 import QtGui
from PyQt4 import QtCore


class UI_about(QtGui.QDialog):
    def __init__(self, parent=None):
        super(UI_about, self).__init__(parent)
        courseLabel = QtGui.QLabel("358152: Python Programming I COM SCI X 418.104B (Winter 2018)", self)
        nameLabel = QtGui.QLabel("Nina Tunas", self)
        labLabel = QtGui.QLabel("Lab 10", self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(courseLabel)
        vbox.addWidget(nameLabel)
        vbox.addWidget(labLabel)
        self.setLayout(vbox)
        self.setWindowTitle("About Python 1 Lab 10")