from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTableWidgetItem
from pyqtgraph.Qt import QtCore
import os
from multiprocessing import freeze_support
import statistics


class StatsWindow(QWidget):
    """creates the window that display stats of the quadrants"""
    def __init__(self):
        super().__init__()

        self.setupUI()

        self.output = [[] for i in range(4)]



    def setupUI(self):

        vertical_layout = QtWidgets.QVBoxLayout()

        self.stats_table = QtWidgets.QTableWidget()
        self.stats_table.setMinimumSize(QtCore.QSize(850,50))
        vertical_layout.addWidget(self.stats_table)
        self.stats_table.setRowCount(4)
        # set column count
        self.stats_table.setColumnCount(8)
        self.stats_table.setHorizontalHeaderLabels(
            ('X Mean', 'X Stdev', 'X Max', 'X Min', 'Y Mean', 'Y Stdev', 'Y Max', 'Y Min'))
        self.stats_table.setVerticalHeaderLabels(
            ('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        self.setLayout(vertical_layout)

    def update(self, name, quadrant_list_x, quadrant_list_y):
        """this function is called whenever the button press to show statistic is called"""
        try:
            self.setWindowTitle(name)
        except:
            self.setWindowTitle('Statistics')

        self.output = [[] for i in range(4)]

        for i in range(4):
            try:
                self.output[i].append(str(round(statistics.mean(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(statistics.stdev(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(max(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(min(quadrant_list_x[i]), 3)))
            except:
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
            try:
                self.output[i].append(str(round(statistics.mean(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(statistics.stdev(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(max(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(min(quadrant_list_y[i]), 3)))
            except:
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')

        for i in range(4):
            for j in range(8):
                self.stats_table.setItem(i, j, QTableWidgetItem(self.output[i][j]))


if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = StatsWindow("Stats", [], [])
    ui.show()
    sys.exit(app.exec_())