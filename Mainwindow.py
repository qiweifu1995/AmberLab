# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AmberLab_detailed2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit

import pandas as pd
import os
import Helper
import Analysis
import time
from itertools import islice
from pyqtgraph import PlotWidget
import numpy as np
from PyQt5 import QtGui  # Place this at the top of your file.
import pyqtgraph as pg
import statistics


class OtherWindow(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Please select a sampling rate: 250, 500, or 1000")
        self.lineEdit = QLineEdit('100')
        self.pushButton_1 = QPushButton('Ok')
        self.pushButton_2 = QPushButton('Close')      
        
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton_1)
        layout.addWidget(self.pushButton_2)
        
        self.setLayout(layout)
        self.pushButton_1.clicked.connect(self.ok_clicked)
        self.pushButton_2.clicked.connect(self.close_clicked)
    def ok_clicked(self):
        self.hide() 
        Ui_MainWindow.OtherWindow_Button_ok_clicked(Ui_MainWindow,self.lineEdit.text())
    def close_clicked(self):
        self.hide()      
        ###

        

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 749)
        MainWindow.setMinimumSize(QtCore.QSize(150, 150))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.layout_vertical_filecontrol = QtWidgets.QVBoxLayout()
        self.layout_vertical_filecontrol.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout_vertical_filecontrol.setContentsMargins(20, -1, 20, -1)
        self.layout_vertical_filecontrol.setObjectName("layout_vertical_filecontrol")
        self.label_files = QtWidgets.QLabel(self.centralwidget)
        self.label_files.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_files.setAlignment(QtCore.Qt.AlignCenter)
        self.label_files.setObjectName("label_files")
        self.layout_vertical_filecontrol.addWidget(self.label_files)

        self.file_list_view = QtWidgets.QListWidget(self.centralwidget)
        self.file_list_view.setObjectName("file_list_view")
        self.layout_vertical_filecontrol.addWidget(self.file_list_view)

        self.layout_horizontal_renamebutton = QtWidgets.QHBoxLayout()
        self.layout_horizontal_renamebutton.setObjectName("layout_horizontal_renamebutton")
        self.button_rename = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_rename.sizePolicy().hasHeightForWidth())
        self.button_rename.setSizePolicy(sizePolicy)
        self.button_rename.setMinimumSize(QtCore.QSize(50, 0))
        self.button_rename.setMaximumSize(QtCore.QSize(100, 16777215))
        self.button_rename.setObjectName("button_rename")
        self.layout_horizontal_renamebutton.addWidget(self.button_rename)
        self.layout_vertical_filecontrol.addLayout(self.layout_horizontal_renamebutton)
        spacerItem = QtWidgets.QSpacerItem(120, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout_vertical_filecontrol.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.layout_vertical_filecontrol.addWidget(self.line_2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layout_vertical_filecontrol.addWidget(self.label)
        self.layout_horizontal_checkbox = QtWidgets.QHBoxLayout()
        self.layout_horizontal_checkbox.setObjectName("layout_horizontal_checkbox")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.layout_horizontal_checkbox.addItem(spacerItem1)
        self.layout_vertical_checkbox = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox.setObjectName("layout_vertical_checkbox")
        self.checkbox_ch1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch1.setObjectName("checkbox_ch1")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch1)
        self.checkbox_ch2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch2.setObjectName("checkbox_ch2")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch2)
        self.checkbox_ch3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch3.setObjectName("checkbox_ch3")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch3)
        self.checkbox_ch12 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch12.setObjectName("checkbox_ch12")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch12)
        self.checkbox_ch13 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch13.setObjectName("checkbox_ch13")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch13)
        self.checkbox_ch23 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_ch23.setObjectName("checkbox_ch23")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch23)
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.layout_vertical_checkbox.addWidget(self.checkBox_7)
        self.layout_horizontal_checkbox.addLayout(self.layout_vertical_checkbox)
        self.layout_vertical_filecontrol.addLayout(self.layout_horizontal_checkbox)
        self.layout_horizontal_update = QtWidgets.QHBoxLayout()
        self.layout_horizontal_update.setObjectName("layout_horizontal_update")
        self.button_update = QtWidgets.QPushButton(self.centralwidget)
        self.button_update.setMinimumSize(QtCore.QSize(50, 0))
        self.button_update.setMaximumSize(QtCore.QSize(100, 16777215))
        self.button_update.setObjectName("button_update")
        self.layout_horizontal_update.addWidget(self.button_update)
        self.layout_vertical_filecontrol.addLayout(self.layout_horizontal_update)
        spacerItem2 = QtWidgets.QSpacerItem(120, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout_vertical_filecontrol.addItem(spacerItem2)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.layout_vertical_filecontrol.addWidget(self.line_3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.layout_vertical_filecontrol.addWidget(self.label_2)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setObjectName("listView")
        self.layout_vertical_filecontrol.addWidget(self.listView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_copy = QtWidgets.QPushButton(self.centralwidget)
        self.button_copy.setMinimumSize(QtCore.QSize(50, 0))
        self.button_copy.setMaximumSize(QtCore.QSize(80, 16777215))
        self.button_copy.setObjectName("button_copy")
        self.horizontalLayout.addWidget(self.button_copy)
        self.button_paste = QtWidgets.QPushButton(self.centralwidget)
        self.button_paste.setMinimumSize(QtCore.QSize(50, 0))
        self.button_paste.setMaximumSize(QtCore.QSize(80, 16777215))
        self.button_paste.setObjectName("button_paste")
        self.horizontalLayout.addWidget(self.button_paste)
        self.layout_vertical_filecontrol.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_screenshot = QtWidgets.QPushButton(self.centralwidget)
        self.button_screenshot.setMaximumSize(QtCore.QSize(100, 16777215))
        self.button_screenshot.setObjectName("button_screenshot")
        self.horizontalLayout_2.addWidget(self.button_screenshot)
        self.layout_vertical_filecontrol.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.layout_vertical_filecontrol.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.layout_vertical_filecontrol)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.tab_widgets_main = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_widgets_main.sizePolicy().hasHeightForWidth())
        self.tab_widgets_main.setSizePolicy(sizePolicy)
        self.tab_widgets_main.setMinimumSize(QtCore.QSize(700, 0))
        self.tab_widgets_main.setAutoFillBackground(False)
        self.tab_widgets_main.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tab_widgets_main.setObjectName("tab_widgets_main")
        self.tab_statistic = QtWidgets.QWidget()
        self.tab_statistic.setObjectName("tab_statistic")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_statistic)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(80, 0))
        self.label_8.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.lineEdit_runtime = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_runtime.sizePolicy().hasHeightForWidth())
        self.lineEdit_runtime.setSizePolicy(sizePolicy)
        self.lineEdit_runtime.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_runtime.setObjectName("lineEdit_runtime")
        self.horizontalLayout_8.addWidget(self.lineEdit_runtime)
        self.gridLayout_2.addLayout(self.horizontalLayout_8, 5, 0, 1, 1)
        self.gridlayout_statistic = QtWidgets.QGridLayout()
        self.gridlayout_statistic.setObjectName("gridlayout_statistic")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listWidget_sampingrate = QtWidgets.QListWidget(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_sampingrate.sizePolicy().hasHeightForWidth())
        self.listWidget_sampingrate.setSizePolicy(sizePolicy)
        self.listWidget_sampingrate.setMinimumSize(QtCore.QSize(150, 150))
        self.listWidget_sampingrate.setMaximumSize(QtCore.QSize(16777215, 200))
        self.listWidget_sampingrate.setObjectName("listWidget_sampingrate")
        self.verticalLayout_2.addWidget(self.listWidget_sampingrate)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.pushButton_resample = QtWidgets.QPushButton(self.tab_statistic)
        self.pushButton_resample.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_resample.setObjectName("pushButton_resample")
        self.horizontalLayout_28.addWidget(self.pushButton_resample)
        self.verticalLayout_2.addLayout(self.horizontalLayout_28)
        self.gridlayout_statistic.addLayout(self.verticalLayout_2, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridlayout_statistic, 0, 0, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(60, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.lineEdit_count = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_count.sizePolicy().hasHeightForWidth())
        self.lineEdit_count.setSizePolicy(sizePolicy)
        self.lineEdit_count.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_count.setObjectName("lineEdit_count")
        self.horizontalLayout_5.addWidget(self.lineEdit_count)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.tableView_statistic = QtWidgets.QTableWidget(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_statistic.sizePolicy().hasHeightForWidth())
        self.tableView_statistic.setSizePolicy(sizePolicy)
        self.tableView_statistic.setMinimumSize(QtCore.QSize(150, 150))
        self.tableView_statistic.setMaximumSize(QtCore.QSize(16777215, 200))
        self.tableView_statistic.setObjectName("tableView_statistic")
        self.tableView_statistic.setColumnCount(5)
        self.tableView_statistic.setRowCount(4)
        self.tableView_statistic.setHorizontalHeaderLabels(['Mean', 'Median', 'Standard Deviation', 'Min', 'Max'])
        self.tableView_statistic.setVerticalHeaderLabels(['Green', 'Red', 'Blue', 'Orange'])
        self.verticalLayout_5.addWidget(self.tableView_statistic)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 4, 1, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(80, 0))
        self.label_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_6.addWidget(self.label_6)
        self.lineEdit_startingtime = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_startingtime.sizePolicy().hasHeightForWidth())
        self.lineEdit_startingtime.setSizePolicy(sizePolicy)
        self.lineEdit_startingtime.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_startingtime.setObjectName("lineEdit_startingtime")
        self.horizontalLayout_6.addWidget(self.lineEdit_startingtime)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_12 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(80, 0))
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_12.addWidget(self.label_12)
        self.lineEdit_ch1hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch1hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch1hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch1hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch1hit.setObjectName("lineEdit_ch1hit")
        self.horizontalLayout_12.addWidget(self.lineEdit_ch1hit)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem5)
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setMinimumSize(QtCore.QSize(80, 0))
        self.label_14.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_14.addWidget(self.label_14)
        self.lineEdit_ch3hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch3hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch3hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch3hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch3hit.setObjectName("lineEdit_ch3hit")
        self.horizontalLayout_14.addWidget(self.lineEdit_ch3hit)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem6)
        self.gridLayout_3.addLayout(self.horizontalLayout_14, 0, 2, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(80, 0))
        self.label_13.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_13.addWidget(self.label_13)
        self.lineEdit_ch2hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch2hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch2hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch2hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch2hit.setObjectName("lineEdit_ch2hit")
        self.horizontalLayout_13.addWidget(self.lineEdit_ch2hit)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem7)
        self.gridLayout_3.addLayout(self.horizontalLayout_13, 0, 1, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(80, 0))
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.lineEdit_ch12hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch12hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch12hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch12hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch12hit.setObjectName("lineEdit_ch12hit")
        self.horizontalLayout_16.addWidget(self.lineEdit_ch12hit)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem8)
        self.gridLayout_3.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_16 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QtCore.QSize(80, 0))
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_17.addWidget(self.label_16)
        self.lineEdit_ch13hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch13hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch13hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch13hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch13hit.setObjectName("lineEdit_ch13hit")
        self.horizontalLayout_17.addWidget(self.lineEdit_ch13hit)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem9)
        self.gridLayout_3.addLayout(self.horizontalLayout_17, 1, 1, 1, 1)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_17 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QtCore.QSize(80, 0))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_18.addWidget(self.label_17)
        self.lineEdit_ch23hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch23hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch23hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch23hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch23hit.setObjectName("lineEdit_ch23hit")
        self.horizontalLayout_18.addWidget(self.lineEdit_ch23hit)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem10)
        self.gridLayout_3.addLayout(self.horizontalLayout_18, 1, 2, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout_3)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 6, 2, 1, 1)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_19 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QtCore.QSize(80, 0))
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_19.addWidget(self.label_19)
        self.lineEdit_totaldispensed = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_totaldispensed.sizePolicy().hasHeightForWidth())
        self.lineEdit_totaldispensed.setSizePolicy(sizePolicy)
        self.lineEdit_totaldispensed.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_totaldispensed.setObjectName("lineEdit_totaldispensed")
        self.horizontalLayout_19.addWidget(self.lineEdit_totaldispensed)
        self.gridLayout_2.addLayout(self.horizontalLayout_19, 9, 0, 1, 1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(80, 0))
        self.label_11.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_11.addWidget(self.label_11)
        self.lineEdit_totallost = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_totallost.sizePolicy().hasHeightForWidth())
        self.lineEdit_totallost.setSizePolicy(sizePolicy)
        self.lineEdit_totallost.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_totallost.setObjectName("lineEdit_totallost")
        self.horizontalLayout_11.addWidget(self.lineEdit_totallost)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem11)
        self.gridLayout_2.addLayout(self.horizontalLayout_11, 5, 2, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_2.addLayout(self.verticalLayout_6, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_statistic)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem12, 2, 2, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem13, 11, 0, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(80, 0))
        self.label_10.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.lineEdit_totalsorted = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_totalsorted.sizePolicy().hasHeightForWidth())
        self.lineEdit_totalsorted.setSizePolicy(sizePolicy)
        self.lineEdit_totalsorted.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_totalsorted.setObjectName("lineEdit_totalsorted")
        self.horizontalLayout_10.addWidget(self.lineEdit_totalsorted)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem14)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 4, 2, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(80, 0))
        self.label_9.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.lineEdit_totaldroplets = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_totaldroplets.sizePolicy().hasHeightForWidth())
        self.lineEdit_totaldroplets.setSizePolicy(sizePolicy)
        self.lineEdit_totaldroplets.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_totaldroplets.setObjectName("lineEdit_totaldroplets")
        self.horizontalLayout_9.addWidget(self.lineEdit_totaldroplets)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem15)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 3, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.tab_statistic)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 8, 0, 1, 1)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_20 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QtCore.QSize(80, 0))
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_20.addWidget(self.label_20)
        self.lineEdit_dispensemissed = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_dispensemissed.sizePolicy().hasHeightForWidth())
        self.lineEdit_dispensemissed.setSizePolicy(sizePolicy)
        self.lineEdit_dispensemissed.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_dispensemissed.setObjectName("lineEdit_dispensemissed")
        self.horizontalLayout_20.addWidget(self.lineEdit_dispensemissed)
        self.gridLayout_2.addLayout(self.horizontalLayout_20, 10, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(80, 0))
        self.label_7.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lineEdit_endingtime = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_endingtime.sizePolicy().hasHeightForWidth())
        self.lineEdit_endingtime.setSizePolicy(sizePolicy)
        self.lineEdit_endingtime.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_endingtime.setObjectName("lineEdit_endingtime")
        self.horizontalLayout_7.addWidget(self.lineEdit_endingtime)
        self.gridLayout_2.addLayout(self.horizontalLayout_7, 4, 0, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.tab_statistic)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout_2.addWidget(self.line_9, 1, 0, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.tab_statistic)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout_2.addWidget(self.line_10, 1, 2, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.tab_statistic)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout_2.addWidget(self.line_8, 0, 1, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.tab_statistic)
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout_2.addWidget(self.line_11, 7, 0, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.tab_statistic)
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.gridLayout_2.addWidget(self.line_12, 7, 2, 1, 1)
        self.tab_widgets_main.addTab(self.tab_statistic, "")
        
        
