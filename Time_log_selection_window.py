from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
import os
from multiprocessing import freeze_support


class TimeLogFileSelectionWindow(QWidget):
    """Class that allows user to select the files for syringes, also handles UI for file combine of filters"""
    def __init__(self, file_list: QListWidget, file_model: Qt.QStandardItemModel, file_index: list):
        super().__init__()
        self.setupUI()
        self.main_file_list = file_list
        self.file_model = file_model
        self.file_index = file_index

        #caller keeps track of which file index to work on, 0 for filter, 1 for log files
        self.caller = 0

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
        self.file_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.file_list)

        layout_h = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        layout_h.addWidget(self.ok_button)
        layout_h.addWidget(self.cancel_button)

        layout.addLayout(layout_h)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.ok_clicked)
        self.cancel_button.clicked.connect(self.close_clicked)

    def populate_list(self):
        """function to populate the file list with updated information"""
        self.file_list.clear()
        for i in range(self.main_file_list.count()):
            item = self.main_file_list.item(i).text()
            self.file_list.addItem(item)
        # update the automatic default name for syringe
        syringe_number = self.file_model.rowCount()+1
        self.line_edit_name.setText("Syringe " + str(syringe_number))

    def remove_item(self, index: list):
        """function for removing syringe or file"""

        # check for valid input
        if len(index) != 2:
            return

        # check if parent node
        if index[0] < 0:
            self.file_index.pop(index[1])
            self.file_model.removeRow(index[1])

        # child node
        else:
            del self.file_index[index[0]][index[1]]
            self.file_model.item(index[0]).removeRow(index[1])

            # delet syringe group if empty
            if not self.file_index[index[0]]:
                self.file_model.removeRow(index[0])

        print(self.file_index)

    def ok_clicked(self):
        """handler for ok clicked"""
        index_holder = []
        for item in self.file_list.selectedIndexes():
            # find all the index of selected item
            index_holder.append(item.row())

        if self.caller == 1:
            # this case handles the call request by time log
            if len(index_holder) > 0:
                syringe = Qt.QStandardItem(self.line_edit_name.text())
                self.file_model.appendRow(syringe)
                syringe_number = self.file_model.rowCount() - 1
                for i in range(len(index_holder)):
                    item = Qt.QStandardItem(self.main_file_list.item(i).text())
                    self.file_model.item(syringe_number).appendRow(item)
                self.file_index.append(index_holder)
            self.hide()

        elif self.caller == 0:
            # this case handles the call request by window filters



    def close_clicked(self):
        """handle close button clicked"""
        self.hide()


if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = TimeLogFileSelectionWindow()
    ui.show()
    sys.exit(app.exec_())