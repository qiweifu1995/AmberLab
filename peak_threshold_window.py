from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDoubleSpinBox, QSizePolicy
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial


class ThresholdWindow(QWidget):
    """Window that prompt user for voltage to use """
    threshold_set = QtCore.pyqtSignal()
    apply_all_set = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        self.thresholds = [0.0, 0.0, 0.0, 0.0]
        voltage_validator = QtGui.QDoubleValidator(0, 12, 3, self)
        self.label = QLabel("Please enter threshold for each channel. Range: 0-12V")
        layout.addWidget(self.label)

        """set up green channel UI"""
        self.horizontal_layout_green = QHBoxLayout()
        self.horizontal_layout_green.setObjectName("horizontal_layout_green")
        self.label_green = QtWidgets.QLabel("Green: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_green.sizePolicy().hasHeightForWidth())
        self.label_green.setSizePolicy(sizePolicy)
        self.label_green.setAlignment(QtCore.Qt.AlignCenter)
        self.label_green.setMinimumSize(QtCore.QSize(40, 0))
        self.label_green.setObjectName("label_green")
        self.horizontal_layout_green.addWidget(self.label_green)
        self.spinbox_green = QDoubleSpinBox()
        self.spinbox_green.setDecimals(3)
        self.spinbox_green.setMaximum(12)
        self.spinbox_green.setMinimum(0)
        self.spinbox_green.setSuffix("V")
        self.spinbox_green.setSingleStep(0.1)
        self.spinbox_green.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.spinbox_green.setMinimumSize(QtCore.QSize(20, 20))
        self.spinbox_green.setObjectName("spinbox_green")
        self.horizontal_layout_green.addWidget(self.spinbox_green)
        layout.addLayout(self.horizontal_layout_green)

        """set up Red channel UI"""
        self.horizontal_layout_Red = QHBoxLayout()
        self.horizontal_layout_Red.setObjectName("horizontal_layout_Red")
        self.label_Red = QtWidgets.QLabel("Red: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Red.sizePolicy().hasHeightForWidth())
        self.label_Red.setSizePolicy(sizePolicy)
        self.label_Red.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Red.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Red.setObjectName("label_Red")
        self.horizontal_layout_Red.addWidget(self.label_Red)
        self.spinbox_red = QDoubleSpinBox()
        self.spinbox_red.setDecimals(3)
        self.spinbox_red.setMaximum(12)
        self.spinbox_red.setMinimum(0)
        self.spinbox_red.setSuffix("V")
        self.spinbox_red.setSingleStep(0.1)
        self.spinbox_red.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.spinbox_red.setMinimumSize(QtCore.QSize(20, 20))
        self.spinbox_red.setObjectName("spinbox_red")
        self.horizontal_layout_Red.addWidget(self.spinbox_red)
        layout.addLayout(self.horizontal_layout_Red)

        """set up Blue channel UI"""
        self.horizontal_layout_Blue = QHBoxLayout()
        self.horizontal_layout_Blue.setObjectName("horizontal_layout_Blue")
        self.label_Blue = QtWidgets.QLabel("Blue: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Blue.sizePolicy().hasHeightForWidth())
        self.label_Blue.setSizePolicy(sizePolicy)
        self.label_Blue.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Blue.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Blue.setObjectName("label_Blue")
        self.horizontal_layout_Blue.addWidget(self.label_Blue)
        self.spinbox_blue = QDoubleSpinBox()
        self.spinbox_blue.setDecimals(3)
        self.spinbox_blue.setMaximum(12)
        self.spinbox_blue.setMinimum(0)
        self.spinbox_blue.setSuffix("V")
        self.spinbox_blue.setSingleStep(0.1)
        self.spinbox_blue.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.spinbox_blue.setMinimumSize(QtCore.QSize(20, 20))
        self.spinbox_blue.setObjectName("spinbox_blue")
        self.horizontal_layout_Blue.addWidget(self.spinbox_blue)
        layout.addLayout(self.horizontal_layout_Blue)

        """set up Orange channel UI"""
        self.horizontal_layout_Orange = QHBoxLayout()
        self.horizontal_layout_Orange.setObjectName("horizontal_layout_Orange")
        self.label_Orange = QtWidgets.QLabel("Orange: ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Orange.sizePolicy().hasHeightForWidth())
        self.label_Orange.setSizePolicy(sizePolicy)
        self.label_Orange.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Orange.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Orange.setObjectName("label_Orange")
        self.horizontal_layout_Orange.addWidget(self.label_Orange)
        self.spinbox_orange = QDoubleSpinBox()
        self.spinbox_orange.setDecimals(3)
        self.spinbox_orange.setMaximum(12)
        self.spinbox_orange.setMinimum(0)
        self.spinbox_orange.setSuffix("V")
        self.spinbox_orange.setSingleStep(0.1)
        self.spinbox_orange.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.spinbox_orange.setMinimumSize(QtCore.QSize(20, 20))
        self.spinbox_orange.setObjectName("spinbox_orange")
        self.horizontal_layout_Orange.addWidget(self.spinbox_orange)
        layout.addLayout(self.horizontal_layout_Orange)

        self.pushButton_1 = QPushButton('Ok')
        self.pushButton_2 = QPushButton('Apply to All')
        self.pushButton_3 = QPushButton('Close')

        layout.addWidget(self.pushButton_1)
        layout.addWidget(self.pushButton_2)
        layout.addWidget(self.pushButton_3)

        self.setLayout(layout)
        self.spinbox_green.editingFinished.connect(partial(self.edit_handler, self.spinbox_green, 0))
        self.spinbox_red.editingFinished.connect(partial(self.edit_handler, self.spinbox_red, 1))
        self.spinbox_blue.editingFinished.connect(partial(self.edit_handler, self.spinbox_blue, 2))
        self.spinbox_orange.editingFinished.connect(partial(self.edit_handler, self.spinbox_orange, 3))
        self.pushButton_1.clicked.connect(self.ok_clicked)
        self.pushButton_2.clicked.connect(self.apply_all_clicked)
        self.pushButton_3.clicked.connect(self.close_clicked)
        self.setWindowTitle("Peak Threshold")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

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