### Peak Width

        self.tab_peakwidth = QtWidgets.QWidget()
        self.tab_peakwidth.setObjectName("tab_peakwidth")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_peakwidth)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.tab_widget_peak_width = QtWidgets.QTabWidget(self.tab_peakwidth)
        self.tab_widget_peak_width.setObjectName("tab_widget_peak_width")
        self.sub_tab_width_scatter = QtWidgets.QWidget()
        self.sub_tab_width_scatter.setObjectName("sub_tab_width_scatter")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.sub_tab_width_scatter)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setContentsMargins(10, 10, -1, 10)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_87 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_87.setFont(font)
        self.label_87.setObjectName("label_87")
        self.gridLayout_13.addWidget(self.label_87, 0, 1, 1, 1)
        self.horizontalLayout_42 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_42.setObjectName("horizontalLayout_42")
        self.label_88 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_88.setObjectName("label_88")
        self.horizontalLayout_42.addWidget(self.label_88)
        self.comboBox_5 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_5.sizePolicy().hasHeightForWidth())
        self.comboBox_5.setSizePolicy(sizePolicy)
        self.comboBox_5.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.horizontalLayout_42.addWidget(self.comboBox_5)
        self.gridLayout_13.addLayout(self.horizontalLayout_42, 1, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_13.addWidget(self.lineEdit_5, 1, 1, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_13.addWidget(self.lineEdit_6, 2, 1, 1, 1)
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.label_89 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_89.setObjectName("label_89")
        self.horizontalLayout_46.addWidget(self.label_89)
        self.comboBox_6 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_6.sizePolicy().hasHeightForWidth())
        self.comboBox_6.setSizePolicy(sizePolicy)
        self.comboBox_6.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.horizontalLayout_46.addWidget(self.comboBox_6)
        self.gridLayout_13.addLayout(self.horizontalLayout_46, 2, 0, 1, 1)
        self.label_90 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_90.setFont(font)
        self.label_90.setObjectName("label_90")
        self.gridLayout_13.addWidget(self.label_90, 0, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_7.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_13.addWidget(self.lineEdit_7, 1, 2, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_8.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_13.addWidget(self.lineEdit_8, 2, 2, 1, 1)
        self.lineEdit_5.setText("-1")
        self.lineEdit_6.setText("-1")
        self.lineEdit_7.setText("100")
        self.lineEdit_8.setText("100")
        self.label_91 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_91.setFont(font)
        self.label_91.setObjectName("label_91")
        self.gridLayout_13.addWidget(self.label_91, 0, 2, 1, 1)        
        self.verticalLayout_16.addLayout(self.gridLayout_13)
        self.line_36 = QtWidgets.QFrame(self.sub_tab_width_scatter)
        self.line_36.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.verticalLayout_16.addWidget(self.line_36)
        self.label_95 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_95.setFont(font)
        self.label_95.setObjectName("label_95")
        self.verticalLayout_16.addWidget(self.label_95)
                
        
      
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout_16.addWidget(self.lineEdit_9, 1, 0, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_12.sizePolicy().hasHeightForWidth())
        self.lineEdit_12.setSizePolicy(sizePolicy)
        self.lineEdit_12.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout_16.addWidget(self.lineEdit_12, 1, 3, 1, 1)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_10.sizePolicy().hasHeightForWidth())
        self.lineEdit_10.setSizePolicy(sizePolicy)
        self.lineEdit_10.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_10.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout_16.addWidget(self.lineEdit_10, 1, 1, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_11.sizePolicy().hasHeightForWidth())
        self.lineEdit_11.setSizePolicy(sizePolicy)
        self.lineEdit_11.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout_16.addWidget(self.lineEdit_11, 1, 2, 1, 1)
        self.label_92 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_92.setFont(font)
        self.label_92.setObjectName("label_92")
        self.gridLayout_16.addWidget(self.label_92, 0, 0, 1, 1)
        self.label_96 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_96.setFont(font)
        self.label_96.setObjectName("label_96")
        self.gridLayout_16.addWidget(self.label_96, 0, 1, 1, 1)
        self.label_97 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_97.setFont(font)
        self.label_97.setObjectName("label_97")
        self.gridLayout_16.addWidget(self.label_97, 0, 2, 1, 1)
        self.label_98 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_98.setFont(font)
        self.label_98.setObjectName("label_98")
        self.gridLayout_16.addWidget(self.label_98, 0, 3, 1, 1)
        self.verticalLayout_16.addLayout(self.gridLayout_16)
        self.label_93 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_93.setFont(font)
        self.label_93.setObjectName("label_93")
        self.verticalLayout_16.addWidget(self.label_93)

        
        self.lineEdit_9.setText("default")
        self.lineEdit_10.setText("default")
        self.lineEdit_11.setText("default")
        self.lineEdit_12.setText("default")
        

        self.horizontalLayout_49 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_49.setObjectName("horizontalLayout_41")
        self.label_84 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_84.sizePolicy().hasHeightForWidth())
        self.label_84.setSizePolicy(sizePolicy)
        self.label_84.setMinimumSize(QtCore.QSize(80, 0))
        self.label_84.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_84.setObjectName("label_84")
        self.horizontalLayout_49.addWidget(self.label_84)
        self.lineEdit_gatevoltage_5 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_gatevoltage_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_gatevoltage_5.setSizePolicy(sizePolicy)
        self.lineEdit_gatevoltage_5.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_gatevoltage_5.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_gatevoltage_5.setObjectName("lineEdit_gatevoltage_5")
        self.horizontalLayout_49.addWidget(self.lineEdit_gatevoltage_5)
        self.label_85 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_85.setObjectName("label_85")
        self.horizontalLayout_49.addWidget(self.label_85)

        self.lineEdit_gatevoltage_6 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_gatevoltage_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_gatevoltage_6.setSizePolicy(sizePolicy)
        self.lineEdit_gatevoltage_6.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_gatevoltage_6.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_gatevoltage_6.setObjectName("lineEdit_gatevoltage_6")
        self.horizontalLayout_49.addWidget(self.lineEdit_gatevoltage_6)
        
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_49.addItem(spacerItem21)
        self.verticalLayout_16.addLayout(self.horizontalLayout_49)
        
        self.layout_horizontal_update_2 = QtWidgets.QHBoxLayout()
        self.layout_horizontal_update_2.setObjectName("layout_horizontal_update_2")
        self.button_update_2 = QtWidgets.QPushButton(self.sub_tab_width_scatter)
        self.button_update_2.setMinimumSize(QtCore.QSize(50, 0))
        self.button_update_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.button_update_2.setObjectName("button_update_2")
        self.layout_horizontal_update_2.addWidget(self.button_update_2)
        self.verticalLayout_16.addLayout(self.layout_horizontal_update_2)
        
### tableview_7 
#         self.tableView_7 = QtWidgets.QTableWidget(self.sub_tab_width_scatter)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.tableView_statistic.sizePolicy().hasHeightForWidth())
#         self.tableView_7.setSizePolicy(sizePolicy)
#         self.tableView_7.setMinimumSize(QtCore.QSize(150, 150))
#         self.tableView_7.setMaximumSize(QtCore.QSize(600, 400))

#         self.tableView_7.setObjectName("tableView_7")
#         self.verticalLayout_16.addWidget(self.tableView_7)
# #         self.tableView_7.setColumnCount(1)
#         self.tableView_7.setRowCount(1)
# #         self.tableView_7.setHorizontalHeaderLabels(['Left', 'Medium', 'Right','Total'])
#         self.tableView_7.setVerticalHeaderLabels(['Medium', ])  

        spacerItem22 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_16.addItem(spacerItem22)
        
        self.gridLayout_15.addLayout(self.verticalLayout_16, 0, 0, 1, 1)
        self.line_38 = QtWidgets.QFrame(self.sub_tab_width_scatter)
        self.line_38.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_38.setObjectName("line_38")
        self.gridLayout_15.addWidget(self.line_38, 0, 1, 1, 1)
        
        
#         self.widget_9 = QtWidgets.QWidget(self.sub_tab_width_scatter)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
#         self.widget_9.setSizePolicy(sizePolicy)
#         self.widget_9.setMinimumSize(QtCore.QSize(500, 500))
#         self.widget_9.setObjectName("widget_9")
#         self.gridLayout_15.addWidget(self.widget_9, 0, 2, 1, 1)

        self.graphWidget_width_scatter = PlotWidget(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget_width_scatter.sizePolicy().hasHeightForWidth())
        self.graphWidget_width_scatter.setSizePolicy(sizePolicy)
        self.graphWidget_width_scatter.setMinimumSize(QtCore.QSize(500, 500))
        self.graphWidget_width_scatter.setObjectName("graphWidget_width_scatter")
        self.gridLayout_15.addWidget(self.graphWidget_width_scatter, 0, 2, 1, 1)
        
        self.graphWidget_width_scatter.setTitle("test scatter plot", color="w", size="30pt")
        styles = {"color": "r", "font-size": "20px"}
        self.graphWidget_width_scatter.setBackground('w')

        self.graphWidget_width_scatter.setLabel('left', 'Green', **styles)
        self.graphWidget_width_scatter.setLabel('bottom', 'Far Red', **styles)
        
        
        self.lr_x_axis = pg.LinearRegionItem([1,1])
        self.lr_y_axis = pg.LinearRegionItem([1,1], orientation = 'horizontal')
        self.graphWidget_width_scatter.addItem(self.lr_x_axis)
        self.graphWidget_width_scatter.addItem(self.lr_y_axis)  
        
        
        self.tab_widget_peak_width.addTab(self.sub_tab_width_scatter, "")

    
    
        
        self.sub_tab_width_histogram = QtWidgets.QWidget()
        self.sub_tab_width_histogram.setObjectName("sub_tab_width_histogram")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.sub_tab_width_histogram)
        self.gridLayout_11.setObjectName("gridLayout_11")
        
        
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_54 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_54.sizePolicy().hasHeightForWidth())
        self.label_54.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_54.setFont(font)
        self.label_54.setObjectName("label_54")
        self.verticalLayout_8.addWidget(self.label_54)
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.listView_channels_3 = QtWidgets.QListWidget(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_channels_3.sizePolicy().hasHeightForWidth())
        self.listView_channels_3.setSizePolicy(sizePolicy)
        self.listView_channels_3.setMinimumSize(QtCore.QSize(150, 150))
        self.listView_channels_3.setMaximumSize(QtCore.QSize(200, 200))
        self.listView_channels_3.setObjectName("listView_channels_3")
        self.listView_channels_3.addItem("Green")
        self.listView_channels_3.addItem("Red")
        self.listView_channels_3.addItem("Blue")
        self.listView_channels_3.addItem("Orange")
        self.listView_channels_3.setCurrentRow(0)        

        
        self.horizontalLayout_34.addWidget(self.listView_channels_3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_34)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.pushButton_saveplot_2 = QtWidgets.QPushButton(self.sub_tab_width_histogram)
        self.pushButton_saveplot_2.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_saveplot_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_saveplot_2.setObjectName("pushButton_saveplot_2")
        self.horizontalLayout_35.addWidget(self.pushButton_saveplot_2)
        self.verticalLayout_8.addLayout(self.horizontalLayout_35)
        self.line_32 = QtWidgets.QFrame(self.sub_tab_width_histogram)
        self.line_32.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.verticalLayout_8.addWidget(self.line_32)
        
        
        self.label_59 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_59.sizePolicy().hasHeightForWidth())
        self.label_59.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_59.setFont(font)
        self.label_59.setObjectName("label_59")
        self.verticalLayout_8.addWidget(self.label_59)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.label_60 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_60.sizePolicy().hasHeightForWidth())
        self.label_60.setSizePolicy(sizePolicy)
        self.label_60.setMinimumSize(QtCore.QSize(80, 0))
        self.label_60.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_60.setObjectName("label_60")
        self.horizontalLayout_37.addWidget(self.label_60)
        self.lineEdit_gatevoltage_2 = QtWidgets.QLineEdit(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_gatevoltage_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_gatevoltage_2.setSizePolicy(sizePolicy)
        self.lineEdit_gatevoltage_2.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_gatevoltage_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_gatevoltage_2.setObjectName("lineEdit_gatevoltage_2")
        self.horizontalLayout_37.addWidget(self.lineEdit_gatevoltage_2)
        self.label_76 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        self.label_76.setObjectName("label_76")
        self.horizontalLayout_37.addWidget(self.label_76)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_37.addItem(spacerItem22)
        self.verticalLayout_8.addLayout(self.horizontalLayout_37)
        
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_41.setObjectName("horizontalLayout_41")
        self.label_82 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_82.sizePolicy().hasHeightForWidth())
        self.label_82.setSizePolicy(sizePolicy)
        self.label_82.setMinimumSize(QtCore.QSize(80, 0))
        self.label_82.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_82.setObjectName("label_82")
        self.horizontalLayout_41.addWidget(self.label_82)
        self.lineEdit_gatevoltage_4 = QtWidgets.QLineEdit(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_gatevoltage_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_gatevoltage_4.setSizePolicy(sizePolicy)
        self.lineEdit_gatevoltage_4.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_gatevoltage_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_gatevoltage_4.setObjectName("lineEdit_gatevoltage_4")
        self.horizontalLayout_41.addWidget(self.lineEdit_gatevoltage_4)
#         self.label_76 = QtWidgets.QLabel(self.sub_tab_width_histogram)
#         self.label_76.setObjectName("label_76")
#         self.horizontalLayout_37.addWidget(self.label_76)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_41.addItem(spacerItem21)
        self.verticalLayout_8.addLayout(self.horizontalLayout_41)
        
        
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.label_77 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_77.sizePolicy().hasHeightForWidth())
        self.label_77.setSizePolicy(sizePolicy)
        self.label_77.setMinimumSize(QtCore.QSize(80, 0))
        self.label_77.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_77.setObjectName("label_77")
        self.horizontalLayout_38.addWidget(self.label_77)
        self.lineEdit_percentage_2 = QtWidgets.QLineEdit(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentage_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentage_2.setSizePolicy(sizePolicy)
        self.lineEdit_percentage_2.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_percentage_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_percentage_2.setObjectName("lineEdit_percentage_2")
        self.horizontalLayout_38.addWidget(self.lineEdit_percentage_2)
        self.label_78 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        self.label_78.setObjectName("label_78")
        self.horizontalLayout_38.addWidget(self.label_78)
        spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_38.addItem(spacerItem23)
        self.verticalLayout_8.addLayout(self.horizontalLayout_38)
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.label_79 = QtWidgets.QLabel(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_79.sizePolicy().hasHeightForWidth())
        self.label_79.setSizePolicy(sizePolicy)
        self.label_79.setMinimumSize(QtCore.QSize(80, 0))
        self.label_79.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_79.setObjectName("label_79")
        self.horizontalLayout_39.addWidget(self.label_79)
        self.lineEdit_binwidth_3 = QtWidgets.QLineEdit(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_binwidth_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_binwidth_3.setSizePolicy(sizePolicy)
        self.lineEdit_binwidth_3.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_binwidth_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_binwidth_3.setObjectName("lineEdit_binwidth_3")
        
        self.lineEdit_binwidth_3.setText("1")
        
        
        self.horizontalLayout_39.addWidget(self.lineEdit_binwidth_3)
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_39.addItem(spacerItem24)
        self.verticalLayout_8.addLayout(self.horizontalLayout_39)
        spacerItem25 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem25)
        
        self.gridLayout_11.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
        
        
        self.line_39 = QtWidgets.QFrame(self.sub_tab_width_histogram)
        self.line_39.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_39.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_39.setObjectName("line_39")
        
        
        self.gridLayout_11.addWidget(self.line_39, 0, 1, 2, 2)


  # sub_tab_width_histogram histogram
        self.histogram_graphWidget_3 = PlotWidget(self.sub_tab_width_histogram)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram_graphWidget_3.sizePolicy().hasHeightForWidth())
        self.histogram_graphWidget_3.setSizePolicy(sizePolicy)
        self.histogram_graphWidget_3.setMinimumSize(QtCore.QSize(700, 499))
        self.histogram_graphWidget_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.histogram_graphWidget_3.setObjectName("histogram_graphWidget_3")
        
        self.gridLayout_11.addWidget(self.histogram_graphWidget_3, 0, 2, 1, 1)
        
        styles = {"color": "r", "font-size": "20px"}
        self.histogram_graphWidget_3.setLabel('left', 'Frequency', **styles)
        self.histogram_graphWidget_3.setBackground('w')
        self.histogram_graphWidget_3.setXRange(1, 10.5, padding=0)
        self.histogram_graphWidget_3.setYRange(1, 10.5, padding=0)




        self.lineEdit_gatevoltage_2.setText("-1")
        self.lineEdit_gatevoltage_4.setText("100")

        #         # threshold end


        self.tab_widget_peak_width.addTab(self.sub_tab_width_histogram, "")
        self.gridLayout_10.addWidget(self.tab_widget_peak_width, 0, 0, 1, 1)
        self.tab_widgets_main.addTab(self.tab_peakwidth, "")
        
