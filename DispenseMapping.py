# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import pandas as pd
from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QFileDialog
import os, csv, Wells, math


class Mapping_MainWindow(object):
    fileindex = []
    well_object = Wells.Wells
    well_state = []
    well_mode = 96
    chunk_size = 200

    def setupUi(self, MainWindow):

        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1007, 688)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_5.setObjectName("gridLayout_5")

        spacerItem = QtWidgets.QSpacerItem(1, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 10, 10, 10, 1)

        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 1)

        self.PlateNumber = QtWidgets.QComboBox(self.centralwidget)
        self.PlateNumber.setObjectName("PlateNumber")
        self.gridLayout_5.addWidget(self.PlateNumber, 0, 0, 1, 1)
        self.PlateNumber.currentIndexChanged.connect(self.plate_update)

        self.horizontalLayout.addLayout(self.gridLayout_5)

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.AnalogTab = QtWidgets.QWidget()
        self.AnalogTab.setObjectName("AnalogTab")
        self.tabWidget.addTab(self.AnalogTab, "")
        self.ImageTab = QtWidgets.QWidget()
        self.ImageTab.setObjectName("ImageTab")

        self.tabWidget.addTab(self.ImageTab, "")
        self.StatsTab = QtWidgets.QWidget()
        self.StatsTab.setObjectName("StatsTab")
        self.tabWidget.addTab(self.StatsTab, "")

        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1007, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExport = QtWidgets.QMenu(self.menuFile)
        self.menuExport.setObjectName("menuExport")
        self.menuPeak_Profiles = QtWidgets.QMenu(self.menuExport)
        self.menuPeak_Profiles.setObjectName("menuPeak_Profiles")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        self.menu_WellSetting = QtWidgets.QMenu(self.menuOptions)
        self.menu_WellSetting.setObjectName("menu_WellSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.action48 = QtWidgets.QAction(MainWindow)
        self.action48.setCheckable(True)
        self.action48.setObjectName("action48")
        self.action_chunck_size = QtWidgets.QAction(MainWindow)
        self.action_chunck_size.setCheckable(True)
        self.action_chunck_size.setObjectName("action_chunk_size")
        self.actionPeaks_Signal_All = QtWidgets.QAction(MainWindow)
        self.actionPeaks_Signal_All.setObjectName("actionPeaks_Signal_All")
        self.action_i = QtWidgets.QAction(MainWindow)
        self.action_i.setObjectName("action_i")
        self.actionAll = QtWidgets.QAction(MainWindow)
        self.actionAll.setObjectName("actionAll")
        self.actionCurrent = QtWidgets.QAction(MainWindow)
        self.actionCurrent.setObjectName("actionCurrent")
        self.actionImage_Root_Folder_Location = QtWidgets.QAction(MainWindow)
        self.actionImage_Root_Folder_Location.setObjectName("actionImage_Root_Folder_Location")
        self.menuPeak_Profiles.addAction(self.actionAll)
        self.menuPeak_Profiles.addAction(self.actionCurrent)
        self.menuExport.addAction(self.menuPeak_Profiles.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuFile.addAction(self.actionClose)
        self.menu_WellSetting.addAction(self.action48)
        self.menu_WellSetting.addAction(self.action_chunck_size)
        self.menuOptions.addAction(self.menu_WellSetting.menuAction())
        self.menuOptions.addAction(self.actionImage_Root_Folder_Location)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        # in analog tab

        self.graphicsView9 = PlotWidget(self.AnalogTab)
        self.graphicsView9.setGeometry(QtCore.QRect(0, 0, 1500, 800))
        self.graphicsView9.setObjectName("graphicsView9")
        self.graphicsView9.hide()

        # promoted cell in Image Tab

        self.graphicsView2 = PlotWidget()
        # self.graphicsView2.setGeometry(QtCore.QRect(450, 0, 450, 300))
        self.graphicsView2.setObjectName("graphicsView2")

        self.graphicsView3 = PlotWidget()
        # self.graphicsView3.setGeometry(QtCore.QRect(900, 0, 450, 300))
        self.graphicsView3.setObjectName("graphicsView3")

        self.graphicsView4 = PlotWidget()
        # self.graphicsView4.setGeometry(QtCore.QRect(0, 300, 450, 300))
        self.graphicsView4.setObjectName("graphicsView4")

        self.graphicsView5 = PlotWidget()
        # self.graphicsView5.setGeometry(QtCore.QRect(450, 300, 450, 300))
        self.graphicsView5.setObjectName("graphicsView5")

        self.graphicsView6 = PlotWidget()
        # self.graphicsView6.setGeometry(QtCore.QRect(900, 300, 450, 300))
        self.graphicsView6.setObjectName("graphicsView6")

        self.graphicsView7 = PlotWidget()
        # self.graphicsView7.setGeometry(QtCore.QRect(0, 600, 450, 300))
        self.graphicsView7.setObjectName("graphicsView7")

        self.graphicsView8 = PlotWidget()
        # self.graphicsView8.setGeometry(QtCore.QRect(450, 600, 450, 300))
        self.graphicsView8.setObjectName("graphicsView8")

        self.graphicsView1 = PlotWidget()
        # self.graphicsView1.setGeometry(QtCore.QRect(0, 0, 450, 300))
        self.graphicsView1.setObjectName("graphicsView1")

        self.Graph_Layout = QtWidgets.QGridLayout()
        self.AnalogTab.setLayout(self.Graph_Layout)
        self.Graph_Layout.addWidget(self.graphicsView1, 0, 0)
        self.Graph_Layout.addWidget(self.graphicsView2, 0, 1)
        self.Graph_Layout.addWidget(self.graphicsView3, 0, 2)
        self.Graph_Layout.addWidget(self.graphicsView4, 0, 3)
        self.Graph_Layout.addWidget(self.graphicsView5, 1, 0)
        self.Graph_Layout.addWidget(self.graphicsView6, 1, 1)
        self.Graph_Layout.addWidget(self.graphicsView7, 1, 2)
        self.Graph_Layout.addWidget(self.graphicsView8, 1, 3)

        self.actionClose.triggered.connect(sys.exit)
        self.action48.triggered.connect(self.set_well_mode)
        self.action_chunck_size.triggered.connect(self.set_chunk_size)

        # background color
        for j in range(1, 10):
            i = str(j)
            styles = {'color': 'r', 'font-size': '20px'}
            code1 = ["self.graphicsView", i, ".setBackground('w')"]
            code2 = ["self.graphicsView", i, ".setTitle('Chart #", i, "', color='k', size='20pt')"]
            code3 = ["self.graphicsView", i, ".setLabel('left', 'Voltage', **styles)"]
            code4 = ["self.graphicsView", i, ".setLabel('bottom', 'Samples', **styles)"]
            code5 = ["self.graphicsView", i, ".addLegend()"]
            code6 = ["self.graphicsView", i, ".showGrid(x=True, y=True)"]

            join1 = "".join(code1)
            join2 = "".join(code2)
            join3 = "".join(code3)
            join4 = "".join(code4)
            join5 = "".join(code5)
            join6 = "".join(code6)

            exec(join1)
            exec(join2)
            exec(join3)
            exec(join4)
            exec(join5)
            exec(join6)

        # wells

        #        test_list = [1,2,3,4,5]

        ########################## create well blocks, ex: Well1
        for j in range(1, 13):
            for j_row in range(3, 11):
                column = str(j)
                i = str(j)
                i_row = str(j_row)

                well_number = str((j_row - 2) + (j - 1) * 8)

                code1 = ["self.Well", well_number, " = QtWidgets.QCheckBox(self.centralwidget)"]
                code2 = ["self.Well", well_number, ".setObjectName('Well", well_number, "')"]
                code3 = ["self.gridLayout_4.addWidget(self.Well", well_number, ", ", i_row, ",", column, ", 1, 1) "]
                join1 = "".join(code1)
                join2 = "".join(code2)
                join3 = "".join(code3)
                exec(join1)
                exec(join2)
                exec(join3)

                code1 = ["self.Well", well_number, ".setEnabled(False)"]
                join1 = "".join(code1)
                exec(join1)

        ########################## ends

        self.Well1.toggled.connect(lambda: self.btnstate(self.Well1, 1))
        self.Well2.toggled.connect(lambda: self.btnstate(self.Well2, 2))
        self.Well3.toggled.connect(lambda: self.btnstate(self.Well3, 3))
        self.Well4.toggled.connect(lambda: self.btnstate(self.Well4, 4))
        self.Well5.toggled.connect(lambda: self.btnstate(self.Well5, 5))
        self.Well6.toggled.connect(lambda: self.btnstate(self.Well6, 6))
        self.Well7.toggled.connect(lambda: self.btnstate(self.Well7, 7))
        self.Well8.toggled.connect(lambda: self.btnstate(self.Well8, 8))
        self.Well9.toggled.connect(lambda: self.btnstate(self.Well9, 9))
        self.Well10.toggled.connect(lambda: self.btnstate(self.Well10, 10))
        self.Well11.toggled.connect(lambda: self.btnstate(self.Well11, 11))
        self.Well12.toggled.connect(lambda: self.btnstate(self.Well12, 12))
        self.Well13.toggled.connect(lambda: self.btnstate(self.Well13, 13))
        self.Well14.toggled.connect(lambda: self.btnstate(self.Well14, 14))
        self.Well15.toggled.connect(lambda: self.btnstate(self.Well15, 15))
        self.Well16.toggled.connect(lambda: self.btnstate(self.Well16, 16))
        self.Well17.toggled.connect(lambda: self.btnstate(self.Well17, 17))
        self.Well18.toggled.connect(lambda: self.btnstate(self.Well18, 18))
        self.Well19.toggled.connect(lambda: self.btnstate(self.Well19, 19))
        self.Well20.toggled.connect(lambda: self.btnstate(self.Well20, 20))
        self.Well21.toggled.connect(lambda: self.btnstate(self.Well21, 21))
        self.Well22.toggled.connect(lambda: self.btnstate(self.Well22, 22))
        self.Well23.toggled.connect(lambda: self.btnstate(self.Well23, 23))
        self.Well24.toggled.connect(lambda: self.btnstate(self.Well24, 24))
        self.Well25.toggled.connect(lambda: self.btnstate(self.Well25, 25))
        self.Well26.toggled.connect(lambda: self.btnstate(self.Well26, 26))
        self.Well27.toggled.connect(lambda: self.btnstate(self.Well27, 27))
        self.Well28.toggled.connect(lambda: self.btnstate(self.Well28, 28))
        self.Well29.toggled.connect(lambda: self.btnstate(self.Well29, 29))
        self.Well30.toggled.connect(lambda: self.btnstate(self.Well30, 30))
        self.Well31.toggled.connect(lambda: self.btnstate(self.Well31, 31))
        self.Well32.toggled.connect(lambda: self.btnstate(self.Well32, 32))
        self.Well33.toggled.connect(lambda: self.btnstate(self.Well33, 33))
        self.Well34.toggled.connect(lambda: self.btnstate(self.Well34, 34))
        self.Well35.toggled.connect(lambda: self.btnstate(self.Well35, 35))
        self.Well36.toggled.connect(lambda: self.btnstate(self.Well36, 36))
        self.Well37.toggled.connect(lambda: self.btnstate(self.Well37, 37))
        self.Well38.toggled.connect(lambda: self.btnstate(self.Well38, 38))
        self.Well39.toggled.connect(lambda: self.btnstate(self.Well39, 39))
        self.Well40.toggled.connect(lambda: self.btnstate(self.Well40, 40))
        self.Well41.toggled.connect(lambda: self.btnstate(self.Well41, 41))
        self.Well42.toggled.connect(lambda: self.btnstate(self.Well42, 42))
        self.Well43.toggled.connect(lambda: self.btnstate(self.Well43, 43))
        self.Well44.toggled.connect(lambda: self.btnstate(self.Well44, 44))
        self.Well45.toggled.connect(lambda: self.btnstate(self.Well45, 45))
        self.Well46.toggled.connect(lambda: self.btnstate(self.Well46, 46))
        self.Well47.toggled.connect(lambda: self.btnstate(self.Well47, 47))
        self.Well48.toggled.connect(lambda: self.btnstate(self.Well48, 48))
        self.Well49.toggled.connect(lambda: self.btnstate(self.Well49, 49))
        self.Well50.toggled.connect(lambda: self.btnstate(self.Well50, 50))
        self.Well51.toggled.connect(lambda: self.btnstate(self.Well51, 51))
        self.Well52.toggled.connect(lambda: self.btnstate(self.Well52, 52))
        self.Well53.toggled.connect(lambda: self.btnstate(self.Well53, 53))
        self.Well54.toggled.connect(lambda: self.btnstate(self.Well54, 54))
        self.Well55.toggled.connect(lambda: self.btnstate(self.Well55, 55))
        self.Well56.toggled.connect(lambda: self.btnstate(self.Well56, 56))
        self.Well57.toggled.connect(lambda: self.btnstate(self.Well57, 57))
        self.Well58.toggled.connect(lambda: self.btnstate(self.Well58, 58))
        self.Well59.toggled.connect(lambda: self.btnstate(self.Well59, 59))
        self.Well60.toggled.connect(lambda: self.btnstate(self.Well60, 60))
        self.Well61.toggled.connect(lambda: self.btnstate(self.Well61, 61))
        self.Well62.toggled.connect(lambda: self.btnstate(self.Well62, 62))
        self.Well63.toggled.connect(lambda: self.btnstate(self.Well63, 63))
        self.Well64.toggled.connect(lambda: self.btnstate(self.Well64, 64))
        self.Well65.toggled.connect(lambda: self.btnstate(self.Well65, 65))
        self.Well66.toggled.connect(lambda: self.btnstate(self.Well66, 66))
        self.Well67.toggled.connect(lambda: self.btnstate(self.Well67, 67))
        self.Well68.toggled.connect(lambda: self.btnstate(self.Well68, 68))
        self.Well69.toggled.connect(lambda: self.btnstate(self.Well69, 69))
        self.Well70.toggled.connect(lambda: self.btnstate(self.Well70, 70))
        self.Well71.toggled.connect(lambda: self.btnstate(self.Well71, 71))
        self.Well72.toggled.connect(lambda: self.btnstate(self.Well72, 72))
        self.Well73.toggled.connect(lambda: self.btnstate(self.Well73, 73))
        self.Well74.toggled.connect(lambda: self.btnstate(self.Well74, 74))
        self.Well75.toggled.connect(lambda: self.btnstate(self.Well75, 75))
        self.Well76.toggled.connect(lambda: self.btnstate(self.Well76, 76))
        self.Well77.toggled.connect(lambda: self.btnstate(self.Well77, 77))
        self.Well78.toggled.connect(lambda: self.btnstate(self.Well78, 78))
        self.Well79.toggled.connect(lambda: self.btnstate(self.Well79, 79))
        self.Well80.toggled.connect(lambda: self.btnstate(self.Well80, 80))
        self.Well81.toggled.connect(lambda: self.btnstate(self.Well81, 81))
        self.Well82.toggled.connect(lambda: self.btnstate(self.Well82, 82))
        self.Well83.toggled.connect(lambda: self.btnstate(self.Well83, 83))
        self.Well84.toggled.connect(lambda: self.btnstate(self.Well84, 84))
        self.Well85.toggled.connect(lambda: self.btnstate(self.Well85, 85))
        self.Well86.toggled.connect(lambda: self.btnstate(self.Well86, 86))
        self.Well87.toggled.connect(lambda: self.btnstate(self.Well87, 87))
        self.Well88.toggled.connect(lambda: self.btnstate(self.Well88, 88))
        self.Well89.toggled.connect(lambda: self.btnstate(self.Well89, 89))
        self.Well90.toggled.connect(lambda: self.btnstate(self.Well90, 90))
        self.Well91.toggled.connect(lambda: self.btnstate(self.Well91, 91))
        self.Well92.toggled.connect(lambda: self.btnstate(self.Well92, 92))
        self.Well93.toggled.connect(lambda: self.btnstate(self.Well93, 93))
        self.Well94.toggled.connect(lambda: self.btnstate(self.Well94, 94))
        self.Well95.toggled.connect(lambda: self.btnstate(self.Well95, 95))
        self.Well96.toggled.connect(lambda: self.btnstate(self.Well96, 96))

        # push buttons

        ##########################  create push buttons, ex: pushButton1
        for j in range(1, 13):
            i = str(j)
            column_index = str(j)
            code1 = ["self.pushButton", i, " = QtWidgets.QPushButton(self.centralwidget)"]
            code2 = ["self.pushButton", i, ".setMaximumSize(QtCore.QSize(17, 17))"]
            code3 = ["self.pushButton", i, ".setObjectName('pushButton", i, "')"]
            code4 = ["self.gridLayout_4.addWidget(self.pushButton", i, ", 2, ", column_index, ", 1, 1)"]
            join1 = "".join(code1)
            join2 = "".join(code2)
            join3 = "".join(code3)
            join4 = "".join(code4)
            exec(join1)
            exec(join2)
            exec(join3)
            exec(join4)
        ########################## ends

        self.pushButtonSwitch1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSwitch1.setMaximumSize(QtCore.QSize(68, 34))
        self.pushButtonSwitch1.setObjectName('pushButtonSwitch1')
        self.gridLayout_4.addWidget(self.pushButtonSwitch1, 12, 2, 2, 3)

        self.pushButtonSwitch2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSwitch2.setMaximumSize(QtCore.QSize(68, 34))
        self.pushButtonSwitch2.setObjectName('pushButtonSwitch2')
        self.gridLayout_4.addWidget(self.pushButtonSwitch2, 12, 6, 2, 3)

        self.pushButtonSwitch1.clicked.connect(self.show_9_plots)
        self.pushButtonSwitch2.clicked.connect(self.show_1_plot)

        # labels
        ########################## create row index, ex: label1
        for j in range(1, 9):
            i = str(j)
            row = str(j + 2)
            code1 = ["self.label", i, " = QtWidgets.QLabel(self.centralwidget)"]
            code2 = ["self.label", i, ".setObjectName('label", i, "')"]
            code3 = ["self.gridLayout_4.addWidget(self.label", i, ", ", row, ", 0, 1, 1)"]
            join1 = "".join(code1)
            join2 = "".join(code2)
            join3 = "".join(code3)
            exec(join1)
            exec(join2)
            exec(join3)
        ########################## create row index ends

        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setObjectName('labelStatus')
        self.gridLayout_4.addWidget(self.labelStatus, 14, 0, 1, 10)

        self.pushButton1.clicked.connect(lambda: self.pressed(self.pushButton1))
        self.pushButton2.clicked.connect(lambda: self.pressed(self.pushButton2))
        self.pushButton3.clicked.connect(lambda: self.pressed(self.pushButton3))
        self.pushButton4.clicked.connect(lambda: self.pressed(self.pushButton4))
        self.pushButton5.clicked.connect(lambda: self.pressed(self.pushButton5))
        self.pushButton6.clicked.connect(lambda: self.pressed(self.pushButton6))
        self.pushButton7.clicked.connect(lambda: self.pressed(self.pushButton7))
        self.pushButton8.clicked.connect(lambda: self.pressed(self.pushButton8))
        self.pushButton9.clicked.connect(lambda: self.pressed(self.pushButton9))
        self.pushButton10.clicked.connect(lambda: self.pressed(self.pushButton10))
        self.pushButton11.clicked.connect(lambda: self.pressed(self.pushButton11))
        self.pushButton12.clicked.connect(lambda: self.pressed(self.pushButton12))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionOpen.triggered.connect(self.openfolder)
        self.labelStatus.setText("Current plot mode: 9 plots")

    def set_chunk_size(self):
        """function for changing the chunk size fromm 200 to 1000"""
        if self.action_chunck_size.isChecked():
            self.chunk_size = 1000
        else:
            self.chunk_size = 200

    def set_well_mode(self):
        if self.action48.isChecked():
            self.well_mode = 48
        else:
            self.well_mode = 96

    def show_9_plots(self):
        text = "Current plot mode: 9 plots"
        self.labelStatus.setText(text)
        self.labelStatus.adjustSize()

        """self.graphicsView9.setGeometry(QtCore.QRect(0, 0, 0, 0))

        self.graphicsView2.setGeometry(QtCore.QRect(450, 0, 450, 300))
        self.graphicsView3.setGeometry(QtCore.QRect(900, 0, 450, 300))
        self.graphicsView4.setGeometry(QtCore.QRect(0, 300, 450, 300))
        self.graphicsView5.setGeometry(QtCore.QRect(450, 300, 450, 300))
        self.graphicsView6.setGeometry(QtCore.QRect(900, 300, 450, 300))
        self.graphicsView7.setGeometry(QtCore.QRect(0, 600, 450, 300))
        self.graphicsView8.setGeometry(QtCore.QRect(450, 600, 450, 300))
        self.graphicsView1.setGeometry(QtCore.QRect(0, 0, 450, 300))
        """
        self.graphicsView1.show()
        self.graphicsView2.show()
        self.graphicsView3.show()
        self.graphicsView4.show()
        self.graphicsView5.show()
        self.graphicsView6.show()
        self.graphicsView7.show()
        self.graphicsView8.show()
        self.graphicsView9.hide()

    def show_1_plot(self):
        text = "Current plot mode: 1 plot"
        self.labelStatus.setText(text)
        self.labelStatus.adjustSize()

        self.graphicsView2.hide()
        self.graphicsView3.hide()
        self.graphicsView4.hide()
        self.graphicsView5.hide()
        self.graphicsView6.hide()
        self.graphicsView7.hide()
        self.graphicsView8.hide()
        self.graphicsView1.hide()

        self.graphicsView9.show()
        self.graphicsView9.setGeometry(QtCore.QRect(0, 0, 1500, 800))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.pushButtonSwitch1.setText(_translate("MainWindow", "9-plots"))
        self.pushButtonSwitch2.setText(_translate("MainWindow", "1-plot"))
        self.labelStatus.setText(_translate('MainWindow', "Current plot mode: Empty "))

        ########################## assign button letter
        for j in range(1, 13):
            i = str(j)
            code1 = ["self.pushButton", i, ".setText(_translate('MainWindow', '", i, "'))"]
            join1 = "".join(code1)
            exec(join1)
        ########################## assign ends

        ########################## assign row index letter
        for j in range(1, 9):
            i = str(j)
            row_letter = j + 64

            code1 = ["self.label", i, ".setText(_translate('MainWindow', chr(row_letter)))"]
            join1 = "".join(code1)
            exec(join1)
        ########################## assign ends

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AnalogTab), _translate("MainWindow", "Analog Signal"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ImageTab), _translate("MainWindow", "Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.StatsTab), _translate("MainWindow", "Statistic"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuPeak_Profiles.setTitle(_translate("MainWindow", "Peak Profiles"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.menu_WellSetting.setTitle(_translate("MainWindow", "WellSetting"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.action48.setText(_translate("MainWindow", "48 Wells"))
        self.action_chunck_size.setText(_translate("MainWindow", "Legacy Chunk Size"))
        self.actionPeaks_Signal_All.setText(_translate("MainWindow", "Peaks Signal (All)"))
        self.action_i.setText(_translate("MainWindow", " i"))
        self.actionAll.setText(_translate("MainWindow", "All"))
        self.actionCurrent.setText(_translate("MainWindow", "Current "))
        self.actionImage_Root_Folder_Location.setText(_translate("MainWindow", "Image Root Folder Location"))

    def pressed(self, a):

        button_number = int(a.text())
        print(button_number)

        for j in range(1, 97):
            i = str(j)
            code1 = ["self.Well", i, ".setChecked(False)"]
            join1 = "".join(code1)
            exec(join1)

        if self.PlateNumber.currentIndex() * 12 + button_number - 1 < len(self.well_object.plate_data):
            for i in range(len(self.well_object.plate_data[self.PlateNumber.currentIndex() * 12 + button_number - 1])):
                print("range is", i)
                print(self.PlateNumber.currentIndex() * 12 + button_number - 1)
                print(len(self.well_object.plate_data))
                if len(self.well_object.plate_data[self.PlateNumber.currentIndex() * 12 + button_number - 1][i]) > 0:
                    print("content",
                          self.well_object.plate_data[self.PlateNumber.currentIndex() * 12 + button_number - 1][i])
                    holder = str((button_number - 1) * 8 + i + 1)

                    code1 = ["self.Well", holder, ".setChecked(True)"]
                    print(code1)
                    join1 = "".join(code1)
                    exec(join1)

    def openfolder(self):
        """function return the list of """
        root_folder = QFileDialog.getExistingDirectory(self.mainwindow, 'Open')
        self.fileindex = Wells.index_files(root_folder)
        print(self.fileindex)
        self.well_object = Wells.Wells(root_folder, self.fileindex, self.chunk_size, self.well_mode)
        self.PlateNumber.clear()
        # for i in range(8):
        # print(self.well_object.plate_data[0][i])
        # for i in range(8):
        # print(self.well_object.plate_data[1][i])
        for i in range(math.ceil(self.well_object.number_of_strips / 12)):
            text_holder = 'Plate ' + str(i + 1)
            self.PlateNumber.addItem(text_holder)
        self.tabWidget.setCurrentIndex(0)

    def plate_update(self):
        """update plate information when plate number changes"""

        for strip in range(self.PlateNumber.currentIndex() * 12, self.PlateNumber.currentIndex() * 12 + 12):
            for well in range(8):
                # print(strip)
                well_number = str(8 * (strip % 12) + well + 1)
                try:
                    holder = self.well_object.plate_data[strip][well]
                    if len(holder) == 0:
                        code1 = ["self.Well", well_number, ".setEnabled(False)"]
                        join1 = "".join(code1)
                        exec(join1)
                    else:
                        code1 = ["self.Well", well_number, ".setEnabled(True)"]
                        join1 = "".join(code1)
                        exec(join1)
                except IndexError:
                    code1 = ["self.Well", well_number, ".setEnabled(False)"]
                    join1 = "".join(code1)
                    exec(join1)

    def btnstate(self, b, c):
        global well_number1, well_number2, well_number3, well_number4, well_number5, well_number6, well_number7, well_number8, total_numbers_of_graph
        index = list(range(1, self.chunk_size + 1))

        last_work_check = total_numbers_of_graph

        a = self.labelStatus.text()
        print("btnstate called", a)

        if b.isChecked():
            if well_number1 == 0:
                well_number1 = int(c)
                graph_number = "1"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number2 == 0:
                well_number2 = int(c)
                graph_number = "2"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number3 == 0:
                well_number3 = int(c)
                graph_number = "3"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number4 == 0:
                well_number4 = int(c)
                graph_number = "4"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number5 == 0:
                well_number5 = int(c)
                graph_number = "5"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number6 == 0:
                well_number6 = int(c)
                graph_number = "6"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number7 == 0:
                well_number7 = int(c)
                graph_number = "7"
                total_numbers_of_graph = total_numbers_of_graph + 1

            elif well_number8 == 0:
                well_number8 = int(c)
                graph_number = "8"
                total_numbers_of_graph = total_numbers_of_graph + 1

            if last_work_check != total_numbers_of_graph and a == "Current plot mode: 9 plots":
                """
                if total_numbers_of_graph == 1:
                    code1 = ["self.graphicsView", graph_number,".setGeometry(QtCore.QRect(0, 0, 1000,800))"]
                    code2 = ["self.graphicsView", graph_number,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    exec(join2)
                """
                if total_numbers_of_graph == 2:
                    """
                    code1 = ["self.graphicsView", graph_number,".setGeometry(QtCore.QRect(700, 0, 700,800))"]
                    code2 = ["self.graphicsView", graph_number,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    exec(join2)
                    """
                    if (well_number1 != 0) and (well_number1 != int(c)):
                        graph_number_1st_picture = "1"
                    elif well_number2 != 0 and (well_number2 != int(c)):
                        graph_number_1st_picture = "2"
                    elif well_number3 != 0 and (well_number3 != int(c)):
                        graph_number_1st_picture = "3"
                    elif well_number4 != 0 and (well_number4 != int(c)):
                        graph_number_1st_picture = "4"
                    elif well_number5 != 0 and (well_number5 != int(c)):
                        graph_number_1st_picture = "5"
                    elif well_number6 != 0 and (well_number6 != int(c)):
                        graph_number_1st_picture = "6"
                    elif well_number7 != 0 and (well_number7 != int(c)):
                        graph_number_1st_picture = "7"
                    elif well_number8 != 0 and (well_number8 != int(c)):
                        graph_number_1st_picture = "8"

                    """code1 = ["self.graphicsView", graph_number_1st_picture,".setGeometry(QtCore.QRect(0, 0, 700,800))"]
                    code2 = ["self.graphicsView", graph_number_1st_picture,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    #exec(join2)"""
                """else:
                    self.graphicsView2.setGeometry(QtCore.QRect(450, 0, 450, 300))
                    self.graphicsView3.setGeometry(QtCore.QRect(900, 0, 450, 300))
                    self.graphicsView4.setGeometry(QtCore.QRect(0, 300, 450, 300))
                    self.graphicsView5.setGeometry(QtCore.QRect(450, 300, 450, 300))
                    self.graphicsView6.setGeometry(QtCore.QRect(900, 300, 450, 300))
                    self.graphicsView7.setGeometry(QtCore.QRect(0, 600, 450, 300))
                    self.graphicsView8.setGeometry(QtCore.QRect(450, 600, 450, 300))
                    self.graphicsView1.setGeometry(QtCore.QRect(0, 0, 450, 300))"""

                ##### draw

                ### in Image tab
                """
                code1 = ["int(Dispense_Mapping_well_as_index.loc[well_number", graph_number," ,'Peak Record Index'])"]
                join1 = "".join(code1)
                """
                code1 = ["well_number", graph_number]
                join1 = "".join(code1)

                record_index = eval(join1)
                # print(record_index)

                record_index_strip = math.ceil(eval(join1) / 8) + 12 * self.PlateNumber.currentIndex()
                record_index_well = (eval(join1) - 1) % 8 + 1
                print("record index strip: ", record_index_strip)
                print("record index Well: ", record_index_well)

                #                 record_index = int(Dispense_Mapping_well_as_index.loc[well_number1 ,'Peak Record Index'])
                """
                record_index_min = (record_index - 1) * 1000
                record_index_max = record_index * 1000
                Peak_Record_with_index = Peak_Record[(record_index_min + 1):(record_index_max + 1)].reset_index()
    #                 index = Peak_Record_with_index[0:1000]['index'].values.tolist()


                channel_1 = Peak_Record_with_index[0:1000]['Channel 1'].values.tolist()
                channel_2 = Peak_Record_with_index[0:1000]['Channel 2'].values.tolist()
                channel_3 = Peak_Record_with_index[0:1000]['Channel 3'].values.tolist()
                channel_4 = Peak_Record_with_index[0:1000]['Channel 4'].values.tolist()
                """

                channel_1 = []
                channel_2 = []
                channel_3 = []
                channel_4 = []
                for i in self.well_object.plate_data[record_index_strip - 1][record_index_well - 1]:
                    channel_1.append(float(i[0]))
                    channel_2.append(float(i[1]))
                    channel_3.append(float(i[2]))
                    channel_4.append(float(i[3]))

                # print(channel_1)

                # self.graphicsView1.plot(channel_1)
                print('plot1?')
                code1 = ["self.graphicsView", graph_number,
                         ".plot(index, channel_1, name='Channel_1', pen='g', symbol='o', symbolSize=3, symbolBrush=('g'))"]
                print('plot2?')
                code2 = ["self.graphicsView", graph_number,
                         ".plot(index, channel_2, name='Channel_2', pen='r', symbol='o', symbolSize=3, symbolBrush=('r'))"]
                print('plot3?')
                code3 = ["self.graphicsView", graph_number,
                         ".plot(index, channel_3, name='Channel_3', pen='b', symbol='o', symbolSize=3, symbolBrush=('b'))"]
                print('plot4?')
                code4 = ["self.graphicsView", graph_number,
                         ".plot(index, channel_4, name='Channel_4', pen='m', symbol='o', symbolSize=3, symbolBrush=('m'))"]

                join1 = "".join(code1)
                join2 = "".join(code2)
                join3 = "".join(code3)
                join4 = "".join(code4)

                code5 = ["self.graphicsView", graph_number, ".setTitle('Strip ", str(record_index_strip), " Well ",
                         str(record_index_well), "', color='k', size='20pt')"]
                join5 = "".join(code5)

                exec(join1)
                exec(join2)
                exec(join3)
                exec(join4)
                exec(join5)

                ### in analog tab

            if last_work_check != total_numbers_of_graph and a == "Current plot mode: 1 plot":
                """
                code1 = ["int(Dispense_Mapping_well_as_index.loc[well_number", graph_number," ,'Peak Record Index'])"]
                join1 = "".join(code1)
                record_index = eval(join1)
                """
                print("plotting 1 plot")

                code1 = ["well_number", graph_number]
                join1 = "".join(code1)

                record_index = eval(join1)

                record_index_strip = math.ceil(eval(join1) / 8) + self.PlateNumber.currentIndex()
                record_index_well = eval(join1) % 8

                channel_1 = []
                channel_2 = []
                channel_3 = []
                channel_4 = []
                for i in self.well_object.plate_data[record_index_strip - 1][record_index_well - 1]:
                    channel_1.append(float(i[0]))
                    channel_2.append(float(i[1]))
                    channel_3.append(float(i[2]))
                    channel_4.append(float(i[3]))

                self.graphicsView9.plot(index, channel_1, name='Channel_1', pen='g', symbol='o', symbolSize=3,
                                        symbolBrush=('g'))
                self.graphicsView9.plot(index, channel_2, name='Channel_2', pen='r', symbol='o', symbolSize=3,
                                        symbolBrush=('r'))
                self.graphicsView9.plot(index, channel_3, name='Channel_3', pen='b', symbol='o', symbolSize=3,
                                        symbolBrush=('b'))
                self.graphicsView9.plot(index, channel_4, name='Channel_4', pen='m', symbol='o', symbolSize=3,
                                        symbolBrush=('m'))

        else:
            if well_number1 == int(c):
                self.graphicsView1.clear()
                well_number1 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number2 == int(c):
                self.graphicsView2.clear()
                well_number2 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number3 == int(c):
                self.graphicsView3.clear()
                well_number3 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number4 == int(c):
                self.graphicsView4.clear()
                well_number4 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number5 == int(c):
                self.graphicsView5.clear()
                well_number5 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number6 == int(c):
                self.graphicsView6.clear()
                well_number6 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number7 == int(c):
                self.graphicsView7.clear()
                well_number7 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            elif well_number8 == int(c):
                self.graphicsView8.clear()
                well_number8 = 0
                total_numbers_of_graph = total_numbers_of_graph - 1

            ### replot graph for analog tab

            if a == "Current plot mode: 1 plot":
                self.graphicsView9.clear()
                jj = 0
                for i in (well_number1, well_number2, well_number3, well_number4,
                          well_number5, well_number6, well_number7, well_number8):
                    print(i)
                    jj = jj + 1
                    if i != 0:
                        j = str(jj)
                        index = list(
                            range(self.chunk_size * int(j) - (self.chunk_size - 1), self.chunk_size * int(j) + 1))
                        print(j)

                        code1 = ["int(Dispense_Mapping_well_as_index.loc[well_number", j, " ,'Peak Record Index'])"]
                        join1 = "".join(code1)
                        record_index = eval(join1)
                        print(record_index)

                        record_index_min = (record_index - 1) * self.chunk_size
                        record_index_max = record_index * self.chunk_size
                        Peak_Record_with_index = Peak_Record[
                                                 (record_index_min + 1):(record_index_max + 1)].reset_index()

                        channel_1 = Peak_Record_with_index[0:self.chunk_size]['Channel 1'].values.tolist()
                        channel_2 = Peak_Record_with_index[0:self.chunk_size]['Channel 2'].values.tolist()
                        channel_3 = Peak_Record_with_index[0:self.chunk_size]['Channel 3'].values.tolist()
                        channel_4 = Peak_Record_with_index[0:self.chunk_size]['Channel 4'].values.tolist()

                        self.graphicsView9.plot(index, channel_1, name='Channel_1', pen='k', symbol='o', symbolSize=3,
                                                symbolBrush=('k'))
                        self.graphicsView9.plot(index, channel_2, name='Channel_2', pen='r', symbol='o', symbolSize=3,
                                                symbolBrush=('r'))
                        self.graphicsView9.plot(index, channel_3, name='Channel_3', pen='b', symbol='o', symbolSize=3,
                                                symbolBrush=('b'))
                        self.graphicsView9.plot(index, channel_4, name='Channel_4', pen='m', symbol='o', symbolSize=3,
                                                symbolBrush=('m'))

            """if a == "Current plot mode: 9 plots":

                if total_numbers_of_graph == 1:
                    self.graphicsView2.setGeometry(QtCore.QRect(450, 0, 450, 300))
                    self.graphicsView3.setGeometry(QtCore.QRect(900, 0, 450, 300))
                    self.graphicsView4.setGeometry(QtCore.QRect(0, 300, 450, 300))
                    self.graphicsView5.setGeometry(QtCore.QRect(450, 300, 450, 300))
                    self.graphicsView6.setGeometry(QtCore.QRect(900, 300, 450, 300))
                    self.graphicsView7.setGeometry(QtCore.QRect(0, 600, 450, 300))
                    self.graphicsView8.setGeometry(QtCore.QRect(450, 600, 450, 300))
                    self.graphicsView1.setGeometry(QtCore.QRect(0, 0, 450, 300))


                    if well_number8 != 0 :
                        graph_number = "8"
                    elif well_number7 != 0:
                        graph_number = "7"
                    elif well_number6 != 0:
                        graph_number = "6"
                    elif well_number5 != 0:
                        graph_number = "5"
                    elif well_number4 != 0:
                        graph_number = "4"
                    elif well_number3 != 0:
                        graph_number = "3"
                    elif well_number2 != 0:
                        graph_number = "2"
                    elif well_number1 != 0:
                        graph_number = "1"

                    code1 = ["self.graphicsView", graph_number,".setGeometry(QtCore.QRect(0, 0, 1000,800))"]
                    code2 = ["self.graphicsView", graph_number,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    exec(join2)


                elif total_numbers_of_graph == 2:


                    if well_number1 != 0 :
                        graph_number_1st_picture = "1"
                    elif well_number2 != 0:
                        graph_number_1st_picture = "2"
                    elif well_number3 != 0:
                        graph_number_1st_picture = "3"
                    elif well_number4 != 0:
                        graph_number_1st_picture = "4"
                    elif well_number5 != 0:
                        graph_number_1st_picture = "5"
                    elif well_number6 != 0:
                        graph_number_1st_picture = "6"
                    elif well_number7 != 0:
                        graph_number_1st_picture = "7"
                    elif well_number8 != 0:
                        graph_number_1st_picture = "8"

                    code1 = ["self.graphicsView", graph_number_1st_picture,".setGeometry(QtCore.QRect(0, 0, 700,800))"]
                    code2 = ["self.graphicsView", graph_number_1st_picture,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    exec(join2)

                    if well_number8 != 0 :
                        graph_number = "8"
                    elif well_number7 != 0:
                        graph_number = "7"
                    elif well_number6 != 0:
                        graph_number = "6"
                    elif well_number5 != 0:
                        graph_number = "5"
                    elif well_number4 != 0:
                        graph_number = "4"
                    elif well_number3 != 0:
                        graph_number = "3"
                    elif well_number2 != 0:
                        graph_number = "2"
                    elif well_number1 != 0:
                        graph_number = "1"


                    code1 = ["self.graphicsView", graph_number,".setGeometry(QtCore.QRect(700, 0, 700,800))"]
                    code2 = ["self.graphicsView", graph_number,".raise_()"]
                    join1 = "".join(code1)
                    join2 = "".join(code2)
                    exec(join1)
                    exec(join2)
                else:
                    self.graphicsView2.setGeometry(QtCore.QRect(450, 0, 450, 300))
                    self.graphicsView3.setGeometry(QtCore.QRect(900, 0, 450, 300))
                    self.graphicsView4.setGeometry(QtCore.QRect(0, 300, 450, 300))
                    self.graphicsView5.setGeometry(QtCore.QRect(450, 300, 450, 300))
                    self.graphicsView6.setGeometry(QtCore.QRect(900, 300, 450, 300))
                    self.graphicsView7.setGeometry(QtCore.QRect(0, 600, 450, 300))
                    self.graphicsView8.setGeometry(QtCore.QRect(450, 600, 450, 300))
                    self.graphicsView1.setGeometry(QtCore.QRect(0, 0, 450, 300))
        """


## read file


## find first/last well number


# find first/last well is in which strip


# set index as well number,and change type, for plot use
well_number1 = 0
well_number2 = 0
well_number3 = 0
well_number4 = 0
well_number5 = 0
well_number6 = 0
well_number7 = 0
well_number8 = 0
total_numbers_of_graph = 0

if __name__ == "__main__":
    import sys

    app = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Mapping_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

