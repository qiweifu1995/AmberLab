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
        
        self.graphWidget.setTitle("test scatter plot", color="w", size="30pt")
        styles = {"color": "#fff", "font-size": "20px"}
        
        self.graphWidget.setLabel('left', 'Green', **styles)
        self.graphWidget.setLabel('bottom', 'Far Red', **styles)
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
        
        # threshold
        self.x_axis_threshold = QtWidgets.QLineEdit(self.splitter)
        self.x_axis_threshold.setObjectName("x_axis_threshold")
        
        self.y_axis_threshold = QtWidgets.QLineEdit(self.splitter)
        self.y_axis_threshold.setObjectName("y_axis_threshold")
        
        self.x_axis_threshold.setText("0")
        self.y_axis_threshold.setText("0")
        
        self.data_line_x = self.graphWidget.plot([0,0], [0,0], pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.data_line_y = self.graphWidget.plot([0,0], [0,0], pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
                
        self.x_axis_threshold.textChanged.connect(self.thresholdUpdated)
        self.y_axis_threshold.textChanged.connect(self.thresholdUpdated)
        # threshold end
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

        self.pushButton.clicked.connect(lambda:self.draw())
        self.pushButton_2.clicked.connect(lambda:self.clear())
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "start plot"))
        self.pushButton_2.setText(_translate("MainWindow", "clear plot"))
        

        
    def draw(self):
        
        # set x axis
        """self.Ch1_channel0 = [2.408,2.617,2.706,2.57,2.273,2.275,2.24,2.299,2.302,2.434,2.349,2.317,2.361,2.435,2.409,2.293,2.357,2.523,
                             2.927,2.331,2.359,2.939,2.363,2.399,2.312,2.333,2.703,2.404,2.225,2.34,2.373,2.273,2.31,2.323,2.298,2.35,
                             2.324,2.342,2.353,2.251,2.543,2.297,2.273,2.394,2.327,2.22,2.411,2.324,2.339,2.423,4.249,2.322,2.478,2.604,
                             2.364,2.375,2.412,2.272,2.406,2.357,2.266,2.321,2.469,2.41,2.36,2.423,2.208,2.309,2.915,2.319,2.162,2.19,
                             2.466,2.295,2.303,2.328,2.496,2.309,2.324,2.507,2.303,2.464,2.313,2.55,2.788,2.338,2.194,2.406,2.323,2.252,
                             2.329,2.267,2.304,2.946,2.446,2.118,2.301,2.431,2.468,2.273,2.383,2.301,2.342,2.372,2.368,2.3,2.296,2.525,
                             2.333,2.333,2.298,2.348,3.398,2.349,2.382,2.43,2.18,2.434,2.422,2.449,2.241,2.472,2.396,2.303,2.468,2.361,
                             2.445,2.3,2.459,2.329,2.32,2.339,2.315,2.391,2.336,2.337,2.38,2.341,2.302,2.4,2.846,2.306,2.276,2.322,2.396,
                             2.544,2.54,2.407,2.303,2.43,2.344,2.306,2.962,2.38,2.316,2.337,2.369,2.41,2.364,2.453,2.319,2.406,2.433,2.379,
                             2.444,2.266,2.349,2.334,2.309,2.378,2.307,2.317,2.516,2.247,2.251,2.666,2.474,2.304,2.345,2.353,2.224,2.322,
                             2.198,2.301,2.302,2.55,2.341,2.415,2.4,2.336,2.328,2.376,2.333,2.401,2.228,2.271,2.304,2.277,3.694,2.303,2.45,
                             2.33,2.3,2.239,2.331,2.439,2.702,2.118,2.35,2.233,2.32,2.362,2.308,2.354,2.776,2.217,2.334,2.356,2.516,2.515,
                             2.304,2.386,2.295]
        # set y axis
        self.Ch1_channel1 = [2.123, 2.41, 2.381, 2.246, 2.137, 2.048, 2.2, 2.241, 1.894, 2.191, 2.073, 1.966, 2.098, 2.405, 2.234, 2.114, 
                             2.192, 2.2, 2.438, 2.166, 2.167, 2.471, 2.089, 2.122, 2.248, 2.167, 2.414, 2.174, 2.069, 2.197, 2.254, 2.198, 
                             2.099, 2.118, 2.071, 2.131, 2.081, 2.169, 1.973, 2.108, 2.22, 2.091, 1.96, 2.148, 2.156, 2.185, 1.997, 2.018, 
                             2.197, 2.269, 3.113, 2.166, 2.24, 2.263, 2.108, 2.232, 2.149, 2.04, 2.089, 2.063, 2.049, 2.2, 2.219, 2.179, 
                             2.208, 2.022, 2.112, 1.984, 2.779, 2.126, 1.996, 2.062, 2.115, 2.331, 2.063, 2.057, 2.186, 2.068, 2.025, 2.187, 
                             1.962, 2.227, 2.09, 2.18, 3.244, 2.238, 1.957, 2.081, 2.107, 2.148, 2.165, 2.116, 2.042, 1.844, 2.173, 1.917, 
                             2.002, 2.335, 2.428, 2.181, 2.396, 2.131, 2.05, 2.208, 2.158, 2.317, 2.185, 2.246, 2.173, 2.419, 2.174, 1.974, 
                             1.797, 2.083, 2.328, 2.197, 2.139, 2.037, 2.164, 2.22, 2.166, 1.891, 2.149, 1.973, 2.134, 2.099, 2.19, 2.198, 
                             2.279, 1.949, 2.108, 2.14, 2.187, 2.07, 2.347, 2.131, 2.295, 2.261, 2.042, 2.198, 1.775, 2.182, 2.134, 2.153, 
                             2.057, 2.094, 2.144, 2.077, 2.013, 2.059, 2.065, 2.048, 2.046, 2.184, 2.157, 2.109, 2.089, 2.038, 2.159, 2.062, 
                             2.065, 2.139, 2.155, 2.125, 2.121, 2.142, 1.992, 2.096, 2.222, 2.156, 2.042, 1.904, 1.883, 1.928, 2.017, 2.089, 
                             1.739, 1.913, 2.003, 1.884, 1.873, 2.247, 2.052, 1.957, 2.121, 1.951, 2.112, 1.889, 1.884, 2.149, 2.105, 2.024, 
                             2.126, 1.693, 1.86, 2.177, 2.254, 1.955, 1.796, 1.823, 1.842, 1.823, 1.791, 1.99, 1.803, 1.743, 2.21, 2.034, 
                             2.005, 2.015, 2.112, 1.992, 1.979, 2.103, 2.413, 1.998, 1.985, 1.988, 2.099, 2.07, 2.009, 2.075, 1.916]
        """
        self.Ch1_channel0 = np.random.normal(5,1, 500000)
        self.Ch1_channel1 = np.random.normal(5, 1, 500000)
        max_voltage = 12
        bins = 1000
        steps = max_voltage / bins

        # all data is first sorted into a histogram
        histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins, [[0,max_voltage], [0,max_voltage]], density=True)
        max_density = histo.max()

        # made empty array to hold the sorted data according to density
        density_listx = []
        density_listy = []
        for i in range(6):
            density_listx.append([])
            density_listy.append([])

        print("start")
        for i in range(len(self.Ch1_channel0)):
            """legend_range = 0.07
            aa = [ii for ii, e in enumerate(self.Ch1_channel0) if (self.Ch1_channel0[i] + legend_range) > e > (self.Ch1_channel0[i] - legend_range)]
            bb = [ii for ii, e in enumerate(self.Ch1_channel1) if (self.Ch1_channel1[i] + legend_range) > e > (self.Ch1_channel1[i] - legend_range)]
            
            ab_set = len(set(aa) & set(bb))   
            """
            x = self.Ch1_channel0[i]
            y = self.Ch1_channel1[i]

            # checking for density, the value divided by steps serves as the index
            density = histo[int(x/steps)][int(y/steps)]
            percentage = density / max_density * 100
            if i%10000 == 0:
                print(i)
            if 15 > percentage >= 0:
                density_listx[0].append(x)
                density_listy[0].append(y)
            elif 30 > percentage >= 15:
                density_listx[1].append(x)
                density_listy[1].append(y)
            elif 45 > percentage >= 30:
                density_listx[2].append(x)
                density_listy[2].append(y)
            elif 60 > percentage >= 45:
                density_listx[3].append(x)
                density_listy[3].append(y)
            elif 75 > percentage >= 60:
                density_listx[4].append(x)
                density_listy[4].append(y)
            else:
                density_listx[5].append(x)
                density_listy[5].append(y)
        for i in range(6):
            if i == 0:
                red = 0
                blue =  255/15
                green =  255
            elif i == 1:
                red = 0
                blue = 255
                green = 255 - 255/15
            elif i == 2:
                red = 255/15
                blue = 255
                green = 0
            elif i == 3:
                red = 255
                blue = 255 - 255/15
                green = 0
            elif i == 4:
                red = 255
                blue = 255/15
                green = 255/15
            else:
                red = 255
                blue = 255
                green = 255
            self.graphWidget.plot(density_listx[i], density_listy[i], symbol='o', pen=None,
                                  symbolSize=5, symbolBrush=(red, blue, green))

        self.graphWidget.addLegend()    

        self.graphWidget.plot(name = "0~15%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(0,0,255))
        self.graphWidget.plot(name = "15~30%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(0,255,255))
        self.graphWidget.plot(name = "30~45%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(0,255,0))
        self.graphWidget.plot(name = "45~60%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(255,255,0))
        self.graphWidget.plot(name = "60~75%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(255,0,0))
        self.graphWidget.plot(name = ">75%",symbol='o',symbolPen=None,symbolSize=5, symbolBrush=(255,255,255))
        
        
#    >0%    0,0,1   blue        
#    >15%   0,1,1  cyan
#    >30%   0,1,0  green
#    >45%   1,1,0  yellow
#    >60%   1,0,0   red 
#    >75%   1,1,1   white

        #threshold
        self.thresholdUpdated()

    def thresholdUpdated(self):
        
        text_x = float(self.x_axis_threshold.text())
        text_y = float(self.y_axis_threshold.text())

        # x
        line_xx = [text_x,text_x]
        line_yy = [0,max(self.Ch1_channel1)]
        
        self.data_line_x.setData(line_xx, line_yy)
        # y
        line_x = [0,max(self.Ch1_channel0)]
        line_y = [text_y,text_y]
    
        self.data_line_y.setData(line_x, line_y)
        
        filtered_gate_voltage_x = [x for x in self.Ch1_channel0 if x > text_x]
        filtered_gate_voltage_y = [x for x in self.Ch1_channel1 if x > text_y]
        
        # filter y axis
        a = (np.array(self.Ch1_channel0) > text_x ).tolist()
        b = (np.array(self.Ch1_channel0) < text_x ).tolist()
        
        # filter x axis
        c = (np.array(self.Ch1_channel1) > text_y ).tolist()
        d = (np.array(self.Ch1_channel1) < text_y ).tolist()        
        

        count_quadrant1 = 0
        count_quadrant2 = 0
        count_quadrant3 = 0
        count_quadrant4 = 0
        
        for i in range(len(a)):
            if a[i] and c[i]:
                count_quadrant1 += 1
            elif not a[i] and c[i]:
                count_quadrant2 +=1
            elif a[i] and not c[i]:
                count_quadrant3 +=1
            elif not a[i] and not c[i]:
                count_quadrant4 +=1    
                
        print("quadrant 1(top right):",count_quadrant1)
        print("quadrant 2(top left):",count_quadrant2)
        print("quadrant 3(bottom right):",count_quadrant3)
        print("quadrant 4(bottom left):",count_quadrant4)
        ###  

    def regionUpdated(self,lr1,lr2):
        # for y axis
        lr1_min, lr1_max = lr1.getRegion()
        # for x axis
        lr2_min, lr2_max = lr2.getRegion()
        
        
        # filter y axis
        a = (np.array(self.Ch1_channel0) > lr2_min ).tolist()
        b = (np.array(self.Ch1_channel0) < lr2_max ).tolist()
        
        # filter x axis
        c = (np.array(self.Ch1_channel1) > lr1_min ).tolist()
        d = (np.array(self.Ch1_channel1) < lr1_max ).tolist()

#         print(a,b,c,d)

        count = 0
        for i in range(len(a)):
            if a[i] and b[i] and c[i] and d[i]:
                count = count + 1
        print("number of points inside the box:",count)

    
    

        
    def clear(self):
        self.graphWidget.clear()
        

if __name__ == "__main__":
    import sys
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