### Peak width end


        
        self.tab_scatter = QtWidgets.QWidget()
        self.tab_scatter.setObjectName("tab_scatter")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_scatter)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tab_widgets_scatter = QtWidgets.QTabWidget(self.tab_scatter)
        self.tab_widgets_scatter.setObjectName("tab_widgets_scatter")
        
        self.subtab_scatter = QtWidgets.QWidget()
        self.subtab_scatter.setObjectName("subtab_scatter")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.subtab_scatter)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setContentsMargins(10, 10, -1, 10)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_30 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.gridLayout_6.addWidget(self.label_30, 0, 1, 1, 1)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_31 = QtWidgets.QLabel(self.subtab_scatter)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_30.addWidget(self.label_31)
        self.comboBox = QtWidgets.QComboBox(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_30.addWidget(self.comboBox)
        self.gridLayout_6.addLayout(self.horizontalLayout_30, 1, 0, 1, 1)
        self.lineEdit_scatterxvoltage = QtWidgets.QLineEdit(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_scatterxvoltage.sizePolicy().hasHeightForWidth())
        self.lineEdit_scatterxvoltage.setSizePolicy(sizePolicy)
        self.lineEdit_scatterxvoltage.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_scatterxvoltage.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_scatterxvoltage.setObjectName("lineEdit_scatterxvoltage")
        self.gridLayout_6.addWidget(self.lineEdit_scatterxvoltage, 1, 1, 1, 1)
        self.lineEdit_scatteryvoltage = QtWidgets.QLineEdit(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_scatteryvoltage.sizePolicy().hasHeightForWidth())
        self.lineEdit_scatteryvoltage.setSizePolicy(sizePolicy)
        self.lineEdit_scatteryvoltage.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_scatteryvoltage.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_scatteryvoltage.setObjectName("lineEdit_scatteryvoltage")
        self.gridLayout_6.addWidget(self.lineEdit_scatteryvoltage, 2, 1, 1, 1)
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_32 = QtWidgets.QLabel(self.subtab_scatter)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_31.addWidget(self.label_32)
        self.comboBox_2 = QtWidgets.QComboBox(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_31.addWidget(self.comboBox_2)
        self.gridLayout_6.addLayout(self.horizontalLayout_31, 2, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout_6.addWidget(self.label_29, 0, 0, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_6)
        self.line_14 = QtWidgets.QFrame(self.subtab_scatter)
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.verticalLayout_9.addWidget(self.line_14)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem20, 0, 2, 1, 1)
        self.radioButton_scatterlinear = QtWidgets.QRadioButton(self.subtab_scatter)
        self.radioButton_scatterlinear.setChecked(True)
        self.radioButton_scatterlinear.setObjectName("radioButton_scatterlinear")
        self.gridLayout_4.addWidget(self.radioButton_scatterlinear, 1, 0, 1, 1)
        self.radioButton_scatterlog = QtWidgets.QRadioButton(self.subtab_scatter)
        self.radioButton_scatterlog.setObjectName("radioButton_scatterlog")
        self.gridLayout_4.addWidget(self.radioButton_scatterlog, 1, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.gridLayout_4.addWidget(self.label_33, 0, 0, 1, 1)
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_35 = QtWidgets.QLabel(self.subtab_scatter)
        self.label_35.setObjectName("label_35")
        self.horizontalLayout_32.addWidget(self.label_35)
        self.spinBox_scatterscaling = QtWidgets.QSpinBox(self.subtab_scatter)
        self.spinBox_scatterscaling.setMinimum(2)
        self.spinBox_scatterscaling.setMaximum(10)
        self.spinBox_scatterscaling.setObjectName("spinBox_scatterscaling")
        self.horizontalLayout_32.addWidget(self.spinBox_scatterscaling)
        self.gridLayout_4.addLayout(self.horizontalLayout_32, 0, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_4)
        self.line_13 = QtWidgets.QFrame(self.subtab_scatter)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.verticalLayout_9.addWidget(self.line_13)
        self.label_36 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.verticalLayout_9.addWidget(self.label_36)
        self.tableView_scatterquadrants = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatterquadrants.setObjectName("tableView_scatterquadrants")
        self.verticalLayout_9.addWidget(self.tableView_scatterquadrants)
        self.label_37 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_9.addWidget(self.label_37)
        self.tableView_scatterxaxis = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatterxaxis.setObjectName("tableView_scatterxaxis")
        self.verticalLayout_9.addWidget(self.tableView_scatterxaxis)
        self.label_38 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.verticalLayout_9.addWidget(self.label_38)
        self.tableView_scatteryaxis = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatteryaxis.setObjectName("tableView_scatteryaxis")
        self.verticalLayout_9.addWidget(self.tableView_scatteryaxis)

        ### Quadrants table
        # set row count
        self.tableView_scatterquadrants.setRowCount(4)
        # set column count
        self.tableView_scatterquadrants.setColumnCount(3)
        self.tableView_scatterquadrants.setHorizontalHeaderLabels(('Count', '%', '% Total Droplets'))
        self.tableView_scatterquadrants.setVerticalHeaderLabels(
            ('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        ### 2nd table
        # set row count
        self.tableView_scatterxaxis.setRowCount(4)
        # set column count
        self.tableView_scatterxaxis.setColumnCount(3)
        self.tableView_scatterxaxis.setHorizontalHeaderLabels(('Mean', 'St Dev', 'Median'))
        self.tableView_scatterxaxis.setVerticalHeaderLabels(('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        ### 3rd table
        # set row count
        self.tableView_scatteryaxis.setRowCount(4)
        # set column count
        self.tableView_scatteryaxis.setColumnCount(3)
        self.tableView_scatteryaxis.setHorizontalHeaderLabels(('Mean', 'St Dev', 'Median'))
        self.tableView_scatteryaxis.setVerticalHeaderLabels(('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        self.horizontalLayout_29.addLayout(self.verticalLayout_9)
        self.line_7 = QtWidgets.QFrame(self.subtab_scatter)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_29.addWidget(self.line_7)

        #         self.widget_scatter = QtWidgets.QWidget(self.subtab_scatter)
        #         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        #         sizePolicy.setHorizontalStretch(0)
        #         sizePolicy.setVerticalStretch(0)
        #         sizePolicy.setHeightForWidth(self.widget_scatter.sizePolicy().hasHeightForWidth())
        #         self.widget_scatter.setSizePolicy(sizePolicy)
        #         self.widget_scatter.setMinimumSize(QtCore.QSize(500, 500))
        #         self.widget_scatter.setObjectName("widget_scatter")
        #         self.horizontalLayout_29.addWidget(self.widget_scatter)

        self.graphWidget = PlotWidget(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.graphWidget.setObjectName("graphWidget")
        self.horizontalLayout_29.addWidget(self.graphWidget)

        self.graphWidget.setTitle("test scatter plot", color="w", size="30pt")
        styles = {"color": "r", "font-size": "20px"}
        self.graphWidget.setBackground('w')

        self.graphWidget.setLabel('left', 'Green', **styles)
        self.graphWidget.setLabel('bottom', 'Far Red', **styles)

        # threshold

        self.lineEdit_scatterxvoltage.setText("0")
        self.lineEdit_scatteryvoltage.setText("0")

        self.data_line_x = self.graphWidget.plot([0, 1], [1, 1],
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.data_line_y = self.graphWidget.plot([1, 1], [0, 1],
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))

        self.lineEdit_scatterxvoltage.editingFinished.connect(self.thresholdUpdated_2)
        self.lineEdit_scatteryvoltage.editingFinished.connect(self.thresholdUpdated_2)
        # threshold end

        self.tab_widgets_scatter.addTab(self.subtab_scatter, "")
        




###### subtab_peakdisplay change to peak height histogram


        self.tab_gating = QtWidgets.QWidget()
        self.tab_gating.setObjectName("tab_gating")
        
        
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.tab_gating)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_21 = QtWidgets.QLabel(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.listView_channels = QtWidgets.QListWidget(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_channels.sizePolicy().hasHeightForWidth())
        self.listView_channels.setSizePolicy(sizePolicy)
        self.listView_channels.setMinimumSize(QtCore.QSize(150, 150))
        self.listView_channels.setMaximumSize(QtCore.QSize(200, 200))
        self.listView_channels.setObjectName("listView_channels")
        self.listView_channels.addItem("Green")
        self.listView_channels.addItem("Red")
        self.listView_channels.addItem("Blue")
        self.listView_channels.addItem("Orange")
        self.listView_channels.setCurrentRow(0)
        self.horizontalLayout_23.addWidget(self.listView_channels)
        self.verticalLayout.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.pushButton_saveplot = QtWidgets.QPushButton(self.tab_gating)
        self.pushButton_saveplot.setMinimumSize(QtCore.QSize(60, 0))
        self.pushButton_saveplot.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_saveplot.setObjectName("pushButton_saveplot")
        self.horizontalLayout_21.addWidget(self.pushButton_saveplot)
        self.verticalLayout.addLayout(self.horizontalLayout_21)
        self.line_4 = QtWidgets.QFrame(self.tab_gating)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_22 = QtWidgets.QLabel(self.tab_gating)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 0, 0, 1, 1)
        self.radioButton_linear = QtWidgets.QRadioButton(self.tab_gating)
        self.radioButton_linear.setMinimumSize(QtCore.QSize(80, 0))
        self.radioButton_linear.setMaximumSize(QtCore.QSize(80, 16777215))
        self.radioButton_linear.setChecked(True)
        self.radioButton_linear.setObjectName("radioButton_linear")
        self.gridLayout.addWidget(self.radioButton_linear, 1, 0, 1, 1)
        self.radioButton__logarithmic = QtWidgets.QRadioButton(self.tab_gating)
        self.radioButton__logarithmic.setMinimumSize(QtCore.QSize(80, 0))
        self.radioButton__logarithmic.setMaximumSize(QtCore.QSize(80, 16777215))
        self.radioButton__logarithmic.setObjectName("radioButton__logarithmic")
        self.gridLayout.addWidget(self.radioButton__logarithmic, 1, 1, 1, 1)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_34 = QtWidgets.QLabel(self.tab_gating)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_24.addWidget(self.label_34)
        self.spinBox_scaling = QtWidgets.QSpinBox(self.tab_gating)
        self.spinBox_scaling.setMinimumSize(QtCore.QSize(20, 0))
        self.spinBox_scaling.setMaximumSize(QtCore.QSize(40, 16777215))
        self.spinBox_scaling.setMinimum(2)
        self.spinBox_scaling.setMaximum(10)
        self.spinBox_scaling.setObjectName("spinBox_scaling")
        self.horizontalLayout_24.addWidget(self.spinBox_scaling)
        self.gridLayout.addLayout(self.horizontalLayout_24, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_5 = QtWidgets.QFrame(self.tab_gating)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.label_23 = QtWidgets.QLabel(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.verticalLayout.addWidget(self.label_23)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_24 = QtWidgets.QLabel(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setMinimumSize(QtCore.QSize(80, 0))
        self.label_24.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_25.addWidget(self.label_24)
        self.lineEdit_gatevoltage = QtWidgets.QLineEdit(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_gatevoltage.sizePolicy().hasHeightForWidth())
        self.lineEdit_gatevoltage.setSizePolicy(sizePolicy)
        self.lineEdit_gatevoltage.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_gatevoltage.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_gatevoltage.setObjectName("lineEdit_gatevoltage")
        self.horizontalLayout_25.addWidget(self.lineEdit_gatevoltage)
        self.label_25 = QtWidgets.QLabel(self.tab_gating)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_25.addWidget(self.label_25)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem16)
        self.verticalLayout.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_26 = QtWidgets.QLabel(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setMinimumSize(QtCore.QSize(80, 0))
        self.label_26.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_26.addWidget(self.label_26)
        self.lineEdit_percentage = QtWidgets.QLineEdit(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentage.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentage.setSizePolicy(sizePolicy)
        self.lineEdit_percentage.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_percentage.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_percentage.setObjectName("lineEdit_percentage")
        self.horizontalLayout_26.addWidget(self.lineEdit_percentage)
        self.label_27 = QtWidgets.QLabel(self.tab_gating)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_26.addWidget(self.label_27)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_26.addItem(spacerItem17)
        self.verticalLayout.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_28 = QtWidgets.QLabel(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QtCore.QSize(80, 0))
        self.label_28.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_27.addWidget(self.label_28)
        self.lineEdit_binwidth = QtWidgets.QLineEdit(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_binwidth.sizePolicy().hasHeightForWidth())
        self.lineEdit_binwidth.setSizePolicy(sizePolicy)
        self.lineEdit_binwidth.setMinimumSize(QtCore.QSize(80, 0))
        self.lineEdit_binwidth.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_binwidth.setObjectName("lineEdit_binwidth")
        self.lineEdit_binwidth.setText("0.1")
        self.horizontalLayout_27.addWidget(self.lineEdit_binwidth)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_27.addItem(spacerItem18)
        self.verticalLayout.addLayout(self.horizontalLayout_27)
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem19)
        self.horizontalLayout_22.addLayout(self.verticalLayout)
        self.line_6 = QtWidgets.QFrame(self.tab_gating)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_22.addWidget(self.line_6)

        #         self.widget_gating = QtWidgets.QWidget(self.tab_gating)
        #         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        #         sizePolicy.setHorizontalStretch(0)
        #         sizePolicy.setVerticalStretch(0)
        #         sizePolicy.setHeightForWidth(self.widget_gating.sizePolicy().hasHeightForWidth())

        #         self.widget_gating.setSizePolicy(sizePolicy)
        #         self.widget_gating.setMinimumSize(QtCore.QSize(700, 499))
        #         self.widget_gating.setMaximumSize(QtCore.QSize(16777215, 16777215))
        #         self.widget_gating.setObjectName("widget_gating")
        #         self.horizontalLayout_22.addWidget(self.widget_gating)

        # histogram
        self.histogram_graphWidget = PlotWidget(self.tab_gating)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram_graphWidget.sizePolicy().hasHeightForWidth())
        self.histogram_graphWidget.setSizePolicy(sizePolicy)
        self.histogram_graphWidget.setMinimumSize(QtCore.QSize(700, 499))
        self.histogram_graphWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.histogram_graphWidget.setObjectName("histogram_graphWidget")
        self.horizontalLayout_22.addWidget(self.histogram_graphWidget)
        styles = {"color": "r", "font-size": "20px"}
        self.histogram_graphWidget.setLabel('left', 'Frequency', **styles)
        self.histogram_graphWidget.setBackground('w')
        self.histogram_graphWidget.setXRange(1, 10.5, padding=0)
        self.histogram_graphWidget.setYRange(1, 10.5, padding=0)

        #         # threshold

        self.lineEdit_gatevoltage.setText("0")
        self.lineEdit_gatevoltage.editingFinished.connect(self.thresholdUpdated)
        #         # threshold end

        self.tab_widgets_scatter.addTab(self.tab_gating, "")
        
        
        



        
        
      



        self.verticalLayout_4.addWidget(self.tab_widgets_scatter)
        self.tab_widgets_main.addTab(self.tab_scatter, "")
        
###### subtab sweep        
        self.tab_sweep = QtWidgets.QWidget()
        self.tab_sweep.setObjectName("tab_sweep")
#         self.tab_sweep = QtWidgets.QWidget()
#         self.tab_sweep.setObjectName("tab_sweep")

        
        self.tab_widgets_scatter.addTab(self.tab_sweep, "")          
#         self.tab_widgets_main.addTab(self.tab_sweep, "")        

        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_sweep)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.tab_sweep)
        self.tabWidget.setObjectName("tabWidget")
        self.subtab_parameter = QtWidgets.QWidget()
        self.subtab_parameter.setObjectName("subtab_parameter")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.subtab_parameter)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_option1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_option1.setObjectName("horizontalLayout_option1")
        self.comboBox_option1 = QtWidgets.QComboBox(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_option1.sizePolicy().hasHeightForWidth())
        self.comboBox_option1.setSizePolicy(sizePolicy)
        self.comboBox_option1.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_option1.setObjectName("comboBox_option1")
        self.comboBox_option1.addItem("")
        self.horizontalLayout_option1.addWidget(self.comboBox_option1)
        self.verticalLayout_12.addLayout(self.horizontalLayout_option1)
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")

        # Sweep Histogram 1
        self.widget_sweepparam2 = PlotWidget(self.subtab_parameter)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_sweepparam2.sizePolicy().hasHeightForWidth())
        self.widget_sweepparam2.setSizePolicy(sizePolicy)
        self.widget_sweepparam2.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_sweepparam2.setObjectName("widget_sweepparam2")
        styles = {"color": "r", "font-size": "20px"}
        self.widget_sweepparam2.setLabel('left', 'Frequency', **styles)
        self.widget_sweepparam2.setLabel('bottom', 'Green', **styles)
        self.widget_sweepparam2.setBackground('w')
        self.widget_sweepparam2.setXRange(1, 10.5, padding=0)
        self.widget_sweepparam2.setYRange(1, 10.5, padding=0)

        # Sweep Histogram 2
        self.widget_sweepparam1 = PlotWidget(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_sweepparam1.sizePolicy().hasHeightForWidth())
        self.widget_sweepparam1.setSizePolicy(sizePolicy)
        self.widget_sweepparam1.setMinimumSize(QtCore.QSize(200, 200))
        self.widget_sweepparam1.setObjectName("widget_sweepparam1")
        styles = {"color": "r", "font-size": "20px"}
        self.widget_sweepparam1.setLabel('left', 'Frequency', **styles)
        self.widget_sweepparam1.setLabel('bottom', 'Green', **styles)
        self.widget_sweepparam1.setBackground('w')
        self.widget_sweepparam1.setXRange(1, 10.5, padding=0)
        self.widget_sweepparam1.setYRange(1, 10.5, padding=0)

        self.horizontalLayout_44.addWidget(self.widget_sweepparam2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_44)
        self.horizontalLayout_43.addLayout(self.verticalLayout_12)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_option2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_option2.setObjectName("horizontalLayout_option2")
        self.comboBox_option2 = QtWidgets.QComboBox(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_option2.sizePolicy().hasHeightForWidth())
        self.comboBox_option2.setSizePolicy(sizePolicy)
        self.comboBox_option2.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_option2.setObjectName("comboBox_option2")
        self.comboBox_option2.addItem("")
        self.horizontalLayout_option2.addWidget(self.comboBox_option2)
        self.verticalLayout_17.addLayout(self.horizontalLayout_option2)
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")

        self.horizontalLayout_45.addWidget(self.widget_sweepparam1)
        self.verticalLayout_17.addLayout(self.horizontalLayout_45)
        self.horizontalLayout_43.addLayout(self.verticalLayout_17)
        self.verticalLayout_13.addLayout(self.horizontalLayout_43)
        self.line_28 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_28.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.verticalLayout_13.addWidget(self.line_28)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.label_41 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)
        self.label_41.setAlignment(QtCore.Qt.AlignCenter)
        self.label_41.setObjectName("label_41")
        self.horizontalLayout_47.addWidget(self.label_41)
        self.lineEdit_percentagelow1 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentagelow1.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentagelow1.setSizePolicy(sizePolicy)
        self.lineEdit_percentagelow1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_percentagelow1.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit_percentagelow1.setObjectName("lineEdit_percentagelow1")
        self.horizontalLayout_47.addWidget(self.lineEdit_percentagelow1)
        self.label_43 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setAlignment(QtCore.Qt.AlignCenter)
        self.label_43.setObjectName("label_43")
        self.horizontalLayout_47.addWidget(self.label_43)
        self.label_45 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy)
        self.label_45.setAlignment(QtCore.Qt.AlignCenter)
        self.label_45.setObjectName("label_45")
        self.horizontalLayout_47.addWidget(self.label_45)
        self.lineEdit_percentagehigh1 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentagehigh1.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentagehigh1.setSizePolicy(sizePolicy)
        self.lineEdit_percentagehigh1.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit_percentagehigh1.setObjectName("lineEdit_percentagehigh1")
        self.horizontalLayout_47.addWidget(self.lineEdit_percentagehigh1)
        self.label_46 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy)
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName("label_46")
        self.horizontalLayout_47.addWidget(self.label_46)
        self.line_31 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_31.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.horizontalLayout_47.addWidget(self.line_31)
        self.label_44 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName("label_44")
        self.horizontalLayout_47.addWidget(self.label_44)
        self.lineEdit_percentagelow2 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentagelow2.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentagelow2.setSizePolicy(sizePolicy)
        self.lineEdit_percentagelow2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit_percentagelow2.setObjectName("lineEdit_percentagelow2")
        self.horizontalLayout_47.addWidget(self.lineEdit_percentagelow2)
        self.label_47 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy)
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName("label_47")
        self.horizontalLayout_47.addWidget(self.label_47)
        self.label_42 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)
        self.label_42.setAlignment(QtCore.Qt.AlignCenter)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_47.addWidget(self.label_42)
        self.lineEdit_percentagehigh2 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_percentagehigh2.sizePolicy().hasHeightForWidth())
        self.lineEdit_percentagehigh2.setSizePolicy(sizePolicy)
        self.lineEdit_percentagehigh2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit_percentagehigh2.setObjectName("lineEdit_percentagehigh2")
        self.horizontalLayout_47.addWidget(self.lineEdit_percentagehigh2)
        self.label_48 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy)
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_47.addWidget(self.label_48)
        self.verticalLayout_14.addLayout(self.horizontalLayout_47)
        self.line_27 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_27.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.verticalLayout_14.addWidget(self.line_27)
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.verticalLayout_channelsbinwidth = QtWidgets.QVBoxLayout()
        self.verticalLayout_channelsbinwidth.setObjectName("verticalLayout_channelsbinwidth")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.lineEdit_binwidth_2 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_binwidth_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_binwidth_2.setSizePolicy(sizePolicy)
        self.lineEdit_binwidth_2.setObjectName("lineEdit_binwidth_2")
        self.gridLayout_9.addWidget(self.lineEdit_binwidth_2, 1, 1, 1, 1)
        self.label_56 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_56.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_56.setObjectName("label_56")
        self.gridLayout_9.addWidget(self.label_56, 1, 0, 1, 1)
        self.label_55 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_55.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_55.setObjectName("label_55")
        self.gridLayout_9.addWidget(self.label_55, 0, 0, 1, 1)
        self.listView_channels_2 = QtWidgets.QListWidget(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_channels_2.sizePolicy().hasHeightForWidth())
        self.listView_channels_2.setSizePolicy(sizePolicy)
        self.listView_channels_2.setMinimumSize(QtCore.QSize(20, 20))
        self.listView_channels_2.setObjectName("listView_channels_2")
        self.listView_channels_2.addItem("Green")
        self.listView_channels_2.addItem("Red")
        self.listView_channels_2.addItem("Blue")
        self.listView_channels_2.addItem("Orange")
        self.gridLayout_9.addWidget(self.listView_channels_2, 0, 1, 1, 1)
        self.verticalLayout_channelsbinwidth.addLayout(self.gridLayout_9)
        self.horizontalLayout_48.addLayout(self.verticalLayout_channelsbinwidth)
        self.line_29 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_29.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.horizontalLayout_48.addWidget(self.line_29)
        self.verticalLayout_gatingthresholds = QtWidgets.QVBoxLayout()
        self.verticalLayout_gatingthresholds.setObjectName("verticalLayout_gatingthresholds")
        self.label_49 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setMinimumSize(QtCore.QSize(0, 40))
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName("label_49")
        self.verticalLayout_gatingthresholds.addWidget(self.label_49)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setContentsMargins(-1, 10, -1, 10)
        self.gridLayout_7.setHorizontalSpacing(10)
        self.gridLayout_7.setVerticalSpacing(20)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_50 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_50.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_50.setObjectName("label_50")
        self.gridLayout_7.addWidget(self.label_50, 0, 0, 1, 1)
        self.label_61 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_61.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_61.setObjectName("label_61")
        self.gridLayout_7.addWidget(self.label_61, 2, 0, 1, 1)
        self.lineEdit_increments = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_increments.setObjectName("lineEdit_increments")
        self.gridLayout_7.addWidget(self.lineEdit_increments, 2, 1, 1, 1)
        self.lineEdit_gatevoltagemaximum = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_gatevoltagemaximum.setObjectName("lineEdit_gatevoltagemaximum")
        self.gridLayout_7.addWidget(self.lineEdit_gatevoltagemaximum, 1, 1, 1, 1)
        self.lineEdit_gatevoltageminimum = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_gatevoltageminimum.setObjectName("lineEdit_gatevoltageminimum")
        self.gridLayout_7.addWidget(self.lineEdit_gatevoltageminimum, 0, 1, 1, 1)
        self.label_62 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_62.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_62.setObjectName("label_62")
        self.gridLayout_7.addWidget(self.label_62, 1, 0, 1, 1)
        self.label_63 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_63.setObjectName("label_63")
        self.gridLayout_7.addWidget(self.label_63, 0, 2, 1, 1)
        self.label_64 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_64.setObjectName("label_64")
        self.gridLayout_7.addWidget(self.label_64, 1, 2, 1, 1)
        self.label_66 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_66.setObjectName("label_66")
        self.gridLayout_7.addWidget(self.label_66, 2, 2, 1, 1)
        self.verticalLayout_gatingthresholds.addLayout(self.gridLayout_7)
        self.horizontalLayout_48.addLayout(self.verticalLayout_gatingthresholds)
        self.line_30 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.horizontalLayout_48.addWidget(self.line_30)
        self.verticalLayout_axislimits = QtWidgets.QVBoxLayout()
        self.verticalLayout_axislimits.setObjectName("verticalLayout_axislimits")
        self.label_68 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_68.sizePolicy().hasHeightForWidth())
        self.label_68.setSizePolicy(sizePolicy)
        self.label_68.setMinimumSize(QtCore.QSize(0, 40))
        self.label_68.setAlignment(QtCore.Qt.AlignCenter)
        self.label_68.setObjectName("label_68")
        self.verticalLayout_axislimits.addWidget(self.label_68)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, 10, -1, 10)
        self.gridLayout_8.setVerticalSpacing(20)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_sweepxlimits1 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepxlimits1.setObjectName("lineEdit_sweepxlimits1")
        self.gridLayout_8.addWidget(self.lineEdit_sweepxlimits1, 0, 1, 1, 1)
        self.label_71 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_71.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_71.setObjectName("label_71")
        self.gridLayout_8.addWidget(self.label_71, 1, 0, 1, 1)
        self.label_69 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_69.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_69.setObjectName("label_69")
        self.gridLayout_8.addWidget(self.label_69, 0, 0, 1, 1)
        self.label_70 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_70.setObjectName("label_70")
        self.gridLayout_8.addWidget(self.label_70, 0, 2, 1, 1)
        self.pushButton_relimit2 = QtWidgets.QPushButton(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_relimit2.sizePolicy().hasHeightForWidth())
        self.pushButton_relimit2.setSizePolicy(sizePolicy)
        self.pushButton_relimit2.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_relimit2.setObjectName("pushButton_relimit2")
        self.gridLayout_8.addWidget(self.pushButton_relimit2, 2, 3, 1, 1)
        self.lineEdit_sweepylimits1 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepylimits1.setObjectName("lineEdit_sweepylimits1")
        self.gridLayout_8.addWidget(self.lineEdit_sweepylimits1, 1, 1, 1, 1)
        self.lineEdit_sweepylimits2 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepylimits2.setObjectName("lineEdit_sweepylimits2")
        self.gridLayout_8.addWidget(self.lineEdit_sweepylimits2, 1, 3, 1, 1)
        self.pushButton_relimit1 = QtWidgets.QPushButton(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_relimit1.sizePolicy().hasHeightForWidth())
        self.pushButton_relimit1.setSizePolicy(sizePolicy)
        self.pushButton_relimit1.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_relimit1.setObjectName("pushButton_relimit1")
        self.gridLayout_8.addWidget(self.pushButton_relimit1, 2, 1, 1, 1)
        self.label_72 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_72.setObjectName("label_72")
        self.gridLayout_8.addWidget(self.label_72, 1, 2, 1, 1)
        self.lineEdit_sweepxlimits2 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepxlimits2.setObjectName("lineEdit_sweepxlimits2")
        self.gridLayout_8.addWidget(self.lineEdit_sweepxlimits2, 0, 3, 1, 1)
        self.pushButton_auto1 = QtWidgets.QPushButton(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_auto1.sizePolicy().hasHeightForWidth())
        self.pushButton_auto1.setSizePolicy(sizePolicy)
        self.pushButton_auto1.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_auto1.setObjectName("pushButton_auto1")
        self.gridLayout_8.addWidget(self.pushButton_auto1, 3, 1, 1, 1)
        self.pushButton_auto2 = QtWidgets.QPushButton(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_auto2.sizePolicy().hasHeightForWidth())
        self.pushButton_auto2.setSizePolicy(sizePolicy)
        self.pushButton_auto2.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_auto2.setObjectName("pushButton_auto2")
        self.gridLayout_8.addWidget(self.pushButton_auto2, 3, 3, 1, 1)
        self.verticalLayout_axislimits.addLayout(self.gridLayout_8)
        self.horizontalLayout_48.addLayout(self.verticalLayout_axislimits)
        self.verticalLayout_14.addLayout(self.horizontalLayout_48)
        self.verticalLayout_13.addLayout(self.verticalLayout_14)
        self.tabWidget.addTab(self.subtab_parameter, "")
        self.subtab_result = QtWidgets.QWidget()
        self.subtab_result.setObjectName("subtab_result")
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout(self.subtab_result)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.verticalLayout_sweepresult1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_sweepresult1.setObjectName("verticalLayout_sweepresult1")
        self.label_39 = QtWidgets.QLabel(self.subtab_result)
        self.label_39.setAlignment(QtCore.Qt.AlignCenter)
        self.label_39.setObjectName("label_39")
        self.verticalLayout_sweepresult1.addWidget(self.label_39)
        self.horizontalLayout_ = QtWidgets.QHBoxLayout()
        self.horizontalLayout_.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_.setSpacing(10)
        self.horizontalLayout_.setObjectName("horizontalLayout_")
        self.label_40 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_40.sizePolicy().hasHeightForWidth())
        self.label_40.setSizePolicy(sizePolicy)
        self.label_40.setObjectName("label_40")
        self.horizontalLayout_.addWidget(self.label_40)
        self.line_16 = QtWidgets.QFrame(self.subtab_result)
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.horizontalLayout_.addWidget(self.line_16)
        self.label_51 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_51.sizePolicy().hasHeightForWidth())
        self.label_51.setSizePolicy(sizePolicy)
        self.label_51.setObjectName("label_51")
        self.horizontalLayout_.addWidget(self.label_51)
        self.line_15 = QtWidgets.QFrame(self.subtab_result)
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.horizontalLayout_.addWidget(self.line_15)
        self.label_52 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy)
        self.label_52.setObjectName("label_52")
        self.horizontalLayout_.addWidget(self.label_52)
        self.line_17 = QtWidgets.QFrame(self.subtab_result)
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.horizontalLayout_.addWidget(self.line_17)
        self.label_53 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_53.sizePolicy().hasHeightForWidth())
        self.label_53.setSizePolicy(sizePolicy)
        self.label_53.setObjectName("label_53")
        self.horizontalLayout_.addWidget(self.label_53)
        self.horizontalLayout_.setStretch(0, 1)
        self.horizontalLayout_.setStretch(1, 1)
        self.horizontalLayout_.setStretch(2, 1)
        self.horizontalLayout_.setStretch(3, 1)
        self.horizontalLayout_.setStretch(4, 1)
        self.horizontalLayout_.setStretch(5, 1)
        self.horizontalLayout_.setStretch(6, 1)
        self.verticalLayout_sweepresult1.addLayout(self.horizontalLayout_)
        self.widget_sweepresult1 = QtWidgets.QTableWidget(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_sweepresult1.sizePolicy().hasHeightForWidth())
        self.widget_sweepresult1.setSizePolicy(sizePolicy)
        self.widget_sweepresult1.setObjectName("widget_sweepresult1")
        self.verticalLayout_sweepresult1.addWidget(self.widget_sweepresult1)
        self.horizontalLayout_54.addLayout(self.verticalLayout_sweepresult1)
        self.line_26 = QtWidgets.QFrame(self.subtab_result)
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.horizontalLayout_54.addWidget(self.line_26)
        self.verticalLayout_sweepresult2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_sweepresult2.setObjectName("verticalLayout_sweepresult2")
        self.label_65 = QtWidgets.QLabel(self.subtab_result)
        self.label_65.setAlignment(QtCore.Qt.AlignCenter)
        self.label_65.setObjectName("label_65")
        self.verticalLayout_sweepresult2.addWidget(self.label_65)
        self.horizontalLayout_57 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_57.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_57.setSpacing(10)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.label_67 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_67.sizePolicy().hasHeightForWidth())
        self.label_67.setSizePolicy(sizePolicy)
        self.label_67.setObjectName("label_67")
        self.horizontalLayout_57.addWidget(self.label_67)
        self.line_21 = QtWidgets.QFrame(self.subtab_result)
        self.line_21.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.horizontalLayout_57.addWidget(self.line_21)
        self.label_73 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_73.sizePolicy().hasHeightForWidth())
        self.label_73.setSizePolicy(sizePolicy)
        self.label_73.setObjectName("label_73")
        self.horizontalLayout_57.addWidget(self.label_73)
        self.line_22 = QtWidgets.QFrame(self.subtab_result)
        self.line_22.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.horizontalLayout_57.addWidget(self.line_22)
        self.label_74 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_74.sizePolicy().hasHeightForWidth())
        self.label_74.setSizePolicy(sizePolicy)
        self.label_74.setObjectName("label_74")
        self.horizontalLayout_57.addWidget(self.label_74)
        self.line_23 = QtWidgets.QFrame(self.subtab_result)
        self.line_23.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.horizontalLayout_57.addWidget(self.line_23)
        self.label_75 = QtWidgets.QLabel(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_75.sizePolicy().hasHeightForWidth())
        self.label_75.setSizePolicy(sizePolicy)
        self.label_75.setObjectName("label_75")
        self.horizontalLayout_57.addWidget(self.label_75)
        self.horizontalLayout_57.setStretch(0, 1)
        self.horizontalLayout_57.setStretch(1, 1)
        self.horizontalLayout_57.setStretch(2, 1)
        self.horizontalLayout_57.setStretch(3, 1)
        self.horizontalLayout_57.setStretch(4, 1)
        self.horizontalLayout_57.setStretch(5, 1)
        self.horizontalLayout_57.setStretch(6, 1)
        self.verticalLayout_sweepresult2.addLayout(self.horizontalLayout_57)
        self.widget_sweepresult2 = QtWidgets.QTableWidget(self.subtab_result)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_sweepresult2.sizePolicy().hasHeightForWidth())
        self.widget_sweepresult2.setSizePolicy(sizePolicy)
        self.widget_sweepresult2.setObjectName("widget_sweepresult2")
        self.verticalLayout_sweepresult2.addWidget(self.widget_sweepresult2)
        self.horizontalLayout_54.addLayout(self.verticalLayout_sweepresult2)
        self.tabWidget.addTab(self.subtab_result, "")
        self.verticalLayout_3.addWidget(self.tabWidget)

        self.tab_timelog = QtWidgets.QWidget()
        self.tab_timelog.setObjectName("tab_timelog")
        self.tab_widgets_main.addTab(self.tab_timelog, "")
        self.tab_peakmax = QtWidgets.QWidget()
        self.tab_peakmax.setObjectName("tab_peakmax")
        self.tab_widgets_main.addTab(self.tab_peakmax, "")

        


        self.tab_report = QtWidgets.QWidget()
        self.tab_report.setObjectName("tab_report")
        self.tab_widgets_main.addTab(self.tab_report, "")
        self.horizontalLayout_4.addWidget(self.tab_widgets_main)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 22))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionAdd_New = QtWidgets.QAction(MainWindow)
        self.actionAdd_New.setObjectName("actionAdd_New")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuFiles.addAction(self.actionImport)
        self.menuFiles.addAction(self.actionAdd_New)
        self.menuFiles.addAction(self.actionClose)
        self.menubar.addAction(self.menuFiles.menuAction())

        # list of all connected functions
        self.actionImport.triggered.connect(self.openfolder)
        self.actionAdd_New.triggered.connect(self.add)
        self.button_update.clicked.connect(self.pressed)
        self.button_update_2.clicked.connect(self.filter_width_table)
        
        self.lineEdit_gatevoltagemaximum.textChanged.connect(self.sweep_update)
        self.lineEdit_gatevoltageminimum.textChanged.connect(self.sweep_update)
        self.lineEdit_increments.textChanged.connect(self.sweep_update)



        self.retranslateUi(MainWindow)
        self.tab_widgets_main.setCurrentIndex(0)
        self.tab_widgets_scatter.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.file_dict_list = []
        self.sweep_1_data = []
        self.working_data = []
        self.current_file_dict = {}
        self.ui_state = Helper.ui_state()

        self.file_list_view.itemChanged.connect(self.update_names)
        self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)
        self.lineEdit_binwidth_2.editingFinished.connect(self.update_sweep_graphs)
        self.lineEdit_binwidth.editingFinished.connect(self.draw)

        self.file_list_view.itemChanged.connect(self.update_names)
        self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)
        
        self.lineEdit_5.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_6.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_7.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_8.editingFinished.connect(self.lr_peak_width_plot)


        
        
        self.recalculate_peak_dataset = True

        self.lr_x_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)
        self.lr_y_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)

        self.comboBox_6.currentIndexChanged.connect(self.width_scatter_channel_to_histogram_channel)
        self.comboBox_5.currentIndexChanged.connect(self.width_scatter_channel_to_histogram_channel)
        self.listView_channels_3.currentItemChanged.connect(self.width_histogram_channel_to_scatter_channel)
        self.lineEdit_gatevoltage_2.editingFinished.connect(self.width_histogram_channel_to_scatter_channel)
        self.lineEdit_gatevoltage_4.editingFinished.connect(self.width_histogram_channel_to_scatter_channel)
        
        self.w = OtherWindow(self)
        self.pushButton_resample.clicked.connect(self.openWindow)
        

    def width_scatter_channel_to_histogram_channel(self):
        self.listView_channels_3.setCurrentRow(self.comboBox_5.currentIndex())
        self.recalculate_peak_dataset = True
    
    def width_histogram_channel_to_scatter_channel(self):
        self.comboBox_5.setCurrentIndex(self.listView_channels_3.currentRow())
        self.lineEdit_5.setText(self.lineEdit_gatevoltage_2.text())
        self.lineEdit_7.setText(self.lineEdit_gatevoltage_4.text())
        self.lr_peak_width_plot()
        self.recalculate_peak_dataset = True
        
    def OtherWindow_Button_ok_clicked(self,text):
        self.chunk_resample = int(text)
        self.reset = True


    def openWindow(self):
        
        self.w.show()
    def update_sampling_Rate(self):
        
        self.listWidget_sampingrate.clear()
        
        self.listWidget_sampingrate.addItem('Ch1:'+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("Ch2:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("Ch3:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("Ch1_2:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("Ch1_3:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("Ch2_3:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("All Hit:1000")
#         self.listWidget_sampingrate.setCurrentRow(0)
        
        
    def update_names(self):
        """update the name of the sweep dropboxes"""
        self.comboBox_option1.clear()
        self.comboBox_option2.clear()
        for i in range(self.file_list_view.count()):
            self.comboBox_option1.addItem(self.file_list_view.item(i).text())
            self.comboBox_option2.addItem(self.file_list_view.item(i).text())

    def update_working_data(self):
#         try: print("Ui_MainWindow.reset:", Ui_MainWindow.reset)
#         except : print("Ui_MainWindow.reset: FALSE")

        
        
        if self.update or self.filter_update:
            self.peak_width_working_data  = []
            for i in range(4):
                self.peak_width_working_data.append([])
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
            if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1 ']][1][i]
            if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch2 ']][1][i]
            if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch3 ']][1][i]
            if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1-2']][1][i]
            if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1-3']][1][i]
            if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch2-3']][1][i]
            if len(self.peak_width_working_data) == 0:
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
            print("self.peak_width_working_data under working data",len(self.peak_width_working_data[0]),len(self.peak_width_working_data))        
            self.draw_peak_width(True)
            self.draw_peak_width_2(True)
            
        if self.update:
            self.working_data = []
            self.filtered_working_data = []
            for i in range(4):
                self.working_data.append([])
                self.filtered_working_data.append([])
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]
            if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch1 ']][0][i]                  
            if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch2 ']][0][i]
            if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch3 ']][0][i]
            if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch1-2']][0][i]
            if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch1-3']][0][i]
            if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Ch2-3']][0][i]
            if len(self.working_data) == 0:
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]
            print("self.working_data",len(self.working_data),len(self.working_data[0]),len(self.working_data[1]),len(self.working_data[2]),len(self.working_data[3]))        

        ### filter data by using min and max width
        
        if self.filtered_working_data[3] == [] or self.filtered_working_data[2] == []:
            self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if x >= -1 and x <= 100]
            self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if x >= -1 and x <= 100]
            self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if x >= -1 and x <= 100]
            self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if x >= -1 and x <= 100]
            self.filtered_working_data[0] = self.working_data[0]
            self.filtered_working_data[1] = self.working_data[1]
            self.filtered_working_data[2] = self.working_data[2]
            self.filtered_working_data[3] = self.working_data[3]
            

                        

            
            
        if self.recalculate_peak_dataset == True:
