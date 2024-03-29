# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scatterplottest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import numpy as np
from PyQt5 import QtGui  # Place this at the top of your file.
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(50, 50, 1300, 500))
        self.graphWidget.setObjectName("graphWidget")
        
        styles = {"color": "f#ff", "font-size": "20px"}
        self.graphWidget.setTitle("test histogram",size="30pt")
        self.graphWidget.setLabel('left', 'Frequency', **styles)
        self.graphWidget.setLabel('bottom', 'Green', **styles)
                
        self.graphWidget.setBackground('w')
#         self.graphWidget.setXRange(1, 10, padding=0)
#         self.graphWidget.setYRange(1, 10, padding=0)
        
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(150, 600, 441, 101))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # threshold
        self.x_axis_threshold = QtWidgets.QLineEdit(self.splitter)
        self.x_axis_threshold.setObjectName("x_axis_threshold")
        
        self.x_axis_threshold.setText("0")

        
        self.x_axis_threshold.textChanged.connect(self.thresholdUpdated)

        # threshold end
        
        
        self.pushButton.clicked.connect(lambda:self.draw())
        self.pushButton_2.clicked.connect(lambda:self.clear())
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "start plot"))
        self.pushButton_2.setText(_translate("MainWindow", "clear plot"))
        

        
    def draw(self):   
        self.width = [2.408,2.617,2.706,2.57,2.273,2.275,2.24,2.299,2.302,2.434,2.349,2.317,2.361,2.435,2.409,2.293,2.357,2.523,2.927,2.331,2.359,2.939,2.363,2.399,2.312,2.333,2.703,2.404,2.225,2.34,2.373,2.273,2.31,2.323,2.298,2.35,2.324,2.342,2.353,2.251,2.543,2.297,2.273,2.394,2.327,2.22,2.411,2.324,2.339,2.423,4.249,2.322,2.478,2.604,2.364,2.375,2.412,2.272,2.406,2.357,2.266,2.321,2.469,2.41,2.36,2.423,2.208,2.309,2.915,2.319,2.162,2.19,2.466,2.295,2.303,2.328,2.496,2.309,2.324,2.507,2.303,2.464,2.313,2.55,2.788,2.338,2.194,2.406,2.323,2.252,2.329,2.267,2.304,6.946,2.446,2.118,2.301,2.431,2.468,2.273,2.383,2.301,2.342,2.372,2.368,2.3,2.296,2.525,2.333,2.333,2.298,2.348,3.398,2.349,2.382,2.43,2.18,2.434,2.422,2.449,2.241,2.472,2.396,2.303,2.468,2.361,2.445,2.3,2.459,2.329,2.32,2.339,2.315,2.391,2.336,2.337,2.38,2.341,2.302,2.4,2.846,2.306,2.276,2.322,2.396,2.544,2.54,2.407,2.303,2.43,2.344,2.306,2.962,2.38,2.316,2.337,2.369,2.41,2.364,2.453,2.319,2.406,2.433,2.379,2.444,2.266,2.349,2.334,2.309,2.378,2.307,2.317,2.516,2.247,2.251,2.666,2.474,2.304,2.345,2.353,2.224,2.322,2.198,2.301,2.302,2.55,2.341,2.415,2.4,2.336,2.328,2.376,2.333,2.401,2.228,2.271,2.304,2.277,3.694,2.303,2.45,2.33,2.3,2.239,2.331,2.439,2.702,2.118,2.35,2.233,2.32,2.362,2.308,2.354,2.776,2.217,2.334,2.356,2.516,2.515,2.304,2.386,2.295]
        range_width = int(max(self.width))+1
        y,x = np.histogram(self.width, bins=np.linspace(0, range_width , range_width*10+1))
        separate_y = [0]*len(y)
        for i in range(len(y)):
            separate_y = [0]*len(y)
            separate_y[i] = y[i]
            self.graphWidget.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(255,255,0))

        self.graphWidget.setXRange(0, max(x), padding=0)
        self.graphWidget.setYRange(0, max(y), padding=0)
        
        #after 1st map so the line will appear before the histogram
        self.data_line_x = self.graphWidget.plot([0,0], [0,0], pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.thresholdUpdated()
        
    def clear(self):
        self.graphWidget.clear()

    def thresholdUpdated(self):
        
        text_x = float(self.x_axis_threshold.text())
        # x
        line_xx = [text_x,text_x]
        line_yy = [0,200]
        
        self.data_line_x.setData(line_xx, line_yy)

        filtered_gate_voltage_x = [x for x in self.width if x > text_x]


        print("smaller than threshold(left):",(len(self.width)-len(filtered_gate_voltage_x)))        
        print("bigger than threshold(right):",len(filtered_gate_voltage_x))
        
        ###  
        

if __name__ == "__main__":
    import sys
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
