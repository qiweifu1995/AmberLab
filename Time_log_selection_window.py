from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QListView, QHBoxLayout, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
import os
from multiprocessing import freeze_support


class TimeLogFileSelectionWindow(QWidget):
    """Class that allows user to select the files for syringes"""
    def __init__(self, file_list):
        super().__init__()
        self.setupUI()
        self.main_file_list = file_list

    def setupUI(self):
        self.setWindowTitle("Syringe File Selection")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setMaximumSize(400,400)
        self.setSizePolicy(sizePolicy)

        layout = QVBoxLayout()
        self.label = QLabel("Syringe Name")
        layout.addWidget(self.label)

        self.line_edit_name = QLineEdit("Syringe 1")
        layout.addWidget(self.line_edit_name)

        self.file_list = QtWidgets.QListWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.file_list.setSizePolicy(sizePolicy)
        self.file_list.setMinimumSize(QtCore.QSize(100, 100))
        self.file_list.setMaximumSize(QtCore.QSize(400, 400))
        layout.addWidget(self.file_list)

        layout_h = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        layout_h.addWidget(self.ok_button)
        layout_h.addWidget(self.cancel_button)

        layout.addLayout(layout_h)

        self.setLayout(layout)

    def populate_list(self):
        self.file_list.clear()
        for i in range(self.main_file_list.count()):
            item = self.main_file_list.item(i).text()
            self.file_list.addItem(item)

if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = TimeLogFileSelectionWindow()
    ui.show()
    sys.exit(app.exec_())