#             try:
#                 points_inside_square = self.points_inside_square
#             except:  
                ## x-axis
            if self.comboBox_5.currentIndex()==0:
                self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex()==1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
  
            elif self.comboBox_5.currentIndex()==1:
                self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex()==0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                  
            elif self.comboBox_5.currentIndex()==2:                        
                self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex()==0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

            elif self.comboBox_5.currentIndex()==3:
                self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex()==0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex()==2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                    

                    
#                 width_data = self.peak_width_working_data[self.comboBox_5.currentIndex()]
#                 width_index1 = [i for i, x in enumerate(width_data) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]

#                 ## y-axis
#                 width_data = self.peak_width_working_data[self.comboBox_6.currentIndex()]
#                 width_index2 = [i for i, x in enumerate(width_data) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

#                 points_inside_square = [value for value in width_index1 if value in width_index2]

#             peak_data_x = self.working_data[self.comboBox_5.currentIndex()]  
#             peak_data_y = self.working_data[self.comboBox_6.currentIndex()] 
    


#             self.filtered_working_data[self.comboBox_5.currentIndex()] = [ peak_data_x[i] for i in points_inside_square]
#             self.filtered_working_data[self.comboBox_6.currentIndex()] = [ peak_data_y[i] for i in points_inside_square]
            
            
            self.recalculate_peak_dataset = False
     
            self.draw(True)
            self.draw_2(True)
            self.update_sweep_graphs(True)
            

            
            
    def update_statistic(self):
        """update the statistic table"""
        stats = []
        self.tableView_statistic.clear()
        self.tableView_statistic.setHorizontalHeaderLabels(['Mean', 'Median', 'Standard Deviation', 'Min', 'Max'])
        self.tableView_statistic.setVerticalHeaderLabels(['Green', 'Red', 'Blue', 'Orange'])
        for i in range(4):
            mean = statistics.mean(self.working_data[i])
            median = statistics.median(self.working_data[i])
            stddv = statistics.stdev(self.working_data[i])
            max_value = max(self.working_data[i])
            min_value = min(self.working_data[i])
            stats.append([mean, median, stddv, max_value, min_value])
        for x in range(4):
            for y in range(5):
                item = QTableWidgetItem(str(round(stats[x][y], 2)))
                self.tableView_statistic.setItem(x, y, item)

    def sweep_update_low(self):
        """update sweep parameter threshold for low"""
        sweep_thresh = float(self.lineEdit_gatevoltageminimum.text())
        if len(self.sweep_1_data) > 0:
            filtered_gate_voltage = [x for x in self.sweep_1_data if x > sweep_thresh]
            percentage = round(100 * len(filtered_gate_voltage) / len(self.sweep_1_data), 2)
            self.lineEdit_percentagelow1.setText(str(percentage))
        if len(self.sweep_2_data) > 0:
            filtered_gate_voltage = [x for x in self.sweep_2_data if x > sweep_thresh]
            percentage = round(100 * len(filtered_gate_voltage) / len(self.sweep_2_data), 2)
            self.lineEdit_percentagelow2.setText(str(percentage))

    def sweep_update_high(self):
        """update sweep parameter threshold for above"""
        sweep_thresh = float(self.lineEdit_gatevoltagemaximum.text())
        if len(self.sweep_1_data) > 0:
            filtered_gate_voltage = [x for x in self.sweep_1_data if x > sweep_thresh]
            percentage = round(100 * len(filtered_gate_voltage) / len(self.sweep_1_data), 2)
            self.lineEdit_percentagehigh1.setText(str(percentage))
        if len(self.sweep_2_data) > 0:
            filtered_gate_voltage = [x for x in self.sweep_2_data if x > sweep_thresh]
            percentage = round(100 * len(filtered_gate_voltage) / len(self.sweep_2_data), 2)
            self.lineEdit_percentagehigh2.setText(str(percentage))

    def sweep_update(self):
        """update the sweep result table"""
        try:
            range_max = float(self.lineEdit_gatevoltagemaximum.text())
            range_min = float(self.lineEdit_gatevoltageminimum.text())
            increment = float(self.lineEdit_increments.text())
        except:
            range_max = 0
            range_min = 0
            increment = 0
        if 0 < increment < range_max - range_min and (range_max - range_min) / increment < 500 and \
                len(self.sweep_1_data) > 0 and len(self.sweep_2_data) > 0:
            print("Updating Sweep Table")
            self.widget_sweepresult1.clear()
            self.widget_sweepresult1.setRowCount(int((range_max - range_min) / increment))
            self.widget_sweepresult1.setColumnCount(4)
            self.widget_sweepresult1.setHorizontalHeaderLabels(("Voltages", "Counts Above Threshold",
                                                                "Total Count", "Percentages"))
            self.widget_sweepresult1.verticalHeader().hide()
            self.widget_sweepresult2.clear()
            self.widget_sweepresult2.setRowCount(int((range_max - range_min) / increment))
            self.widget_sweepresult2.setColumnCount(4)
            self.widget_sweepresult2.setHorizontalHeaderLabels(("Voltages", "Counts Above Threshold",
                                                                "Total Count", "Percentages"))
            self.widget_sweepresult2.verticalHeader().hide()
            if len(self.sweep_1_data) > 0:
                counter = range_min
                sweep_list = []
                i = 0
                while counter < range_max:
                    filtered_gate_voltage_x = [x for x in self.sweep_1_data if x > counter]
                    percentage = round(100 * len(filtered_gate_voltage_x) / len(self.sweep_1_data), 2)
                    sweep_list.append([counter, len(filtered_gate_voltage_x), len(self.sweep_1_data), percentage])
                    counter += increment
                    i += 1
                for x, row in enumerate(sweep_list):
                    for y in range(4):
                        item = QTableWidgetItem(str(round(row[y], 2)))
                        self.widget_sweepresult1.setItem(x, y, item)
                self.widget_sweepresult1.show()
            if len(self.sweep_2_data) > 0:
                counter = range_min
                sweep_list = []
                i = 0
                while counter < range_max:
                    filtered_gate_voltage_x = [x for x in self.sweep_2_data if x > counter]
                    percentage = round(100 * len(filtered_gate_voltage_x) / len(self.sweep_2_data), 2)
                    sweep_list.append([counter, len(filtered_gate_voltage_x), len(self.sweep_2_data), percentage])
                    counter += increment
                    i += 1
                for x, row in enumerate(sweep_list):
                    for y in range(4):
                        item = QTableWidgetItem(str(round(row[y], 2)))
                        self.widget_sweepresult2.setItem(x, y, item)
                self.widget_sweepresult2.show()

    def thresholdUpdated(self):
        text_x = float(self.lineEdit_gatevoltage.text())
        # x
        line_xx = [text_x, text_x]
        line_yy = [0, 200]

        self.data_line.setData(line_xx, line_yy)

        filtered_gate_voltage_x = [x for x in self.width if x > text_x]

        percentage = round(100 * len(filtered_gate_voltage_x) / len(self.width), 2)
        self.lineEdit_percentage.setText(str(percentage))
        


