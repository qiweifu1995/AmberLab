from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTableWidgetItem
from pyqtgraph.Qt import QtCore
import os
from multiprocessing import freeze_support
import statistics


class Settingwindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUI()
    def setupUI(self):

        vertical_layout = QtWidgets.QVBoxLayout()

        self.stats_table = QtWidgets.QTableWidget()
        self.stats_table.setMinimumSize(QtCore.QSize(850,50))
        vertical_layout.addWidget(self.stats_table)
        self.stats_table.setRowCount(4)
        # set column count
        self.stats_table.setColumnCount(10)
        self.stats_table.setHorizontalHeaderLabels(
            ('X Mean', 'X Stdev', 'X Max', 'X Min', 'Y Mean', 'Y Stdev', 'Y Max', 'Y Min', "Y/X Ratio", "Ratio Stdev"))
        self.stats_table.setVerticalHeaderLabels(
            ('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        self.setLayout(vertical_layout)