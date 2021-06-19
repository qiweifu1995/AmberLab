from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5 import QtWidgets, QtCore, Qt

class ThresholdWindow(QWidget):
    """Window that prompt user for voltage to use """
    def __init__(self, parent=None):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Please enter threshold for each channel. Range: 0-12V")
        layout.addWidget(self.label)

        """set up green channel UI"""
        self.horizontal_layout_green = QHBoxLayout()
        self.horizontal_layout_green.setObjectName("horizontal_layout_green")
        self.label_green = QtWidgets.QLabel("Green (V): ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_green.sizePolicy().hasHeightForWidth())
        self.label_green.setSizePolicy(sizePolicy)
        self.label_green.setAlignment(QtCore.Qt.AlignCenter)
        self.label_green.setMinimumSize(QtCore.QSize(40, 0))
        self.label_green.setObjectName("label_green")
        self.horizontal_layout_green.addWidget(self.label_green)
        self.lineEdit_Green = QLineEdit('0')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Green.sizePolicy().hasHeightForWidth())
        self.lineEdit_Green.setSizePolicy(sizePolicy)
        self.lineEdit_Green.setMinimumSize(QtCore.QSize(20, 0))
        self.lineEdit_Green.setObjectName("lineEdit_Green")
        self.horizontal_layout_green.addWidget(self.lineEdit_Green)
        layout.addLayout(self.horizontal_layout_green)

        """set up Red channel UI"""
        self.horizontal_layout_Red = QHBoxLayout()
        self.horizontal_layout_Red.setObjectName("horizontal_layout_Red")
        self.label_Red = QtWidgets.QLabel("Red (V): ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Red.sizePolicy().hasHeightForWidth())
        self.label_Red.setSizePolicy(sizePolicy)
        self.label_Red.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Red.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Red.setObjectName("label_Red")
        self.horizontal_layout_Red.addWidget(self.label_Red)
        self.lineEdit_Red = QLineEdit('0')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Red.sizePolicy().hasHeightForWidth())
        self.lineEdit_Red.setSizePolicy(sizePolicy)
        self.lineEdit_Red.setMinimumSize(QtCore.QSize(20, 0))
        self.lineEdit_Red.setObjectName("lineEdit_Red")
        self.horizontal_layout_Red.addWidget(self.lineEdit_Red)
        layout.addLayout(self.horizontal_layout_Red)

        """set up Blue channel UI"""
        self.horizontal_layout_Blue = QHBoxLayout()
        self.horizontal_layout_Blue.setObjectName("horizontal_layout_Blue")
        self.label_Blue = QtWidgets.QLabel("Blue (V): ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Blue.sizePolicy().hasHeightForWidth())
        self.label_Blue.setSizePolicy(sizePolicy)
        self.label_Blue.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Blue.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Blue.setObjectName("label_Blue")
        self.horizontal_layout_Blue.addWidget(self.label_Blue)
        self.lineEdit_Blue = QLineEdit('0')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Blue.sizePolicy().hasHeightForWidth())
        self.lineEdit_Blue.setSizePolicy(sizePolicy)
        self.lineEdit_Blue.setMinimumSize(QtCore.QSize(20, 0))
        self.lineEdit_Blue.setObjectName("lineEdit_Blue")
        self.horizontal_layout_Blue.addWidget(self.lineEdit_Blue)
        layout.addLayout(self.horizontal_layout_Blue)

        """set up Orange channel UI"""
        self.horizontal_layout_Orange = QHBoxLayout()
        self.horizontal_layout_Orange.setObjectName("horizontal_layout_Orange")
        self.label_Orange = QtWidgets.QLabel("Orange (V): ")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Orange.sizePolicy().hasHeightForWidth())
        self.label_Orange.setSizePolicy(sizePolicy)
        self.label_Orange.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Orange.setMinimumSize(QtCore.QSize(40, 0))
        self.label_Orange.setObjectName("label_Orange")
        self.horizontal_layout_Orange.addWidget(self.label_Orange)
        self.lineEdit_Orange = QLineEdit('0')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Orange.sizePolicy().hasHeightForWidth())
        self.lineEdit_Orange.setSizePolicy(sizePolicy)
        self.lineEdit_Orange.setMinimumSize(QtCore.QSize(20, 0))
        self.lineEdit_Orange.setObjectName("lineEdit_Orange")
        self.horizontal_layout_Orange.addWidget(self.lineEdit_Orange)
        layout.addLayout(self.horizontal_layout_Orange)



        self.lineEdit_Green = QLineEdit('0')
        self.pushButton_1 = QPushButton('Ok')
        self.pushButton_2 = QPushButton('Close')


        layout.addWidget(self.pushButton_1)
        layout.addWidget(self.pushButton_2)

        self.setLayout(layout)
        self.pushButton_1.clicked.connect(self.ok_clicked)
        self.pushButton_2.clicked.connect(self.close_clicked)
        self.setWindowTitle("Peak Threshold")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

    def ok_clicked(self):
        # if number entered, "ui.textEdit" will be edited.
        # "ui." means the main class "Ui_MainWindow". Use "Self." when calling in main class

        self.hide()
        Ui_MainWindow.OtherWindow_Button_ok_clicked(Ui_MainWindow, self.lineEdit.text())

        ui.textbox = ui.textbox + "\n" + "Resamole set to " + str(self.lineEdit.text())
        ui.textEdit.setPlainText(ui.textbox)

    def close_clicked(self):
        self.hide()