#     def thresholdUpdated_peak_width(self):
#         width_count = len(self.peak_width)
#         self.lineEdit_percentage.setText(str(width_count))

#         text_x = float(self.lineEdit_gatevoltage_2.text())
#         # x
#         line_xx = [text_x, text_x]
#         line_yy = [0, 200]

#         self.data_line_peak_width.setData(line_xx, line_yy)

#         filtered_gate_voltage_x = [x for x in self.peak_width if x > text_x]
        

#         percentage = round(100 * len(filtered_gate_voltage_x) / len(self.peak_width), 2)
#         self.lineEdit_percentage.setText(str(percentage))
        
    def update_sweep_graphs(self, bypass=False):
        self.sweep_bins = float(self.lineEdit_binwidth_2.text())
        update1, update2, data_updated = self.ui_state.sweep_update(channel_select=self.sweep_channel,
                                                                    file1=self.sweep_file_1,
                                                                    file2=self.sweep_file_2, bins=self.sweep_bins)
        if update1:
            self.update_sweep_1(data_updated)
        elif bypass:
            self.update_sweep_1(bypass)
        if update2:
            self.update_sweep_2(data_updated)
        elif bypass:
            self.update_sweep_2(bypass)

    def update_sweep_1(self, data_updated=False):
        self.widget_sweepparam2.clear()
        channel = self.listView_channels_2.currentRow()
        if channel == -1:
            self.listView_channels_2.setCurrentRow(0)
        axis_name = self.listView_channels_2.currentItem().text()
        self.widget_sweepparam2.setLabel('bottom', axis_name)
        print("update sweep 1")
        r, g, b = Helper.rgb_select(channel)
        if data_updated:
            self.sweep_1_data = self.working_data[channel]
