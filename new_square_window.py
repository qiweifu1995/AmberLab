from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTableWidgetItem
from pyqtgraph.Qt import QtCore
import os
from multiprocessing import freeze_support
import statistics


class MySignalEmitter(QtCore.QThread):
    # Define a custom signal with a value
    custom_signal = QtCore.pyqtSignal(object)

class SquareWindow(QWidget):
    """creates the window that display stats of the quadrants"""
    def __init__(self):
        super().__init__()
        self.confirm_clicked = MySignalEmitter()
        self.setupUI()
        self.setWindowTitle("New Square")
        self.origin = (0, 0)
        self.size = (0, 0)
        self.repeat = False
        self.repeat_num = 0

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

        ### set up triggers from here
        self.confirm_button.clicked.connect(self.confirmed)
        self.cancel_button.clicked.connect(self.cancelled)

    def confirmed(self):
        """this function returns data back to filter"""
        try:
            self.origin = (float(self.origin_lineedit_x.text()), float(self.origin_lineedit_y.text()))
        except:
            self.origin = (0.0, 0.0)

        try:
            self.size = (float(self.width_lineedit.text()), float(self.height_lineedit.text()))
        except:
            self.size = (0.0, 0.0)

        self.repeat = self.repeat_checkbox.checkState()

        try:
            self.repeat_num = int(self.repeat_lineedit.text())
        except:
            self.repeat_num = 1
        print("confirmed square")
        self.confirm_clicked.custom_signal.emit({"origin": self.origin, "size": self.size, "repeat": self.repeat, "repeat_num": self.repeat_num})

    def cancelled(self):
        """this handles closing the filter"""
        self.hide()


if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = SquareWindow()
    ui.show()
    sys.exit(app.exec_())