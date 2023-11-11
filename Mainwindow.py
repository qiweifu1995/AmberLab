# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AmberLab_detailed2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMainWindow
from functools import partial
import pickle
import Wells
import math

from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor

from pyqtgraph.Qt import QtGui, QtCore

import pandas as pd
import os
import Helper
import Analysis
import time
from pyqtgraph import PlotWidget
import numpy as np

import pyqtgraph as pg
import statistics
from scipy.signal import savgol_filter

from multiprocessing import freeze_support

import Filter_window
import peak_threshold_window
import Time_log_selection_window
from Time_log_selection_window import Time_log_functions
from Helper import ThreadState
from enum import Enum
import logging
logging.basicConfig(format="%(message)s", level=logging.INFO)

class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
### Pop-up windows for the new filters


class Ui_MainWindow(QMainWindow):
    CHANNEL_NAME = ["488nm Green", "638nm Red", "405nm Blue", "561nm Orange", "Ch5", "Ch6"]

    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        # store everything about new filter
        self.analog = {}
        self.thresholds = []
        self.tree_dic = {}
        # StandardItem class created at very top, it combines the brach font and color in to one-line-code
        # 0, is the parent brach above all
        # 0,0 is the 0 child brach which has a 0, parent
        self.tree_dic[(0,)] = {}
        self.tree_dic[(0,)]['tree_standarditem'] = StandardItem('Create graph', 12, set_bold=True)
        self.file_dict_list = []
        self.sweep_1_data = []
        self.working_data = []
        self.current_file_dict = {}
        self.ui_state = Helper.ui_state()
        self.version_number = "2.0"
        self.thread = []
        self.time_log_file_model = QStandardItemModel()
        self.time_log_file_indexes = []
        # extraction thread holds the threads created for each file
        self.extraction_thread_state = []
        # extraction queue holds the index of threads to get extracted
        self.extraction_queue = []
        self.well_checkbox_queue = []
        self.setupUi()


    def setupUi(self):

        ### GUI setup
        self.setWindowTitle("AuraLab Analysis Suite Ver. " + self.version_number)
        self.setObjectName("MainWindow")
        self.resize(1500, 900)
        self.setMinimumSize(QtCore.QSize(150, 150))
        self.setMaximumSize(QtCore.QSize(16777215, 16777215))

        ### main tab setup
        self.centralwidget = QtWidgets.QWidget(self)
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

        self.layout_progress_bar = QtWidgets.QVBoxLayout()
        self.layout_progress_bar.setObjectName("layout_progress_bar")
        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setMaximumSize(250,40)
        self.layout_progress_bar.addWidget(self.progress_label)
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setValue(0)
        self.layout_progress_bar.addWidget(self.pbar)
        self.layout_vertical_filecontrol.addLayout(self.layout_progress_bar)


        spacerItem = QtWidgets.QSpacerItem(120, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout_vertical_filecontrol.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        #self.layout_vertical_filecontrol.addWidget(self.line_2)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        #self.layout_vertical_filecontrol.addWidget(self.label)
        self.layout_horizontal_checkbox = QtWidgets.QHBoxLayout()
        self.layout_horizontal_checkbox.setObjectName("layout_horizontal_checkbox")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        #self.layout_horizontal_checkbox.addItem(spacerItem1)
        self.layout_vertical_checkbox = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox.setObjectName("layout_vertical_checkbox")
        self.checkbox_ch1 = QtWidgets.QCheckBox()
        self.checkbox_ch1.setObjectName("checkbox_ch1")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch1)
        self.checkbox_ch2 = QtWidgets.QCheckBox()
        self.checkbox_ch2.setObjectName("checkbox_ch2")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch2)
        self.checkbox_ch3 = QtWidgets.QCheckBox()
        self.checkbox_ch3.setObjectName("checkbox_ch3")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch3)
        self.checkbox_ch12 = QtWidgets.QCheckBox()
        self.checkbox_ch12.setObjectName("checkbox_ch12")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch12)
        self.checkbox_ch13 = QtWidgets.QCheckBox()
        self.checkbox_ch13.setObjectName("checkbox_ch13")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch13)
        self.checkbox_ch23 = QtWidgets.QCheckBox()
        self.checkbox_ch23.setObjectName("checkbox_ch23")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_ch23)

        self.checkbox_Droplet_Record = QtWidgets.QCheckBox()
        self.checkbox_Droplet_Record.setObjectName("checkbox_Droplet_Record")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_Droplet_Record)

        self.checkbox_Locked_Out_Peaks = QtWidgets.QCheckBox()
        self.checkbox_Locked_Out_Peaks.setObjectName("checkbox_Locked_Out_Peaks")
        #self.layout_vertical_checkbox.addWidget(self.checkbox_Locked_Out_Peaks)

        self.checkBox_7 = QtWidgets.QCheckBox()
        self.checkBox_7.setObjectName("checkBox_7")
        #self.layout_vertical_checkbox.addWidget(self.checkBox_7)
        self.layout_horizontal_checkbox.addLayout(self.layout_vertical_checkbox)
        self.layout_vertical_filecontrol.addLayout(self.layout_horizontal_checkbox)
        self.layout_horizontal_update = QtWidgets.QHBoxLayout()
        self.layout_horizontal_update.setObjectName("layout_horizontal_update")
        self.button_update = QtWidgets.QPushButton(self.centralwidget)
        self.button_update.setMinimumSize(QtCore.QSize(50, 0))
        self.button_update.setMaximumSize(QtCore.QSize(100, 16777215))
        self.button_update.setObjectName("button_update")
        self.layout_horizontal_update.addWidget(self.button_update)
        self.button_extract_all = QtWidgets.QPushButton("Extract All")
        self.button_extract_all.setMinimumSize(QtCore.QSize(50, 0))
        self.button_extract_all.setMaximumSize(QtCore.QSize(100, 16777215))
        self.layout_horizontal_update.addWidget(self.button_extract_all)
        self.layout_vertical_filecontrol.addLayout(self.layout_horizontal_update)
        spacerItem2 = QtWidgets.QSpacerItem(120, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.layout_vertical_filecontrol.addItem(spacerItem2)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.layout_vertical_filecontrol.addWidget(self.line_3)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

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
        self.tableView_statistic.setRowCount(6)
        self.tableView_statistic.setHorizontalHeaderLabels(['Mean', 'Median', 'Standard Deviation', 'Min', 'Max'])
        self.tableView_statistic.setVerticalHeaderLabels(self.CHANNEL_NAME)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_12, 1, 0, 1, 1)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_14, 1, 2, 1, 1)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_13, 1, 1, 1, 1)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_16, 2, 0, 1, 1)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_17, 2, 1, 1, 1)
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
        self.gridLayout_3.addLayout(self.horizontalLayout_18, 2, 2, 1, 1)
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

        self.horizontalLayout_ch_4_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_4_hit.setObjectName("horizontalLayout_ch_4_hit")
        self.label_ch_4_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_4_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_4_hit.setSizePolicy(sizePolicy)
        self.label_ch_4_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_4_hit.setObjectName("label_ch_4_hit")
        self.horizontalLayout_ch_4_hit.addWidget(self.label_ch_4_hit)
        self.lineEdit_ch4_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch4_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch4_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch4_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch4_hit.setObjectName("lineEdit_ch4_hit")
        self.horizontalLayout_ch_4_hit.addWidget(self.lineEdit_ch4_hit)
        spacerItem_ch4_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_4_hit.addItem(spacerItem_ch4_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_4_hit, 3, 0, 1, 1)

        self.horizontalLayout_ch_14_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_14_hit.setObjectName("horizontalLayout_ch_14_hit")
        self.label_ch_14_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_14_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_14_hit.setSizePolicy(sizePolicy)
        self.label_ch_14_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_14_hit.setObjectName("label_ch_14_hit")
        self.horizontalLayout_ch_14_hit.addWidget(self.label_ch_14_hit)
        self.lineEdit_ch_14_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_14_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_14_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_14_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_14_hit.setObjectName("lineEdit_ch_14_hit")
        self.horizontalLayout_ch_14_hit.addWidget(self.lineEdit_ch_14_hit)
        spacerItem_ch_14_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                    QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_14_hit.addItem(spacerItem_ch_14_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_14_hit, 3, 1, 1, 1)

        self.horizontalLayout_ch_24_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_24_hit.setObjectName("horizontalLayout_ch_24_hit")
        self.label_ch_24_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_24_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_24_hit.setSizePolicy(sizePolicy)
        self.label_ch_24_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_24_hit.setObjectName("label_ch_24_hit")
        self.horizontalLayout_ch_24_hit.addWidget(self.label_ch_24_hit)
        self.lineEdit_ch_24_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_24_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_24_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_24_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_24_hit.setObjectName("lineEdit_ch_24_hit")
        self.horizontalLayout_ch_24_hit.addWidget(self.lineEdit_ch_24_hit)
        spacerItem_ch_24_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_24_hit.addItem(spacerItem_ch_24_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_24_hit, 3, 2, 1, 1)

        self.horizontalLayout_ch_34_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_34_hit.setObjectName("horizontalLayout_ch_34_hit")
        self.label_ch_34_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_34_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_34_hit.setSizePolicy(sizePolicy)
        self.label_ch_34_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_34_hit.setObjectName("label_ch_34_hit")
        self.horizontalLayout_ch_34_hit.addWidget(self.label_ch_34_hit)
        self.lineEdit_ch_34_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_34_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_34_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_34_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_34_hit.setObjectName("lineEdit_ch_34_hit")
        self.horizontalLayout_ch_34_hit.addWidget(self.lineEdit_ch_34_hit)
        spacerItem_ch_34_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_34_hit.addItem(spacerItem_ch_34_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_34_hit, 4, 0, 1, 1)

        self.horizontalLayout_ch_123_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_123_hit.setObjectName("horizontalLayout_ch_123_hit")
        self.label_ch_123_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_123_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_123_hit.setSizePolicy(sizePolicy)
        self.label_ch_123_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_123_hit.setObjectName("label_ch_123_hit")
        self.horizontalLayout_ch_123_hit.addWidget(self.label_ch_123_hit)
        self.lineEdit_ch_123_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_123_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_123_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_123_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_123_hit.setObjectName("lineEdit_ch_123_hit")
        self.horizontalLayout_ch_123_hit.addWidget(self.lineEdit_ch_123_hit)
        spacerItem_ch_123_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                     QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_123_hit.addItem(spacerItem_ch_123_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_123_hit, 4, 1, 1, 1)

        self.horizontalLayout_ch_124_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_124_hit.setObjectName("horizontalLayout_ch_124_hit")
        self.label_ch_124_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_124_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_124_hit.setSizePolicy(sizePolicy)
        self.label_ch_124_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_124_hit.setObjectName("label_ch_124_hit")
        self.horizontalLayout_ch_124_hit.addWidget(self.label_ch_124_hit)
        self.lineEdit_ch_124_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_124_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_124_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_124_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_124_hit.setObjectName("lineEdit_ch_124_hit")
        self.horizontalLayout_ch_124_hit.addWidget(self.lineEdit_ch_124_hit)
        spacerItem_ch_124_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_124_hit.addItem(spacerItem_ch_124_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_124_hit, 4, 2, 1, 1)

        self.horizontalLayout_ch_134_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_134_hit.setObjectName("horizontalLayout_ch_134_hit")
        self.label_ch_134_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_134_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_134_hit.setSizePolicy(sizePolicy)
        self.label_ch_134_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_134_hit.setObjectName("label_ch_134_hit")
        self.horizontalLayout_ch_134_hit.addWidget(self.label_ch_134_hit)
        self.lineEdit_ch_134_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_134_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_134_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_134_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_134_hit.setObjectName("lineEdit_ch_134_hit")
        self.horizontalLayout_ch_134_hit.addWidget(self.lineEdit_ch_134_hit)
        spacerItem_ch_134_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_134_hit.addItem(spacerItem_ch_134_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_134_hit, 5, 0, 1, 1)

        self.horizontalLayout_ch_234_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_234_hit.setObjectName("horizontalLayout_ch_234_hit")
        self.label_ch_234_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_234_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_234_hit.setSizePolicy(sizePolicy)
        self.label_ch_234_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_234_hit.setObjectName("label_ch_234_hit")
        self.horizontalLayout_ch_234_hit.addWidget(self.label_ch_234_hit)
        self.lineEdit_ch_234_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_234_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_234_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_234_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_234_hit.setObjectName("lineEdit_ch_234_hit")
        self.horizontalLayout_ch_234_hit.addWidget(self.lineEdit_ch_234_hit)
        spacerItem_ch_234_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_234_hit.addItem(spacerItem_ch_234_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_234_hit, 5, 1, 1, 1)

        self.horizontalLayout_ch_1234_hit = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ch_1234_hit.setObjectName("horizontalLayout_ch_1234_hit")
        self.label_ch_1234_hit = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ch_1234_hit.sizePolicy().hasHeightForWidth())
        self.label_ch_1234_hit.setSizePolicy(sizePolicy)
        self.label_ch_1234_hit.setMinimumSize(QtCore.QSize(80, 0))
        self.label_ch_1234_hit.setObjectName("label_ch_1234_hit")
        self.horizontalLayout_ch_1234_hit.addWidget(self.label_ch_1234_hit)
        self.lineEdit_ch_1234_hit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch_1234_hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_ch_1234_hit.setSizePolicy(sizePolicy)
        self.lineEdit_ch_1234_hit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_ch_1234_hit.setObjectName("lineEdit_ch_1234_hit")
        self.horizontalLayout_ch_1234_hit.addWidget(self.lineEdit_ch_1234_hit)
        spacerItem_ch_1234_hit = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_ch_1234_hit.addItem(spacerItem_ch_1234_hit)
        self.gridLayout_3.addLayout(self.horizontalLayout_ch_1234_hit, 5, 2, 1, 1)

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

        self.horizontalLayout_out_of_range_droplet = QtWidgets.QHBoxLayout()
        self.horizontalLayout_out_of_range_droplet.setObjectName("horizontalLayout_out_of_range_droplet")
        self.horizontalLayout_out_of_range_droplet.setContentsMargins(0, 0, -1, -1)
        self.label_out_of_range_droplet = QtWidgets.QLabel(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_out_of_range_droplet.sizePolicy().hasHeightForWidth())
        self.label_out_of_range_droplet.setSizePolicy(sizePolicy)
        self.label_out_of_range_droplet.setMinimumSize(QtCore.QSize(80, 0))
        self.label_out_of_range_droplet.setObjectName("label_out_of_range_droplet")
        self.horizontalLayout_out_of_range_droplet.addWidget(self.label_out_of_range_droplet)
        self.lineEdit_out_of_range_droplet = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_out_of_range_droplet.sizePolicy().hasHeightForWidth())
        self.lineEdit_out_of_range_droplet.setSizePolicy(sizePolicy)
        self.lineEdit_out_of_range_droplet.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_out_of_range_droplet.setObjectName("lineEdit_out_of_range_droplet")
        self.horizontalLayout_out_of_range_droplet.addWidget(self.lineEdit_out_of_range_droplet)
        spacerItem_out_of_range_droplet = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_out_of_range_droplet.addItem(spacerItem_out_of_range_droplet)
        self.gridLayout_3.addLayout(self.horizontalLayout_out_of_range_droplet, 0, 0, 1, 1)



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

        #### subtab peak linear graph
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_150 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_150.setObjectName("horizontalLayout_150")
        self.verticalLayout_51 = QtWidgets.QVBoxLayout()
        self.verticalLayout_51.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_51.setObjectName("verticalLayout_51")
        self.gridLayout_41 = QtWidgets.QGridLayout()
        self.gridLayout_41.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_41.setObjectName("gridLayout_41")
        self.label_271 = QtWidgets.QLabel(self.tab_3)
        self.label_271.setAlignment(QtCore.Qt.AlignCenter)
        self.label_271.setObjectName("label_271")
        self.gridLayout_41.addWidget(self.label_271, 0, 0, 1, 2)
        self.label_273 = QtWidgets.QLabel(self.tab_3)
        self.label_273.setAlignment(QtCore.Qt.AlignCenter)
        self.label_273.setObjectName("label_273")
        self.gridLayout_41.addWidget(self.label_273, 7, 0, 1, 2)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_41.addWidget(self.pushButton_5, 8, 0, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_41.addWidget(self.pushButton_3, 12, 0, 1, 2)
        self.label_270 = QtWidgets.QLabel(self.tab_3)
        self.label_270.setAlignment(QtCore.Qt.AlignCenter)
        self.label_270.setObjectName("label_270")
        self.gridLayout_41.addWidget(self.label_270, 3, 0, 1, 1)
        self.label_272 = QtWidgets.QLabel(self.tab_3)
        self.label_272.setAlignment(QtCore.Qt.AlignCenter)
        self.label_272.setObjectName("label_272")
        self.gridLayout_41.addWidget(self.label_272, 5, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_41.addWidget(self.pushButton_4, 11, 0, 1, 2)
        self.lineEdit_32 = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_32.sizePolicy().hasHeightForWidth())
        self.lineEdit_32.setSizePolicy(sizePolicy)
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.gridLayout_41.addWidget(self.lineEdit_32, 3, 1, 1, 1)

        self.lineEdit_35 = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_35.sizePolicy().hasHeightForWidth())
        self.lineEdit_35.setSizePolicy(sizePolicy)
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.gridLayout_41.addWidget(self.lineEdit_35, 6, 1, 1, 1)

        self.label_278 = QtWidgets.QLabel(self.tab_3)
        self.label_278.setAlignment(QtCore.Qt.AlignCenter)
        self.label_278.setObjectName("label_278")
        self.gridLayout_41.addWidget(self.label_278, 6, 0, 1, 1)

        self.comboBox_13 = QtWidgets.QComboBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_13.sizePolicy().hasHeightForWidth())
        self.comboBox_13.setSizePolicy(sizePolicy)
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("Ch1 ")
        self.comboBox_13.addItem("Ch2 ")
        self.comboBox_13.addItem("Ch3 ")
        self.comboBox_13.addItem("Ch1-2")
        self.comboBox_13.addItem("Ch1-3")
        self.comboBox_13.addItem("Ch2-3")
        self.comboBox_13.addItem("Droplet Record")
        self.comboBox_13.addItem("Locked Out Peaks")
        self.comboBox_13.addItem("Peak Record")

        self.gridLayout_41.addWidget(self.comboBox_13, 1, 0, 1, 2)
        self.lineEdit_31 = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_31.sizePolicy().hasHeightForWidth())
        self.lineEdit_31.setSizePolicy(sizePolicy)
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.gridLayout_41.addWidget(self.lineEdit_31, 5, 1, 1, 1)

        self.lineEdit_32.setText("0")
        self.lineEdit_31.setText("15")
        self.lineEdit_35.setText("0")

        self.layout_vertical_checkbox_2 = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox_2.setObjectName("layout_vertical_checkbox_2")

        self.channel_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_1.setObjectName("self.channel_1")

        self.channel_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_2.setObjectName("self.channel_2")

        self.channel_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_3.setObjectName("self.channel_3")

        self.channel_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_4.setObjectName("self.channel_4")

        self.channel_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_5.setObjectName("self.channel_5")

        self.channel_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.channel_6.setObjectName("self.channel_6")

        self.layout_vertical_checkbox_2.addWidget(self.channel_1)
        self.layout_vertical_checkbox_2.addWidget(self.channel_2)
        self.layout_vertical_checkbox_2.addWidget(self.channel_3)
        self.layout_vertical_checkbox_2.addWidget(self.channel_4)
        self.layout_vertical_checkbox_2.addWidget(self.channel_5)
        self.layout_vertical_checkbox_2.addWidget(self.channel_6)

        self.channel_1.setChecked(True)
        self.channel_2.setChecked(True)
        self.channel_3.setChecked(True)
        self.channel_4.setChecked(True)
        self.channel_5.setChecked(True)
        self.channel_6.setChecked(True)

        self.gridLayout_41.addItem(self.layout_vertical_checkbox_2, 14, 0, 1, 2)

        self.label_277 = QtWidgets.QLabel(self.tab_3)
        self.label_277.setAlignment(QtCore.Qt.AlignCenter)
        self.label_277.setObjectName("label_277")
        self.gridLayout_41.addWidget(self.label_277, 15, 0, 1, 2)

        self.Smooth_enable = QtWidgets.QCheckBox(self.tab_3)
        self.Smooth_enable.setObjectName("Smooth_enable")
        self.gridLayout_41.addWidget(self.Smooth_enable, 16, 0, 1, 2)

        self.lineEdit_33 = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_33.sizePolicy().hasHeightForWidth())
        self.lineEdit_33.setSizePolicy(sizePolicy)
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.gridLayout_41.addWidget(self.lineEdit_33, 17, 1, 1, 1)

        self.lineEdit_34 = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_34.sizePolicy().hasHeightForWidth())
        self.lineEdit_34.setSizePolicy(sizePolicy)
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.gridLayout_41.addWidget(self.lineEdit_34, 18, 1, 1, 1)

        self.lineEdit_33.setText("7")
        self.lineEdit_34.setText("29")

        self.label_275 = QtWidgets.QLabel(self.tab_3)
        self.label_275.setAlignment(QtCore.Qt.AlignCenter)
        self.label_275.setObjectName("label_275")
        self.gridLayout_41.addWidget(self.label_275, 17, 0, 1, 1)
        self.label_276 = QtWidgets.QLabel(self.tab_3)
        self.label_276.setAlignment(QtCore.Qt.AlignCenter)
        self.label_276.setObjectName("label_276")
        self.gridLayout_41.addWidget(self.label_276, 18, 0, 1, 1)

        spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_41.addItem(spacerItem26, 13, 0, 1, 2)

        spacerItem25 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_41.addItem(spacerItem25, 9, 0, 1, 2)
        self.label_274 = QtWidgets.QLabel(self.tab_3)
        self.label_274.setAlignment(QtCore.Qt.AlignCenter)
        self.label_274.setObjectName("label_274")
        self.gridLayout_41.addWidget(self.label_274, 10, 0, 1, 2)
        self.verticalLayout_51.addLayout(self.gridLayout_41)
        spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_51.addItem(spacerItem26)
        self.horizontalLayout_150.addLayout(self.verticalLayout_51)
        self.line_100 = QtWidgets.QFrame(self.tab_3)
        self.line_100.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_100.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_100.setObjectName("line_100")
        self.horizontalLayout_150.addWidget(self.line_100)

        self.widget_28 = PlotWidget(self.tab_3)

        #         self.widget_28 = QtWidgets.QWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)

        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_28.sizePolicy().hasHeightForWidth())
        self.widget_28.setSizePolicy(sizePolicy)
        self.widget_28.setMinimumSize(QtCore.QSize(500, 500))
        self.widget_28.setObjectName("widget_28")
        self.horizontalLayout_150.addWidget(self.widget_28)

        styles = {"color": "r", "font-size": "20px"}
        self.widget_28.setLabel('left', 'Height', **styles)
        self.widget_28.setBackground('w')

        self.tab_widgets_main.addTab(self.tab_3, "")

        self.treeView = QtWidgets.QTreeView()

        self.layout_vertical_filecontrol.addWidget(self.treeView)

        self.filter_button_layout = QtWidgets.QHBoxLayout()
        self.filter_add_button = QtWidgets.QPushButton("Add")
        self.filter_remove_button = QtWidgets.QPushButton("Remove")
        self.filter_button_layout.addWidget(self.filter_add_button)
        self.filter_button_layout.addWidget(self.filter_remove_button)

        self.layout_vertical_filecontrol.addLayout(self.filter_button_layout)

        # original treeview is has a colomn like header, need to hide that 
        self.treeView.setHeaderHidden(True)

        # setup a model for the braches
        self.treeModel = QStandardItemModel()

        # disable double clike expand option, double clike now link to the open filter window
        self.treeView.setExpandsOnDoubleClick(False)



        # to create a child , call the parent, append the color and font to it
        # to create the very first parent, call the model its self
        self.treeModel.appendRow(self.tree_dic[(0,)]['tree_standarditem'])

        # create a test child branch
        # self.tree_dic[(0,0)] = {}
        # self.tree_dic[(0,0)]['tree_standarditem'] = StandardItem('test branch', 10, set_bold=True)

        # to create a child , call the parent, append the color and font to it
        # self.tree_dic[(0,)]['tree_standarditem'].appendRow(self.tree_dic[(0,0)]['tree_standarditem'])

        # default tree_index
        self.tree_index = (0,)

        # self.dialog = Filter_window.window_filter(ui)
        # self.tree_dic[(0,)]['tree_windowfilter'] = self.dialog

        self.treeView.setModel(self.treeModel)
        self.treeView.expandAll()
        self.treeView.doubleClicked.connect(self.getValue)

        #### polygon linear end

        ###### subtab sweep
        self.tab_sweep = QtWidgets.QWidget()
        self.tab_sweep.setObjectName("tab_sweep")
        #         self.tab_sweep = QtWidgets.QWidget()
        #         self.tab_sweep.setObjectName("tab_sweep")

        self.tab_widgets_main.addTab(self.tab_sweep, "")

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
        for ch in self.CHANNEL_NAME:
            self.comboBox_option1.addItem(ch)

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
        self.widget_sweepparam2.setLabel('bottom', 'Signal(V)', **styles)
        self.widget_sweepparam2.setTitle("")
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
        self.widget_sweepparam1.setLabel('bottom', 'Signal(V)', **styles)
        self.widget_sweepparam1.setTitle("")
        self.widget_sweepparam1.setBackground('w')
        self.widget_sweepparam1.setXRange(1, 10.5, padding=0)
        self.widget_sweepparam1.setYRange(1, 10.5, padding=0)

        self.horizontalLayout_44.addWidget(self.widget_sweepparam2)

        ### sweep end

        #         self.verticalLayout_4 = QtWidgets.QVBoxLayout(tab_subgating)
        #         self.verticalLayout_4.setObjectName("verticalLayout_4")
        #         self.tab_widgets_scatter = QtWidgets.QTabWidget(self.tab_scatter)
        #         self.tab_widgets_scatter.setObjectName("tab_widgets_scatter")

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
        for ch in self.CHANNEL_NAME:
            self.comboBox_option2.addItem(ch)

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

        # self.label_55 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_55.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        # self.label_55.setObjectName("label_55")
        # self.gridLayout_9.addWidget(self.label_55, 0, 0, 1, 1)
        # self.listView_channels_2 = QtWidgets.QListWidget(self.subtab_parameter)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.listView_channels_2.sizePolicy().hasHeightForWidth())
        # self.listView_channels_2.setSizePolicy(sizePolicy)
        # self.listView_channels_2.setMinimumSize(QtCore.QSize(20, 20))
        # self.listView_channels_2.setObjectName("listView_channels_2")
        # self.listView_channels_2.addItem("Green")
        # self.listView_channels_2.addItem("Red")
        # self.listView_channels_2.addItem("Blue")
        # self.listView_channels_2.addItem("Orange")
        # self.gridLayout_9.addWidget(self.listView_channels_2, 0, 1, 1, 1)
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
        # self.label_50 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_50.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        # self.label_50.setObjectName("label_50")
        # self.gridLayout_7.addWidget(self.label_50, 0, 0, 1, 1)
        # self.label_61 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_61.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        # self.label_61.setObjectName("label_61")
        # self.gridLayout_7.addWidget(self.label_61, 2, 0, 1, 1)
        # self.lineEdit_increments = QtWidgets.QLineEdit(self.subtab_parameter)
        # self.lineEdit_increments.setObjectName("lineEdit_increments")
        # self.gridLayout_7.addWidget(self.lineEdit_increments, 2, 1, 1, 1)
        # self.lineEdit_gatevoltagemaximum = QtWidgets.QLineEdit(self.subtab_parameter)
        # self.lineEdit_gatevoltagemaximum.setObjectName("lineEdit_gatevoltagemaximum")
        # self.gridLayout_7.addWidget(self.lineEdit_gatevoltagemaximum, 1, 1, 1, 1)
        # self.lineEdit_gatevoltageminimum = QtWidgets.QLineEdit(self.subtab_parameter)
        # self.lineEdit_gatevoltageminimum.setObjectName("lineEdit_gatevoltageminimum")
        # self.gridLayout_7.addWidget(self.lineEdit_gatevoltageminimum, 0, 1, 1, 1)
        # self.label_62 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_62.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        # self.label_62.setObjectName("label_62")
        # self.gridLayout_7.addWidget(self.label_62, 1, 0, 1, 1)
        # self.label_63 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_63.setObjectName("label_63")
        # self.gridLayout_7.addWidget(self.label_63, 0, 2, 1, 1)
        # self.label_64 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_64.setObjectName("label_64")
        # self.gridLayout_7.addWidget(self.label_64, 1, 2, 1, 1)
        # self.label_66 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_66.setObjectName("label_66")
        # self.gridLayout_7.addWidget(self.label_66, 2, 2, 1, 1)

        # self.lineEdit_binwidth_2 = QtWidgets.QLineEdit()
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.lineEdit_binwidth_2.sizePolicy().hasHeightForWidth())
        # self.lineEdit_binwidth_2.setSizePolicy(sizePolicy)
        # self.lineEdit_binwidth_2.setObjectName("lineEdit_binwidth_2")
        # self.gridLayout_7.addWidget(self.lineEdit_binwidth_2, 3, 1, 1, 1)
        # self.label_56 = QtWidgets.QLabel(self.subtab_parameter)
        # self.label_56.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        # self.label_56.setObjectName("label_56")
        # self.gridLayout_7.addWidget(self.label_56, 3, 0, 1, 1)

        self.verticalLayout_gatingthresholds.addLayout(self.gridLayout_7)
        self.horizontalLayout_48.addLayout(self.verticalLayout_gatingthresholds)
        self.line_30 = QtWidgets.QFrame(self.subtab_parameter)
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")

        self.verticalLayout_axislimits = QtWidgets.QVBoxLayout()
        self.verticalLayout_axislimits.setObjectName("verticalLayout_axislimits")
        self.sweep_h_layout = QtWidgets.QHBoxLayout()
        self.label_sweep1 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sweep1.sizePolicy().hasHeightForWidth())
        self.label_sweep1.setSizePolicy(sizePolicy)
        self.label_sweep1.setMinimumSize(QtCore.QSize(0, 40))
        self.label_sweep1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sweep1.setObjectName("label_sweep1")
        self.label_sweep2 = QtWidgets.QLabel(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sweep2.sizePolicy().hasHeightForWidth())
        self.label_sweep2.setSizePolicy(sizePolicy)
        self.label_sweep2.setMinimumSize(QtCore.QSize(0, 40))
        self.label_sweep2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sweep2.setObjectName("label_sweep2")
        self.sweep_h_layout.addWidget(self.label_sweep1)
        self.sweep_h_layout.addWidget(self.label_sweep2)
        self.verticalLayout_axislimits.addLayout(self.sweep_h_layout)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setContentsMargins(-1, 10, -1, 10)
        self.gridLayout_8.setVerticalSpacing(20)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_sweepxlimits1 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepxlimits1.setObjectName("lineEdit_sweepxlimits1")
        self.gridLayout_8.addWidget(self.lineEdit_sweepxlimits1, 0, 1, 1, 1)
        self.label_71 = QtWidgets.QLabel("End Voltage")
        self.gridLayout_8.addWidget(self.label_71, 1, 0, 1, 1)
        self.label_69 = QtWidgets.QLabel("Start Voltage")
        self.label_69.setObjectName("label_69")
        self.gridLayout_8.addWidget(self.label_69, 0, 0, 1, 1)

        self.label_70 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_70.setObjectName("label_70")
        self.gridLayout_8.addWidget(self.label_70, 0, 3, 1, 1)
        self.label_increment2 = QtWidgets.QLabel("Sweep Increment")
        self.label_bin1 = QtWidgets.QLabel("Bin Size")
        self.gridLayout_8.addWidget(self.label_bin1, 3, 0, 1, 1)
        self.lineEdit_increment2 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_increment2.sizePolicy().hasHeightForWidth())
        self.lineEdit_increment2.setSizePolicy(sizePolicy)
        self.lineEdit_increment2.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_increment2.setObjectName("lineEdit_increment2")
        self.gridLayout_8.addWidget(self.lineEdit_increment2, 2, 4, 1, 1)
        self.gridLayout_8.addWidget(self.label_increment2, 2, 3, 1, 1)
        self.lineEdit_sweepylimits1 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepylimits1.setObjectName("lineEdit_sweepylimits1")
        self.gridLayout_8.addWidget(self.lineEdit_sweepylimits1, 1, 1, 1, 1)
        self.lineEdit_sweepylimits2 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepylimits2.setObjectName("lineEdit_sweepylimits2")
        self.gridLayout_8.addWidget(self.lineEdit_sweepylimits2, 1, 4, 1, 1)
        self.label_increment1 = QtWidgets.QLabel("Sweep Increment")
        self.lineEdit_increment1 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_increment1.sizePolicy().hasHeightForWidth())
        self.lineEdit_increment1.setSizePolicy(sizePolicy)
        self.lineEdit_increment1.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_increment1.setObjectName("lineEdit_increment1")
        self.gridLayout_8.addWidget(self.label_increment1, 2, 0, 1, 1)
        self.gridLayout_8.addWidget(self.lineEdit_increment1, 2, 1, 1, 1)
        self.label_72 = QtWidgets.QLabel(self.subtab_parameter)
        self.label_72.setObjectName("label_72")
        self.gridLayout_8.addWidget(self.label_72, 1, 3, 1, 1)
        self.lineEdit_sweepxlimits2 = QtWidgets.QLineEdit(self.subtab_parameter)
        self.lineEdit_sweepxlimits2.setObjectName("lineEdit_sweepxlimits2")
        self.gridLayout_8.addWidget(self.lineEdit_sweepxlimits2, 0, 4, 1, 1)
        self.lineEdit_bin1 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_bin1.sizePolicy().hasHeightForWidth())
        self.lineEdit_bin1.setSizePolicy(sizePolicy)
        self.lineEdit_bin1.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_bin1.setObjectName("lineEdit_bin1")
        self.gridLayout_8.addWidget(self.lineEdit_bin1, 3, 1, 1, 1)
        self.label_bin2 = QtWidgets.QLabel("Bin Size")
        self.lineEdit_bin2 = QtWidgets.QLineEdit(self.subtab_parameter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_bin2.sizePolicy().hasHeightForWidth())
        self.lineEdit_bin2.setSizePolicy(sizePolicy)
        self.lineEdit_bin2.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_bin2.setObjectName("lineEdit_bin2")
        self.gridLayout_8.addWidget(self.lineEdit_bin2, 3, 4, 1, 1)
        self.gridLayout_8.addWidget(self.label_bin2, 3, 3, 1, 1)
        self.verticalLayout_axislimits.addLayout(self.gridLayout_8)

        self.horizontalLayout_48.addLayout(self.verticalLayout_axislimits)
        self.horizontalLayout_48.addWidget(self.line_30)
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

        self.time_log_tab_init()

        self.dispense_mapping_tab_init()


        # report tab

        self.tab_report = QtWidgets.QWidget()
        self.tab_report.setObjectName("tab_report")

        self.horizontalLayout_report_tab = QtWidgets.QHBoxLayout(self.tab_report)
        self.horizontalLayout_report_tab.setObjectName("horizontalLayout_report_tab")

        self.textEdit = QtWidgets.QTextEdit(self.tab_report)
        self.textEdit.setObjectName("textEdit")

        self.horizontalLayout_report_tab.addWidget(self.textEdit)
        self.tab_widgets_main.addTab(self.tab_report, "")

        self.textbox = "Current version: AuraLab V1.23" + "\n" + "you can find logs here:"
        self.textEdit.setPlainText(self.textbox)

        ### tab end

        self.horizontalLayout_4.addWidget(self.tab_widgets_main)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_4)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 22))
        self.menubar.setObjectName("menubar")
        self.menuFiles = QtWidgets.QMenu(self.menubar)
        self.menuFiles.setObjectName("menuFiles")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionImport = QtWidgets.QAction(self)
        self.actionImport.setObjectName("actionImport")
        self.actionAdd_New = QtWidgets.QAction(self)
        self.actionAdd_New.setObjectName("actionAdd_New")
        self.actionMapping = QtWidgets.QAction("Load Dispense Mapping")
        self.actionClose = QtWidgets.QAction(self)
        self.actionClose.setObjectName("actionClose")
        self.menuFiles.addAction(self.actionImport)
        self.menuFiles.addAction(self.actionAdd_New)
        self.menuFiles.addAction(self.actionMapping)

        # save project
        self.actionAdd_Save = QtWidgets.QAction(self)
        self.actionAdd_Save.setObjectName("actionAdd_Save")
        self.actionAdd_Load = QtWidgets.QAction(self)
        self.actionAdd_Load.setObjectName("actionAdd_Load")

        self.menuFiles.addAction(self.actionAdd_Save)
        self.menuFiles.addAction(self.actionAdd_Load)

        # save single file
        self.actionAdd_SaveSingleFile = QtWidgets.QAction(self)
        self.actionAdd_SaveSingleFile.setObjectName("actionAdd_SaveSingleFile")

        self.menuFiles.addAction(self.actionAdd_SaveSingleFile)

        # save parameters
        self.actionAdd_SaveParameters = QtWidgets.QAction(self)
        self.actionAdd_SaveParameters.setObjectName("actionAdd_SaveParameters")
        self.actionAdd_LoadParameters = QtWidgets.QAction(self)
        self.actionAdd_LoadParameters.setObjectName("actionAdd_LoadParameters")

        self.menuFiles.addAction(self.actionAdd_SaveParameters)
        self.menuFiles.addAction(self.actionAdd_LoadParameters)

        #         self.menuFiles.addAction(self.Save)
        self.menuFiles.addAction(self.actionClose)
        self.menubar.addAction(self.menuFiles.menuAction())

        # list of all connected functions
        self.actionImport.triggered.connect(self.openfolder)
        self.actionAdd_New.triggered.connect(self.add)

        self.button_update.clicked.connect(self.pressed)
        self.button_extract_all.clicked.connect(self.extract_all_clicked)
        #self.button_update_2.clicked.connect(self.filter_width_table)
        self.pushButton_5.clicked.connect(self.reset_linear_plot)
        self.pushButton_4.clicked.connect(self.last_page)
        self.pushButton_3.clicked.connect(self.next_page)

        # self.lineEdit_gatevoltagemaximum.textChanged.connect(self.sweep_update)
        # self.lineEdit_gatevoltageminimum.textChanged.connect(self.sweep_update)
        # self.lineEdit_increments.textChanged.connect(self.sweep_update)

        self.retranslateUi()

        self.tab_widgets_main.setCurrentIndex(0)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        # self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        # self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)
        pen = pg.mkPen(color='r', width=5, style=QtCore.Qt.DashLine)
        self.sweep1_low_line = pg.InfiniteLine(0, movable=False, pen=pen)
        self.sweep1_high_line = pg.InfiniteLine(0, movable=False, pen=pen)
        self.sweep2_low_line = pg.InfiniteLine(0, movable=False, pen=pen)
        self.sweep2_high_line = pg.InfiniteLine(0, movable=False, pen=pen)

        self.lineEdit_sweepxlimits1.editingFinished.connect(self.sweep_update_low_1)
        self.lineEdit_sweepxlimits2.editingFinished.connect(self.sweep_update_low_2)
        self.lineEdit_sweepylimits1.editingFinished.connect(self.sweep_update_high_1)
        self.lineEdit_sweepylimits2.editingFinished.connect(self.sweep_update_high_2)
        self.lineEdit_sweepxlimits1.editingFinished.connect(self.sweep_update_line)
        self.lineEdit_sweepxlimits2.editingFinished.connect(self.sweep_update_line)
        self.lineEdit_sweepylimits1.editingFinished.connect(self.sweep_update_line)
        self.lineEdit_sweepylimits2.editingFinished.connect(self.sweep_update_line)

        self.lineEdit_sweepxlimits1.editingFinished.connect(self.sweep_update)
        self.lineEdit_sweepxlimits2.editingFinished.connect(self.sweep_update)
        self.lineEdit_sweepylimits1.editingFinished.connect(self.sweep_update)
        self.lineEdit_sweepylimits2.editingFinished.connect(self.sweep_update)
        self.lineEdit_increment1.editingFinished.connect(self.sweep_update)
        self.lineEdit_increment2.editingFinished.connect(self.sweep_update)

        self.lineEdit_bin1.editingFinished.connect(self.update_sweep_graphs)
        self.lineEdit_bin2.editingFinished.connect(self.update_sweep_graphs)


        # self.lineEdit_binwidth_2.editingFinished.connect(self.update_sweep_graphs)
        #
        # self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        # self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)

        self.channel_1.stateChanged.connect(self.linear_plot)
        self.channel_2.stateChanged.connect(self.linear_plot)
        self.channel_3.stateChanged.connect(self.linear_plot)
        self.channel_4.stateChanged.connect(self.linear_plot)
        self.channel_5.stateChanged.connect(self.linear_plot)
        self.channel_6.stateChanged.connect(self.linear_plot)

        self.recalculate_peak_dataset = True
        self.comboBox_option1.currentIndexChanged.connect(self.sweep_1_index_changed)
        self.comboBox_option2.currentIndexChanged.connect(self.sweep_2_index_changed)

        self.w = peak_threshold_window.ThresholdWindow()
        self.w.threshold_set.connect(self.threshold_set)
        self.w.apply_all_set.connect(self.threshold_apply_all)
        self.pushButton_resample.clicked.connect(self.openWindow)

        self.actionAdd_Save.triggered.connect(self.save)
        self.actionAdd_Load.triggered.connect(self.load)
        self.actionMapping.triggered.connect(self.open_dispense_folder)

        # triggers for the log, havn't update adter new filter window function included.

        self.checkbox_ch1.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 1 state changed to ",
                                         afterchange=self.checkbox_ch1.isChecked()))
        self.checkbox_ch2.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 2 state changed to ",
                                         afterchange=self.checkbox_ch2.isChecked()))
        self.checkbox_ch3.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 3 state changed to ",
                                         afterchange=self.checkbox_ch3.isChecked()))
        self.checkbox_ch12.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 1-2 state changed to ",
                                         afterchange=self.checkbox_ch12.isChecked()))
        self.checkbox_ch13.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 1-3 state changed to ",
                                         afterchange=self.checkbox_ch13.isChecked()))
        self.checkbox_ch23.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Channel 2-3 state changed to ",
                                         afterchange=self.checkbox_ch23.isChecked()))
        self.checkbox_Droplet_Record.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Droplet_Record state changed to ",
                                         afterchange=self.checkbox_Droplet_Record.isChecked()))
        self.checkbox_Locked_Out_Peaks.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox Locked Out Peaks state changed to ",
                                         afterchange=self.checkbox_Locked_Out_Peaks.isChecked()))
        self.checkBox_7.stateChanged.connect(
            lambda: self.textbox_trigger(change="checkbox All Channel state changed to ",
                                         afterchange=self.checkBox_7.isChecked()))

        self.channel_1.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_1 state changed to ",
                                         afterchange=self.channel_1.isChecked()))
        self.channel_2.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_2 state changed to ",
                                         afterchange=self.channel_2.isChecked()))
        self.channel_3.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_3 state changed to ",
                                         afterchange=self.channel_3.isChecked()))
        self.channel_4.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_4 state changed to ",
                                         afterchange=self.channel_4.isChecked()))
        self.channel_5.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_5 state changed to ",
                                         afterchange=self.channel_5.isChecked()))
        self.channel_6.stateChanged.connect(
            lambda: self.textbox_trigger(change="Raw data viewer channel_6 state changed to ",
                                         afterchange=self.channel_6.isChecked()))



        # listview trigger
        # self.listView_channels_2.currentItemChanged.connect(
        #     lambda: self.textbox_trigger(change="Sweept channel selection changed to ",
        #                                  afterchange=self.listView_channels_2.currentItem().text()))

        self.file_list_view.currentItemChanged.connect(lambda: self.textbox_trigger(change="loading file changed to ",
                                                                                    afterchange=self.file_list_view.currentItem().text()))

        # self.lineEdit_gatevoltagemaximum.textChanged.connect(
        #     lambda: self.textbox_trigger(change="Sweep gating threshold voltage maximum changed to ",
        #                                  afterchange=self.lineEdit_gatevoltagemaximum.text()))
        # self.lineEdit_gatevoltageminimum.textChanged.connect(
        #     lambda: self.textbox_trigger(change="Sweep gating threshold voltage minimum change to ",
        #                                  afterchange=self.lineEdit_gatevoltageminimum.text()))
        # self.lineEdit_increments.textChanged.connect(
        #     lambda: self.textbox_trigger(change="Sweep gating threshold increments changed to ",
        #                                  afterchange=self.lineEdit_increments.text()))
        #
        # self.lineEdit_binwidth_2.textChanged.connect(
        #     lambda: self.textbox_trigger(change="Sweep tab bin width changed to ",
        #                                  afterchange=self.lineEdit_binwidth_2.text()))

        self.file_list_view.itemChanged.connect(self.chart_title_change)
        self.file_list_view.currentRowChanged.connect(self.threshold_fetch)

    def dispense_mapping_tab_init(self):
        """this method contains all the QT UI components for the mapping """
        self.tab_peakmax = QtWidgets.QWidget()
        self.tab_peakmax.setObjectName("tab_peakmax")
        self.tab_widgets_main.addTab(self.tab_peakmax, "")

        h_divider_line = QtWidgets.QFrame()
        h_divider_line.setFrameShape(QtWidgets.QFrame.HLine)
        h_divider_line.setFrameShadow(QtWidgets.QFrame.Sunken)

        #main vertical layout
        top_horizontal_layout = QtWidgets.QHBoxLayout()
        main_vertical_layout = QtWidgets.QVBoxLayout()
        self.well_plots_layout = QtWidgets.QGridLayout()
        self.well_plots = [[] for i in range(8)]
        for i in range (8):
            plot = PlotWidget()
            styles = {'color': 'r', 'font-size': '12px'}
            self.well_plots[i] = PlotWidget(background="w")
            self.well_plots[i].setLabel('left', 'Voltage', **styles)
            self.well_plots[i].setLabel('bottom', 'Samples', **styles)
            legend = self.well_plots[i].addLegend(offset=(1, 1), verSpacing=-20)
            self.well_plots[i].showGrid(x=True, y=True)

            if i < 4:
                self.well_plots_layout.addWidget(self.well_plots[i], 0, i, 1, 1)
            else:
                self.well_plots_layout.addWidget(self.well_plots[i], 1, i-4, 1, 1)

        top_horizontal_layout.addLayout(self.well_plots_layout)
        spacerItem_3 = QtWidgets.QSpacerItem(0, 2000, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        top_horizontal_layout.addItem(spacerItem_3)
        main_vertical_layout.addLayout(top_horizontal_layout)
        main_vertical_layout.addWidget(h_divider_line)
        spacerItem = QtWidgets.QSpacerItem(5, 200, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        bottom_horizontal_layout = QtWidgets.QHBoxLayout()
        bottom_horizontal_layout.addSpacerItem(spacerItem)
        main_vertical_layout.addLayout(bottom_horizontal_layout)

        self.col_buttons = [QtWidgets.QPushButton(str(i+1)) for i in range(12)]
        v_labels = [chr(i) for i in range(65, 73)]
        self.well_selector_layout = QtWidgets.QGridLayout()

        for i in range(12):
            self.well_selector_layout.addWidget(self.col_buttons[i], 0, i+1, 1, 1)
            self.col_buttons[i].setFixedSize(QtCore.QSize(20, 20))
            self.col_buttons[i].setCheckable(True)
            self.col_buttons[i].clicked.connect(self.col_button_clicked)
        for i in range(8):
            self.well_selector_layout.addWidget(QtWidgets.QLabel(v_labels[i]), i+1, 0, 1, 1)

        self.well_selector_checkboxes = []
        for i in range(12):
            self.well_selector_checkboxes.append([])
            for j in range(8):
                self.well_selector_checkboxes[i].append(WellsCheckBox(i,j))
                self.well_selector_layout.addWidget(self.well_selector_checkboxes[i][j], j+1, i+1, 1, 1)
                self.well_selector_checkboxes[i][j].stateChanged.connect(self.well_clicked)

        bottom_horizontal_layout.addLayout(self.well_selector_layout)

        self.well_left_button = QtWidgets.QToolButton()
        self.well_left_button.setArrowType(QtCore.Qt.LeftArrow)
        self.well_right_button = QtWidgets.QToolButton()
        self.well_right_button.setArrowType(QtCore.Qt.RightArrow)

        self.plate_combobox = QtWidgets.QComboBox()
        self.well_selector_layout.addWidget(self.well_left_button, 9, 0, 1, 1)
        self.well_selector_layout.addWidget(self.plate_combobox, 9, 1, 1, 11)
        self.well_selector_layout.addWidget(self.well_right_button, 9, 12, 1, 1)


        V_divider_line = QtWidgets.QFrame()
        V_divider_line.setFrameShape(QtWidgets.QFrame.VLine)
        V_divider_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        spacerItem2 = QtWidgets.QSpacerItem(2000, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        bottom_horizontal_layout.addWidget(V_divider_line)

        options_layout = QtWidgets.QFormLayout()
        self.radio_group = QtWidgets.QGroupBox()
        group_v_layout = QtWidgets.QVBoxLayout()
        self.radiobutton_200 = QtWidgets.QRadioButton("200 Sample Size")
        self.radiobutton_200.setChecked(True)
        self.radiobutton_1000 = QtWidgets.QRadioButton("1000 Sample Size")
        group_divider_line = QtWidgets.QFrame()
        group_divider_line.setFrameShape(QtWidgets.QFrame.HLine)
        group_divider_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        group_v_layout.addWidget(self.radiobutton_200)
        group_v_layout.addWidget(self.radiobutton_1000)
        self.radio_group.setLayout(group_v_layout)
        options_layout.addRow("File Format:", self.radio_group)

        self.radio_group_2 = QtWidgets.QGroupBox()
        group_v_layout_2 = QtWidgets.QVBoxLayout()
        self.radiobutton_96 = QtWidgets.QRadioButton("96 Wells Mode")
        self.radiobutton_96.setChecked(True)
        self.radiobutton_48 = QtWidgets.QRadioButton("48 Wells Mode")
        group_v_layout_2.addWidget(self.radiobutton_96)
        group_v_layout_2.addWidget(self.radiobutton_48)
        self.radio_group_2.setLayout(group_v_layout_2)
        options_layout.addRow("Wells Mode:", self.radio_group_2)

        group_divider_line = QtWidgets.QFrame()
        group_divider_line.setFrameShape(QtWidgets.QFrame.VLine)
        group_divider_line.setFrameShadow(QtWidgets.QFrame.Sunken)


        options_layout_2 = QtWidgets.QFormLayout()
        self.name_option = QtWidgets.QLabel("Legends Channel Names Setting: ")
        self.green_name = QtWidgets.QLineEdit()
        self.red_name = QtWidgets.QLineEdit()
        self.blue_name = QtWidgets.QLineEdit()
        self.orange_name = QtWidgets.QLineEdit()
        options_layout_2.addRow(self.name_option)
        options_layout_2.addRow("488nm Channel Name: ", self.green_name)
        options_layout_2.addRow("638nm Channel Name: ", self.red_name)
        options_layout_2.addRow("405nm Channel Name: ", self.blue_name)
        options_layout_2.addRow("561nm Channel Name: ", self.orange_name)

        bottom_horizontal_layout.addLayout(options_layout)
        bottom_horizontal_layout.addWidget(group_divider_line)
        bottom_horizontal_layout.addLayout(options_layout_2)
        bottom_horizontal_layout.addItem(spacerItem2)

        self.plate_combobox.currentIndexChanged.connect(self.plate_update)
        self.well_left_button.clicked.connect(self.plate_left_button_clicked)
        self.well_right_button.clicked.connect(self.plate_right_button_clicked)

        self.tab_peakmax.setLayout(main_vertical_layout)







    def time_log_tab_init(self):
        """the function which contains all the Qt UI components for the time log tab"""
        font = QFont('Open Sans', 14)
        font.setBold(True)

        self.tab_timelog = QtWidgets.QWidget()
        self.tab_timelog.setObjectName("tab_timelog")

        # the layout that will hold both the top and bottom plot
        main_vertical_layout = QtWidgets.QVBoxLayout()
        main_vertical_layout.setObjectName("main_layout")

        # the horizontal layout for the top half of the widget
        top_horizontal_layout = QtWidgets.QHBoxLayout()
        top_horizontal_layout.setObjectName("top_horizontal_layout")

        # the top left vertical layout that holds the mode combo box and file selector
        top_left_v_layout = QtWidgets.QVBoxLayout()
        top_left_v_layout.setObjectName("top_vertical_layout")

        self.log_label_top = QtWidgets.QLabel("Time Log Viewer 1")
        self.log_label_top.setFont(font)
        main_vertical_layout.addWidget(self.log_label_top)

        # init top combo box for log
        self.comboBox_top_log = QtWidgets.QComboBox(self.tab_timelog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_option2.sizePolicy().hasHeightForWidth())
        self.comboBox_top_log.setSizePolicy(sizePolicy)
        self.comboBox_top_log.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox_top_log.addItem("Total Sorted Positives")
        self.comboBox_top_log.addItem("Total Lost Positives")
        self.comboBox_top_log.addItem("Total Droplets")
        self.comboBox_top_log.addItem("Positive Rate")
        self.comboBox_top_log.addItem("Droplet Frequency")
        self.comboBox_top_log.addItem("Sorted Rate")
        self.comboBox_top_log.addItem("Locked Out Frequency")
        top_left_v_layout.addWidget(self.comboBox_top_log)

        # init top file selector for log
        self.log_file_select_top = QtWidgets.QTreeView(self.tab_timelog)
        self.log_file_select_top.setObjectName("log_file_select_top")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.log_file_select_top.setSizePolicy(sizePolicy)
        self.log_file_select_top.setMinimumSize(QtCore.QSize(100, 100))
        self.log_file_select_top.setMaximumSize(QtCore.QSize(200, 400))
        self.log_file_select_top.setHeaderHidden(True)
        self.log_file_select_top.setModel(self.time_log_file_model)
        self.log_file_select_top.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        top_left_v_layout.addWidget(self.log_file_select_top)

        # layout to hold the two buttons
        top_left_button_layout = QtWidgets.QHBoxLayout()
        top_left_button_layout.setObjectName("top_left_button_layout")

        self.time_log_add_button_1 = QtWidgets.QPushButton("Add Syringe")
        self.time_log_remove_button_1 = QtWidgets.QPushButton("Remove")
        top_left_button_layout.addWidget(self.time_log_add_button_1)
        top_left_button_layout.addWidget(self.time_log_remove_button_1)
        top_left_v_layout.addLayout(top_left_button_layout)

        top_horizontal_layout.addLayout(top_left_v_layout)

        #adding the line divider
        self.line_top_vertical = QtWidgets.QFrame(self.subtab_result)
        self.line_top_vertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_top_vertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_top_vertical.setObjectName("line_top_vertical")
        top_horizontal_layout.addWidget(self.line_top_vertical)

        #adding the tip graph
        self.time_log_graph_top = PlotWidget(self.tab_timelog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.time_log_graph_top.setSizePolicy(sizePolicy)
        self.time_log_graph_top.setMinimumSize(QtCore.QSize(400, 350))
        self.time_log_graph_top.setObjectName("time_log_graph_top")
        self.time_log_graph_top.setBackground('w')
        top_horizontal_layout.addWidget(self.time_log_graph_top)
        main_vertical_layout.addLayout(top_horizontal_layout)

        # line divider between top and bottom plot
        self.line_horizontal = QtWidgets.QFrame(self.subtab_result)
        self.line_horizontal.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horizontal.setObjectName("line_horizontal")
        main_vertical_layout.addWidget(self.line_horizontal)

        self.log_label_bot = QtWidgets.QLabel("Time Log Viewer 2")
        self.log_label_bot.setFont(font)
        main_vertical_layout.addWidget(self.log_label_bot)

        # the horizontal layout for the bottom half of the widget
        bottom_horizontal_layout = QtWidgets.QHBoxLayout()
        bottom_horizontal_layout.setObjectName("top_horizontal_layout")

        # the bottom left vertical layout that holds the mode combo box and file selector
        bottom_left_v_layout = QtWidgets.QVBoxLayout()
        bottom_left_v_layout.setObjectName("top_vertical_layout")

        # init bottom combo box for log
        self.comboBox_bot_log = QtWidgets.QComboBox(self.tab_timelog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_option2.sizePolicy().hasHeightForWidth())
        self.comboBox_bot_log.setSizePolicy(sizePolicy)
        self.comboBox_bot_log.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox_bot_log.addItem("Total Sorted Positives")
        self.comboBox_bot_log.addItem("Total Lost Positives")
        self.comboBox_bot_log.addItem("Total Droplets")
        self.comboBox_bot_log.addItem("Positive Rate")
        self.comboBox_bot_log.addItem("Droplet Frequency")
        self.comboBox_bot_log.addItem("Sorted Rate")
        self.comboBox_bot_log.addItem("Locked Out Frequency")
        bottom_left_v_layout.addWidget(self.comboBox_bot_log)

        # init bottom file selector for log
        self.log_file_select_bot = QtWidgets.QTreeView(self.tab_timelog)
        self.log_file_select_bot.setObjectName("log_file_select_bot")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.log_file_select_bot.setSizePolicy(sizePolicy)
        self.log_file_select_bot.setMinimumSize(QtCore.QSize(100, 100))
        self.log_file_select_bot.setMaximumSize(QtCore.QSize(200, 400))
        self.log_file_select_bot.setHeaderHidden(True)
        self.log_file_select_bot.setModel(self.time_log_file_model)
        self.log_file_select_bot.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        bottom_left_v_layout.addWidget(self.log_file_select_bot)
        bottom_horizontal_layout.addLayout(bottom_left_v_layout)
        # layout to hold the two buttons
        bottom_left_button_layout = QtWidgets.QHBoxLayout()
        bottom_left_button_layout.setObjectName("bottom_left_button_layout")

        self.time_log_add_button_2 = QtWidgets.QPushButton("Add Syringe")
        self.time_log_remove_button_2 = QtWidgets.QPushButton("Remove")
        bottom_left_button_layout.addWidget(self.time_log_add_button_2)
        bottom_left_button_layout.addWidget(self.time_log_remove_button_2)
        bottom_left_v_layout.addLayout(bottom_left_button_layout)

        # adding the line divider
        self.line_bot_vertical = QtWidgets.QFrame(self.subtab_result)
        self.line_bot_vertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_bot_vertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_bot_vertical.setObjectName("line_bot_vertical")
        bottom_horizontal_layout.addWidget(self.line_bot_vertical)

        # adding the bottom graph
        self.time_log_graph_bot = PlotWidget(self.tab_timelog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.time_log_graph_bot.setSizePolicy(sizePolicy)
        self.time_log_graph_bot.setMinimumSize(QtCore.QSize(400, 350))
        self.time_log_graph_bot.setObjectName("time_log_graph_bot")
        self.time_log_graph_bot.setBackground('w')
        bottom_horizontal_layout.addWidget(self.time_log_graph_bot)
        main_vertical_layout.addLayout(bottom_horizontal_layout)

        # line divider between top and bottom plot
        self.line_horizontal_2 = QtWidgets.QFrame(self.subtab_result)
        self.line_horizontal_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horizontal_2.setObjectName("line_horizontal")
        main_vertical_layout.addWidget(self.line_horizontal_2)

        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        main_vertical_layout.addItem(spacerItem)

        self.tab_timelog.setLayout(main_vertical_layout)

        self.tab_widgets_main.addTab(self.tab_timelog, "")

        self.time_log_add_button_1.clicked.connect(self.time_log_add_syringe)
        self.time_log_add_button_2.clicked.connect(self.time_log_add_syringe)
        self.time_log_remove_button_1.clicked.connect(self.time_log_remove_item_top)
        self.time_log_remove_button_2.clicked.connect(self.time_log_remove_item_bot)
        self.log_file_select_top.clicked.connect(self.time_log_top_clicked)
        self.log_file_select_bot.clicked.connect(self.time_log_bot_clicked)
        self.comboBox_top_log.currentIndexChanged.connect(self.time_log_combo_box_clicked_top)
        self.comboBox_bot_log.currentIndexChanged.connect(self.time_log_combo_box_clicked_bot)
        self.filter_remove_button.clicked.connect(self.filter_remove_item)
        self.filter_add_button.clicked.connect(self.filter_add_syringe)


    def filter_add_syringe(self):
        """function for handing add button click for filter addition"""
        self.time_log_window.caller = 0
        self.tree_index = (len([key for key in self.tree_dic.keys() if len(key) == 1]),)
        self.time_log_window.populate_list()
        self.time_log_window.show()
        self.time_log_window.activateWindow()

    def time_log_add_syringe(self):
        """function for handling add button click event for time log function"""
        self.time_log_window.caller = 1
        self.time_log_window.populate_list()
        self.time_log_window.show()
        self.time_log_window.activateWindow()

    def filter_remove_item(self):
        """function for removing created filter"""
        # fetch the currently selected filter index, this is the specific index used by filter window
        index = self.treeView.selectedIndexes()[0]
        self.tree_index = (index.row(),)
        while index.parent().row() != -1:
            self.tree_index += (index.parent().row(),)
            index = index.parent()
        print("selected item to delete: " + str(self.tree_index))

        # access the parent node of the selected item, then delete the indexed child row
        if len(self.tree_index) > 1:
            self.tree_dic[self.tree_index[1:]]['tree_standarditem'].removeRow(self.tree_index[0])
        else:
            self.treeModel.removeRow(self.tree_index[0])

        # need to delete all child filter from the dictionary, check for all keys that has the same proceeding index
        keys = [key for key in self.tree_dic.keys() if len(key) > len(self.tree_index)]
        print("Keys with longer length" + str(keys))
        for key in keys:
            # find the starting index location
            starting_index = len(key) - len(self.tree_index)
            if self.tree_index == key[starting_index:]:
                # remove all dictionary entry with the same starting index
                self.tree_dic.pop(key)
        # need to find other sibling filter, move them up to the deleted filter and update their own index
        while self.tree_index in self.tree_dic.keys():
            self.tree_dic.pop(self.tree_index)
            child_index = self.tree_index[0] + 1
            next_index = (child_index,) + self.tree_index[1:]
            # check if index exist for sibling filter with lower index, if so replace and repeat
            if next_index in self.tree_dic.keys():
                self.tree_dic[self.tree_index] = self.tree_dic[next_index]
                self.tree_dic[self.tree_index]['tree_windowfilter'].tree_index_update(self.tree_index)
                # extract all the key that have longer index, thus all possible child should be in this list
                keys = [key for key in self.tree_dic.keys() if len(key) > len(next_index)]
                print("Children Keys with longer length" + str(keys))
                # check all the lower level keys for child nodes
                for key in keys:
                    # find the starting index location
                    starting_index = len(key) - len(next_index)
                    if next_index == key[starting_index:]:
                        # remove all dictionary entry with the same starting index
                        new_key = key[:starting_index] + self.tree_index
                        old_key = key[:starting_index] + next_index
                        self.tree_dic[new_key] = self.tree_dic.pop(old_key)
                        # update the buildin index of each window
                        self.tree_dic[new_key]['tree_windowfilter'].tree_index_update(new_key)
                self.tree_index = next_index
            else:
                self.tree_index = next_index
        print(self.tree_index)
        print(self.tree_dic.keys())

    def time_log_top_clicked(self):
        """handles top syringe select when clicked"""
        index = self.log_file_select_top.selectedIndexes()
        self.time_log_window.time_log_process_data(index, 0)
        self.time_log_window.data_transform(0, Time_log_functions(self.comboBox_top_log.currentIndex()))

    def time_log_bot_clicked(self):
        """handles bot syringe select when clicked"""
        index = self.log_file_select_bot.selectedIndexes()
        self.time_log_window.time_log_process_data(index, 1)
        self.time_log_window.data_transform(1, Time_log_functions(self.comboBox_bot_log.currentIndex()))

    def time_log_combo_box_clicked_top(self):
        """handle when top function of log changes"""
        self.time_log_window.data_transform(0, Time_log_functions(self.comboBox_top_log.currentIndex()))

    def time_log_combo_box_clicked_bot(self):
        """handle when bot function of log changes"""
        self.time_log_window.data_transform(1, Time_log_functions(self.comboBox_bot_log.currentIndex()))

    def time_log_remove_item_top(self):
        """function for handling removing item, calls the time log class"""
        try:
            #fetch the index of the selected file, need to idnex [0] since the items are returned in a list
            index = self.log_file_select_top.selectedIndexes()[0]
            print(index.row())
            print(index.parent().row())
            self.time_log_window.remove_item([index.parent().row(), index.row()])
            self.log_file_select_top.clearSelection()
        except IndexError:
            print("No file selected")

    def time_log_remove_item_bot(self):
        """function for handling removing item, calls the time log class"""
        try:
            index = self.log_file_select_bot.selectedIndexes()[0]
            print(index.row())
            print(index.parent().row())
            self.time_log_window.remove_item([index.parent().row(), index.row()])
            self.log_file_select_bot.clearSelection()
        except IndexError:
            print("No file selected")


    def threshold_set(self):
        """function handling when user finished inputing a voltage"""
        print(self.w.thresholds)
        threshold_holder = self.w.thresholds.copy()
        self.listWidget_sampingrate.clear()
        self.listWidget_sampingrate.addItem("Green: " + str(round(threshold_holder[0], 3)) + "V")
        self.listWidget_sampingrate.addItem("Red: " + str(round(threshold_holder[1], 3)) + "V")
        self.listWidget_sampingrate.addItem("Blue: " + str(round(threshold_holder[2], 3)) + "V")
        self.listWidget_sampingrate.addItem("Orange: " + str(round(threshold_holder[3], 3)) + "V")
        try:
            self.thresholds[self.file_list_view.currentRow()] = threshold_holder
        except (IndexError, AttributeError):
            print("File does not exist")
            return
        print(self.thresholds)

    def threshold_apply_all(self):
        """function handling when user click set all """
        print(self.w.thresholds)
        threshold_holder = self.w.thresholds.copy()
        self.listWidget_sampingrate.clear()
        self.listWidget_sampingrate.addItem("Green: " + str(round(threshold_holder[0], 3)) + "V")
        self.listWidget_sampingrate.addItem("Red: " + str(round(threshold_holder[1], 3)) + "V")
        self.listWidget_sampingrate.addItem("Blue: " + str(round(threshold_holder[2], 3)) + "V")
        self.listWidget_sampingrate.addItem("Orange: " + str(round(threshold_holder[3], 3)) + "V")
        try:
            for i in range(self.file_list_view.count()):
                self.thresholds[i] = threshold_holder
        except (IndexError, AttributeError):
            print("File does not exist")
            return
        print(self.thresholds)

    def threshold_fetch(self):
        """this function is called when user clicks on a different file, fetch that files's thesholds"""
        try:
            threshold_holder = self.thresholds[self.file_list_view.currentRow()].copy()
        except (IndexError, AttributeError):
            print("File Not Exist")
            return
        self.w.import_threshold(threshold_holder)
        self.listWidget_sampingrate.clear()
        self.listWidget_sampingrate.addItem("Green: " + str(round(threshold_holder[0], 3)) + "V")
        self.listWidget_sampingrate.addItem("Red: " + str(round(threshold_holder[1], 3)) + "V")
        self.listWidget_sampingrate.addItem("Blue: " + str(round(threshold_holder[2], 3)) + "V")
        self.listWidget_sampingrate.addItem("Orange: " + str(round(threshold_holder[3], 3)) + "V")


    # ###  window filter
    def getValue(self, val):
        # current selected row is val
        current_branch = val
        # find out the index
        self.tree_index = (val.row(),)

        while current_branch.parent().row() != -1:
            self.tree_index += (current_branch.parent().row(),)
            current_branch = current_branch.parent()

        # open the branch
        self.tree_dic[self.tree_index]['tree_windowfilter'].show()
        self.tree_dic[self.tree_index]['tree_windowfilter'].showNormal()
        self.tree_dic[self.tree_index]['tree_windowfilter'].activateWindow()

    def get_selected_filter(self, val):
        return
    ###  window filter ends

    def chart_title_change(self):
        if self.file_list_view.currentItem():
            change = self.file_list_view.currentItem().text()
        else:
            self.file_list_view.setCurrentRow(0)
            change = self.file_list_view.currentItem().text()

        if len(str(change)) > 30:
            change = str(change)[0:30]


        self.widget_28.setTitle(str(change), color="b", size="10pt")


    #         = PlotWidget(self.tab_gating)

    def textbox_trigger(self, change, afterchange):
        # record change in the log
        self.textbox = self.textbox + "\n" + str(change) + str(afterchange)

        self.textEdit.setPlainText(self.textbox)
        # done

    def reset_linear_plot(self):
        self.linear_plot()
        self.widget_28.autoRange()

    def last_page(self):
        lower_bond = int(self.lineEdit_32.text())
        upper_bond = int(self.lineEdit_31.text())
        nrows = upper_bond - lower_bond

        self.lineEdit_32.setText(str(lower_bond - nrows))
        self.lineEdit_31.setText(str(upper_bond - nrows))

        self.linear_plot()

    def next_page(self):
        lower_bond = int(self.lineEdit_32.text())
        upper_bond = int(self.lineEdit_31.text())
        nrows = upper_bond - lower_bond

        self.lineEdit_32.setText(str(lower_bond + nrows))
        self.lineEdit_31.setText(str(upper_bond + nrows))

        self.linear_plot()

    def linear_plot(self):

        self.widget_28.clear()
        text1 = self.comboBox_13.currentText()
        header = 0
        try:
            if int(self.lineEdit_35.text()) > 0:
                sample_size = int(self.lineEdit_35.text())
                if text1 == "Peak Record":
                    header = 2
                print(sample_size)
            else:
                sample_size = 100
                if text1 == "Peak Record":
                    header = 2
                    sample_size = 200
                    print(sample_size)
        except:
            sample_size = 200
            if text1 == "Peak Record":
                header = 2
                sample_size = 200
                print(sample_size)

        lower_bond = int(self.lineEdit_32.text())
        upper_bond = int(self.lineEdit_31.text())
        nrows = upper_bond - lower_bond
        if nrows > 15:
            self.lineEdit_31.setText(str(lower_bond + 15))
            nrows = 15

        self.main_file_select = self.file_list_view.currentRow()
        self.polygon_file_dict = self.file_dict_list[self.main_file_select]
        os.chdir(self.polygon_file_dict["Root Folder"])
        file = self.polygon_file_dict[text1]

        data = pd.read_csv(file, skiprows=sample_size * lower_bond, nrows=sample_size * nrows, header=header)
        length = len(data.columns)

        data.columns = list(range(0, length))

        height_data = data[0].values.tolist()
        height_index = list(range(len(height_data)))

        poly_degree = int(self.lineEdit_33.text())
        window_length = int(self.lineEdit_34.text()) // 2 * 2 - 1
        self.widget_28.addLegend()

        for i in range(0, sample_size * nrows, sample_size):
            self.widget_28.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))

        #                     self.data_line_y = self.graphWidget.plot([1, 1], [0, 1],
        #                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))

        if self.Smooth_enable.isChecked():
            if self.channel_1.isChecked():
                height_data = savgol_filter(data[0], window_length, poly_degree)
                pen = pg.mkPen(color=(83, 229, 29), width=2)
                self.widget_28.plot(height_index, height_data, name='Channel_1', pen=pen, symbol='o', symbolSize=0,
                                    symbolBrush=('m'))
            if self.channel_2.isChecked():
                height_data = savgol_filter(data[1], window_length, poly_degree)
                pen = pg.mkPen(color=(238, 17, 47), width=2)
                self.widget_28.plot(height_index, height_data, name='Channel_2', pen=pen, symbol='o', symbolSize=0,
                                    symbolBrush=('m'))
            if self.channel_3.isChecked():
                height_data = savgol_filter(data[2], window_length, poly_degree)
                pen = pg.mkPen(color=(48, 131, 240), width=2)
                self.widget_28.plot(height_index, height_data, name='Channel_3', pen=pen, symbol='o', symbolSize=0,
                                    symbolBrush=('m'))
            if self.channel_4.isChecked():
                height_data = savgol_filter(data[3], window_length, poly_degree)
                pen = pg.mkPen(color=(238, 134, 30), width=2)
                self.widget_28.plot(height_index, height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0,
                                    symbolBrush=('m'))
        else:
            if self.channel_1.isChecked():
                pen = pg.mkPen(color=(83, 229, 29), width=2)
                self.widget_28.plot(height_index, data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o',
                                    symbolSize=0, symbolBrush=('m'))
            if self.channel_2.isChecked():
                pen = pg.mkPen(color=(238, 17, 47), width=2)
                self.widget_28.plot(height_index, data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o',
                                    symbolSize=0, symbolBrush=('m'))
            if self.channel_3.isChecked():
                pen = pg.mkPen(color=(48, 131, 240), width=2)
                self.widget_28.plot(height_index, data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o',
                                    symbolSize=0, symbolBrush=('m'))
            if self.channel_4.isChecked():
                pen = pg.mkPen(color=(238, 134, 30), width=2)
                self.widget_28.plot(height_index, data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o',
                                    symbolSize=0, symbolBrush=('m'))

    def openWindow(self):
        self.w.show()

    def update_working_data(self):
        #         try: print("Ui_self.reset:", Ui_self.reset)
        #         except : print("Ui_self.reset: FALSE")

        print('self.update', self.update)
        if self.update:
            self.peak_width_working_data = []
            self.peak_num_working_data = []
            for i in range(4):
                self.peak_width_working_data.append([])
                self.peak_num_working_data.append([])

            if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1 ']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch1 ']][2][i]
            if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch2 ']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch2 ']][2][i]
            if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch3 ']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch3 ']][2][i]
            if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1-2']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch1-2']][2][i]
            if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch1-3']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch1-3']][2][i]
            if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Ch2-3']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Ch2-3']][2][i]
            if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict[
                'Droplet Record'] in self.analog.keys():
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Droplet Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Droplet Record']][2][i]
            if self.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict[
                'Locked Out Peaks'] in self.analog.keys():
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Locked Out Peaks']][2][i]
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Peak Record']][2][i]

            if len(self.peak_width_working_data) == 0:
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Peak Record']][2][i]


        if self.update:
            self.working_data = []
            self.filtered_working_data = []
            self.filtered_peak_num_working_data = []
            for i in range(4):
                self.working_data.append([])
                self.filtered_working_data.append([])
                self.filtered_peak_num_working_data.append([])

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

            if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict[
                'Droplet Record'] in self.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Droplet Record']][0][i]

            if self.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict[
                'Locked Out Peaks'] in self.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Locked Out Peaks']][0][i]

            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]

            if len(self.working_data) == 0:
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]

            ### filter data by using min and max width
        """
        if self.filtered_working_data[3] == [] or self.filtered_working_data[2] == []:
            self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0])]
            self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1])]
            self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2])]
            self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3])]
            self.filtered_working_data[0] = self.working_data[0]
            self.filtered_working_data[1] = self.working_data[1]
            self.filtered_working_data[2] = self.working_data[2]
            self.filtered_working_data[3] = self.working_data[3]
            self.filtered_peak_num_working_data = self.peak_num_working_data.copy()
        """
        print("0,self.recalculate_peak_dataset", self.recalculate_peak_dataset)
        if self.recalculate_peak_dataset == True:
            ## x-axis

            self.recalculate_peak_dataset = False

            self.data_updated = True

    def update_statistic(self):
        """update the statistic table"""
        if self.update:
            stats = []
            self.tableView_statistic.clear()
            self.tableView_statistic.setHorizontalHeaderLabels(['Mean', 'Median', 'Standard Deviation', 'Max', 'Min'])
            self.tableView_statistic.setVerticalHeaderLabels(self.CHANNEL_NAME)
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

    def sweep_update_low_1(self):
        """update sweep parameter threshold for low"""
        sweep_thresh = float(self.lineEdit_sweepxlimits1.text())
        try:
            if self.sweep_1_data:
                data_1 = self.sweep_1_data
                filtered_gate_voltage = [x for x in data_1 if x > sweep_thresh]
                percentage = round(100 * len(filtered_gate_voltage) / len(data_1), 2)
                self.lineEdit_percentagelow1.setText(str(percentage))
        except AttributeError:
            print("Issue loading data 1")

    def sweep_update_low_2(self):
        """update sweep parameter threshold for low"""
        sweep_thresh = float(self.lineEdit_sweepxlimits2.text())
        try:
            if self.sweep_2_data:
                data_2 = self.sweep_2_data
                filtered_gate_voltage = [x for x in data_2 if x > sweep_thresh]
                percentage = round(100 * len(filtered_gate_voltage) / len(data_2), 2)
                self.lineEdit_percentagelow2.setText(str(percentage))
        except AttributeError:
            print("Issue loading data 2")

    def sweep_update_high_1(self):
        """update sweep parameter threshold for above"""
        sweep_thresh = float(self.lineEdit_sweepylimits1.text())
        try:
            if self.sweep_1_data:
                data_1 = self.sweep_1_data
                filtered_gate_voltage = [x for x in data_1 if x > sweep_thresh]
                percentage = round(100 * len(filtered_gate_voltage) / len(data_1), 2)
                self.lineEdit_percentagehigh1.setText(str(percentage))
        except AttributeError:
            print("Issue loading data")

    def sweep_update_high_2(self):
        """update sweep parameter threshold for above"""
        sweep_thresh = float(self.lineEdit_sweepylimits2.text())
        try:
            if self.sweep_2_data:
                data_2 = self.sweep_2_data
                filtered_gate_voltage = [x for x in data_2 if x > sweep_thresh]
                percentage = round(100 * len(filtered_gate_voltage) / len(data_2), 2)
                self.lineEdit_percentagehigh2.setText(str(percentage))
        except AttributeError:
            print("Issue loading data")

    def sweep_update(self):
        """update the sweep result table"""
        try:
            range_max_1 = float(self.lineEdit_sweepylimits1.text())
            range_min_1 = float(self.lineEdit_sweepxlimits1.text())
            increment_1 = float(self.lineEdit_increment1.text())
        except:
            range_max_1 = 0
            range_min_1 = 0
            increment_1 = 0
        try:
            range_max_2 = float(self.lineEdit_sweepylimits2.text())
            range_min_2 = float(self.lineEdit_sweepxlimits2.text())
            increment_2 = float(self.lineEdit_increment2.text())
        except:
            range_max_2 = 0
            range_min_2 = 0
            increment_2 = 0

        if 0 < increment_1 < range_max_1 - range_min_1 and (range_max_1 - range_min_1) / increment_1 < 500 and \
                len(self.sweep_1_data):
            print("Updating Sweep Table 1")
            self.widget_sweepresult1.clear()
            self.widget_sweepresult1.setRowCount(int((range_max_1 - range_min_1) / increment_1))
            self.widget_sweepresult1.setColumnCount(4)
            self.widget_sweepresult1.setHorizontalHeaderLabels(("Voltages", "Counts Above Threshold",
                                                                "Total Count", "Percentages"))
            self.widget_sweepresult1.verticalHeader().hide()
            try:
                if len(self.sweep_1_data) > 0:
                    counter = range_min_1
                    sweep_list = []
                    i = 0
                    while counter < range_max_1:
                        filtered_gate_voltage_x = [x for x in self.sweep_1_data if x > counter]
                        percentage = round(100 * len(filtered_gate_voltage_x) / len(self.sweep_1_data), 2)
                        sweep_list.append([counter, len(filtered_gate_voltage_x), len(self.sweep_1_data), percentage])
                        counter += increment_1
                        i += 1
                    for x, row in enumerate(sweep_list):
                        for y in range(4):
                            item = QTableWidgetItem(str(round(row[y], 2)))
                            self.widget_sweepresult1.setItem(x, y, item)
                    self.widget_sweepresult1.show()
            except AttributeError:
                print("Data 1 not loaded")

        if 0 < increment_2 < range_max_2 - range_min_2 and (range_max_2 - range_min_2) / increment_2 < 500 and \
                len(self.sweep_2_data):
            print("Updating Sweep Table 2")
            self.widget_sweepresult2.clear()
            self.widget_sweepresult2.setRowCount(int((range_max_2 - range_min_2) / increment_2))
            self.widget_sweepresult2.setColumnCount(4)
            self.widget_sweepresult2.setHorizontalHeaderLabels(("Voltages", "Counts Above Threshold",
                                                                "Total Count", "Percentages"))
            self.widget_sweepresult2.verticalHeader().hide()
            try:
                if len(self.sweep_2_data) > 0:
                    counter = range_min_2
                    sweep_list = []
                    i = 0
                    while counter < range_max_2:
                        filtered_gate_voltage_x = [x for x in self.sweep_2_data if x > counter]
                        percentage = round(100 * len(filtered_gate_voltage_x) / len(self.sweep_2_data), 2)
                        sweep_list.append([counter, len(filtered_gate_voltage_x), len(self.sweep_2_data), percentage])
                        counter += increment_2
                        i += 1
                    for x, row in enumerate(sweep_list):
                        for y in range(4):
                            item = QTableWidgetItem(str(round(row[y], 2)))
                            self.widget_sweepresult2.setItem(x, y, item)
                    self.widget_sweepresult2.show()
            except AttributeError:
                print("Data 2 not loaded")

    def update_sweep_graphs(self, bypass=False):
        # self.sweep_bins = float(self.lineEdit_binwidth_2.text())
        update1 = update2 = data_updated = True
        if update1:
            self.update_sweep_1(data_updated)
        elif bypass:
            self.update_sweep_1(bypass)
        if update2:
            self.update_sweep_2(data_updated)
        elif bypass:
            self.update_sweep_2(bypass)

    def sweep_1_index_changed(self):
        """Function used to link update sweep with the index changes"""
        self.update_sweep_1(True)

    def sweep_2_index_changed(self):
        """Function used to link update sweep with the index changes"""
        self.update_sweep_2(True)

    def sweep_update_line(self):
        """Function used to link update sweep with the index changes"""
        self.sweep1_low_line.setValue(float(self.lineEdit_sweepxlimits1.text()))
        self.sweep1_high_line.setValue(float(self.lineEdit_sweepylimits1.text()))
        self.sweep2_low_line.setValue(float(self.lineEdit_sweepxlimits2.text()))
        self.sweep2_high_line.setValue(float(self.lineEdit_sweepylimits2.text()))

    def update_sweep_1(self, data_updated=False):
        self.widget_sweepparam2.clear()
        self.sweep1_low_line.setValue(float(self.lineEdit_sweepxlimits1.text()))
        self.sweep1_high_line.setValue(float(self.lineEdit_sweepylimits1.text()))
        channel = self.comboBox_option1.currentIndex()
        if channel == -1:
            self.comboBox_option1.setCurrentIndex(0)
        axis_name = self.comboBox_option1.currentText()
        #self.widget_sweepparam2.setLabel('bottom', axis_name)
        print("update sweep 1")
        r, g, b = Helper.rgb_select(channel)
        if data_updated or len(self.sweep_1_data) == 0:
            try:
                self.sweep_1_data = self.sweep_left[channel]
            except:
                self.sweep_1_data = []
        try:
            range_width = int(max(self.sweep_1_data)) + 1
        except:
            range_width = 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_bin1.text()))
        y, x = np.histogram(self.sweep_1_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam2.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam2.setXRange(0, max(x), padding=0)
        self.widget_sweepparam2.setYRange(0, max(y), padding=0)
        self.widget_sweepparam2.addItem(self.sweep1_low_line)
        self.widget_sweepparam2.addItem(self.sweep1_high_line)

        self.label_39.setText(self.comboBox_option1.currentText())

    def update_sweep_2(self, data_updated=False):
        self.widget_sweepparam1.clear()
        self.sweep2_low_line.setValue(float(self.lineEdit_sweepxlimits2.text()))
        self.sweep2_high_line.setValue(float(self.lineEdit_sweepylimits2.text()))
        channel = self.comboBox_option2.currentIndex()
        if channel == -1:
            self.comboBox_option2.setCurrentIndex(0)
        axis_name = self.comboBox_option2.currentText()
        #self.widget_sweepparam1.setLabel('bottom', axis_name)
        r, g, b = Helper.rgb_select(channel)
        print("update sweep 2")
        if data_updated or len(self.sweep_2_data) == 0:
            try:
                self.sweep_2_data = self.sweep_right[channel]
            except:
                self.sweep_2_data = []
        try:
            range_width = int(max(self.sweep_2_data)) + 1
        except:
            range_width = 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_bin2.text()))
        y, x = np.histogram(self.sweep_2_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam1.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam1.setXRange(0, max(x), padding=0)
        self.widget_sweepparam1.setYRange(0, max(y), padding=0)
        self.widget_sweepparam1.addItem(self.sweep2_low_line)
        self.widget_sweepparam1.addItem(self.sweep2_high_line)
        self.label_65.setText(self.comboBox_option2.currentText())

    #             self.thresholdUpdated()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_files.setText(_translate("MainWindow", "Files"))
        self.progress_label.setText(_translate("MainWindow", "File Extraction"))
        self.label.setText(_translate("MainWindow", "Channel Selection"))
        self.checkbox_ch1.setText(_translate("MainWindow", "Channel 1"))
        self.checkbox_ch2.setText(_translate("MainWindow", "Channel 2"))
        self.checkbox_ch3.setText(_translate("MainWindow", "Channel 3"))
        self.checkbox_ch12.setText(_translate("MainWindow", "Channel 1-2"))
        self.checkbox_ch13.setText(_translate("MainWindow", "Channel 1-3"))
        self.checkbox_ch23.setText(_translate("MainWindow", "Channel 2-3"))
        self.checkbox_Droplet_Record.setText(_translate("MainWindow", "Droplet Record"))
        self.checkbox_Locked_Out_Peaks.setText(_translate("MainWindow", "Locked Out Peaks"))
        self.checkBox_7.setText(_translate("MainWindow", "Sorted Peaks"))

        self.channel_1.setText(_translate("MainWindow", self.CHANNEL_NAME[0]))
        self.channel_2.setText(_translate("MainWindow", self.CHANNEL_NAME[1]))
        self.channel_3.setText(_translate("MainWindow", self.CHANNEL_NAME[2]))
        self.channel_4.setText(_translate("MainWindow", self.CHANNEL_NAME[3]))
        self.channel_5.setText(_translate("MainWindow", self.CHANNEL_NAME[4]))
        self.channel_6.setText(_translate("MainWindow", self.CHANNEL_NAME[5]))

        self.button_update.setText(_translate("MainWindow", "Extract"))
        #         self.label_2.setText(_translate("MainWindow", "Gate Voltages"))
        #         self.button_copy.setText(_translate("MainWindow", "Copy"))
        #         self.button_paste.setText(_translate("MainWindow", "Paste"))
        #         self.button_screenshot.setText(_translate("MainWindow", "Screenshot"))
        #         self.pushButton_2.setText(_translate("MainWindow", "Save"))
        #         self.pushButton.setText(_translate("MainWindow", "Load"))
        self.label_8.setText(_translate("MainWindow", "Total Runtime"))
        self.label_3.setText(_translate("MainWindow", "Peak Threshold"))
        self.pushButton_resample.setText(_translate("MainWindow", "Resample"))
        self.label_4.setText(_translate("MainWindow", "Count"))
        self.label_6.setText(_translate("MainWindow", "Starting Time"))
        self.label_12.setText(_translate("MainWindow", "Ch1 Hit"))
        self.label_14.setText(_translate("MainWindow", "Ch 3 Hit"))
        self.label_13.setText(_translate("MainWindow", "Ch 2 Hit"))
        self.label_15.setText(_translate("MainWindow", "Ch 1-2 Hit"))
        self.label_16.setText(_translate("MainWindow", "Ch 1-3 Hit"))
        self.label_17.setText(_translate("MainWindow", "Ch 2-3 Hit"))
        self.label_ch_4_hit.setText(_translate("MainWindow", "Ch 4 Hit"))
        self.label_ch_14_hit.setText(_translate("MainWindow", "Ch 1-4 Hit"))
        self.label_ch_24_hit.setText(_translate("MainWindow", "Ch 2-4 Hit"))
        self.label_ch_34_hit.setText(_translate("MainWindow", "Ch 3-4 Hit"))
        self.label_ch_123_hit.setText(_translate("MainWindow", "Ch 1-2-3 Hit"))
        self.label_ch_124_hit.setText(_translate("MainWindow", "Ch 1-2-4 Hit"))
        self.label_ch_134_hit.setText(_translate("MainWindow", "Ch 1-3-4 Hit"))
        self.label_ch_234_hit.setText(_translate("MainWindow", "Ch 2-3-4 Hit"))
        self.label_ch_1234_hit.setText(_translate("MainWindow", "Ch 1-2-3-4 Hit"))
        self.label_19.setText(_translate("MainWindow", "Total Dispensed"))
        self.label_11.setText(_translate("MainWindow", "Total Lost"))
        self.label_5.setText(_translate("MainWindow", "Experiment Summary"))
        self.label_10.setText(_translate("MainWindow", "Total Sorted"))
        self.label_9.setText(_translate("MainWindow", "Total Droplets"))
        self.label_out_of_range_droplet.setText(_translate("MainWindow", "Out of Range"))
        self.label_18.setText(_translate("MainWindow", "Dispensing Stats"))
        self.label_20.setText(_translate("MainWindow", "Dispense Missed"))
        self.label_7.setText(_translate("MainWindow", "Ending Time"))
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_statistic),
                                         _translate("MainWindow", "Statistic"))


        #         self.comboBox_option1.setItemText(0, _translate("MainWindow", "Option 1"))
        #         self.comboBox_option2.setItemText(0, _translate("MainWindow", "Option 2"))
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
        # self.lineEdit_binwidth_2.setText(_translate("MainWindow", "0.1"))
        # self.label_56.setText(_translate("MainWindow", "Bin Width"))
        #         self.label_57
        # self.label_55.setText(_translate("MainWindow", "Channels"))
        # self.label_49.setText(_translate("MainWindow", "Gating Thresholds"))
        # self.label_50.setText(_translate("MainWindow", "Gate Voltage Minimum"))
        # self.label_61.setText(_translate("MainWindow", "Increments"))
        # self.lineEdit_increments.setText(_translate("MainWindow", "0"))
        # self.lineEdit_gatevoltagemaximum.setText(_translate("MainWindow", "0.5"))
        # self.lineEdit_gatevoltageminimum.setText(_translate("MainWindow", "0"))
        # self.label_62.setText(_translate("MainWindow", "Gate Voltage Maximum"))
        # self.label_63.setText(_translate("MainWindow", "V"))
        # self.label_64.setText(_translate("MainWindow", "V"))
        # self.label_66.setText(_translate("MainWindow", "V"))
        self.label_sweep1.setText(_translate("MainWindow", "Sweep 1"))
        self.label_sweep2.setText(_translate("MainWindow", "Sweep 2"))
        self.lineEdit_sweepxlimits1.setText(_translate("MainWindow", "0"))
        #self.label_71.setText(_translate("MainWindow", "End Voltage"))
        #self.label_69.setText(_translate("MainWindow", "Start Voltage"))
        self.label_70.setText(_translate("MainWindow", "Start Voltage"))
        self.lineEdit_increment2.setText(_translate("MainWindow", "0.1"))
        self.lineEdit_sweepylimits1.setText(_translate("MainWindow", "10"))
        self.lineEdit_sweepylimits2.setText(_translate("MainWindow", "10"))
        self.lineEdit_increment1.setText(_translate("MainWindow", "0.1"))
        self.label_72.setText(_translate("MainWindow", "End Voltage"))
        self.lineEdit_sweepxlimits2.setText(_translate("MainWindow", "0"))
        self.lineEdit_bin1.setText(_translate("MainWindow", "0.1"))
        self.lineEdit_bin2.setText(_translate("MainWindow", "0.1"))
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
                                         _translate("MainWindow", "Dispense Mapping"))

        self.label_271.setText(_translate("MainWindow", "Channel Selection"))


        self.label_270.setText(_translate("MainWindow", "Start Peak"))
        self.label_272.setText(_translate("MainWindow", "End Peak"))
        self.label_273.setText(_translate("MainWindow", "*Peak difference < 15"))
        self.label_274.setText(_translate("MainWindow", "Last/Next"))
        self.label_275.setText(_translate("MainWindow", "Polynomial Order"))
        self.label_276.setText(_translate("MainWindow", "Smooth Level"))
        self.label_277.setText(_translate("MainWindow", "Smoothing"))
        self.label_278.setText(_translate("MainWindow", "Custom Sample Size"))
        self.Smooth_enable.setText(_translate("MainWindow", "Enable smooth?"))
        self.pushButton_5.setText(_translate("MainWindow", "Generate Plot"))
        self.pushButton_3.setText(_translate("MainWindow", "Next Page"))
        self.pushButton_4.setText(_translate("MainWindow", "Last Page"))
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_3),
                                         _translate("MainWindow", "Raw Data Viewer"))


        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_sweep),
                                         _translate("MainWindow", "Sweep"))

        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_report),
                                         _translate("MainWindow", "Log"))


        self.menuFiles.setTitle(_translate("MainWindow", "Projects"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionAdd_New.setText(_translate("MainWindow", "Add New"))
        self.actionAdd_Save.setText(_translate("MainWindow", "Save"))
        self.actionAdd_Load.setText(_translate("MainWindow", "Load"))
        self.actionAdd_SaveSingleFile.setText(_translate("MainWindow", "Save Single File"))
        self.actionAdd_SaveParameters.setText(_translate("MainWindow", "Save Parameters"))
        self.actionAdd_LoadParameters.setText(_translate("MainWindow", "Load Parameters"))
        self.actionClose.setText(_translate("MainWindow", "Close"))

    #         self.label_filter.setText(_translate("MainWindow", "test"))

    def pressed(self):
        print('pressed')
        check0 = time.time()

        try:
            self.chart_title_change()
        except:
            self.file_list_view.setCurrentRow(0)
            self.chart_title_change()

        # global Ch1,Ch2,Ch3,Ch1_2,Ch1_3,Ch2_3,Locked,Raw_Time_Log,current_file_dict
        self.main_file_select = self.file_list_view.currentRow()
        self.ch1_checkbox = self.checkbox_ch1.isChecked()
        self.ch2_checkbox = self.checkbox_ch2.isChecked()
        self.ch3_checkbox = self.checkbox_ch3.isChecked()
        self.ch12_checkbox = self.checkbox_ch12.isChecked()
        self.ch13_checkbox = self.checkbox_ch13.isChecked()
        self.ch23_checkbox = self.checkbox_ch23.isChecked()
        self.Droplet_Record_checkbox = self.checkbox_Droplet_Record.isChecked()
        self.locked_out_checkbox = self.checkbox_Locked_Out_Peaks.isChecked()
        self.all_checkbox = self.checkBox_7.isChecked()

        self.peak_num_mode = []
        self.peak_num_in = []


        # self.sweep_channel = self.listView_channels_2.currentRow()
        #         if self.comboBox_option1.currentIndex() > 2:
        #             self.sweep_file_1 = self.comboBox_option1.currentIndex() - 3
        #             self.sweep_1_dict = self.file_dict_list[self.sweep_file_1]
        #         else:
        #             self.sweep_file_1 = self.comboBox_option1.currentIndex()
        #         if self.comboBox_option2.currentIndex() > 2:
        #             self.sweep_file_2 = self.comboBox_option2.currentIndex() - 3

        #             self.sweep_2_dict = self.file_dict_list[self.sweep_file_2]
        #         else:
        #             self.sweep_file_2 = self.comboBox_option2.currentIndex()
        # self.sweep_bins = float(self.lineEdit_binwidth_2.text())
        self.current_file_dict = self.file_dict_list[self.main_file_select]

        os.chdir(self.current_file_dict["Root Folder"])
        # summary
        if self.current_file_dict["Summary"] != "":
            stats = Helper.Stats(self.current_file_dict["Summary"])
            self.lineEdit_startingtime.setText(stats.start_time)
            self.lineEdit_endingtime.setText(stats.end_time)
            self.lineEdit_runtime.setText(stats.total_runtime)
            self.lineEdit_out_of_range_droplet.setText(stats.droplets_out_of_range)
            self.lineEdit_totalsorted.setText(stats.total_sorted)
            self.lineEdit_totallost.setText(stats.total_lost)
            self.lineEdit_totaldispensed.setText(stats.total_dispensed)
            self.lineEdit_totaldroplets.setText(stats.total_droplets)
            self.lineEdit_dispensemissed.setText(stats.dispense_missed)
            self.lineEdit_ch1hit.setText(stats.ch1_hit)
            self.lineEdit_ch2hit.setText(stats.ch2_hit)
            self.lineEdit_ch3hit.setText(stats.ch3_hit)
            self.lineEdit_ch4_hit.setText(stats.ch4_hit)
            self.lineEdit_ch12hit.setText(stats.ch12_hit)
            self.lineEdit_ch13hit.setText(stats.ch13_hit)
            self.lineEdit_ch23hit.setText(stats.ch23_hit)
            self.lineEdit_ch_14_hit.setText(stats.ch14_hit)
            self.lineEdit_ch_24_hit.setText(stats.ch24_hit)
            self.lineEdit_ch_34_hit.setText(stats.ch34_hit)
            self.lineEdit_ch_123_hit.setText(stats.ch123_hit)
            self.lineEdit_ch_124_hit.setText(stats.ch124_hit)
            self.lineEdit_ch_134_hit.setText(stats.ch134_hit)
            self.lineEdit_ch_234_hit.setText(stats.ch234_hit)
            self.lineEdit_ch_1234_hit.setText(stats.ch1234_hit)

        channel = 0
        width_enable = True


        try:
            if self.reset == True:
                reset = True
            else:
                reset = False
        except:
            reset = False

        ### check Voltage threshold(V)
        threshold = [0, 0, 0, 0, 0, 0]
        peaks_threshold = []
        width_min = [0, 0, 0, 0, 0, 0]
        width_max = [500, 500, 500, 500, 500, 500]

        """
        if self.current_file_dict["Param"] != "":
            with open(self.current_file_dict["Param"]) as param_file:
                stats_reader = csv.reader(param_file, delimiter=",")
                location = [[0, 0], [0, 0]]
                param_holder = []
                for x, lines in enumerate(stats_reader):
                    param_holder.append(lines)
                    for y, field in enumerate(lines):
                        if field == "Peak Threshold (V)":
                            location[0] = [x, y]
                        if field == "BG Threshold (V)":
                            location[1] = [x, y]
                try:
                    for i in range(1, 5):
                        peaks_threshold.append(float(param_holder[location[0][0] + i][location[0][1]]))
                        width_threshold.append(float(param_holder[location[1][0] + i][location[1][1]]))
                        print("Peaks Threshold Found: ", peaks_threshold)
                        print("Width Threshold Found: ", width_threshold)
                except:
                    print("Peaks Threshold Not Found")
        if len(peaks_threshold) == 0:
            peaks_threshold = [2.7, 3.6, 3.3, 1]

        try:
            # test if numbers entered in threshold
            for i in range(4):
                threshold[i] = float(threshold[i])
        except:
            # if not, find in parameter file
            if len(width_threshold) == 0:
                threshold = [2.7, 3.6, 3.3, 1]
            else:
                threshold = width_threshold
        ### check end
        """
        try:
            self.update = self.ui_state.working_file_update_check(file=self.current_file_dict, chall=self.all_checkbox,
                                                                  ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                                  ch3=self.ch3_checkbox,
                                                                  ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                                  ch2_3=self.ch23_checkbox,
                                                                  locked_out=self.locked_out_checkbox,
                                                                  Droplet_Record=self.Droplet_Record_checkbox,
                                                                  reset=Ui_MainWindow.reset)
            print('file', self.main_file_select)
        except:
            self.update = self.ui_state.working_file_update_check(file=self.current_file_dict, chall=self.all_checkbox,
                                                                  ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                                  ch3=self.ch3_checkbox,
                                                                  ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                                  ch2_3=self.ch23_checkbox,
                                                                  locked_out=self.locked_out_checkbox,
                                                                  Droplet_Record=self.Droplet_Record_checkbox)
            print('file', self.main_file_select)

        threshold_check = self.ui_state.threshold_check(self.thresholds, self.file_list_view.currentRow())
        peaks_threshold = self.thresholds[self.file_list_view.currentRow()]

        if self.update or threshold_check:
            peak_enable = True
        else:
            peak_enable = False
        print("peak recalculate enable check is :", peak_enable)
        print("resample parameter self.reset check is :", reset)

        self.data_updated = False

        check1 = time.time()

        if self.current_file_dict["Peak Record"] in self.analog and not reset and not threshold_check:
            print("--------------------------------------------------------not reset")
            check2 = time.time()
            self.update_working_data()
            check2A = time.time()
            if self.data_updated == True:
                check3 = time.time()
                check3A = time.time()
                self.update_sweep_graphs(True)
            else:
                check3 = time.time()

            check4 = time.time()

            #self.draw_peak_width()
            check4A = time.time()
            #self.draw_peak_width_2()
            check4B = time.time()

            self.update_sweep_graphs()
            check4C = time.time()
            self.sweep_update_high()
            check4D = time.time()
            self.sweep_update_low()
            check4E = time.time()
            self.sweep_update()
            check4F = time.time()

            self.update_statistic()
            check4G = time.time()
            #self.update_sampling_Rate()
            check5 = time.time()

            self.update_checkbox()
            self.tree_dic[(self.file_list_view.currentRow(),)]['tree_windowfilter'].channel_list_update(
                self.comboBox_14_list)

        else:
            print("--------------------------------------------------------reset")
            """
            analog_file = Analysis.file_extracted_data_Qing(self.current_file_dict, threshold,
                                                  peaks_threshold, width_min, width_max,
                                                  width_enable, peak_enable, channel, 200,
                                                  0, stats.ch1_hit, stats.ch2_hit, stats.ch3_hit, stats.ch12_hit,
                                                  stats.ch13_hit,
                                                  stats.ch23_hit, stats.Droplet_Record_hit,
                                                  stats.total_sorted, rethreshold=threshold_check)
            
            print("data extration complete, drawing....")
            self.analog.update(analog_file)

            self.save_a = self.analog
            heck2 = time.time()

            self.update_working_data()

            # direct everything into window filters
            # self.draw is histogram
            # self.draw_2 triggers 2nd and 3rd filter
            if self.data_updated == True:
                self.update_sweep_graphs(True)

            self.update_statistic()
            """
            if self.extraction_thread_state[self.main_file_select] in (ThreadState.IDLING, ThreadState.FINISHED)\
                    and ThreadState.RUNNING not in self.extraction_thread_state:
                self.run_extraction(self.main_file_select, threshold, peaks_threshold, width_min, width_max, width_enable, peak_enable, channel, stats, threshold_check)
                self.comboBox_14_list = {}
                if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1 "
                if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2 "
                if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch3 "
                if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-2"
                if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-3"
                if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2-3"
                if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict['Droplet Record'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Droplet Record"
                if self.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict['Locked Out Peaks'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Locked Out Peaks"
                if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Peak Record"
                ### End

#                self.tree_dic[(self.file_list_view.currentRow(),)]['tree_windowfilter'].channel_list_update(
#                   self.comboBox_14_list)
                print("complete!")
            elif ThreadState.RUNNING in self.extraction_thread_state and \
                    self.extraction_thread_state[self.main_file_select] in (ThreadState.IDLING, ThreadState.FINISHED):
                # this case will add a index to the extraction q
                self.extraction_queue.append([self.main_file_select, threshold, peaks_threshold, width_min, width_max,
                                              width_enable, peak_enable, channel, stats, threshold_check])
                self.comboBox_14_list = {}
                if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1 "
                if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2 "
                if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch3 "
                if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-2"
                if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-3"
                if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2-3"
                if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict['Droplet Record'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Droplet Record"
                if self.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict['Locked Out Peaks'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Locked Out Peaks"
                if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                    self.comboBox_14_list[len(self.comboBox_14_list)] = "Peak Record"
                # self.tree_dic[(self.file_list_view.currentRow(),)]['tree_windowfilter'].channel_list_update(
                #     self.comboBox_14_list)
                self.file_list_view.item(self.main_file_select).setForeground(QColor(255, 255, 0))
                self.extraction_thread_state[self.main_file_select] = ThreadState.PENDING
                logging.info("New file added to extraction queue")
            else:
                logging.info("Thread not ready for processing")

    def extract_all_clicked(self):
        """function call to handle when extract all is clicked"""

        threshold = [0, 0, 0, 0, 0, 0]
        width_min = [0, 0, 0, 0, 0, 0]
        width_max = [500, 500, 500, 500, 500, 500]
        width_enable = True
        channel = 0



        for current_file_index in range(self.file_list_view.count()):

            current_file_dict = self.file_dict_list[current_file_index]
            stats = Helper.Stats(current_file_dict["Summary"])
            threshold_check = self.ui_state.threshold_check(self.thresholds, self.file_list_view.currentRow())
            peaks_threshold = self.thresholds[self.file_list_view.currentRow()]

            if self.update or threshold_check:
                peak_enable = True
            else:
                peak_enable = False

            # this will iterate through each file index and append to extraction list
            if self.extraction_thread_state[current_file_index] in (ThreadState.IDLING, ThreadState.FINISHED)\
                    and ThreadState.RUNNING not in self.extraction_thread_state:
                self.run_extraction(current_file_index, threshold, peaks_threshold, width_min, width_max, width_enable, peak_enable, channel, stats, threshold_check)

            elif ThreadState.RUNNING in self.extraction_thread_state and \
                    self.extraction_thread_state[current_file_index] in (ThreadState.IDLING, ThreadState.FINISHED):
                # this case will add a index to the extraction q
                self.extraction_queue.append([current_file_index, threshold, peaks_threshold, width_min, width_max,
                                              width_enable, peak_enable, channel, stats, threshold_check])
                self.file_list_view.item(current_file_index).setForeground(QColor(255, 255, 0))
                self.extraction_thread_state[current_file_index] = ThreadState.PENDING


    def update_checkbox(self):
        self.comboBox_14_list = {}
        if self.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1 "
        if self.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2 "
        if self.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch3 "
        if self.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-2"
        if self.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-3"
        if self.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2-3"
        if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict['Droplet Record'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Droplet Record"
        if self.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict['Locked Out Peaks'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Locked Out Peaks"
        if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Peak Record"

    def save(self):
        """ function to save current instance """
        file = QFileDialog.getSaveFileName(self, "Save File", os.getcwd(), "AuraLab Save File (*.abl)")
        file_str = str(file[0])
        if file_str:
            full_file_dir = file_str
            file_out = open(full_file_dir, "wb")
            time_log_reconstruct_index = {}
            offset = 2
            for i in range(self.time_log_file_model.rowCount()):
                item = self.time_log_file_model.item(i)
                key = item.text()
                if key in time_log_reconstruct_index.keys():
                    key = key + " (" + str(offset) + ")"
                    offset += 1
                holder = []
                for j in range(item.rowCount()):
                    holder.append(item.child(j).text())
                time_log_reconstruct_index[key] = holder

            print(time_log_reconstruct_index)


            output = Helper.SaveObject(self.analog, self.thresholds, self.file_dict_list, self.working_data,
                                       self.current_file_dict, self.ui_state, self.time_log_file_indexes,
                                       self.extraction_thread_state, self.tree_dic, self.time_log_window,
                                       time_log_reconstruct_index)
            pickle.dump(output, file_out)
            file_out.close()
            print(full_file_dir + " finished writing")

    def load(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select save file", filter="(*.abl)")
        with open(file, "rb") as input_file:
            self.tree_dic = {}
            self.treeModel.clear()
            data = pickle.load(input_file)
            self.analog = data.analog
            self.thresholds = data.thresholds
            self.file_dict_list = data.file_dict_list
            self.working_data = data.working_data
            self.current_file_dict = data.current_file_dict
            self.ui_state = data.ui_state
            self.time_log_file_indexes = data.time_log_file_indexes
            self.extraction_thread_state = data.extraction_thread_state
            print(data.tree_dic_keys)
            self.file_list_view.clear()
            self.thread = []
            for i, file in enumerate(self.file_dict_list):
                self.file_list_view.addItem(file["Peak Record"])
                self.thread.append(QtCore.QThread())
            for key in data.filter_data_dict.keys():
                if len(key) == 1:
                    """this should be the root"""
                    self.tree_dic[key] = {}
                    filter_name = data.filter_names_dict[key]
                    self.tree_dic[key]['tree_standarditem'] = StandardItem(filter_name, 12, set_bold=True)
                    self.treeModel.appendRow(self.tree_dic[key]['tree_standarditem'])
                    print(data.filter_data_dict[key])
                    self.tree_dic[key]['tree_windowfilter'] = Filter_window.window_filter(ui, saved_data=
                    data.filter_data_dict[key])
                else:
                    parent_key = key[1:]
                    self.tree_dic[key] = {}
                    filter_name = data.filter_names_dict[key]
                    self.tree_dic[key]['tree_standarditem'] = StandardItem(filter_name, 12, set_bold=True)
                    self.tree_dic[parent_key]['tree_standarditem'].appendRow(self.tree_dic[key]['tree_standarditem'])
                    self.tree_dic[key]['tree_windowfilter'] = Filter_window.window_filter(ui, saved_data=
                    data.filter_data_dict[key])

        self.time_log_window = Time_log_selection_window.TimeLogFileSelectionWindow(
            self.file_list_view, self.time_log_file_model, self.time_log_file_indexes, self.tree_dic, self.treeModel,
            ui, self.file_dict_list, self.time_log_graph_top, self.time_log_graph_bot)
        self.time_log_window.import_data(data.time_log_data)
        self.time_log_file_model.clear()
        print(data.time_log_reconstruct_index)
        for key in data.time_log_reconstruct_index.keys():
            current_item = QStandardItem(key)
            if data.time_log_reconstruct_index[key]:
                for child in data.time_log_reconstruct_index[key]:
                    current_item.appendRow(QStandardItem(child))
            self.time_log_file_model.appendRow(current_item)


    def add(self):
        name, _ = QFileDialog.getOpenFileNames(self, 'Open File', filter="*peak*")
        #         self.comboBox_option1.addItem("Current Data")
        #         self.comboBox_option2.addItem("Current Data")
        #         self.comboBox_option1.addItem("Current Data post Width/Peaks # Filter")
        #         self.comboBox_option2.addItem("Current Data post Width/Peaks # Filter")
        #         self.comboBox_option1.addItem("Current Data post 2nd Filter")
        #         self.comboBox_option2.addItem("Current Data post 2nd Filter")
        #         if self.comboBox_option1.count() == 0:
        #             self.comboBox_option1.addItem("Current Data")
        #             self.comboBox_option2.addItem("Current Data")
        for f in name:
            self.file_dict_list.append(Helper.project_namelist(f))
            self.file_list_view.addItem(f)
            self.thread.append(QtCore.QThread())
            self.extraction_thread_state.append(ThreadState.IDLING)
            self.thresholds.append([0.0, 0.0, 0.0, 0.0])
        #             self.comboBox_option1.addItem(f)
        #             self.comboBox_option2.addItem(f)
        for i in range(self.file_list_view.count()):
            item = self.file_list_view.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.ui_state.threshold_initialize(self.thresholds)
        self.update_file_color()


    def update_file_color(self):
        """call this function to update the color of file selection"""
        logging.info(self.extraction_thread_state)
        for i in range(len(self.extraction_thread_state)):
            if self.extraction_thread_state[i] == ThreadState.IDLING:
                self.file_list_view.item(i).setForeground(QColor(128, 128, 128))
            elif self.extraction_thread_state[i] == ThreadState.RUNNING:
                self.file_list_view.item(i).setForeground(QColor(0, 128, 0))
            elif self.extraction_thread_state[i] == ThreadState.PENDING:
                self.file_list_view.item(i).setForeground(QColor(255, 255, 0))
            else:
                self.file_list_view.item(i).setForeground(QColor(0, 0, 0))


    def openfolder(self):
        """function handling the open folder operation"""
        #         self.comboBox_option1.clear()
        #         self.comboBox_option2.clear()
        name, _ = QFileDialog.getOpenFileNames(self, 'Open File', filter="*peak*")
        # sort the files so they will be correctly organized in the time log
        name.sort()
        if name:
            self.analog = {}
            self.tree_dic = {}
            self.file_list_view.clear()
            self.file_dict_list.clear()
            self.time_log_file_model.clear()
            self.treeModel.clear()
            self.thresholds = []
            self.thread = []
            self.extraction_thread_state = []
            for f in name:
                print(f)
                self.file_dict_list.append(Helper.project_namelist(f))
                self.file_list_view.addItem(f)
                #             self.comboBox_option1.addItem(f)
                #             self.comboBox_option2.addItem(f)
                # record change in the log
                self.textbox = self.textbox + "\n" + "open file:" + str(f)
                self.textEdit.setPlainText(self.textbox)
            #initialize the filter window with loaded files
            for i in range(self.file_list_view.count()):
                # create a thread for each of the file added
                self.thread.append(QtCore.QThread())
                self.extraction_thread_state.append(ThreadState.IDLING)
                # create item for the list view
                item = self.file_list_view.item(i)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                # initialize the tree dic
                self.tree_dic[(i,)] = {}
                text = item.text()
                self.tree_dic[(i,)]['tree_standarditem'] = StandardItem(text, 12, set_bold=True)
                self.treeModel.appendRow(self.tree_dic[(i,)]['tree_standarditem'])
                self.tree_index = (i,)
                self.tree_dic[(i,)]['tree_windowfilter'] = Filter_window.window_filter(ui, self.file_dict_list[i], root=i)
                self.thresholds.append([0.0, 0.0, 0.0, 0.0])
            self.ui_state.threshold_initialize(self.thresholds)
            self.time_log_window = Time_log_selection_window.TimeLogFileSelectionWindow(
                self.file_list_view, self.time_log_file_model, self.time_log_file_indexes, self.tree_dic, self.treeModel,
                ui, self.file_dict_list, self.time_log_graph_top, self.time_log_graph_bot)
            self.update_file_color()
            print(self.tree_dic.keys())

    # start of the dispense mapping file
    def open_dispense_folder(self):
        """function return the list of """
        root_folder = QFileDialog.getExistingDirectory(self, 'Open')
        self.fileindex = Wells.index_files(root_folder)
        print(self.fileindex)

        if self.radiobutton_200.isChecked():
            self.chunk_size = 200
        else:
            self.chunk_size = 1000

        if self.radiobutton_96.isChecked():
            self.well_mode = 96
        else:
            self.well_mode = 48

        self.well_object = Wells.Wells(root_folder, self.fileindex, self.chunk_size, self.well_mode)
        self.plate_combobox.clear()
        # for i in range(8):
        # print(self.well_object.plate_data[0][i])
        # for i in range(8):
        # print(self.well_object.plate_data[1][i])
        for i in range(math.ceil(self.well_object.number_of_strips / 12)):
            text_holder = 'Plate ' + str(i + 1)
            self.plate_combobox.addItem(text_holder)
        self.tabWidget.setCurrentIndex(4)
        self.plate_update()
        
    def plate_update(self):
        """update plate information when plate number changes"""
        self.well_checkbox_queue = []
        for strip in range(self.plate_combobox.currentIndex() * 12, self.plate_combobox.currentIndex() * 12 + 12):
            for well in range(8):
                # print(strip)
                current_strip = strip % 12
                try:
                    holder = self.well_object.plate_data[strip][well]
                    if len(holder) == 0:
                        self.well_selector_checkboxes[current_strip][well].setEnabled(False)
                    else:
                        self.well_selector_checkboxes[current_strip][well].setEnabled(True)
                except IndexError:
                    self.well_selector_checkboxes[current_strip][well].setEnabled(False)
        for strip in range(12):
            self.col_buttons[strip].setEnabled(False)
            for well in range(8):
                if self.well_selector_checkboxes[strip][well].isEnabled():
                    self.col_buttons[strip].setEnabled(True)
                    break

    def plate_left_button_clicked(self):
        """update the selected plate"""
        if self.plate_combobox.currentIndex() > 0:
            self.plate_combobox.setCurrentIndex(self.plate_combobox.currentIndex()-1)

    def plate_right_button_clicked(self):
        """update the selected plate"""
        if self.plate_combobox.currentIndex() < self.plate_combobox.count() - 1:
            self.plate_combobox.setCurrentIndex(self.plate_combobox.currentIndex() + 1)

    def col_button_clicked(self):
        """this function handle when a button is clicked"""
        print("Total layout row: " + str(self.well_plots_layout.rowCount()))
        print("Total layout col: " + str(self.well_plots_layout.columnCount()))
        button = self.sender()
        button.setCheckable(True)
        selected_col = int(button.text()) - 1
        for strip in range(12):
            if strip != selected_col:
                self.col_buttons[strip].setChecked(False)
            for well in range(8):
                if strip == selected_col:
                    if self.col_buttons[strip].isChecked():
                        if self.well_selector_checkboxes[strip][well].isEnabled():
                            self.well_selector_checkboxes[strip][well].setChecked(True)
                    else:
                        self.well_plots[well].hide()
                        self.well_plots[well].setParent(None)
                        if self.well_selector_checkboxes[strip][well].isEnabled():
                            self.well_selector_checkboxes[strip][well].setChecked(False)
                else:
                    self.well_selector_checkboxes[strip][well].setChecked(False)
        self.well_checkbox_queue = []
        if self.col_buttons[selected_col].isChecked():
            for well in range(8):
                title = str(self.plate_combobox.currentIndex() + 1) + chr(65 + well) + str(selected_col)
                self.well_plots[well].setTitle(title)
                if self.well_selector_checkboxes[selected_col][well].isEnabled():
                    self.well_checkbox_queue.append((selected_col, well, self.well_object.plate_data[self.plate_combobox.currentIndex()*12+selected_col][well]))
            self.wells_plot(1)

    def well_clicked(self):
        """this function handle when a button is clicked"""
        button = self.sender()
        col_triggered = None
        for i in range(12):
            if self.col_buttons[i].isChecked():
                col_triggered = i
        if col_triggered == button.x and button.isChecked():
            return
        else:
            total_selected = 0
            for x in range(12):
                for y in range(8):
                    if self.well_selector_checkboxes[x][y].isChecked():
                        total_selected+=1
            if total_selected > 8:
                if self.well_selector_checkboxes[button.x][button.y].isChecked():
                    self.well_selector_checkboxes[button.x][button.y].setChecked(False)
                    return
            else:
                if col_triggered is not None:
                    self.col_buttons[col_triggered].setChecked(False)
                plate = self.plate_combobox.currentIndex()
                self.well_checkbox_queue.clear()
                for i in range(8):
                    self.well_plots[i].hide()
                    self.well_plots[i].setParent(None)
                for col in range(12):
                    for row in range(8):
                        if self.well_selector_checkboxes[col][row].isChecked():
                            data = self.well_object.plate_data[col + 12 * plate][row]
                            self.well_checkbox_queue.append((col, row, data))
                if len(self.well_checkbox_queue) > 0:
                    self.wells_plot(0)

    def wells_plot(self, mode):
        """function called to plot all the items in the queue"""
        for i in range(8):
            self.well_plots[i].clear()
            self.well_plots[i].setParent(None)
            self.well_plots[i].hide()
        strip_offset = self.plate_combobox.currentIndex() * 12
        print("Total layout row: " + str(self.well_plots_layout.rowCount()))
        print("Total layout col: " + str(self.well_plots_layout.columnCount()))

        # update channel names
        if self.green_name.text():
            ch1_name = self.green_name.text()
        else:
            ch1_name = "Channel 1"

        if self.red_name.text():
            ch2_name = self.red_name.text()
        else:
            ch2_name = "Channel 2"

        if self.blue_name.text():
            ch3_name = self.blue_name.text()
        else:
            ch3_name = "Channel 3"

        if self.orange_name.text():
            ch4_name = self.orange_name.text()
        else:
            ch4_name = "Channel 4"

        # mode 0 means single well selections
        if mode == 0:
            for count in range(8):
                if count < 4:
                    self.well_plots_layout.addWidget(self.well_plots[count], 0, count, 1, 1)
                else:
                    self.well_plots_layout.addWidget(self.well_plots[count], 1, count - 4, 1, 1)
                self.well_plots[count].show()
                for i in range(len(self.well_checkbox_queue), 8, 1):
                    self.well_plots[i].hide()
            if len(self.well_checkbox_queue) > 4:
                self.well_plots_layout.setRowStretch(0, 1000)
                self.well_plots_layout.setRowMinimumHeight(0, 1000)
                self.well_plots_layout.setRowStretch(1, 1000)
                self.well_plots_layout.setRowMinimumHeight(1, 1000)
            else:
                self.well_plots_layout.setRowStretch(0, 1000)
                self.well_plots_layout.setRowMinimumHeight(0, 1000)
                self.well_plots_layout.setRowStretch(1, 0)
                self.well_plots_layout.setRowMinimumHeight(1, 0)

            if len(self.well_checkbox_queue) > 4:
                for i in range(4):
                    self.well_plots_layout.setColumnStretch(i, 1000)
                    self.well_plots_layout.setColumnMinimumWidth(i, 1000)
            else:
                for i in range(4):
                    if i < len(self.well_checkbox_queue):
                        self.well_plots_layout.setColumnStretch(i, 1000)
                        self.well_plots_layout.setColumnMinimumWidth(i, 1000)
                    else:
                        self.well_plots_layout.setColumnStretch(i, 0)
                        self.well_plots_layout.setColumnMinimumWidth(i, 0)

        else:
            for count in range(8):
                if count < 4:
                    self.well_plots_layout.addWidget(self.well_plots[count], 0, count, 1, 1)
                else:
                    self.well_plots_layout.addWidget(self.well_plots[count], 1, count - 4, 1, 1)
                self.well_plots[count].show()
            self.well_plots_layout.setRowStretch(0, 1000)
            self.well_plots_layout.setRowMinimumHeight(0, 1000)
            self.well_plots_layout.setRowStretch(1, 1000)
            self.well_plots_layout.setRowMinimumHeight(1, 1000)
            for i in range(4):
                self.well_plots_layout.setColumnStretch(i, 1000)
                self.well_plots_layout.setColumnMinimumWidth(i, 1000)

        for i in range(self.well_plots_layout.columnCount()):
            self.well_plots_layout.setColumnStretch(i, 1000)
        for i in range(self.well_plots_layout.rowCount()):
            self.well_plots_layout.setRowStretch(i, 1000)

        for count, data in enumerate(self.well_checkbox_queue):
            x = data[0]
            y = data[1]
            peak_profile = data[2]
            title = str(self.plate_combobox.currentIndex()+1) + chr(65+y) + str(x+1)
            ch1_data = []
            ch2_data = []
            ch3_data = []
            ch4_data = []
            for i in peak_profile:
                ch1_data.append(i[0])
                ch2_data.append(i[1])
                ch3_data.append(i[2])
                ch4_data.append(i[3])
            ch1_data = np.array(ch1_data).astype(float)
            ch2_data = np.array(ch2_data).astype(float)
            ch3_data = np.array(ch3_data).astype(float)
            ch4_data = np.array(ch4_data).astype(float)
            if mode == 1:
                self.well_plots[y].plot(ch1_data, name=ch1_name, pen='g', symbol=None)
                self.well_plots[y].plot(ch2_data, name=ch2_name, pen='r', symbol=None)
                self.well_plots[y].plot(ch3_data, name=ch3_name, pen='b', symbol=None)
                self.well_plots[y].plot(ch4_data, name=ch4_name, pen='m', symbol=None)
            else:
                self.well_plots[count].plot(ch1_data, name=ch1_name, pen='g', symbol=None)
                self.well_plots[count].plot(ch2_data, name=ch2_name, pen='r', symbol=None)
                self.well_plots[count].plot(ch3_data, name=ch3_name, pen='b', symbol=None)
                self.well_plots[count].plot(ch4_data, name=ch4_name, pen='m', symbol=None)
                self.well_plots[count].setTitle(title)
        if mode == 1:
            col = self.well_checkbox_queue[0][0]
            for well in range(8):
                title = str(self.plate_combobox.currentIndex() + 1) + chr(65 + well) + str(col + 1)
                self.well_plots[well].setTitle(title)


    def run_extraction(self, thread_index, threshold, peaks_threshold, width_min, width_max, width_enable, peak_enable, channel, stats, threshold_check):
        self.extraction_thread_state[thread_index] = ThreadState.RUNNING
        self.update_file_color()
        self.thread[thread_index] = QtCore.QThread()
        worker = ExtractWorker()
        worker.moveToThread(self.thread[thread_index])
        self.thread[thread_index].started.connect(partial(worker.run, ui, self.file_dict_list[thread_index], threshold,
                                                            peaks_threshold, stats, threshold_check, width_min, width_max,
                                                            width_enable, peak_enable, channel))
        worker.progress.connect(self.extracton_progress_update)
        worker.finished.connect(self.thread[thread_index].quit)
        worker.finished.connect(worker.deleteLater)
        self.thread[thread_index].finished.connect(partial(self.extract_worker_finished, thread_index))
        self.thread[thread_index].finished.connect(self.thread[thread_index].deleteLater)
        self.thread[thread_index].start()

    def extract_worker_finished(self, thread_index: int):
        """function called update state of extract thread"""
        if thread_index < len(self.extraction_thread_state):
            self.extraction_thread_state[thread_index] = ThreadState.FINISHED
            self.update_file_color()
        else:
            logging.INFO("Thread index out of range")
        if self.extraction_queue:
            arg = self.extraction_queue.pop(0)
            logging.info(arg)
            self.run_extraction(*arg)


    def extracton_progress_update(self, progress):
        """function called to update the progress bar of the main menu"""
        self.pbar.setValue(int(progress[0]))
        self.progress_label.setText(progress[1])


class ExtractWorker(QtCore.QObject):
    """This class will be called to run extraction process"""
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(list)

    def run(self, ui, current_file_dict, threshold, peaks_threshold, stats, threshold_check,
            width_min=0, width_max=200, width_enable=True, peak_enable=False, channel=0):

        analog_file = Analysis.file_extracted_data_Qing(self, current_file_dict, threshold,
                                                        peaks_threshold, width_min, width_max,
                                                        width_enable, peak_enable, channel, 200,
                                                        0, stats.ch1_hit, stats.ch2_hit, stats.ch3_hit, stats.ch12_hit,
                                                        stats.ch13_hit,
                                                        stats.ch23_hit, stats.Droplet_Record_hit,
                                                        stats.total_sorted, rethreshold=threshold_check)

        logging.info("Extraction done, updating file")
        ui.analog.update(analog_file)
        ui.update_working_data()

        # direct everything into window filters
        # self.draw is histogram
        # self.draw_2 triggers 2nd and 3rd filter
        #if ui.data_updated == True:
          #  ui.update_sweep_graphs(True)

        #ui.update_statistic()
        logging.info("Worker finished")
        self.finished.emit()

class WellsCheckBox(QtWidgets.QCheckBox):
    """this is the checkbox that will hold its position"""
    def __init__(self, x, y):
        super(WellsCheckBox, self).__init__()
        self.x = x
        self.y = y


if __name__ == "__main__":
    freeze_support()
    import sys

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
