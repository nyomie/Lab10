# This file provides the interface

from PyQt4 import QtGui
from PyQt4 import QtCore
import QtMpl


class UI_central(QtGui.QDialog):
    def __init__(self,parent=None):
        super(UI_central, self).__init__(parent)

        # The widgets for the interface
        self.main_widget = QtGui.QWidget(self)
        self.stockLabel = QtGui.QLabel("Stock", self)
        self.numberStockLabel = QtGui.QLabel("How many?", self)
        self.knownStockLabel = QtGui.QLabel("Known Stocks", self)
        self.officersLabel = QtGui.QLabel("Officers and Directors", self)
        self.stockEdit = QtGui.QTextEdit()
        self.numberStockEdit = QtGui.QTextEdit()
        self.officersTextEdit = QtGui.QTextEdit()
        self.stockCombo = QtGui.QComboBox()
        self.calendar = QtGui.QCalendarWidget()
        self.addButton = QtGui.QPushButton("Add")
        self.officersButton = QtGui.QPushButton("Display Officers")
        self.qtMpl = QtMpl.QtMpl(self.main_widget)
        # First HBox

        self.hboxTop = QtGui.QHBoxLayout()
        self.hboxTop.addWidget(self.stockLabel)
        self.hboxTop.addWidget(self.stockEdit)
        self.hboxTop.addWidget(self.numberStockLabel)
        self.hboxTop.addWidget(self.numberStockEdit)
        self.hboxTop.addWidget(self.calendar)
        self.hboxTop.addWidget(self.addButton)

        # Second HBox

        self.hboxMiddle = QtGui.QHBoxLayout()
        self.hboxMiddle.addWidget(self.knownStockLabel)
        self.hboxMiddle.addWidget(self.stockCombo)
        self.hboxMiddle.addWidget(self.officersButton)

        # Third HBox

        self.hboxBottom = QtGui.QHBoxLayout()
        self.hboxBottom.addWidget(self.officersLabel)
        self.hboxBottom.addWidget(self.officersTextEdit)

        # VBox to put all the HBox together

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.hboxTop)
        self.vbox.addLayout(self.hboxMiddle)
        self.vbox.addLayout(self.hboxBottom)
        self.vbox.addWidget(self.qtMpl)

        self.setLayout(self.vbox)