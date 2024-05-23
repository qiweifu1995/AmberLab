from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDoubleSpinBox, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial


class NameEditWindow(QWidget):
    """Window that prompt user for channel naming """
    ok_clicked = QtCore.pyqtSignal()
    revert_clicked = QtCore.pyqtSignal()

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
        self.label_ch2 = QLineEdit()
        self.label_ch2.setText(self.channel_names[1])
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
        self.label_ch3 = QLineEdit()
        self.label_ch3.setText(self.channel_names[2])
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
        self.label_ch4 = QLineEdit()
        self.label_ch4.setText(self.channel_names[3])
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
        self.label_ch5 = QLineEdit()
        self.label_ch5.setText(self.channel_names[4])
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
        self.label_ch6 = QLineEdit()
        self.label_ch6.setText(self.channel_names[5])
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_ch6.sizePolicy().hasHeightForWidth())
        self.input_ch6.setSizePolicy(sizePolicy)
        self.input_ch6.setObjectName("input_ch6")
        self.channel_6_layout.addWidget(self.input_ch6)
        layout.addLayout(self.channel_6_layout)

        self.setLayout(layout)

    def edit_handler(self, edit_in: QDoubleSpinBox, ch):
        """handles when edit is done"""
        print("Validating")
        if edit_in.hasAcceptableInput():
            self.thresholds[ch] = edit_in.value()

    def import_threshold(self, threshold_in):
        """this function is called by main widnow to update the spinboz to current file values"""
        self.thresholds = threshold_in
        self.spinbox_green.setValue(threshold_in[0])
        self.spinbox_red.setValue(threshold_in[1])
        self.spinbox_blue.setValue(threshold_in[2])
        self.spinbox_orange.setValue(threshold_in[3])

    def ok_clicked(self):
        """send out signal to pass the threshold"""
        self.threshold_set.emit()
        self.hide()
    def apply_all_clicked(self):
        self.apply_all_set.emit()
        self.hide()

    def close_clicked(self):
        self.hide()