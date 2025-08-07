from PyQt5 import QtWidgets, QtGui
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
        self.setFixedWidth(250)
        vertical_layout = QtWidgets.QGridLayout()

        self.origin_label = QtWidgets.QLabel("Origin")
        self.origin_label_x = QtWidgets.QLabel("Origin X: ")
        self.origin_label_x.setMinimumWidth(110)
        self.origin_label_y = QtWidgets.QLabel("Origin Y: ")
        self.origin_lineedit_x = QtWidgets.QLineEdit()
        lineedit_x_validator = QtGui.QDoubleValidator(0.0, 33000.0, 2, self.origin_lineedit_x)
        self.origin_lineedit_x.setValidator(lineedit_x_validator)
        self.origin_lineedit_y = QtWidgets.QLineEdit()
        lineedit_y_validator = QtGui.QDoubleValidator(0.0, 33000.0, 2, self.origin_lineedit_y)
        self.origin_lineedit_y.setValidator(lineedit_y_validator)
        self.height_label = QtWidgets.QLabel("Height: ")
        self.width_label = QtWidgets.QLabel("Width: ")
        self.height_lineedit = QtWidgets.QLineEdit()
        height_validator = QtGui.QDoubleValidator(0.0, 33000.0, 2, self.height_lineedit)
        self.height_lineedit.setValidator(height_validator)
        self.width_lineedit = QtWidgets.QLineEdit()
        width_validator = QtGui.QDoubleValidator(0.0, 33000.0, 2, self.width_lineedit)
        self.width_lineedit.setValidator(width_validator)
        vertical_layout.addWidget(self.origin_label,1,0, 1, 2)
        vertical_layout.addWidget(self.origin_label_x,2,0, 1, 1)
        vertical_layout.addWidget(self.origin_label_y,3,0, 1, 1)
        vertical_layout.addWidget(self.origin_lineedit_x, 2, 1, 1, 1)
        vertical_layout.addWidget(self.origin_lineedit_y, 3, 1, 1, 1)


        self.line_divider = QtWidgets.QFrame()
        self.line_divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        vertical_layout.addWidget(self.line_divider, 4, 0, 1, 2)
        self.size_label = QtWidgets.QLabel("Size")
        vertical_layout.addWidget(self.size_label, 5, 0, 1, 1)
        vertical_layout.addWidget(self.height_label, 6, 0, 1, 1)
        vertical_layout.addWidget(self.height_lineedit, 6, 1, 1, 1)
        vertical_layout.addWidget(self.width_label, 7, 0, 1, 1)
        vertical_layout.addWidget(self.width_lineedit, 7, 1, 1, 1)
        self.line_divider_2 = QtWidgets.QFrame()
        self.line_divider_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_divider_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        vertical_layout.addWidget(self.line_divider_2, 8, 0, 1, 2)

        self.repeat_checkbox = QtWidgets.QCheckBox("Repeat? (1-4)")
        vertical_layout.addWidget(self.repeat_checkbox, 9, 0, 1, 1)
        self.repeat_lineedit = QtWidgets.QLineEdit()
        repeat_validator = QtGui.QIntValidator(1,4,self.repeat_lineedit)
        self.repeat_lineedit.setValidator(repeat_validator)
        vertical_layout.addWidget(self.repeat_lineedit, 9, 1, 1, 1)

        self.confirm_button = QtWidgets.QPushButton("Confirm")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        vertical_layout.addWidget(self.confirm_button, 10, 0, 1, 1)
        vertical_layout.addWidget(self.cancel_button, 10, 1, 1, 1)
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