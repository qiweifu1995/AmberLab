import os
from multiprocessing import freeze_support

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDoubleSpinBox, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial


class NameEditWindow(QWidget):
    """Window that prompt user for channel naming """
    ok_clicked = QtCore.pyqtSignal()
    revert_clicked = QtCore.pyqtSignal()
    close_clicked = QtCore.pyqtSignal()
    DEFAULT_NAMES = ["488nm Green", "638nm Red", "405nm Blue", "561nm Orange", "Ch5", "Ch6"]
    name_output = ["" for i in range(6)]

    def __init__(self, channel_names):
        super().__init__()
        layout = QVBoxLayout()
        self.channel_names = channel_names
        self.label = QLabel("Please enter channel names.")
        layout.addWidget(self.label)


        """set up channel 1 names and inputs"""
        self.channel_1_layout = QHBoxLayout()
        self.channel_1_layout.setObjectName("channel_1_layout")
        self.label_ch1 = QLabel("Channel 1: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch1.sizePolicy().hasHeightForWidth())
        self.label_ch1.setSizePolicy(sizePolicy)
        self.label_ch1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch1.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch1.setObjectName("label_ch1")
        self.channel_1_layout.addWidget(self.label_ch1)
        self.input_ch1 = QLineEdit()
        self.input_ch1.setText(self.channel_names[0])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch1.sizePolicy().hasHeightForWidth())
        self.input_ch1.setSizePolicy(sizePolicy)
        self.input_ch1.setObjectName("input_ch1")
        self.channel_1_layout.addWidget(self.input_ch1)
        layout.addLayout(self.channel_1_layout)

        """set up channel 2 names and inputs"""
        self.channel_2_layout = QHBoxLayout()
        self.channel_2_layout.setObjectName("channel_2_layout")
        self.label_ch2 = QLabel("Channel 2: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch2.sizePolicy().hasHeightForWidth())
        self.label_ch2.setSizePolicy(sizePolicy)
        self.label_ch2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch2.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch2.setObjectName("label_ch2")
        self.channel_2_layout.addWidget(self.label_ch2)
        self.input_ch2 = QLineEdit()
        self.input_ch2.setText(self.channel_names[1])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch2.sizePolicy().hasHeightForWidth())
        self.input_ch2.setSizePolicy(sizePolicy)
        self.input_ch2.setObjectName("input_ch2")
        self.channel_2_layout.addWidget(self.input_ch2)
        layout.addLayout(self.channel_2_layout)

        """set up channel 3 names and inputs"""
        self.channel_3_layout = QHBoxLayout()
        self.channel_3_layout.setObjectName("channel_3_layout")
        self.label_ch3 = QLabel("Channel 3: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch3.sizePolicy().hasHeightForWidth())
        self.label_ch3.setSizePolicy(sizePolicy)
        self.label_ch3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch3.setObjectName("label_ch3")
        self.channel_3_layout.addWidget(self.label_ch3)
        self.input_ch3 = QLineEdit()
        self.input_ch3.setText(self.channel_names[2])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch3.sizePolicy().hasHeightForWidth())
        self.input_ch3.setSizePolicy(sizePolicy)
        self.input_ch3.setObjectName("input_ch3")
        self.channel_3_layout.addWidget(self.input_ch3)
        layout.addLayout(self.channel_3_layout)

        """set up channel 4 names and inputs"""
        self.channel_4_layout = QHBoxLayout()
        self.channel_4_layout.setObjectName("channel_4_layout")
        self.label_ch4 = QLabel("Channel 4: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch4.sizePolicy().hasHeightForWidth())
        self.label_ch4.setSizePolicy(sizePolicy)
        self.label_ch4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch4.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch4.setObjectName("label_ch4")
        self.channel_4_layout.addWidget(self.label_ch4)
        self.input_ch4 = QLineEdit()
        self.input_ch4.setText(self.channel_names[3])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch4.sizePolicy().hasHeightForWidth())
        self.input_ch4.setSizePolicy(sizePolicy)
        self.input_ch4.setObjectName("input_ch4")
        self.channel_4_layout.addWidget(self.input_ch4)
        layout.addLayout(self.channel_4_layout)

        """set up channel 5 names and inputs"""
        self.channel_5_layout = QHBoxLayout()
        self.channel_5_layout.setObjectName("channel_5_layout")
        self.label_ch5 = QLabel("Channel 5: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch5.sizePolicy().hasHeightForWidth())
        self.label_ch5.setSizePolicy(sizePolicy)
        self.label_ch5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch5.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch5.setObjectName("label_ch5")
        self.channel_5_layout.addWidget(self.label_ch5)
        self.input_ch5 = QLineEdit()
        self.input_ch5.setText(self.channel_names[4])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch5.sizePolicy().hasHeightForWidth())
        self.input_ch5.setSizePolicy(sizePolicy)
        self.input_ch5.setObjectName("input_ch5")
        self.channel_5_layout.addWidget(self.input_ch5)
        layout.addLayout(self.channel_5_layout)

        """set up channel 6 names and inputs"""
        self.channel_6_layout = QHBoxLayout()
        self.channel_6_layout.setObjectName("channel_6_layout")
        self.label_ch6 = QLabel("Channel 6: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch6.sizePolicy().hasHeightForWidth())
        self.label_ch6.setSizePolicy(sizePolicy)
        self.label_ch6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ch6.setMinimumSize(QtCore.QSize(40, 0))
        self.label_ch6.setObjectName("label_ch6")
        self.channel_6_layout.addWidget(self.label_ch6)
        self.input_ch6 = QLineEdit()
        self.input_ch6.setText(self.channel_names[5])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch6.sizePolicy().hasHeightForWidth())
        self.input_ch6.setSizePolicy(sizePolicy)
        self.input_ch6.setObjectName("input_ch6")
        self.channel_6_layout.addWidget(self.input_ch6)
        layout.addLayout(self.channel_6_layout)

        """setup buttons"""
        self.pushButton_1 = QPushButton('Ok')
        self.pushButton_2 = QPushButton('Reset to Default')
        self.pushButton_3 = QPushButton('Cancel')
        layout.addWidget(self.pushButton_1)
        layout.addWidget(self.pushButton_2)
        layout.addWidget(self.pushButton_3)
        self.setLayout(layout)
        self.setMinimumSize(300,300)
        self.setWindowTitle("Channel Name Edit")

        self.pushButton_1.clicked.connect(self.ok_clicked)
        self.pushButton_2.clicked.connect(self.revert_clicked)
        self.pushButton_3.clicked.connect(self.close_clicked)

    def import_threshold(self, threshold_in):
        """this function is called by main widnow to update the spinboz to current file values"""
        self.thresholds = threshold_in
        self.spinbox_green.setValue(threshold_in[0])
        self.spinbox_red.setValue(threshold_in[1])
        self.spinbox_blue.setValue(threshold_in[2])
        self.spinbox_orange.setValue(threshold_in[3])

    def ok_clicked(self):
        """send out signal to pass the threshold"""
        if self.input_ch1.text():
            self.name_output[0] = self.input_ch1.text()
        if self.input_ch2.text():
            self.name_output[1] = self.input_ch2.text()
        if self.input_ch3.text():
            self.name_output[2] = self.input_ch3.text()
        if self.input_ch4.text():
            self.name_output[3] = self.input_ch4.text()
        if self.input_ch5.text():
            self.name_output[4] = self.input_ch5.text()
        if self.input_ch6.text():
            self.name_output[5] = self.input_ch6.text()
        self.name_updated.emit()
        self.hide()

    def revert_clicked(self):
        self.name_output = self.DEFAULT_NAMES
        self.names_reverted.emit()
        self.hide()

    def close_clicked(self):
        self.hide()

if __name__ == "__main__":
    freeze_support()
    import sys

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = NameEditWindow(["488nm Green", "638nm Red", "405nm Blue", "561nm Orange", "Ch5", "Ch6"])
    ui.show()
    sys.exit(app.exec_())