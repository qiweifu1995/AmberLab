from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTableWidgetItem
from pyqtgraph.Qt import QtCore
import os
from multiprocessing import freeze_support
import statistics


class SquareWindow(QWidget):
    """creates the window that display stats of the quadrants"""
    def __init__(self):
        super().__init__()

        self.setupUI()
        self.setWindowTitle("New Square")
        self.output = [[] for i in range(4)]



    def setupUI(self):

        vertical_layout = QtWidgets.QGridLayout()

        self.origin_label = QtWidgets.QLabel("Origin")
        self.origin_label_x = QtWidgets.QLabel("Origin X: ")
        self.origin_label_y = QtWidgets.QLabel("Origin Y: ")
        self.origin_lineedit_x = QtWidgets.QLineEdit()
        self.origin_lineedit_y = QtWidgets.QLineEdit()
        self.height_label = QtWidgets.QLabel("Height: ")
        self.width_label = QtWidgets.QLabel("Width: ")
        self.height_lineedit = QtWidgets.QLineEdit()
        self.width_lineedit = QtWidgets.QLineEdit()
        vertical_layout.addWidget(self.origin_label,1,0, 1, 2)
        vertical_layout.addWidget(self.origin_label_x,2,0, 1, 1)
        vertical_layout.addWidget(self.origin_label_y,3,0, 1, 1)
        vertical_layout.addWidget(self.origin_lineedit_x, 2, 1, 1, 1)
        vertical_layout.addWidget(self.origin_lineedit_y, 3, 1, 1, 1)


        self.line_divider = QtWidgets.QFrame()
        self.line_divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        vertical_layout.addWidget(self.line_divider, 4, 0, 1, 2)

        vertical_layout.addWidget(self.height_label, 5, 0, 1, 1)
        vertical_layout.addWidget(self.height_lineedit, 5, 1, 1, 1)
        vertical_layout.addWidget(self.width_label, 6, 0, 1, 1)
        vertical_layout.addWidget(self.width_lineedit, 6, 1, 1, 1)

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
                self.output[i].append(str(round(statistics.median(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(statistics.stdev(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(max(quadrant_list_x[i]), 3)))
                self.output[i].append(str(round(min(quadrant_list_x[i]), 3)))
            except:
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
            try:
                self.output[i].append(str(round(statistics.mean(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(statistics.median(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(statistics.stdev(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(max(quadrant_list_y[i]), 3)))
                self.output[i].append(str(round(min(quadrant_list_y[i]), 3)))
            except:
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
                self.output[i].append('NA')
            try:
                ratio = [b/a for a, b in zip(quadrant_list_x[i], quadrant_list_y[i])]
                self.output[i].append(str(round(statistics.mean(ratio), 3)))
                self.output[i].append(str(round(statistics.stdev(ratio), 3)))
            except:
                self.output[i].append("NA")
                self.output[i].append("NA")


        for i in range(4):
            for j in range(12):
                self.stats_table.setItem(i, j, QTableWidgetItem(self.output[i][j]))


if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = SquareWindow()
    ui.show()
    sys.exit(app.exec_())