#             self.sweep_1_data = []
#             if self.checkBox_7.isChecked() and self.sweep_1_dict['Peak Record'] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Peak Record']][0][channel]
#             if self.checkbox_ch1.isChecked() and self.sweep_1_dict['Ch1 '] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1 ']][0][channel]
#             if self.checkbox_ch2.isChecked() and self.sweep_1_dict['Ch2 '] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch2 ']][0][channel]
#             if self.checkbox_ch3.isChecked() and self.sweep_1_dict['Ch3 '] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch3 ']][0][channel]
#             if self.checkbox_ch12.isChecked() and self.sweep_1_dict['Ch1-2'] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1-2']][0][channel]
#             if self.checkbox_ch13.isChecked() and self.sweep_1_dict['Ch1-3'] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1-3']][0][channel]
#             if self.checkbox_ch23.isChecked() and self.sweep_1_dict['Ch2-3'] != '':
#                 self.sweep_1_data += self.analog[self.sweep_1_dict['Ch2-3']][0][channel]
        range_width = int(max(self.sweep_1_data)) + 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
        y, x = np.histogram(self.sweep_1_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam2.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam2.setXRange(0, max(x), padding=0)
        self.widget_sweepparam2.setYRange(0, max(y), padding=0)

    def update_sweep_2(self, data_updated=False):
        self.widget_sweepparam1.clear()
        channel = self.listView_channels_2.currentRow()
        if channel == -1:
            self.listView_channels_2.setCurrentRow(0)
        axis_name = self.listView_channels_2.currentItem().text()
        self.widget_sweepparam1.setLabel('bottom', axis_name)
        r, g, b = Helper.rgb_select(channel)
        print("update sweep 2")
        if data_updated:
            self.sweep_2_data = self.working_data[channel]
#             self.sweep_2_data = []
#             if self.checkBox_7.isChecked() and self.sweep_2_dict['Peak Record'] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Peak Record']][0][channel]
#             if self.checkbox_ch1.isChecked() and self.sweep_2_dict['Ch1 '] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1 ']][0][channel]
#             if self.checkbox_ch2.isChecked() and self.sweep_2_dict['Ch2 '] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch2 ']][0][channel]
#             if self.checkbox_ch3.isChecked() and self.sweep_2_dict['Ch3 '] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch3 ']][0][channel]
#             if self.checkbox_ch12.isChecked() and self.sweep_2_dict['Ch1-2'] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1-2']][0][channel]
#             if self.checkbox_ch13.isChecked() and self.sweep_2_dict['Ch1-3'] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1-3']][0][channel]
#             if self.checkbox_ch23.isChecked() and self.sweep_2_dict['Ch2-3'] != '':
#                 self.sweep_2_data += self.analog[self.sweep_2_dict['Ch2-3']][0][channel]
        range_width = int(max(self.sweep_2_data)) + 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
        y, x = np.histogram(self.sweep_2_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam1.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam1.setXRange(0, max(x), padding=0)
        self.widget_sweepparam1.setYRange(0, max(y), padding=0)
        
    def draw_peak_width(self,data_updated=False):
        self.histo_bins_peak_width = float(self.lineEdit_binwidth_3.text())

        if self.filter_update or data_updated or self.width_update:
            print("draw_peak_width")
            channel = self.listView_channels_3.currentRow()
            if channel == -1:
                self.listView_channels.setCurrentRow(0)
            self.histogram_graphWidget_3.clear()
            r, g, b = Helper.rgb_select(channel)
            styles = {"color": "r", "font-size": "20px"}
            axis_name = self.listView_channels_3.currentItem().text()
            self.histogram_graphWidget_3.setLabel('bottom', axis_name, **styles)
            
            self.full_peak_width = self.peak_width_working_data[self.listView_channels_3.currentRow()] 
            
            x_low = float(self.lineEdit_gatevoltage_2.text())
            x_high = float(self.lineEdit_gatevoltage_4.text())
            
            self.peak_width = [x for x in self.full_peak_width if x >= x_low and x <=x_high]
            range_width = int(max(self.peak_width)) + 1
            bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_3.text()))
            y, x = np.histogram(self.peak_width, bins=bin_edge)
            separate_y = [0] * len(y)
            for i in range(len(y)):
                separate_y = [0] * len(y)
                separate_y[i] = y[i]
                self.histogram_graphWidget_3.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True,
                                                brush=(r, g, b))

            self.histogram_graphWidget_3.setXRange(0, max(x), padding=0)
            self.histogram_graphWidget_3.setYRange(0, max(y), padding=0)

            
            peak_width_without_zero = [i for i in self.peak_width if i != 0]
            width_count = round(100 * len(peak_width_without_zero) / len(self.full_peak_width), 2)
            self.lineEdit_percentage_2.setText(str(width_count))
            self.lineEdit_gatevoltage_6.setText(str(len(self.full_peak_width)))
            

            # after 1st map so the line layer will appear before the histogram
            self.data_line_peak_width = self.histogram_graphWidget_3.plot([0, 0], [0, 0],
                                                             pen=pg.mkPen(color=('r'), width=5,
                                                                          style=QtCore.Qt.DashLine))
#             self.thresholdUpdated()            
        
    def draw_peak_width_2(self,data_updated=False):
        update = self.ui_state.width_scatter_update(x_select=self.width_scatter_channelx, y_select=self.width_scatter_channely)

        if self.filter_update or data_updated or update:
            print("draw_peak_width_2")
            x_axis_channel = self.comboBox_5.currentIndex()
            y_axis_channel = self.comboBox_6.currentIndex()
            x_axis_name = self.comboBox_5.currentText()
            y_axis_name = self.comboBox_6.currentText()

            self.graphWidget_width_scatter.clear()

            self.graphWidget_width_scatter.setLabel('left', y_axis_name, color='b')
            self.graphWidget_width_scatter.setLabel('bottom', x_axis_name, color='b')

            self.Ch1_channel0_width = self.peak_width_working_data[x_axis_channel]
            self.Ch1_channel1_width = self.peak_width_working_data[y_axis_channel]

            max_voltage = 100
            bins = 1000
            steps = max_voltage / bins
            # all data is first sorted into a histogram
            histo, _, _ = np.histogram2d(self.Ch1_channel0_width, self.Ch1_channel1_width, bins,
                                         [[0, max_voltage], [0, max_voltage]],
                                         density=True)
            max_density = histo.max()

            # made empty array to hold the sorted data according to density
            density_listx = []
            density_listy = []
            for i in range(6):
                density_listx.append([])
                density_listy.append([])

            for i in range(len(self.Ch1_channel0_width)):

                x = self.Ch1_channel0_width[i]
                y = self.Ch1_channel1_width[i]
                a = int(x / steps)
                b = int(y / steps)
                if a >= 1000:
                    a = 999
                if b >= 1000:
                    b = 999
                    
                # checking for density, the value divided by steps serves as the index
                density = histo[a][b]
                percentage = density / max_density * 100
#                 if i % 10000 == 0:
#                     print(i)
                if 20 > percentage >= 0:
                    density_listx[0].append(x)
                    density_listy[0].append(y)
                elif 40 > percentage >= 20:
                    density_listx[1].append(x)
                    density_listy[1].append(y)
                elif 60 > percentage >= 40:
                    density_listx[2].append(x)
                    density_listy[2].append(y)
                elif 80 > percentage >= 60:
                    density_listx[3].append(x)
                    density_listy[3].append(y)
                else:
                    density_listx[4].append(x)
                    density_listy[4].append(y)
            for i in range(5):
                if i == 0:
                    red = 0
                    blue = 255 / 15
                    green = 255
                elif i == 1:
                    red = 0
                    blue = 255
                    green = 255 - 255 / 15
                elif i == 2:
                    red = 255 / 15
                    blue = 255
                    green = 0
                elif i == 3:
                    red = 255
                    blue = 255 - 255 / 15
                    green = 0
                elif i == 4:
                    red = 255
                    blue = 255 / 15
                    green = 255 / 15
                else:
                    red = 255
                    blue = 255
                    green = 255

                self.graphWidget_width_scatter.plot(density_listx[i], density_listy[i], symbol='p', pen=None, symbolPen=None,
                                      symbolSize=5, symbolBrush=(red, blue, green))
 
            self.lr_peak_width_plot()    
            # threshold
#             self.thresholdUpdated_2() 

    def lr_peak_width_plot(self):
        self.graphWidget_width_scatter.removeItem(self.lr_x_axis)
        self.graphWidget_width_scatter.removeItem(self.lr_y_axis)

        x_low = float(self.lineEdit_5.text())
        y_low = float(self.lineEdit_6.text())
        x_high = float(self.lineEdit_7.text())
        y_high = float(self.lineEdit_8.text())
        
        self.lineEdit_gatevoltage_2.setText(str(round(x_low,2)))
        self.lineEdit_gatevoltage_4.setText(str(round(x_high,2)))
        
        self.lr_x_axis = pg.LinearRegionItem([x_low,x_high])
        self.lr_y_axis = pg.LinearRegionItem([y_low,y_high], orientation = 'horizontal')
        self.graphWidget_width_scatter.addItem(self.lr_x_axis)
        self.graphWidget_width_scatter.addItem(self.lr_y_axis)        

#         self.filter_width_table()
        self.recalculate_peak_dataset = True
        
        self.lr_x_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)
        self.lr_y_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)
    
        
    def lr_peak_width_change(self):
        print("lr_peak_width_change")
        x_low,x_high = self.lr_x_axis.getRegion()
        y_low,y_high = self.lr_y_axis.getRegion()
        
        self.lineEdit_5.setText(str(round(x_low,2)))
        self.lineEdit_6.setText(str(round(y_low,2)))
        self.lineEdit_7.setText(str(round(x_high,2)))
        self.lineEdit_8.setText(str(round(y_high,2)))
        self.lineEdit_gatevoltage_2.setText(str(round(x_low,2)))
        self.lineEdit_gatevoltage_4.setText(str(round(x_high,2)))
        
#         self.filter_width_table()
        self.recalculate_peak_dataset = True
        
    def filter_width_table(self):
                ## x-axis
        width_data = self.peak_width_working_data[self.comboBox_5.currentIndex()]
        width_index1 = [i for i, x in enumerate(width_data) if x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
        ## y-axis
        width_data = self.peak_width_working_data[self.comboBox_6.currentIndex()]       
        width_index2 = [i for i, x in enumerate(width_data) if x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

        
#         self.points_inside_square = [value for value in width_index1 if value in width_index2]
        self.points_inside_square = list(set(width_index1).intersection(set(width_index2)))
        
        self.lineEdit_gatevoltage_5.setText(str(len(self.points_inside_square)))
        
        


        
    def draw(self, data_updated=False):

        self.histo_bins = float(self.lineEdit_binwidth.text())
        update = self.ui_state.gating_update(channel_select=self.histo_channel, bins=self.histo_bins)
        if update or data_updated:
            print("update draw")

            
            channel = self.listView_channels.currentRow()
            if channel == -1:
                self.listView_channels.setCurrentRow(0)
            self.histogram_graphWidget.clear()
            r, g, b = Helper.rgb_select(channel)
            styles = {"color": "r", "font-size": "20px"}
            axis_name = self.listView_channels.currentItem().text()
            self.histogram_graphWidget.setLabel('bottom', axis_name, **styles)
            # default
            # self.width = self.analog[current_file_dict['Peak Record']][0][0]
            self.width = self.filtered_working_data[self.listView_channels.currentRow()]

            self.lineEdit_count.setText(str(len(self.width)))
            range_width = int(max(self.width)) + 1
            bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth.text()))
            y, x = np.histogram(self.width, bins=bin_edge)
            separate_y = [0] * len(y)
            for i in range(len(y)):
                separate_y = [0] * len(y)
                separate_y[i] = y[i]
                self.histogram_graphWidget.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True,
                                                brush=(r, g, b))

            self.histogram_graphWidget.setXRange(0, max(x), padding=0)
            self.histogram_graphWidget.setYRange(0, max(y), padding=0)

            # after 1st map so the line layer will appear before the histogram
            self.data_line = self.histogram_graphWidget.plot([0, 0], [0, 0],
                                                             pen=pg.mkPen(color=('r'), width=5,
                                                                          style=QtCore.Qt.DashLine))
            self.thresholdUpdated()

    def draw_2(self, data_updated=False):

        update = self.ui_state.scatter_update(x_select=self.scatter_channelx, y_select=self.scatter_channely)
        if update or data_updated:
            print("update draw2")

            if self.comboBox.currentIndex()==0:
                if self.comboBox_2.currentIndex()==0:
                    points_inside_square = self.width_index0
                elif self.comboBox_2.currentIndex()==1:
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index1)))
                    
                elif self.comboBox_2.currentIndex()==2:
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index2)))
                    
                elif self.comboBox_2.currentIndex()==3: 
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index3)))
                    
                    
            elif self.comboBox.currentIndex()==1:
                if self.comboBox_2.currentIndex()==0:
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index0)))
                    
                elif self.comboBox_2.currentIndex()==1:
                    points_inside_square = self.width_index1
                elif self.comboBox_2.currentIndex()==2:
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index2)))
                    
                elif self.comboBox_2.currentIndex()==3: 
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index3)))
                    
                    
            elif self.comboBox.currentIndex()==2:
                if self.comboBox_2.currentIndex()==0:
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index0)))

                    
                elif self.comboBox_2.currentIndex()==1:
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index1)))
                    
                elif self.comboBox_2.currentIndex()==2:
                    points_inside_square = self.width_index2
                elif self.comboBox_2.currentIndex()==3: 
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index3)))
                    
            elif self.comboBox.currentIndex()==3:
                if self.comboBox_2.currentIndex()==0:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index0)))
 
                elif self.comboBox_2.currentIndex()==1:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index1)))
            
                elif self.comboBox_2.currentIndex()==2:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index2)))

                elif self.comboBox_2.currentIndex()==3: 
                    points_inside_square = self.width_index3                   
                          
            peak_data_x = self.working_data[self.comboBox.currentIndex()]  
            peak_data_y = self.working_data[self.comboBox_2.currentIndex()] 

            self.filtered_working_data[self.comboBox.currentIndex()] = [ peak_data_x[i] for i in points_inside_square]
            self.filtered_working_data[self.comboBox_2.currentIndex()] = [ peak_data_y[i] for i in points_inside_square]

            
            x_axis_channel = self.comboBox.currentIndex()
            y_axis_channel = self.comboBox_2.currentIndex()
            x_axis_name = self.comboBox.currentText()
            y_axis_name = self.comboBox_2.currentText()


            
            self.graphWidget.clear()

            self.graphWidget.setLabel('left', y_axis_name, color='b')
            self.graphWidget.setLabel('bottom', x_axis_name, color='b')

            self.Ch1_channel0 = self.filtered_working_data[x_axis_channel]
            self.Ch1_channel1 = self.filtered_working_data[y_axis_channel]

            max_voltage = 12
            bins = 1000
            steps = max_voltage / bins

            print("x",len(self.Ch1_channel0),"y",len(self.Ch1_channel1))
            

                
            # all data is first sorted into a histogram
            histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins,
                                         [[0, max_voltage], [0, max_voltage]],
                                         density=True)
            max_density = histo.max()

            # made empty array to hold the sorted data according to density
            density_listx = []
            density_listy = []
            for i in range(6):
                density_listx.append([])
                density_listy.append([])

            for i in range(len(self.Ch1_channel0)):
                """legend_range = 0.07
                aa = [ii for ii, e in enumerate(self.Ch1_channel0) if (self.Ch1_channel0[i] + legend_range) > e > (self.Ch1_channel0[i] - legend_range)]
                bb = [ii for ii, e in enumerate(self.Ch1_channel1) if (self.Ch1_channel1[i] + legend_range) > e > (self.Ch1_channel1[i] - legend_range)]
                
                ab_set = len(set(aa) & set(bb))   
                """
                x = self.Ch1_channel0[i]
                y = self.Ch1_channel1[i]
                a = int(x / steps)
                b = int(y / steps)
                if a >= 1000:
                    a = 999
                if b >= 1000:
                    b = 999
                    
                # checking for density, the value divided by steps serves as the index
                density = histo[a][b]
                percentage = density / max_density * 100
#                 if i % 10000 == 0:
#                     print(i)
                if 20 > percentage >= 0:
                    density_listx[0].append(x)
                    density_listy[0].append(y)
                elif 40 > percentage >= 20:
                    density_listx[1].append(x)
                    density_listy[1].append(y)
                elif 60 > percentage >= 40:
                    density_listx[2].append(x)
                    density_listy[2].append(y)
                elif 80 > percentage >= 60:
                    density_listx[3].append(x)
                    density_listy[3].append(y)
                else:
                    density_listx[4].append(x)
                    density_listy[4].append(y)
            for i in range(5):
                if i == 0:
                    red = 0
                    blue = 255 / 15
                    green = 255
                elif i == 1:
                    red = 0
                    blue = 255
                    green = 255 - 255 / 15
                elif i == 2:
                    red = 255 / 15
                    blue = 255
                    green = 0
                elif i == 3:
                    red = 255
                    blue = 255 - 255 / 15
                    green = 0
                elif i == 4:
                    red = 255
                    blue = 255 / 15
                    green = 255 / 15
                else:
                    red = 255
                    blue = 255
                    green = 255

                self.graphWidget.plot(density_listx[i], density_listy[i], symbol='p', pen=None, symbolPen=None,
                                      symbolSize=5, symbolBrush=(red, blue, green))
           

            #    >0%    0,0,1   blue
            #    >15%   0,1,1  cyan
            #    >30%   0,1,0  green
            #    >45%   1,1,0  yellow
            #    >60%   1,0,0   red
            #    >75%   1,1,1   white

            print("draw2 end")
            # threshold
            self.thresholdUpdated_2()

    def thresholdUpdated_2(self):
        self.graphWidget.removeItem(self.data_line_y)
        self.graphWidget.removeItem(self.data_line_x)

        text_x = float(self.lineEdit_scatterxvoltage.text())
        text_y = float(self.lineEdit_scatteryvoltage.text())

        # x
        line_xx = [text_x, text_x]
        line_yy = [0, max(self.Ch1_channel1)]

        self.data_line_x.setData(line_xx, line_yy)
        # y
        line_x = [0, max(self.Ch1_channel0)]
        line_y = [text_y, text_y]

        self.data_line_y.setData(line_x, line_y)
        self.data_line_x = self.graphWidget.plot(line_xx, line_yy,
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.data_line_y = self.graphWidget.plot(line_x, line_y,
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))

        filtered_gate_voltage_x = [x for x in self.Ch1_channel0 if x > text_x]
        filtered_gate_voltage_y = [x for x in self.Ch1_channel1 if x > text_y]

        # filter y axis
        a = (np.array(self.Ch1_channel0) > text_x).tolist()
        b = (np.array(self.Ch1_channel0) < text_x).tolist()

        # filter x axis
        c = (np.array(self.Ch1_channel1) > text_y).tolist()
        d = (np.array(self.Ch1_channel1) < text_y).tolist()

        count_quadrant1 = 0
        count_quadrant2 = 0
        count_quadrant3 = 0
        count_quadrant4 = 0

        channel0_list_quadrant1 = []
        channel1_list_quadrant1 = []
        channel0_list_quadrant2 = []
        channel1_list_quadrant2 = []
        channel0_list_quadrant3 = []
        channel1_list_quadrant3 = []
        channel0_list_quadrant4 = []
        channel1_list_quadrant4 = []

        for i in range(len(a)):
            if a[i] and c[i]:
                channel0_list_quadrant1.append(self.Ch1_channel0[i])
                channel1_list_quadrant1.append(self.Ch1_channel1[i])
                count_quadrant1 += 1
            elif not a[i] and c[i]:
                channel0_list_quadrant2.append(self.Ch1_channel0[i])
                channel1_list_quadrant2.append(self.Ch1_channel1[i])
                count_quadrant2 += 1
            elif not a[i] and not c[i]:
                channel0_list_quadrant3.append(self.Ch1_channel0[i])
                channel1_list_quadrant3.append(self.Ch1_channel1[i])
                count_quadrant3 += 1
            elif a[i] and not c[i]:
                channel0_list_quadrant4.append(self.Ch1_channel0[i])
                channel1_list_quadrant4.append(self.Ch1_channel1[i])
                count_quadrant4 += 1

            
        try:
            droplets = float(self.lineEdit_totaldroplets.text())
            totalpercent1 = round(count_quadrant1 / droplets * 100, 2)
            totalpercent2 = round(count_quadrant2 / droplets * 100, 2)
            totalpercent3 = round(count_quadrant3 / droplets * 100, 2)
            totalpercent4 = round(count_quadrant4 / droplets * 100, 2)
        except:
            totalpercent1 = 0
            totalpercent2 = 0
            totalpercent3 = 0
            totalpercent4 = 0
            

        self.tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(count_quadrant1)))
        self.tableView_scatterquadrants.setItem(0, 1,
                                                QTableWidgetItem(str(round(100 * count_quadrant1 / len(self.Ch1_channel0), 2))))
        self.tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
        self.tableView_scatterquadrants.setItem(1, 0, QTableWidgetItem(str(count_quadrant2)))
        self.tableView_scatterquadrants.setItem(1, 1,
                                                QTableWidgetItem(str(round(100 * count_quadrant2 / len(self.Ch1_channel0), 2))))
        self.tableView_scatterquadrants.setItem(1, 2, QTableWidgetItem(str(totalpercent2)))
        self.tableView_scatterquadrants.setItem(2, 0, QTableWidgetItem(str(count_quadrant3)))
        self.tableView_scatterquadrants.setItem(2, 1,
                                                QTableWidgetItem(str(round(100 * count_quadrant3 / len(self.Ch1_channel0), 2))))
        self.tableView_scatterquadrants.setItem(2, 2, QTableWidgetItem(str(totalpercent3)))
        self.tableView_scatterquadrants.setItem(3, 0, QTableWidgetItem(str(count_quadrant4)))
        self.tableView_scatterquadrants.setItem(3, 1,
                                                QTableWidgetItem(str(round(100 * count_quadrant4 / len(self.Ch1_channel0), 2))))
        self.tableView_scatterquadrants.setItem(3, 2, QTableWidgetItem(str(totalpercent4)))
        
        
        ### mid table

        try:
            self.tableView_scatterxaxis.setItem(0, 0, QTableWidgetItem(str(round(statistics.mean(channel0_list_quadrant1),2))))
            self.tableView_scatterxaxis.setItem(0, 1, QTableWidgetItem(str(round(statistics.stdev(channel0_list_quadrant1),2))))
            self.tableView_scatterxaxis.setItem(0, 2, QTableWidgetItem(str(round(statistics.median(channel0_list_quadrant1),2))))
        except:
            self.tableView_scatterxaxis.setItem(0, 0, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(0, 1, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(0, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatterxaxis.setItem(1, 0, QTableWidgetItem(str(round(statistics.mean(channel0_list_quadrant2),2))))
            self.tableView_scatterxaxis.setItem(1, 1, QTableWidgetItem(str(round(statistics.stdev(channel0_list_quadrant2),2))))
            self.tableView_scatterxaxis.setItem(1, 2, QTableWidgetItem(str(round(statistics.median(channel0_list_quadrant2),2))))
        except:
            self.tableView_scatterxaxis.setItem(1, 0, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(1, 1, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(1, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatterxaxis.setItem(2, 0, QTableWidgetItem(str(round(statistics.mean(channel0_list_quadrant3),2))))
            self.tableView_scatterxaxis.setItem(2, 1, QTableWidgetItem(str(round(statistics.stdev(channel0_list_quadrant3),2))))
            self.tableView_scatterxaxis.setItem(2, 2, QTableWidgetItem(str(round(statistics.median(channel0_list_quadrant3),2))))
        except:
            self.tableView_scatterxaxis.setItem(2, 0, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(2, 1, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(2, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatterxaxis.setItem(3, 0, QTableWidgetItem(str(round(statistics.mean(channel0_list_quadrant4),2))))
            self.tableView_scatterxaxis.setItem(3, 1, QTableWidgetItem(str(round(statistics.stdev(channel0_list_quadrant4),2))))
            self.tableView_scatterxaxis.setItem(3, 2, QTableWidgetItem(str(round(statistics.median(channel0_list_quadrant4),2))))
        except:
            self.tableView_scatterxaxis.setItem(3, 0, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(3, 1, QTableWidgetItem('NaN'))
            self.tableView_scatterxaxis.setItem(3, 2, QTableWidgetItem('NaN'))

        # bottom

        try:
            self.tableView_scatteryaxis.setItem(0, 0, QTableWidgetItem(str(round(statistics.mean(channel1_list_quadrant1),2))))
            self.tableView_scatteryaxis.setItem(0, 1, QTableWidgetItem(str(round(statistics.stdev(channel1_list_quadrant1),2))))
            self.tableView_scatteryaxis.setItem(0, 2, QTableWidgetItem(str(round(statistics.median(channel1_list_quadrant1),2))))
        except:
            self.tableView_scatteryaxis.setItem(0, 0, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(0, 1, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(0, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatteryaxis.setItem(1, 0, QTableWidgetItem(str(round(statistics.mean(channel1_list_quadrant2),2))))
            self.tableView_scatteryaxis.setItem(1, 1, QTableWidgetItem(str(round(statistics.stdev(channel1_list_quadrant2),2))))
            self.tableView_scatteryaxis.setItem(1, 2, QTableWidgetItem(str(round(statistics.median(channel1_list_quadrant2),2))))
        except:
            self.tableView_scatteryaxis.setItem(1, 0, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(1, 1, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(1, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatteryaxis.setItem(2, 0, QTableWidgetItem(str(round(statistics.mean(channel1_list_quadrant3),2))))
            self.tableView_scatteryaxis.setItem(2, 1, QTableWidgetItem(str(round(statistics.stdev(channel1_list_quadrant3),2))))
            self.tableView_scatteryaxis.setItem(2, 2, QTableWidgetItem(str(round(statistics.median(channel1_list_quadrant3),2))))
        except:
            self.tableView_scatteryaxis.setItem(2, 0, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(2, 1, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(2, 2, QTableWidgetItem('NaN'))

        try:
            self.tableView_scatteryaxis.setItem(3, 0, QTableWidgetItem(str(round(statistics.mean(channel1_list_quadrant4),2))))
            self.tableView_scatteryaxis.setItem(3, 1, QTableWidgetItem(str(round(statistics.stdev(channel1_list_quadrant4),2))))
            self.tableView_scatteryaxis.setItem(3, 2, QTableWidgetItem(str(round(statistics.median(channel1_list_quadrant4),2))))
        except:
            self.tableView_scatteryaxis.setItem(3, 0, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(3, 1, QTableWidgetItem('NaN'))
            self.tableView_scatteryaxis.setItem(3, 2, QTableWidgetItem('NaN'))


        ###  


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_files.setText(_translate("MainWindow", "Files"))
        self.button_rename.setText(_translate("MainWindow", "Rename"))
        self.label.setText(_translate("MainWindow", "Channel Selection"))
        self.checkbox_ch1.setText(_translate("MainWindow", "Channel 1"))
        self.checkbox_ch2.setText(_translate("MainWindow", "Channel 2"))
        self.checkbox_ch3.setText(_translate("MainWindow", "Channel 3"))
        self.checkbox_ch12.setText(_translate("MainWindow", "Channel 1-2"))
        self.checkbox_ch13.setText(_translate("MainWindow", "Channel 1-3"))
        self.checkbox_ch23.setText(_translate("MainWindow", "Channel 2-3"))
        self.checkBox_7.setText(_translate("MainWindow", "All Channel"))
        self.button_update.setText(_translate("MainWindow", "Update"))
        self.label_2.setText(_translate("MainWindow", "Gate Voltages"))
        self.button_copy.setText(_translate("MainWindow", "Copy"))
        self.button_paste.setText(_translate("MainWindow", "Paste"))
        self.button_screenshot.setText(_translate("MainWindow", "Screenshot"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.label_8.setText(_translate("MainWindow", "Total Runtime"))
        self.label_3.setText(_translate("MainWindow", "Sampling Rate"))
        self.pushButton_resample.setText(_translate("MainWindow", "Resample"))
        self.label_4.setText(_translate("MainWindow", "Count"))
        self.label_6.setText(_translate("MainWindow", "Starting Time"))
        self.label_12.setText(_translate("MainWindow", "Ch1 Hit"))
        self.label_14.setText(_translate("MainWindow", "Ch 3 Hit"))
        self.label_13.setText(_translate("MainWindow", "Ch 2 Hit"))
        self.label_15.setText(_translate("MainWindow", "Ch 1-2 Hit"))
        self.label_16.setText(_translate("MainWindow", "Ch 1-3 Hit"))
        self.label_17.setText(_translate("MainWindow", "Ch 2-3 Hit"))
        self.label_19.setText(_translate("MainWindow", "Total Dispensed"))
        self.label_11.setText(_translate("MainWindow", "Total Lost"))
        self.label_5.setText(_translate("MainWindow", "Experiment Summary"))
        self.label_10.setText(_translate("MainWindow", "Total Sorted"))
        self.label_9.setText(_translate("MainWindow", "Total Droplets"))
        self.label_18.setText(_translate("MainWindow", "Dispensing Stats"))
        self.label_20.setText(_translate("MainWindow", "Dispense Missed"))
        self.label_7.setText(_translate("MainWindow", "Ending Time"))
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_statistic),
                                         _translate("MainWindow", "Statistic"))
        self.label_21.setText(_translate("MainWindow", "Channels"))
        self.pushButton_saveplot.setText(_translate("MainWindow", "Save Plot"))
        self.label_22.setText(_translate("MainWindow", "Scaling"))
        self.radioButton_linear.setText(_translate("MainWindow", "Linear"))
        self.radioButton__logarithmic.setText(_translate("MainWindow", "Logarithmic"))
        self.label_34.setText(_translate("MainWindow", "Base"))
        self.label_23.setText(_translate("MainWindow", "Gating Threshold"))
        self.label_24.setText(_translate("MainWindow", "Gate Voltage"))
        self.label_25.setText(_translate("MainWindow", "V"))
        self.label_26.setText(_translate("MainWindow", "Percentage"))
        self.label_27.setText(_translate("MainWindow", "%"))
        self.label_28.setText(_translate("MainWindow", "Bin Width"))

        self.label_30.setText(_translate("MainWindow", "Gate Voltages"))
        self.label_31.setText(_translate("MainWindow", "X-Axis"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Green"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Far Red"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Orange"))
        self.label_32.setText(_translate("MainWindow", "Y-Axis"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Green"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Far Red"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "Orange"))
        self.label_29.setText(_translate("MainWindow", "Scatter Plot Axes"))
        self.radioButton_scatterlinear.setText(_translate("MainWindow", "Linear"))
        self.radioButton_scatterlog.setText(_translate("MainWindow", "Logarithmic"))
        self.label_33.setText(_translate("MainWindow", "Scaling"))
        self.label_35.setText(_translate("MainWindow", "Base"))
        self.label_36.setText(_translate("MainWindow", "Quadrants"))
        self.label_37.setText(_translate("MainWindow", "X Axis"))
        self.label_38.setText(_translate("MainWindow", "Y Axis"))
        self.tab_widgets_scatter.setTabText(self.tab_widgets_scatter.indexOf(self.subtab_scatter),
                                            _translate("MainWindow", "Scatter"))
        self.tab_widgets_scatter.setTabText(self.tab_widgets_scatter.indexOf(self.tab_gating),
                                         _translate("MainWindow", "Histogram"))        

        self.tab_widgets_scatter.setTabText(self.tab_widgets_scatter.indexOf(self.tab_sweep), 
                                              _translate("MainWindow", "Sweep"))          

        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_scatter),
                                         _translate("MainWindow", "Peak Height"))
        self.comboBox_option1.setItemText(0, _translate("MainWindow", "Option 1"))
        self.comboBox_option2.setItemText(0, _translate("MainWindow", "Option 2"))
        self.label_41.setText(_translate("MainWindow", "Percentage Low"))
        self.lineEdit_percentagelow1.setText(_translate("MainWindow", "0"))
        self.label_43.setText(_translate("MainWindow", "%"))
        self.label_45.setText(_translate("MainWindow", "Percentage High"))
        self.lineEdit_percentagehigh1.setText(_translate("MainWindow", "0"))
        self.label_46.setText(_translate("MainWindow", "%"))
        self.label_44.setText(_translate("MainWindow", "Percentage Low"))
        self.lineEdit_percentagelow2.setText(_translate("MainWindow", "0"))
        self.label_47.setText(_translate("MainWindow", "%"))
        self.label_42.setText(_translate("MainWindow", "Percentage High"))
        self.lineEdit_percentagehigh2.setText(_translate("MainWindow", "0"))
        self.label_48.setText(_translate("MainWindow", "%"))
        self.lineEdit_binwidth_2.setText(_translate("MainWindow", "0.1"))
        self.label_56.setText(_translate("MainWindow", "Bin Width"))
#         self.label_57
        self.label_55.setText(_translate("MainWindow", "Channels"))
        self.label_49.setText(_translate("MainWindow", "Gating Thresholds"))
        self.label_50.setText(_translate("MainWindow", "Gate Voltage Minimum"))
        self.label_61.setText(_translate("MainWindow", "Increments"))
        self.lineEdit_increments.setText(_translate("MainWindow", "0"))
        self.lineEdit_gatevoltagemaximum.setText(_translate("MainWindow", "0.5"))
        self.lineEdit_gatevoltageminimum.setText(_translate("MainWindow", "0"))
        self.label_62.setText(_translate("MainWindow", "Gate Voltage Maximum"))
        self.label_63.setText(_translate("MainWindow", "V"))
        self.label_64.setText(_translate("MainWindow", "V"))
        self.label_66.setText(_translate("MainWindow", "V"))
        self.label_68.setText(_translate("MainWindow", "Axis Limits"))
        self.lineEdit_sweepxlimits1.setText(_translate("MainWindow", "0,10"))
        self.label_71.setText(_translate("MainWindow", "Y-Limits"))
        self.label_69.setText(_translate("MainWindow", "X-Limits"))
        self.label_70.setText(_translate("MainWindow", "X-Limits"))
        self.pushButton_relimit2.setText(_translate("MainWindow", "Re-Limit"))
        self.lineEdit_sweepylimits1.setText(_translate("MainWindow", "0,10"))
        self.lineEdit_sweepylimits2.setText(_translate("MainWindow", "0,10"))
        self.pushButton_relimit1.setText(_translate("MainWindow", "Re-Limit"))
        self.label_72.setText(_translate("MainWindow", "Y-Limits"))
        self.lineEdit_sweepxlimits2.setText(_translate("MainWindow", "0,10"))
        self.pushButton_auto1.setText(_translate("MainWindow", "Auto"))
        self.pushButton_auto2.setText(_translate("MainWindow", "Auto"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.subtab_parameter), _translate("MainWindow", "Parameter"))
        self.label_39.setText(_translate("MainWindow", "Population 1"))
        self.label_40.setText(_translate("MainWindow", "Voltage"))
        self.label_51.setText(_translate("MainWindow", "Counts Above Thresh"))
        self.label_52.setText(_translate("MainWindow", "Total Events"))
        self.label_53.setText(_translate("MainWindow", "%"))
        self.label_65.setText(_translate("MainWindow", "Population 2"))
        self.label_67.setText(_translate("MainWindow", "Voltage"))
        self.label_73.setText(_translate("MainWindow", "Counts Above Thresh"))
        self.label_74.setText(_translate("MainWindow", "Total Events"))
        self.label_75.setText(_translate("MainWindow", "%"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.subtab_result), 
                                  _translate("MainWindow", "Result"))

        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_timelog),
                                         _translate("MainWindow", "Time Log"))
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_peakmax),
                                         _translate("MainWindow", "Peak Maxes Log"))
        
        self.label_82.setText(_translate("MainWindow", "Max Width"))
        self.label_84.setText(_translate("MainWindow", "Mid Points"))
        self.label_85.setText(_translate("MainWindow", "/"))
        self.button_update_2.setText(_translate("MainWindow", "Quadrants"))
        self.label_87.setText(_translate("MainWindow", "Min"))
        self.label_88.setText(_translate("MainWindow", "X-Axis"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "Green"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "Far Red"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.comboBox_5.setItemText(3, _translate("MainWindow", "Orange"))
        self.label_89.setText(_translate("MainWindow", "Y-Axis"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "Green"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "Far Red"))
        self.comboBox_6.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.comboBox_6.setItemText(3, _translate("MainWindow", "Orange"))
        self.label_90.setText(_translate("MainWindow", "Scatter Plot Axes"))
        self.label_91.setText(_translate("MainWindow", "Max"))
        self.label_95.setText(_translate("MainWindow", "Voltage Threshold (V)"))
        self.label_92.setText(_translate("MainWindow", "Green"))
        self.label_96.setText(_translate("MainWindow", "Far Red"))
        self.label_97.setText(_translate("MainWindow", "Ultra Vio"))
        self.label_98.setText(_translate("MainWindow", "Orange"))
        self.label_93.setText(_translate("MainWindow", "Quadrants")) 
        
        self.tab_widget_peak_width.setTabText(self.tab_widget_peak_width.indexOf(self.sub_tab_width_scatter), 
                                              _translate("MainWindow", "Scatter"))
        self.tab_widget_peak_width.setTabText(self.tab_widget_peak_width.indexOf(self.sub_tab_width_histogram), 
                                              _translate("MainWindow", "Histogram")) 
       
     
        
        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_peakwidth),
                                         _translate("MainWindow", "Peak Width"))
        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_report),
                                         _translate("MainWindow", "Report"))
        self.label_54.setText(_translate("MainWindow", "Channels"))
        self.pushButton_saveplot_2.setText(_translate("MainWindow", "Save Plot"))
        self.label_59.setText(_translate("MainWindow", "Peak Width Threshold"))
        self.label_60.setText(_translate("MainWindow", "Min Width"))
#         self.label_76.setText(_translate("MainWindow", "V"))
        self.label_77.setText(_translate("MainWindow", "Percentage"))
        self.label_78.setText(_translate("MainWindow", "%"))
        self.label_79.setText(_translate("MainWindow", "Bin Width"))
        self.menuFiles.setTitle(_translate("MainWindow", "Projects"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionAdd_New.setText(_translate("MainWindow", "Add New"))
        self.actionClose.setText(_translate("MainWindow", "Close"))

    def pressed(self):
        print('pressed')
        # global Ch1,Ch2,Ch3,Ch1_2,Ch1_3,Ch2_3,Locked,Raw_Time_Log,current_file_dict
        self.main_file_select = self.file_list_view.currentRow()
        self.ch1_checkbox = self.checkbox_ch1.isChecked()
        self.ch2_checkbox = self.checkbox_ch2.isChecked()
        self.ch3_checkbox = self.checkbox_ch3.isChecked()
        self.ch12_checkbox = self.checkbox_ch12.isChecked()
        self.ch13_checkbox = self.checkbox_ch13.isChecked()
        self.ch23_checkbox = self.checkbox_ch23.isChecked()
        self.all_checkbox = self.checkBox_7.isChecked()
        self.histo_channel = self.listView_channels.currentRow()
        self.histo_bins = float(self.lineEdit_binwidth.text())
        self.peak_width_channel = self.listView_channels_3.currentRow()
        self.peak_width_bins = float(self.lineEdit_binwidth_3.text())
        self.scatter_channelx = self.comboBox.currentIndex()
        self.scatter_channely = self.comboBox_2.currentIndex()
        self.width_scatter_channelx = self.comboBox_5.currentIndex()
        self.width_scatter_channely = self.comboBox_6.currentIndex()        
        
        self.sweep_channel = self.listView_channels_2.currentRow()
        self.sweep_file_1 = self.comboBox_option1.currentIndex()
        self.sweep_file_2 = self.comboBox_option2.currentIndex()
        self.sweep_bins = float(self.lineEdit_binwidth_2.text())
        self.current_file_dict = self.file_dict_list[self.main_file_select]
        self.sweep_1_dict = self.file_dict_list[self.sweep_file_1]
        self.sweep_2_dict = self.file_dict_list[self.sweep_file_2]

        os.chdir(self.current_file_dict["Root Folder"])
        # summary
        if self.current_file_dict["Summary"] != "":
            stats = Helper.Stats(self.current_file_dict["Summary"])
            self.lineEdit_startingtime.setText(stats.start_time)
            self.lineEdit_endingtime.setText(stats.end_time)
            self.lineEdit_runtime.setText(stats.total_runtime)
            self.lineEdit_totalsorted.setText(stats.total_sorted)
            self.lineEdit_totallost.setText(stats.total_lost)
            self.lineEdit_totaldispensed.setText(stats.total_dispensed)
            self.lineEdit_totaldroplets.setText(stats.total_droplets)
            self.lineEdit_dispensemissed.setText(stats.dispense_missed)
            self.lineEdit_ch1hit.setText(stats.ch1_hit)
            self.lineEdit_ch2hit.setText(stats.ch2_hit)
            self.lineEdit_ch3hit.setText(stats.ch3_hit)
            self.lineEdit_ch12hit.setText(stats.ch12_hit)
            self.lineEdit_ch13hit.setText(stats.ch13_hit)
            self.lineEdit_ch23hit.setText(stats.ch23_hit)



        # parameter
        """
        df_parameter = pd.read_csv(current_file_dict["Param"], header=None, sep='\n')
        Parameter = df_parameter[0].str.split(',', expand=True)
        
        Laser_Setting_and_Gains =  Parameter.iloc[7:11,0:3]
        Laser_Setting_and_Gains.columns = Parameter.iloc[6,0:3]
        Laser_Setting_and_Gains.index = ['1', '2', '3', '4'] 
        
        Fluidic_Settings =  Parameter.iloc[14:15,0:4]
        Fluidic_Settings.columns = Parameter.iloc[13,0:4]
        Fluidic_Settings.index = ['1']     
        
        Sorting_Parameter1 =  Parameter.iloc[18:19,0:4]
        Sorting_Parameter1.columns = Parameter.iloc[17,0:4]
        Sorting_Parameter1.index = ['1']   
        
        Sorting_Parameter2 =  Parameter.iloc[20:24,0:11]
        Sorting_Parameter2.columns = Parameter.iloc[19,0:11]
        Sorting_Parameter2.index = ['1','2','3','4']          
        
        Sorting_Parameter3 =  Parameter.iloc[25:26,0:5]
        Sorting_Parameter3.columns = Parameter.iloc[24,0:5]
        Sorting_Parameter3.index = ['1']   
        
        """
        
        #         start = time.time()
        if stats.under_sample_factor == "":
            under_sample = 1
        else:
            under_sample = stats.under_sample_factor
        
        channel = self.peak_width_channel
        width_enable = True
        
        try: self.chunksize = self.chunk_resample
        except: self.chunksize = int(1000 / float(under_sample))
            
        
        ### Qiwei's extraction code
        ### Call stats_Ch1 ~ stats_Ch23 to extract
        #         a = Analysis.file_extracted_data(current_file_dict, threshold, width_enable,channel, chunksize, 0)
        #         self.analog.update(a.analog_file)
        #         print(self.analog['200225_171057 AFB AFB Ch1 Hit.csv'][1].peak_voltage)
        ### End

        ### Qing's extraction code
        ### call Ch1list ~Ch23list to extract

            
            
            
        try: 
            if self.reset == True:
                reset = True
            else:
                reset = False
        except: reset = False
        
        threshold = [self.lineEdit_9.text(),self.lineEdit_10.text(),self.lineEdit_11.text(),self.lineEdit_12.text()]
        
        self.width_update,reanalysis = self.ui_state.peak_width_update(channel_select=self.peak_width_channel, bins=self.peak_width_bins,
                                                           peak_width_threshold = self.lineEdit_gatevoltage_2.text(),voltage_threshold = threshold )
        

        try:
            self.update = self.ui_state.working_file_update_check(file=self.main_file_select, chall=self.all_checkbox,
                                                         ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                         ch3=self.ch3_checkbox,
                                                         ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                         ch2_3=self.ch23_checkbox, reset = Ui_MainWindow.reset)
            
        except:
            self.update = self.ui_state.working_file_update_check(file=self.main_file_select, chall=self.all_checkbox,
                                                         ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                         ch3=self.ch3_checkbox,
                                                         ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                         ch2_3=self.ch23_checkbox)            
        
        self.filter_update = self.ui_state.filter_peak_update(x_axis_channel_number = int(self.comboBox_5.currentIndex()), 
                                                              y_axis_channel_number = int(self.comboBox_6.currentIndex()), 
                                                              x_axis_channel_min = float(self.lineEdit_5.text()), 
                                                              x_axis_channel_max = float(self.lineEdit_7.text()), 
                                                              y_axis_channel_min = float(self.lineEdit_6.text()), 
                                                              y_axis_channel_max = float(self.lineEdit_8.text()))
            
        
        if self.update:
            peak_enable =True
        else:
            peak_enable = False
        print("peak recalculate enable check is :",peak_enable) 
        print("resample parameter self.reset check is :",reset) 
        print("filter condition change check is :",self.filter_update) 
            
        if self.current_file_dict["Peak Record"] in self.analog and not reset :
            print("--------------------------------------------------------not reset")
            self.tab_widgets_main.currentIndex
            self.update_working_data()
            self.draw()
            self.draw_peak_width()
            self.draw_2()
            self.draw_peak_width_2()
            self.update_sweep_graphs()
            self.sweep_update_high()
            self.sweep_update_low()
            self.sweep_update()
            self.update_statistic()
            self.update_sampling_Rate()

        else:
            print("--------------------------------------------------------reset")
            a = Analysis.file_extracted_data_Qing(self.current_file_dict,threshold, width_enable, peak_enable, channel, self.chunksize,
                                                  0, stats.ch1_hit, stats.ch2_hit, stats.ch3_hit, stats.ch12_hit, stats.ch13_hit,
                                                  stats.ch23_hit, stats.total_sorted)
            

            print("data extration complete, drawing....")
            
            self.analog.update(a.analog_file)
            self.update_working_data()
            self.draw()
            self.draw_peak_width()
            self.draw_2()
            self.draw_peak_width_2()
            self.update_sweep_graphs()
            self.sweep_update_high()
            self.sweep_update_low()
            self.sweep_update()
            self.update_statistic()
            self.update_sampling_Rate()
            Ui_MainWindow.reset = False
            
            self.lineEdit_9.setText(str(a.threshold[0]))
            self.lineEdit_10.setText(str(a.threshold[1]))
            self.lineEdit_11.setText(str(a.threshold[2]))
            self.lineEdit_12.setText(str(a.threshold[3]))
            
            print("complete!")
        ### End

    def add(self):
        name, _ = QFileDialog.getOpenFileNames(self.mainwindow, 'Open File', filter="*peak*")
        for f in name:
            self.file_dict_list.append(Helper.project_namelist(f))
            self.file_list_view.addItem(f)
            self.comboBox_option1.addItem(f)
            self.comboBox_option2.addItem(f)
        for i in range(self.file_list_view.count()):
            item = self.file_list_view.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def openfolder(self):
        self.analog = {}
        self.file_list_view.clear()
        self.file_dict_list.clear()
        self.comboBox_option1.clear()
        self.comboBox_option2.clear()
        name, _ = QFileDialog.getOpenFileNames(self.mainwindow, 'Open File', filter="*peak*")
        for f in name:
            self.file_dict_list.append(Helper.project_namelist(f))
            self.file_list_view.addItem(f)
            self.comboBox_option1.addItem(f)
            self.comboBox_option2.addItem(f)
        for i in range(self.file_list_view.count()):
            item = self.file_list_view.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)





if __name__ == "__main__":
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
