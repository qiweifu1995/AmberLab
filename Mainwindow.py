# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AmberLab_detailed2.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtGui  # Place this at the top of your file.
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, \
    QWidget, QLineEdit, QTextEdit

from PyQt5.QtWidgets import QTreeView
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor

from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point
import pyqtgraph as pg

import pandas as pd
import os
import Helper
import Analysis
import time
from itertools import islice, compress
from pyqtgraph import PlotWidget
import numpy as np

import pyqtgraph as pg
import statistics
from scipy.signal import savgol_filter
import csv

import matplotlib.path as mpltPath
import concurrent.futures
from multiprocessing import freeze_support
from math import sqrt
import math
import pickle


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
        
### pop-up window for change the sampling rate in main tab (Resample button)
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
        # if number entered, "ui.textEdit" will be edited. 
        # "ui." means the main class "Ui_MainWindow". Use "Self." when calling in main class
        
        self.hide() 
        Ui_MainWindow.OtherWindow_Button_ok_clicked(Ui_MainWindow,self.lineEdit.text())

        ui.textbox = ui.textbox + "\n" + "Resamole set to " +  str(self.lineEdit.text())        
        ui.textEdit.setPlainText(ui.textbox) 
        
        
    def close_clicked(self):
        self.hide()      

### pop-up window end


### Pop-up windows for the new filters
class window_filter(QWidget):
    def __init__(self,parent = None):
        super().__init__()   
        
        
        # tree_index saved the index number for all filters, include its parent and child branch
        # ex. index = 0,1,1 means: select filter index is "No.1", under parent "No.1", upder grand-parent "No.0"
        
        self.tree_index = ui.tree_index
        
        self.quadrant1_list_or_polygon = []
        
        # export parent index
        # ex. index = 0,1,1 ; parent index = 0,1
        if self.tree_index != (0,):
            parent_index = self.tree_index[1:]
            self.quadrant1_list_or_polygon = ui.tree_dic[parent_index]['quadrant1_list_or_polygon']
 


        
    
         #############################################   #############################################   
        # main filter tab
        
        ### layout setup
        outter_layout = QtWidgets.QHBoxLayout()
        vertical_layout = QtWidgets.QVBoxLayout()
        layout = QtWidgets.QGridLayout()
        Multi_peaks_layout = QtWidgets.QGridLayout()
        Scatter_plot_layout = QtWidgets.QGridLayout()
        
        
        ### control pannels
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        # edit filter name 
        self.label_filter_name = QLabel("Filter Name:")
        Scatter_plot_layout.addWidget(self.label_filter_name, 1, 0, 1, 1)
        
        self.lineedit_filter_name = QtWidgets.QLineEdit('')
        Scatter_plot_layout.addWidget(self.lineedit_filter_name, 1, 1, 1, 1)
        
        self.line_filter_name = QtWidgets.QFrame()
        self.line_filter_name.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_filter_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_filter_name, 2, 0, 1, 4)
        
        # some thresholds
        self.label_Axes = QLabel("Scatter Plot Axes")
        sizePolicy.setHeightForWidth(self.label_Axes.sizePolicy().hasHeightForWidth())
        self.label_Axes.setSizePolicy(sizePolicy)
        Scatter_plot_layout.addWidget(self.label_Axes, 3, 0, 1, 1)
        
        self.label_x_Axis = QLabel("X-Axis")
        Scatter_plot_layout.addWidget(self.label_x_Axis, 4, 0, 1, 1)
        
        self.label_y_Axis = QLabel("Y-Axis")
        Scatter_plot_layout.addWidget(self.label_y_Axis, 5, 0, 1, 1)
        
        ### Check box layout
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItem("Height")
        self.comboBox_1.addItem("Width")

        
        
        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItem("Height")
        self.comboBox_2.addItem("Width")        
        
        
        self.comboBox_3 = QtWidgets.QComboBox()
        self.comboBox_3.addItem("Green")
        self.comboBox_3.addItem("Far Red") 
        self.comboBox_3.addItem("Ultra Violet") 
        self.comboBox_3.addItem("Orange") 
        
        self.comboBox_4 = QtWidgets.QComboBox()
        self.comboBox_4.addItem("Green")
        self.comboBox_4.addItem("Far Red") 
        self.comboBox_4.addItem("Ultra Violet") 
        self.comboBox_4.addItem("Orange")         

        Scatter_plot_layout.addWidget(self.comboBox_1, 4, 1, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_2, 5, 1, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_3, 4, 2, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_4, 5, 2, 1, 1)
        
        
        
        self.GateVoltage_x = QtWidgets.QLineEdit('')
        Scatter_plot_layout.addWidget(self.GateVoltage_x, 4, 3, 1, 1)
        self.GateVoltage_y = QtWidgets.QLineEdit('')
        Scatter_plot_layout.addWidget(self.GateVoltage_y, 5, 3, 1, 1)
        
        
        self.line_Scatter_plot = QtWidgets.QFrame()
        self.line_Scatter_plot.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Scatter_plot.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_Scatter_plot, 6, 0, 1, 4)
        
    
    
    
    
        # Multi_peaks_layout grid
        
        self.label_num_peak_title = QtWidgets.QLabel('Multi Peaks Gating')
        sizePolicy.setHeightForWidth(self.label_num_peak_title.sizePolicy().hasHeightForWidth())
        self.label_num_peak_title.setSizePolicy(sizePolicy)
        Multi_peaks_layout.addWidget(self.label_num_peak_title)
        
        self.label_num_peak_1 = QtWidgets.QLabel('Channel')
        sizePolicy.setHeightForWidth(self.label_num_peak_1.sizePolicy().hasHeightForWidth())
        self.label_num_peak_1.setSizePolicy(sizePolicy)
        
        self.label_num_peak_2 = QtWidgets.QLabel('Condition')
        sizePolicy.setHeightForWidth(self.label_num_peak_2.sizePolicy().hasHeightForWidth())
        self.label_num_peak_2.setSizePolicy(sizePolicy)
        
        self.label_num_peak_3 = QtWidgets.QLabel('# of Peaks')
        sizePolicy.setHeightForWidth(self.label_num_peak_3.sizePolicy().hasHeightForWidth())
        self.label_num_peak_3.setSizePolicy(sizePolicy)
        
        self.label_num_peak_4 = QtWidgets.QLabel('Green')
        self.label_num_peak_5 = QtWidgets.QLabel('Red')
        self.label_num_peak_6 = QtWidgets.QLabel('Blue')
        self.label_num_peak_7 = QtWidgets.QLabel('Orange')

        Multi_peaks_layout.addWidget(self.label_num_peak_1, 1, 0)
        Multi_peaks_layout.addWidget(self.label_num_peak_2, 1, 1)
        Multi_peaks_layout.addWidget(self.label_num_peak_3, 1, 2)
        Multi_peaks_layout.addWidget(self.label_num_peak_4, 2, 0)
        Multi_peaks_layout.addWidget(self.label_num_peak_5, 3, 0)
        Multi_peaks_layout.addWidget(self.label_num_peak_6, 4, 0)
        Multi_peaks_layout.addWidget(self.label_num_peak_7, 5, 0)
        
        self.comboBox_peak_num_1 = QtWidgets.QComboBox()
        self.comboBox_peak_num_1.addItem(">=")
        self.comboBox_peak_num_1.addItem("==")
        self.comboBox_peak_num_1.addItem("<=")
        
        self.comboBox_peak_num_2 = QtWidgets.QComboBox()
        self.comboBox_peak_num_2.addItem(">=")
        self.comboBox_peak_num_2.addItem("==")
        self.comboBox_peak_num_2.addItem("<=")
        
        self.comboBox_peak_num_3 = QtWidgets.QComboBox()
        self.comboBox_peak_num_3.addItem(">=")
        self.comboBox_peak_num_3.addItem("==")
        self.comboBox_peak_num_3.addItem("<=")
        
        self.comboBox_peak_num_4 = QtWidgets.QComboBox()
        self.comboBox_peak_num_4.addItem(">=")
        self.comboBox_peak_num_4.addItem("==")
        self.comboBox_peak_num_4.addItem("<=")
        
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_1, 2, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_2, 3, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_3, 4, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_4, 5, 1)
        
        self.lineEdit_peak_num_1 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_2 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_3 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_4 = QtWidgets.QLineEdit('0')

        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_1, 2, 2,1,1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_2, 3, 2,1,1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_3, 4, 2,1,1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_4, 5, 2,1,1)

        self.line_Multi_peaks = QtWidgets.QFrame()
        self.line_Multi_peaks.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Multi_peaks.setFrameShadow(QtWidgets.QFrame.Sunken)
        Multi_peaks_layout.addWidget(self.line_Multi_peaks, 6, 0, 1, 3)

        # Multi peak end

        
        self.line_Multi_peaks = QtWidgets.QFrame()
        self.line_Multi_peaks.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Multi_peaks.setFrameShadow(QtWidgets.QFrame.Sunken)
        Multi_peaks_layout.addWidget(self.line_Multi_peaks, 6, 0, 1, 3)
        
        
        self.label_dots_inside_polygon = QLabel("Inside : 0")
        sizePolicy.setHeightForWidth(self.label_dots_inside_polygon.sizePolicy().hasHeightForWidth())
        self.label_dots_inside_polygon.setSizePolicy(sizePolicy)
#         self.label_8.setMinimumSize(QtCore.QSize(80, 0))
#         self.label_8.setMaximumSize(QtCore.QSize(100, 16777215))
#         self.label_8.setObjectName("label_8")
        layout.addWidget(self.label_dots_inside_polygon, 9, 0, 1, 1)

               
        
        self.polygon_button_1 =  QPushButton('Polygon')
        self.polygon_button_2 =  QPushButton('Clear')
        self.polygon_button_3 =  QPushButton('Shape Edit')
        
        
#         self.button_rename.setSizePolicy(sizePolicy)
        self.polygon_button_3.setMinimumSize(QtCore.QSize(120, 0))
        
        layout.addWidget(self.polygon_button_1, 10, 0, 1, 1)
        layout.addWidget(self.polygon_button_2, 10, 1, 1, 1)
        layout.addWidget(self.polygon_button_3, 10, 2, 1, 1)        
        
        
        

        
      
        # confirm buttons
        
        self.pushButton_confirm = QPushButton('Update')
        layout.addWidget(self.pushButton_confirm, 8, 0, 1, 1)
        
        self.pushButton_1 = QPushButton('Next Filter')
        self.pushButton_2 = QPushButton('Close')  
        self.pushButton_3 = QPushButton('Export Linear Plot')
        

        layout.addWidget(self.pushButton_1, 11, 0, 1, 1)
        layout.addWidget(self.pushButton_2, 11, 1, 1, 1)
        layout.addWidget(self.pushButton_3, 11, 2, 1, 1)
        
        self.pushButton_4 = QPushButton('Export to Sweep1') 
        layout.addWidget(self.pushButton_4, 13, 0, 1, 2)
        self.pushButton_5 = QPushButton('Export to Sweep2') 
        layout.addWidget(self.pushButton_5, 13, 3, 1, 2)
        






        ### Quadrants table
        
    
        self.tableView_scatterquadrants = QtWidgets.QTableWidget()
#         self.tableView_scatterquadrants.setObjectName("tableView_scatterquadrants")
        self.tableView_scatterquadrants.setMaximumSize(QtCore.QSize(1000, 90))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_scatterquadrants.sizePolicy().hasHeightForWidth())
        self.tableView_scatterquadrants.setSizePolicy(sizePolicy)   
        
        layout.addWidget(self.tableView_scatterquadrants, 12, 0, 1, 6)
        
        # set row count
        self.tableView_scatterquadrants.setRowCount(1)
        # set column count
        self.tableView_scatterquadrants.setColumnCount(7)
        self.tableView_scatterquadrants.setHorizontalHeaderLabels(('Count', '% Total Peaks', '% Total Droplets', 'X Single Peak %',
                                                                   'Y Single Peak %', 'X Multi Peak %', 'Y Multi Peak %'))
        self.tableView_scatterquadrants.setVerticalHeaderLabels(
            ('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))
        
        self.tableView_scatterquadrants.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
#         self.tableView_scatterquadrants.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
        ### graph
        self.graphWidget = PlotWidget(title=' ')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Green')
        self.graphWidget.setLabel('bottom', 'Far Red')
        
        # add threshold
        pen = pg.mkPen(color=(0, 120, 180),width = 5)
        self.lr_x_axis = pg.InfiniteLine(0, movable=True, pen = pen)
        self.graphWidget.addItem(self.lr_x_axis) 
        self.lr_y_axis = pg.InfiniteLine(0, movable=True, pen = pen, angle=0)
        self.graphWidget.addItem(self.lr_y_axis) 
        
        
        # retrive data from last window
        

        ### Tab control   
        self.tab_widgets_main = QtWidgets.QTabWidget()
        outter_layout.addWidget(self.tab_widgets_main)
        
        vertical_layout.addLayout(Scatter_plot_layout)
        vertical_layout.addLayout(Multi_peaks_layout) 
        vertical_layout.addLayout(layout) 
        
        
        # tab1
        self.tab_1 = QtWidgets.QWidget()
        self.tab_widgets_main.addTab(self.tab_1,'Scatter Plot')
        
        Scatter_layout = QtWidgets.QHBoxLayout(self.tab_1)        
        Scatter_layout.addWidget(self.graphWidget)
        Scatter_layout.addLayout(vertical_layout)
        
        # tab2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_widgets_main.addTab(self.tab_2, "Histogram")
        
        # tab4
        self.tab_4 = QtWidgets.QWidget()
        self.tab_widgets_main.addTab(self.tab_4, "Linear Plot")
        
        ### layout finish
        self.setLayout(outter_layout)
        
        ### triggers
        self.pushButton_1.clicked.connect(self.ok_clicked)
        self.pushButton_2.clicked.connect(self.close_clicked)
        self.pushButton_3.clicked.connect(self.polygon_linear_plot_triggered_from_scatter_subtab)


        self.pushButton_confirm.clicked.connect(self.draw_graphwidget)
        self.lr_x_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        self.lr_y_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        
        
        self.GateVoltage_x.editingFinished.connect(self.infiniteline_lineedit_update)
        self.GateVoltage_y.editingFinished.connect(self.infiniteline_lineedit_update)
        
        self.polygon_button_1.clicked.connect(self.polygon_triggering)
        self.polygon_button_2.clicked.connect(self.polygon_clean)
        self.polygon_button_3.clicked.connect(self.edit_polygon_shape)
                            
        self.pushButton_4.clicked.connect(self.update_sweep_left)
        self.pushButton_5.clicked.connect(self.update_sweep_right)
        # using polygon function now?
        self.polygon_trigger = False
        
        # end polygon edit function?
        self.stop_edit_trigger = True
        
        self.x = []
        self.y = []
        self.polygon = []
        self.points_inside = []
        self.graphWidget.scene().sigMouseClicked.connect(self.onMouseMoved)
        
                        
         #############################################   #############################################   
        # histogram part
        # Setup layouts
 
        Control_layout = QtWidgets.QGridLayout()
        # setup histogram graph
        
        self.histogram_graphWidget = PlotWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram_graphWidget.sizePolicy().hasHeightForWidth())
        self.histogram_graphWidget.setSizePolicy(sizePolicy)
        self.histogram_graphWidget.setMinimumSize(QtCore.QSize(700, 499))
        self.histogram_graphWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.histogram_graphWidget.setObjectName("histogram_graphWidget")
        styles = {"color": "r", "font-size": "20px"}
        self.histogram_graphWidget.setLabel('left', 'Frequency', **styles)
        self.histogram_graphWidget.setBackground('w')
        self.histogram_graphWidget.setXRange(1, 10.5, padding=0)
        self.histogram_graphWidget.setYRange(1, 10.5, padding=0)
        
        
  
        self.histogram_comboBox_1 = QtWidgets.QComboBox()
        self.histogram_comboBox_1.addItem("Height")
        self.histogram_comboBox_1.addItem("Width")

        
        
        self.histogram_comboBox_2 = QtWidgets.QComboBox()
        self.histogram_comboBox_2.addItem("Green")
        self.histogram_comboBox_2.addItem("Far Red") 
        self.histogram_comboBox_2.addItem("Ultra Violet") 
        self.histogram_comboBox_2.addItem("Orange") 

        Control_layout.addWidget(self.histogram_comboBox_1, 4, 0, 1, 1)
        Control_layout.addWidget(self.histogram_comboBox_2, 5, 0, 1, 1)
        

        # graph parameters adjust
        self.label_bin_width = QLabel("Binwidth")
        Control_layout.addWidget(self.label_bin_width, 6, 0, 1, 1)
        
        self.histogram_binwidth = QtWidgets.QLineEdit('0.2')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram_binwidth.sizePolicy().hasHeightForWidth())
        self.histogram_binwidth.setSizePolicy(sizePolicy)
        
        Control_layout.addWidget(self.histogram_binwidth, 6, 1, 1, 1)
        
        # gate voltage
        self.label_gate_voltage = QLabel("Gate Voltage")
        Control_layout.addWidget(self.label_gate_voltage, 7, 0, 1, 1)
        
        self.histogram_gate_voltage = QtWidgets.QLineEdit('0')
        self.histogram_gate_voltage.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.histogram_gate_voltage, 7, 1, 1, 1)
        
        # percentage
        
        self.label_percentage = QLabel("Percentage:   %")
        self.label_percentage.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_percentage, 8, 0, 1, 1)
        
        self.label_percentage_all = QLabel("Percentage:   %")
        self.label_percentage_all.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_percentage_all, 9, 0, 1, 1)        
        
        # buttons
        self.histogram_pushButton_1 = QPushButton('Update')       

        Control_layout.addWidget(self.histogram_pushButton_1, 10, 0, 1, 1)
        
        
        # Finish layouts
        
        Histogram_layout = QtWidgets.QHBoxLayout(self.tab_2)        
        Histogram_layout.addWidget(self.histogram_graphWidget)
        
        Histogram_layout.addLayout(Control_layout)
        
        # triggers
        self.histogram_pushButton_1.clicked.connect(self.draw_histogram)
        

        ############################################################################################
        # linear plot part
        # copied from the main window, the naming may looks strange. But it works

        #### subtab polygon linear graph
        
        self.horizontalLayout_151 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_151.setObjectName("horizontalLayout_151")
        self.verticalLayout_52 = QtWidgets.QVBoxLayout()
        self.verticalLayout_52.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_52.setObjectName("verticalLayout_52")
        self.gridLayout_42 = QtWidgets.QGridLayout()
        self.gridLayout_42.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.label_181 = QtWidgets.QLabel("Channel Selection")
        self.label_181.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_181, 0, 0, 1, 2)
        self.label_183 = QtWidgets.QLabel("*Peak difference < 15")
        self.label_183.setAlignment(QtCore.Qt.AlignCenter)

        self.gridLayout_42.addWidget(self.label_183, 7, 0, 1, 2)
        
        # pushbuttons
        self.pushButton_6 = QtWidgets.QPushButton("Generate Plot")
        self.gridLayout_42.addWidget(self.pushButton_6, 8, 0, 1, 2)
        self.pushButton_8 = QtWidgets.QPushButton("Last Page")
        self.gridLayout_42.addWidget(self.pushButton_8, 11, 0, 1, 2)
        self.pushButton_7 = QtWidgets.QPushButton("Next Page")
        self.gridLayout_42.addWidget(self.pushButton_7, 12, 0, 1, 2)

        
        self.label_180 = QtWidgets.QLabel("Start Peak")
        self.label_180.setAlignment(QtCore.Qt.AlignCenter)
    
        self.gridLayout_42.addWidget(self.label_180, 3, 0, 1, 1)
        self.label_182 = QtWidgets.QLabel("End Peak")
        self.label_182.setAlignment(QtCore.Qt.AlignCenter)

        self.gridLayout_42.addWidget(self.label_182, 5, 0, 1, 1)
        

        self.lineEdit_36 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_36.sizePolicy().hasHeightForWidth())
        self.lineEdit_36.setSizePolicy(sizePolicy)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.gridLayout_42.addWidget(self.lineEdit_36, 3, 1, 1, 1)
        
        
        self.lineEdit_37 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_37.sizePolicy().hasHeightForWidth())
        self.lineEdit_37.setSizePolicy(sizePolicy)
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.gridLayout_42.addWidget(self.lineEdit_37, 6, 1, 1, 1)
        
        self.label_188 = QtWidgets.QLabel("Custom Sample Size")
        self.label_188.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_188, 6, 0, 1, 1)
        
        

        self.comboBox_14 = QtWidgets.QComboBox(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_14.sizePolicy().hasHeightForWidth())
        self.comboBox_14.setSizePolicy(sizePolicy)
        self.comboBox_14.setObjectName("comboBox_13")

        self.gridLayout_42.addWidget(self.comboBox_14, 1, 0, 1, 2)
        

        self.lineEdit_38 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_38.sizePolicy().hasHeightForWidth())
        self.lineEdit_38.setSizePolicy(sizePolicy)
        self.lineEdit_38.setObjectName("lineEdit_38")
        self.gridLayout_42.addWidget(self.lineEdit_38, 5, 1, 1, 1)
        

        self.lineEdit_36.setText("0")
        self.lineEdit_38.setText("5")
        self.lineEdit_37.setText("0")
        
        



        self.layout_vertical_checkbox_3 = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox_3.setObjectName("layout_vertical_checkbox_3")
        
        self.polygon_channel_1 = QtWidgets.QCheckBox("Channel_1")
        self.polygon_channel_2 = QtWidgets.QCheckBox("Channel_2")
        self.polygon_channel_3 = QtWidgets.QCheckBox("Channel_3")
        self.polygon_channel_4 = QtWidgets.QCheckBox("Channel_4")
        
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_1)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_2)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_3)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_4)

        self.polygon_channel_1.setChecked(True)
        self.polygon_channel_2.setChecked(True)
        self.polygon_channel_3.setChecked(True)
        self.polygon_channel_4.setChecked(True)

        self.gridLayout_42.addItem(self.layout_vertical_checkbox_3, 14, 0, 1,2 )
        

        self.label_187 = QtWidgets.QLabel("Smoothing")
        self.label_187.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_187, 15, 0, 1, 2)
        
        self.polygon_Smooth_enable = QtWidgets.QCheckBox("Smooth Enable")

        self.gridLayout_42.addWidget(self.polygon_Smooth_enable, 16, 0, 1, 2)        
        

        self.lineEdit_39 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_39.sizePolicy().hasHeightForWidth())
        self.lineEdit_39.setSizePolicy(sizePolicy)
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.gridLayout_42.addWidget(self.lineEdit_39, 17, 1, 1, 1)

        

        self.lineEdit_40 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_40.sizePolicy().hasHeightForWidth())
        self.lineEdit_40.setSizePolicy(sizePolicy)
        self.lineEdit_40.setObjectName("lineEdit_40")
        self.gridLayout_42.addWidget(self.lineEdit_40, 18, 1, 1, 1)


        self.lineEdit_39.setText("7")
        self.lineEdit_40.setText("29")
        
        
        

        self.label_185 = QtWidgets.QLabel("Polynomial Order")
        self.label_185.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_185, 17, 0, 1, 1)

        self.label_186 = QtWidgets.QLabel("Smooth Level")
        self.label_186.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_186, 18, 0, 1, 1)  

        
        
        spacerItem28 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_42.addItem(spacerItem28, 13, 0, 1, 2)        
        
        spacerItem27 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_42.addItem(spacerItem27, 9, 0, 1, 2)
        

        self.label_184 = QtWidgets.QLabel("Last/Next")
        self.label_184.setAlignment(QtCore.Qt.AlignCenter)

        self.gridLayout_42.addWidget(self.label_184, 10, 0, 1, 2)
        self.verticalLayout_52.addLayout(self.gridLayout_42)
        
        spacerItem29 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_52.addItem(spacerItem29)
        
        self.horizontalLayout_151.addLayout(self.verticalLayout_52)
        
        self.line_101 = QtWidgets.QFrame(self.tab_4)
        self.line_101.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_101.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_101.setObjectName("line_101")
        self.horizontalLayout_151.addWidget(self.line_101)
        

        self.widget_29 = PlotWidget(self.tab_4)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_29.sizePolicy().hasHeightForWidth())
        self.widget_29.setSizePolicy(sizePolicy)
        self.widget_29.setMinimumSize(QtCore.QSize(500, 500))
        self.widget_29.setObjectName("widget_29")
        self.horizontalLayout_151.addWidget(self.widget_29)
        
        

        styles = {"color": "r", "font-size": "20px"}
        self.widget_29.setLabel('left', 'Height', **styles)
        self.widget_29.setBackground('w')
        
         # triggers
        self.pushButton_6.clicked.connect(self.polygon_reset_linear_plot)
        self.pushButton_8.clicked.connect(self.polygon_last_page)
        self.pushButton_7.clicked.connect(self.polygon_next_page)  
        

        self.reset_comboBox = True
    
        #### linear end
        ##########################################################################################
        
        
    # update the left and right sweep graphs on the sweep tab
    def update_sweep_left(self):
        ui.sweep_left = [[],[],[],[]]
        for ch in range(len(ui.working_data)):
            ui.sweep_left[ch] = [ui.working_data[ch][i] for i in self.points_inside]
        ui.update_sweep_1(data_updated=True)

    def update_sweep_right(self):
        ui.sweep_right = [[],[],[],[]]
        for ch in range(len(ui.working_data)):
            ui.sweep_right[ch] = [ui.working_data[ch][i] for i in self.points_inside]    
        ui.update_sweep_2(data_updated=True)

        
    # two ways to trigger the linear plot: 
    # 1. from the linear plot tab, "generate plot" button, (more like a "reset" button)
    # 2. from main filter tab, "export leaner plot button" 
    # This is the trigger 2 from the main filter tab
    def polygon_linear_plot_triggered_from_scatter_subtab(self):
        # reset upper and lower bond
        self.lineEdit_36.setText("0")
        self.lineEdit_38.setText("5")
        self.lineEdit_37.setText("0")
        
        self.reset_comboBox = True
        self.polygon_linear_plot()
        
    # This is the trigger 1 from the linear tab
    def polygon_reset_linear_plot(self):
        self.polygon_linear_plot()
        self.widget_29.autoRange()
        
    # filp pages funtion in linear plot
    def polygon_last_page(self):
        lower_bond = int(self.lineEdit_36.text())
        upper_bond = int(self.lineEdit_38.text())
        nrows = upper_bond - lower_bond        
        
        self.lineEdit_36.setText(str(lower_bond - nrows))
        self.lineEdit_38.setText(str(upper_bond - nrows))
        
        self.polygon_linear_plot()
        
    def polygon_next_page(self):
        lower_bond = int(self.lineEdit_36.text())
        upper_bond = int(self.lineEdit_38.text())
        nrows = upper_bond - lower_bond        
        
        self.lineEdit_36.setText(str(lower_bond + nrows))
        self.lineEdit_38.setText(str(upper_bond + nrows))

        self.polygon_linear_plot()        
           
    # main linear plot function
    def polygon_linear_plot(self):
        
        # auto switch tab
        self.tab_widgets_main.setCurrentIndex(2)
        
        # reset
        self.widget_29.clear()

                    

        ### to plot a linear graph, need to find the correct index in original .csv file, and trace back the correct index
        ### will extract later
        if self.reset_comboBox == True:
            self.comboBox_14.clear() 

            for list_index in ui.comboBox_14_list:
                list_text = ui.comboBox_14_list[list_index]
                
                polygon_length = 0
                for i in range(list_index):
                    polygon_length += len(ui.analog[ui.current_file_dict[ui.comboBox_14_list[i]]][0][0])

                polygon_length_end = polygon_length + len(ui.analog[ui.current_file_dict[list_text]][0][0])                       
                index_in_all_selected_channel = [x for x, x in enumerate(self.points_inside) if x > polygon_length and x <= polygon_length_end]

                if index_in_all_selected_channel != []:
                    self.comboBox_14.addItem(str(list_text))  

        self.reset_comboBox = False
        
        key_list = list(ui.comboBox_14_list.keys())
        val_list = list(ui.comboBox_14_list.values())

        position = val_list.index(self.comboBox_14.currentText())
        polygon_index = key_list[position]
        polygon_text = self.comboBox_14.currentText()
        
        polygon_length = 0
        
        for i in range(polygon_index):
            polygon_length += len(ui.analog[ui.current_file_dict[ui.comboBox_14_list[i]]][0][0])
               
        polygon_length_end = polygon_length + len(ui.analog[ui.current_file_dict[polygon_text]][0][0])
        
        ### trace end
        
        
        
        
        # get the points after filtering
        index_in_all_selected_channel = [x for x, x in enumerate(self.points_inside) if x >= polygon_length and x <= polygon_length_end]
        index_in_current_channel = [x - polygon_length for x in index_in_all_selected_channel]

        
        ### find data in csv file
        text1 = self.comboBox_14.currentText()
        header = 0
        
        # custom sample size in linear tab, allow user to switch sample size in the filter tab
        try:
            if int(self.lineEdit_37.text())>0:
                sample_size = int(self.lineEdit_37.text())
                if text1 == "Peak Record":
                    header = 2
            else:
                sample_size = self.chunksize
                if text1 == "Peak Record":
                    header = 2
                    sample_size = 200
        except:
            sample_size = 200
            if text1 == "Peak Record":
                header = 2
                sample_size = 200
    
    
    
    
        ### extract original points from .csv file, use parameters on the tab
        upper_bond = int(self.lineEdit_38.text())
        lower_bond = int(self.lineEdit_36.text())
        if lower_bond < len(index_in_current_channel):
            
            # fix exceeded upper bond
            if len(index_in_current_channel) < upper_bond :
                upper_bond  = len(index_in_current_channel)
                self.lineEdit_38.setText(str(upper_bond))
            nrows = upper_bond - lower_bond
            
            if nrows>15:
                self.lineEdit_38.setText(str(lower_bond + 15))
                nrows = 15        
            self.subgating_file_dict = ui.file_dict_list[ui.file_list_view.currentRow()]
            os.chdir(self.subgating_file_dict["Root Folder"])
            file = self.subgating_file_dict[text1]    

            data = pd.DataFrame({0: [],1: [], 2: [],3: []},)

            print("index_in_current_channel",len(index_in_current_channel),':',index_in_current_channel)

            for x in range(lower_bond,upper_bond):
                i = index_in_current_channel[x]
                skip_rows = i * sample_size 
                polygon_data = pd.read_csv(file, skiprows = skip_rows, nrows=sample_size, header=header) 
                length = len(polygon_data.columns) 
                polygon_data.columns = list(range(0,length))
                data = pd.concat([data,polygon_data])


            height_data = data[0].values.tolist()
            height_index = list(range(len(height_data)))

            poly_degree = int(self.lineEdit_39.text())
            window_length = int(self.lineEdit_40.text())//2 *2-1
            self.widget_29.addLegend()  


            for i in range(0,sample_size * nrows,sample_size):         
                self.widget_29.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))


            if self.polygon_Smooth_enable.isChecked():
                if self.polygon_channel_1.isChecked():
                    height_data = savgol_filter(data[0], window_length, poly_degree)
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    height_data = savgol_filter(data[1], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    height_data = savgol_filter(data[2], window_length, poly_degree)
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            else:
                if self.polygon_channel_1.isChecked():
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index,data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index,data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index,data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index,data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
        else: 
            print("Enter a new lower bond value")
            
            

        self.widget_29.autoRange()        
        
        
    # histogram tab main function
    def draw_histogram(self):
        try:
            points_inside_square = self.points_inside_square
        except:
            self.draw_graphwidget()
        
        
        if self.histogram_comboBox_1.currentIndex() == 0:
            self.width = ui.working_data[self.histogram_comboBox_2.currentIndex()]  
        else:
            self.width = ui.peak_width_working_data[self.histogram_comboBox_2.currentIndex()]    
            
        self.full_width = [ self.width[i] for i in self.points_inside_square]

        
        self.width = [x for x in self.full_width if x >= float(self.histogram_gate_voltage.text())]
            

        width_count_filtered = round(100 * len(self.width) / len(self.full_width), 2)
        width_count = "Percentage: " + str(width_count_filtered) + '% of filtered points ' + str(len(self.width)) + '/' + str(len(self.full_width))
        self.label_percentage.setText(width_count)
           
        percentage_all_count = round(100 * len(self.width) / len(ui.working_data[0]), 2)
        percentage_all =  "Percentage: " + str(percentage_all_count) + '% of all points ' + str(len(self.width)) + '/' + str(len(ui.working_data[0]))
        self.label_percentage_all.setText(percentage_all)
            
            
        channel = self.histogram_comboBox_2.currentIndex()
          
        self.histogram_graphWidget.clear()
        r, g, b = Helper.rgb_select(channel)
        styles = {"color": "r", "font-size": "20px"}
        axis_name = self.histogram_comboBox_2.currentText()
        self.histogram_graphWidget.setLabel('bottom', axis_name, **styles)   


        range_width = int(max(self.width)) + 1
        # test binwidth
        bin_edge = Helper.histogram_bin(range_width, float(self.histogram_binwidth.text()))
        y, x = np.histogram(self.width, bins=bin_edge)
        separate_y = [0] * len(y)

        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.histogram_graphWidget.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True,
                                            brush=(r, g, b))

        self.histogram_graphWidget.setXRange(float(self.histogram_gate_voltage.text()), max(x), padding=0)
        self.histogram_graphWidget.setYRange(0, max(y), padding=0)

        # after 1st map so the line layer will appear in front of the histogram
        self.data_line = self.histogram_graphWidget.plot([0, 0], [0, 0],
                                                         pen=pg.mkPen(color=('r'), width=5,
                                                                      style=QtCore.Qt.DashLine))        
        
        
        
        
    # functions used for count peak numbers
    def peak_num_comp(self, number_of_peak, mode, num_in):
        """function to do comparison for peak number filter"""
        if mode == 0:
            if number_of_peak >= num_in:
                return True
            else:
                return False
        elif mode == 1:
            if number_of_peak == num_in:
                return True
            else:
                return False
        elif mode == 2:
            if number_of_peak <= num_in:
                return True
            else:
                return False
        return False

    def peak_num_filter(self):
        """function for peak num filter, mode 0 is >=, mode 1 is ==, mode 2 is =< """
        self.peak_num_filtered_index = []
        holder = [[],[],[],[]]
        for ch in range(4):
            holder[ch] = [i for i, x in enumerate(ui.peak_num_working_data[ch])
                          if self.peak_num_comp(x, self.peak_num_mode[ch], self.peak_num_in[ch])]
        self.peak_num_filtered_index = list(set(holder[0]).intersection(set(holder[1]), set(holder[2]), set(holder[3])))
        print('holder[0]',holder[0])
        print('self.peak_num_filtered_index',self.peak_num_filtered_index)


        
    ### drawing function for main tab scatter pot 

    def draw_graphwidget(self):
        # "update" clicked
        # prepare data
        
        if self.quadrant1_list_or_polygon == []:
            points_inside_square = ui.width_index0
        else:
            points_inside_square = self.quadrant1_list_or_polygon
           
        # edit filter name
        
        
    # updatename to y vs.  x axis
        if self.lineedit_filter_name.text() == '':
            self_brach_name = str(self.comboBox_2.currentText() + " " + self.comboBox_4.currentText() + 'VS. ' +
                                 self.comboBox_1.currentText() + " " + self.comboBox_3.currentText())
            ui.tree_dic[self.tree_index]['tree_standarditem'].setText(self_brach_name)
            self.setWindowTitle(self_brach_name)
        else:
            self_brach_name = str(self.lineedit_filter_name.text())
            ui.tree_dic[self.tree_index]['tree_standarditem'].setText(self_brach_name)
            self.setWindowTitle(self_brach_name)            
        
        
        # check peak number filter
        self.peak_num_mode = []
        self.peak_num_in = []
        self.peak_num_mode.append(self.comboBox_peak_num_1.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_2.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_3.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_4.currentIndex())
        self.peak_num_in.append(int(self.lineEdit_peak_num_1.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_2.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_3.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_4.text()))
        
        if self.peak_num_mode != [0,0,0,0] or self.peak_num_in != [0,0,0,0]:
            self.peak_num_filter()
            points_inside_square = list(set(points_inside_square).intersection(set(self.peak_num_filtered_index)))
            
        self.points_inside_square = points_inside_square  
        # peak number filter end

        if self.comboBox_1.currentIndex() == 0:
            data_in_subgating_x = ui.working_data[self.comboBox_3.currentIndex()]  
        else:
            data_in_subgating_x = ui.peak_width_working_data[self.comboBox_3.currentIndex()]             

        if self.comboBox_2.currentIndex() == 0:
            data_in_subgating_y = ui.working_data[self.comboBox_4.currentIndex()] 
        else:
            data_in_subgating_y = ui.peak_width_working_data[self.comboBox_4.currentIndex()] 

                
        x_axis_channel = self.comboBox_3.currentIndex()
        y_axis_channel = self.comboBox_4.currentIndex()
        x_axis_name = self.comboBox_1.currentText() + " " + self.comboBox_3.currentText()
        y_axis_name = self.comboBox_2.currentText() + " " + self.comboBox_4.currentText()

        
        self.graphWidget.clear()
        self.graphWidget.setLabel('left', y_axis_name, color='b')
        self.graphWidget.setLabel('bottom', x_axis_name, color='b')   


        self.Ch1_channel0 = [ data_in_subgating_x[i] for i in self.points_inside_square]
        self.Ch1_channel1 = [ data_in_subgating_y[i] for i in self.points_inside_square]


                
        # test color setup
        max_voltage = 12
        bins = 1000
        steps = max_voltage / bins

        # all data is first sorted into a histogram
        histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins,
                                     [[0, max_voltage], [0, max_voltage]],
                                     density=True)
        max_density = histo.max()
        percentage_coefficient = int(1)/10
        # made empty array to hold the sorted data according to density
        density_listx = []
        density_listy = []
        for i in range(6):
            density_listx.append([])
            density_listy.append([])


        for i in range(len(self.Ch1_channel0)):
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
            percentage = density / max_density * 100 *percentage_coefficient
            if percentage > 100:
                percentage = 100

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


        # add threshold
        
        self.graphWidget.removeItem(self.lr_x_axis)
        self.graphWidget.removeItem(self.lr_y_axis)
            
        pen = pg.mkPen(color=(0, 120, 180),width = 5)
        self.lr_x_axis = pg.InfiniteLine(0, movable=True, pen = pen)
        self.graphWidget.addItem(self.lr_x_axis) 
        self.lr_y_axis = pg.InfiniteLine(0, movable=True, pen = pen, angle=0)
        self.graphWidget.addItem(self.lr_y_axis) 
        
        self.lr_x_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        self.lr_y_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        
        # reset threshold # test
        self.infiniteline_table_update()
        
        
    ################################################################################################
    ### these are  the mouse-draggable-lines on the main tab, they are called "infinitelines" in the pyqt documents
    def infiniteline_update(self):
        self.GateVoltage_x.setText(str(self.lr_x_axis.value()))
        self.GateVoltage_y.setText(str(self.lr_y_axis.value()))
        self.infiniteline_table_update()
        
    def infiniteline_lineedit_update(self):
        self.lr_x_axis.setValue(float(self.GateVoltage_x.text()))
        self.lr_y_axis.setValue(float(self.GateVoltage_y.text()))
        self.infiniteline_table_update()
    
    def infiniteline_table_update(self):
        single_peak_count_channel0 = 0
        single_peak_count_channel1 = 0
        multi_peak_count_channel0 = 0
        multi_peak_count_channel1 = 0

        channel0_list_quadrant1 = []
        channel1_list_quadrant1 = []

        count_quadrant1 = 0

        # pass the threshold value to next window
        text_x = self.lr_x_axis.value()
        text_y = self.lr_y_axis.value()
        a = (np.array(self.Ch1_channel0) > text_x).tolist()
        c = (np.array(self.Ch1_channel1) > text_y).tolist()


        self.quadrant1_list = [False] * len(a)

        for i in range(len(a)):
            if a[i] and c[i]:
                self.quadrant1_list[i] = True
                channel0_list_quadrant1.append(self.Ch1_channel0[i])
                channel1_list_quadrant1.append(self.Ch1_channel1[i])
                count_quadrant1 += 1
                if ui.Ch1_channel0_peak_num[i] == 1:
                    single_peak_count_channel0 += 1
                elif ui.Ch1_channel0_peak_num[i] > 1:
                    multi_peak_count_channel0 += 1
                if ui.Ch1_channel1_peak_num[i] == 1:
                    single_peak_count_channel1 += 1
                elif ui.Ch1_channel1_peak_num[i] > 1:
                    multi_peak_count_channel1 += 1

        try:
            droplets = float(ui.lineEdit_totaldroplets.text())
            totalpercent1 = round(count_quadrant1 / droplets * 100, 2)
        except:
            totalpercent1 = 0

        if len(self.Ch1_channel0)!=0:
            view1 = str(round(100 * count_quadrant1 / len(self.Ch1_channel0), 2))

            if count_quadrant1 > 0:
                x_single_1 = str(round(100 * single_peak_count_channel0 / count_quadrant1, 2))
                y_single_1 = str(round(100 * single_peak_count_channel1 / count_quadrant1, 2))
                x_multi_1 = str(round(100 * multi_peak_count_channel0 / count_quadrant1, 2))
                y_multi_1 = str(round(100 * multi_peak_count_channel1 / count_quadrant1, 2))
            else:
                x_single_1 = '0'
                y_single_1 = '0'
                x_multi_1 = '0'
                y_multi_1 = '0'


        else:
            view1 = 0
            x_single_1 = '0'
            y_single_1 = '0'
            x_multi_1 = '0'
            y_multi_1 = '0'

        self.tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(count_quadrant1)))
        self.tableView_scatterquadrants.setItem(0, 1, QTableWidgetItem(view1))
        self.tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
        self.tableView_scatterquadrants.setItem(0, 3, QTableWidgetItem(x_single_1))
        self.tableView_scatterquadrants.setItem(0, 4, QTableWidgetItem(y_single_1))
        self.tableView_scatterquadrants.setItem(0, 5, QTableWidgetItem(x_multi_1))
        self.tableView_scatterquadrants.setItem(0, 6, QTableWidgetItem(y_multi_1))


        self.points_inside = list(compress(self.points_inside_square, self.quadrant1_list))

        ### infinite lines end
        ################################################################################################

        
    ################################################################################################
    ### polygon functions
    # 1. when user left-mouse click on the plot, record the coordinates. 
    # 2. Draw a red dot on the location, add lines from the previous dot to this dot.
    # 3. when finish drawing, 
    #    3.1 click the "polygon" button again to stop. 
    #    3.2 Thenline-up the first dot and the last dot.
    # 4. calculate all the points inside
    
    ### when edit the polygon shape
    # 5. user left-mouse click on the plot, record the coordinates. 
    # 6. From all the points recorded from step 1-2, find out which dot is the nearest one.
    # 7. Update the record to the point recently clicked
    # 8. Redraw the line connect to the previous dot
    # 9. Redraw the line connect to the next dot
    # 10. If it is the last dot, need to connect the line to the first dot
    
    # I didn't foresee the "edit" function when I first build the polygon functions. So the codes are quite redundent 
    # in the edit part. Good thing is it will not affect the time much.
    
    
    
    def polygon_triggering(self):
        
        if self.polygon_trigger == False:
    # trigger step 1
            self.polygon_trigger = True
            try:
                self.points = list(zip(self.Ch1_channel0,self.Ch1_channel1))
            except:
                self.points = [[]]
            self.polygon_points = [[]]
            self.polygon_lines = [[]]
            self.points_inside = []
            self.polygon = [[]]
            self.polygon_for_edit = [[]]
            self.points_inside_list = []
        elif self.polygon[-1] == [] and self.x == []:
            print("Polygon button clicked")
        else:
                 
    # step 4
            path = mpltPath.Path(self.polygon[-1])
            self.inside2 = path.contains_points(self.points)

            start_end_dot_x = [self.x[0],self.x[-1]]
            start_end_dot_y = [self.y[0],self.y[-1]]            
            self.polygon_lines[-1].append(self.graphWidget.plot(start_end_dot_x, start_end_dot_y,pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
            self.polygon_points[-1].append(self.graphWidget.plot(start_end_dot_x, start_end_dot_y, pen=None, symbol='o'))
            
            
            # show the dots have index before the first filter
#             self.points_inside.extend(list(compress(self.points_inside_square, self.inside2)))

            self.points_inside_list.append(list(compress(self.points_inside_square, self.inside2)))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func=lambda arr:set(arr) 
            self.points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.points_inside))

            self.label_dots_inside_polygon.setText(points_inside) 
     
            self.polygon.append([])
            self.polygon_points.append([])
            self.polygon_lines.append([])
            self.polygon_for_edit.append([])
            self.x = []
            self.y = []
                    
            # fill quadrant table
            try:
                droplets = float(ui.lineEdit_totaldroplets.text())
                totalpercent1 = round(len(self.Ch1_channel0) / droplets * 100, 2)
            except:
                totalpercent1 = 0

            view1 = str(round(100 * len(self.points_inside) / len(self.Ch1_channel0), 2))
            single_peak_count_channel0 = 0
            multi_peak_count_channel0 = 0
            single_peak_count_channel1 = 0
            multi_peak_count_channel1 = 0


            a = list(set(self.points_inside).intersection(set(self.points_inside_square)))


            for i in range(len(a)):
                if ui.Ch1_channel0_peak_num[i] == 1:
                    single_peak_count_channel0 += 1
                elif ui.Ch1_channel0_peak_num[i] > 1:
                    multi_peak_count_channel0 += 1
                if ui.Ch1_channel1_peak_num[i] == 1:
                    single_peak_count_channel1 += 1
                elif ui.Ch1_channel1_peak_num[i] > 1:
                    multi_peak_count_channel1 += 1

            self.checkC2 = time.time()
            x_single_1 = str(round(100 * single_peak_count_channel0 / len(self.points_inside), 2))
            y_single_1 = str(round(100 * single_peak_count_channel1 / len(self.points_inside), 2))
            x_multi_1 = str(round(100 * multi_peak_count_channel0 / len(self.points_inside), 2))
            y_multi_1 = str(round(100 * multi_peak_count_channel1 / len(self.points_inside), 2))

            self.checkC3 = time.time()
            self.tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(len(self.points_inside))))
            self.tableView_scatterquadrants.setItem(0, 1, QTableWidgetItem(view1))
            self.tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
            self.tableView_scatterquadrants.setItem(0, 3, QTableWidgetItem(x_single_1))
            self.tableView_scatterquadrants.setItem(0, 4, QTableWidgetItem(y_single_1))
            self.tableView_scatterquadrants.setItem(0, 5, QTableWidgetItem(x_multi_1))
            self.tableView_scatterquadrants.setItem(0, 6, QTableWidgetItem(y_multi_1))

            
    # step 2,3 
    def onMouseMoved(self,point):
        if self.stop_edit_trigger and self.polygon_trigger:

            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())

            self.x.append(p.x())
            self.y.append(p.y())

            self.polygon_points[-1].append(self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)], pen=None, symbol='o'))
            self.polygon_lines[-1].append(self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)],pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
            self.polygon[-1].append([p.x(),p.y()])
            self.polygon_for_edit[-1].append([p.x(),p.y()])

    # some redundent functions, used to fix some error. Didn't have time to simplify
        elif self.stop_edit_trigger == False:
            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())     
            
            nearest_distance = 20
            
            
            nearest_index = 0
            nearest_list = 0
            
            list_count = 0
            for i_list in self.polygon_for_edit:
                count = 0
                for i in i_list:
                    diff_x = abs(i[0] - p.x())
                    diff_y = abs(i[1] - p.y())
                    diff_total = sqrt(diff_x*diff_x + diff_y*diff_y)
                    if diff_total < nearest_distance:           
                        nearest_distance = diff_total
                        nearest_index = count
                        nearest_list = list_count
                    count += 1
                list_count += 1

            # remove points

            if nearest_index == 0:
                self.graphWidget.removeItem(self.polygon_points[nearest_list][-1])
            

            self.graphWidget.removeItem(self.polygon_points[nearest_list][nearest_index])
            self.graphWidget.removeItem(self.polygon_points[nearest_list][nearest_index+1])
            # change points  

            self.polygon_for_edit[nearest_list][nearest_index] = [p.x(),p.y()]
            



                          
            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.polygon_points[nearest_list][nearest_index-1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            
                edit_x = [p.x(),p.x()]
                edit_y = [p.y(), p.y()]
                
                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o') 
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')                
                
            if nearest_index == len(self.polygon_for_edit[nearest_list])-1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_points[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.polygon_points[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')





            # remove lines
            if nearest_index == 0:
                self.graphWidget.removeItem(self.polygon_lines[nearest_list][-1])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index+1])
            
            # change lines  
            # bug: when use in unfinished polygon, line will couse error
            
            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index-1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
                

            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
            

            if nearest_index == len(self.polygon_for_edit[nearest_list])-1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))

            self.nearest_list = nearest_list
                        
            
            

    # clear all the polygon shapes.
    def polygon_clean(self):
        self.label_dots_inside_polygon.setText('Inside: 0') 
        self.x = []
        self.y = []
        self.polygon = [[]]
        self.points_inside = [[]]
        try:
            for i_list in range(len(self.polygon_points)):
                for i in range(len(self.polygon_points[i_list])):
                    self.graphWidget.removeItem(self.polygon_points[i_list][i])
                    self.graphWidget.removeItem(self.polygon_lines[i_list][i])

        except:
            print("no polygon drawed")
        self.polygon_trigger = False

        

    # step 7~10, edit coordinates
    
    def edit_polygon_shape(self):
        
        print("edit_polygon_shape activate")
        if self.stop_edit_trigger == True:
            self.polygon_triggering()
            self.stop_edit_trigger = False
        else:
            self.stop_edit_trigger = True
            
            
            
            for ii in range(len(self.polygon_lines)):
                for i in range(len(self.polygon_lines[ii])):
                    self.graphWidget.removeItem(self.polygon_lines[ii][i])     
                    
            for ii in range(len(self.polygon_lines)-1):
                for i in range(1,len(self.polygon_lines[ii])-1):
                    list_x = [self.polygon_for_edit[ii][i][0],self.polygon_for_edit[ii][i-1][0]]
                    list_y = [self.polygon_for_edit[ii][i][1],self.polygon_for_edit[ii][i-1][1]]
                    self.polygon_lines[ii][i] = self.graphWidget.plot(list_x, list_y,
                                                                      pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)) 
                    
            for ii in range(len(self.polygon_lines)-1):
                list_x = [self.polygon_for_edit[ii][0][0],self.polygon_for_edit[ii][-1][0]]
                list_y = [self.polygon_for_edit[ii][0][1],self.polygon_for_edit[ii][-1][1]]                    
                self.polygon_lines[ii][-1] = self.graphWidget.plot(list_x, list_y,
                                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)) 


                    
            for i in range(len(self.polygon_for_edit)-1):
                path = mpltPath.Path(self.polygon_for_edit[i])
                self.inside2 = path.contains_points(self.points)
                self.points_inside = list(compress(self.points_inside_square, self.inside2))
                self.points_inside_list[i] = list(compress(self.points_inside_square, self.inside2))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func=lambda arr:set(arr) 
            self.points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.points_inside))
            self.label_dots_inside_polygon.setText(points_inside)         
        
        
                    
    # close the filter tab
    def close_clicked(self):
        self.close() 
        
        
    # "Next filiter" button on the main filter tab, pass the filtered value to next window
    # and assign a index number to next filter
    def ok_clicked(self):
        # incase user forgot to click polygon again to finish polygon
        
        if self.polygon_trigger == False:
           
            text_x = self.lr_x_axis.value()
            text_y = self.lr_y_axis.value()
            a = (np.array(self.Ch1_channel0) > text_x).tolist()
            c = (np.array(self.Ch1_channel1) > text_y).tolist()


            self.quadrant1_list = [False] * len(a)

            for i in range(len(a)):
                if a[i] and c[i]:
                    self.quadrant1_list[i] = True
                    
            self.quadrant1_list_or_polygon = list(compress(self.points_inside_square, self.quadrant1_list))
        else:
            # run trigger again incase user forgot to finish the shape
            self.polygon_triggering()
            # pass polygon value to next window
            self.quadrant1_list_or_polygon = self.points_inside

        # use self.tree_index instead ui to prevent potential bugs

        find_a_key = False
        key_count = 0
        while not find_a_key:         
            new_index = (key_count,) + self.tree_index
            if new_index in ui.tree_dic:
                key_count += 1
            else:
                find_a_key = True

    
        # tree_dic[self.tree_index]['tree_standarditem'] append the codes for bottom left tree view in main window
        # tree_dic[self.tree_index]['quadrant1_list_or_polygon'] append the filter information
        
        ui.tree_dic[new_index] = {} 
        ui.tree_dic[new_index]['tree_standarditem'] = StandardItem('New graph', 12 - len(new_index))
        ui.tree_dic[self.tree_index]['tree_standarditem'].appendRow(ui.tree_dic[new_index]['tree_standarditem'])
        ui.tree_dic[self.tree_index]['quadrant1_list_or_polygon'] = self.quadrant1_list_or_polygon 
        print('self.quadrant1_list_or_polygon',self.quadrant1_list_or_polygon)
        ui.treeView.expandAll()

        # reassign tree_index, new window need this index to create child branch
        ui.tree_index = new_index
        
        # open a new window for the new branch
        ui.dialog = window_filter(self)
#         ui.window_filter[new_index] = ui.dialog
        ui.tree_dic[new_index]['tree_windowfilter'] = ui.dialog
        ui.dialog.show()

            
    def export_clicked(self):
        ui.lineEdit_filter.setText(self.lineEdit.text())
        self.close() 


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.mainwindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 900)
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
        
        self.checkbox_Droplet_Record = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox_Droplet_Record.setObjectName("checkbox_Droplet_Record")
        self.layout_vertical_checkbox.addWidget(self.checkbox_Droplet_Record)
        
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
        
        self.lineEdit_Droplet_Recordhit = QtWidgets.QLineEdit(self.tab_statistic)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ch13hit.sizePolicy().hasHeightForWidth())
        self.lineEdit_Droplet_Recordhit.setSizePolicy(sizePolicy)
        self.lineEdit_Droplet_Recordhit.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_Droplet_Recordhit.setObjectName("lineEdit_Droplet_Recordhit")
        self.horizontalLayout_17.addWidget(self.lineEdit_Droplet_Recordhit)
        

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
        
        self.layout_vertical_checkbox_2.addWidget(self.channel_1)
        self.layout_vertical_checkbox_2.addWidget(self.channel_2)
        self.layout_vertical_checkbox_2.addWidget(self.channel_3)
        self.layout_vertical_checkbox_2.addWidget(self.channel_4)
        
        self.channel_1.setChecked(True)
        self.channel_2.setChecked(True)
        self.channel_3.setChecked(True)
        self.channel_4.setChecked(True)

        self.gridLayout_41.addItem(self.layout_vertical_checkbox_2, 14, 0, 1, 2 )
        
        
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
        ### peak leanear end
        
        
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
        self.lineEdit_7.setText("1000")
        self.lineEdit_8.setText("1000")
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

        
        self.label_density_adjust1 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_density_adjust1.setFont(font)
        self.label_density_adjust1.setObjectName("label_density_adjust1")
        self.gridLayout_16.addWidget(self.label_density_adjust1, 2, 0, 1, 1)

        self.lineEdit_first_layer_density_adjust = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
#         self.lineEdit_first_layer_density_adjust.setMinimumSize(QtCore.QSize(110, 0))
#         self.lineEdit_first_layer_density_adjust.setMaximumSize(QtCore.QSize(80, 16777215)) 
        self.lineEdit_first_layer_density_adjust.setObjectName("lineEdit_first_layer_density_adjust")
        self.gridLayout_16.addWidget(self.lineEdit_first_layer_density_adjust, 2, 1, 1, 2)
        self.lineEdit_first_layer_density_adjust.setText("1")
        
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

        ####### multipeak

        # Peak Num Updater
        self.line_peak_num = QtWidgets.QFrame(self.sub_tab_width_scatter)
        self.line_peak_num.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_peak_num.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_peak_num.setObjectName("line_peak_num")
        self.verticalLayout_16.addWidget(self.line_peak_num)
        self.gridLayout_peak_num = QtWidgets.QGridLayout()
        self.gridLayout_peak_num.setContentsMargins(10, 10, -1, 10)
        self.gridLayout_peak_num.setObjectName("gridLayout_13")

        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_num_peak_title = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_title.setFont(font)
        self.label_num_peak_title.setObjectName("label_num_peak_title")
        self.verticalLayout_16.addWidget(self.label_num_peak_title)
        self.label_num_peak_1 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_1.setFont(font)
        self.label_num_peak_1.setObjectName("label_num_peak_1")
        self.label_num_peak_2 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_2.setFont(font)
        self.label_num_peak_2.setObjectName("label_num_peak_2")
        self.label_num_peak_3 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_3.setFont(font)
        self.label_num_peak_3.setObjectName("label_num_peak_3")
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_num_peak_4 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_4.setFont(font)
        self.label_num_peak_4.setObjectName("label_num_peak_4")
        self.label_num_peak_5 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_5.setFont(font)
        self.label_num_peak_5.setObjectName("label_num_peak_5")
        self.label_num_peak_6 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_6.setFont(font)
        self.label_num_peak_6.setObjectName("label_num_peak_6")
        self.label_num_peak_7 = QtWidgets.QLabel(self.sub_tab_width_scatter)
        self.label_num_peak_7.setFont(font)
        self.label_num_peak_7.setObjectName("label_num_peak_7")
        self.gridLayout_peak_num.addWidget(self.label_num_peak_1, 0, 0)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_2, 0, 1)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_3, 0, 2)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_4, 1, 0)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_5, 2, 0)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_6, 3, 0)
        self.gridLayout_peak_num.addWidget(self.label_num_peak_7, 4, 0)
        self.comboBox_peak_num_1 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_peak_num_1.sizePolicy().hasHeightForWidth())
        self.comboBox_peak_num_1.setSizePolicy(sizePolicy)
        self.comboBox_peak_num_1.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_peak_num_1.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_peak_num_1.setObjectName("comboBox_peak_num_1")
        self.comboBox_peak_num_1.addItem("")
        self.comboBox_peak_num_1.addItem("")
        self.comboBox_peak_num_1.addItem("")
        self.comboBox_peak_num_2 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_peak_num_2.sizePolicy().hasHeightForWidth())
        self.comboBox_peak_num_2.setSizePolicy(sizePolicy)
        self.comboBox_peak_num_2.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_peak_num_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_peak_num_2.setObjectName("comboBox_peak_num_1")
        self.comboBox_peak_num_2.addItem("")
        self.comboBox_peak_num_2.addItem("")
        self.comboBox_peak_num_2.addItem("")
        self.comboBox_peak_num_3 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_peak_num_3.sizePolicy().hasHeightForWidth())
        self.comboBox_peak_num_3.setSizePolicy(sizePolicy)
        self.comboBox_peak_num_3.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_peak_num_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_peak_num_3.setObjectName("comboBox_peak_num_1")
        self.comboBox_peak_num_3.addItem("")
        self.comboBox_peak_num_3.addItem("")
        self.comboBox_peak_num_3.addItem("")
        self.comboBox_peak_num_4 = QtWidgets.QComboBox(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_peak_num_4.sizePolicy().hasHeightForWidth())
        self.comboBox_peak_num_4.setSizePolicy(sizePolicy)
        self.comboBox_peak_num_4.setMinimumSize(QtCore.QSize(80, 0))
        self.comboBox_peak_num_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox_peak_num_4.setObjectName("comboBox_peak_num_1")
        self.comboBox_peak_num_4.addItem("")
        self.comboBox_peak_num_4.addItem("")
        self.comboBox_peak_num_4.addItem("")
        self.gridLayout_peak_num.addWidget(self.comboBox_peak_num_1, 1, 1)
        self.gridLayout_peak_num.addWidget(self.comboBox_peak_num_2, 2, 1)
        self.gridLayout_peak_num.addWidget(self.comboBox_peak_num_3, 3, 1)
        self.gridLayout_peak_num.addWidget(self.comboBox_peak_num_4, 4, 1)
        self.lineEdit_peak_num_1 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_peak_num_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_peak_num_1.setSizePolicy(sizePolicy)
        self.lineEdit_peak_num_1.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_peak_num_1.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_peak_num_1.setObjectName("lineEdit_peak_num_1")
        self.lineEdit_peak_num_2 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_peak_num_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_peak_num_2.setSizePolicy(sizePolicy)
        self.lineEdit_peak_num_2.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_peak_num_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_peak_num_2.setObjectName("lineEdit_peak_num_2")
        self.lineEdit_peak_num_3 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_peak_num_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_peak_num_3.setSizePolicy(sizePolicy)
        self.lineEdit_peak_num_3.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_peak_num_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_peak_num_3.setObjectName("lineEdit_peak_num_3")
        self.lineEdit_peak_num_4 = QtWidgets.QLineEdit(self.sub_tab_width_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_peak_num_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_peak_num_4.setSizePolicy(sizePolicy)
        self.lineEdit_peak_num_4.setMinimumSize(QtCore.QSize(60, 0))
        self.lineEdit_peak_num_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lineEdit_peak_num_4.setObjectName("lineEdit_peak_num_4")
        self.gridLayout_peak_num.addWidget(self.lineEdit_peak_num_1, 1, 2)
        self.gridLayout_peak_num.addWidget(self.lineEdit_peak_num_2, 2, 2)
        self.gridLayout_peak_num.addWidget(self.lineEdit_peak_num_3, 3, 2)
        self.gridLayout_peak_num.addWidget(self.lineEdit_peak_num_4, 4, 2)

        self.verticalLayout_16.addLayout(self.gridLayout_peak_num)


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


        # may fix a potential bug, leave it here for now
        self.graphWidget_width_scatter = PlotWidget(title=' ')
    

               
            
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget_width_scatter.sizePolicy().hasHeightForWidth())
    
        self.graphWidget_width_scatter.setSizePolicy(sizePolicy)
        self.graphWidget_width_scatter.setMinimumSize(QtCore.QSize(500, 500))
        self.graphWidget_width_scatter.setObjectName("graphWidget_width_scatter")
        self.gridLayout_15.addWidget(self.graphWidget_width_scatter, 0, 2, 1, 1)
        

#         self.graphWidget_width_scatter.setTitle("test scatter plot", color="w", size="30pt")
#         styles = {"color": "r", "font-size": "20px"}
        self.graphWidget_width_scatter.setBackground('w')

        self.graphWidget_width_scatter.setLabel('left', 'Green', **styles)
        self.graphWidget_width_scatter.setLabel('bottom', 'Far Red', **styles)
#         self.graphWidget_width_scatter.setTitle("Your Title Here", color="b", size="10pt")
        
 
        self.lr_x_axis = pg.LinearRegionItem([1,1])
        self.lr_y_axis = pg.LinearRegionItem([1,1], orientation = 1)
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

### extra filter test tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_filter = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_filter.setObjectName("gridLayout_filter")
        
        self.horizontalLayout_filter = QtWidgets.QHBoxLayout()
        self.horizontalLayout_filter.setObjectName("horizontalLayout_filter")
        self.label_filter = QtWidgets.QLabel(self.tab)
        self.label_filter.setObjectName("label_filter")
        self.horizontalLayout_filter.addWidget(self.label_filter)
        
        self.pushButton_filter = QtWidgets.QPushButton(self.tab)
        self.pushButton_filter.setObjectName("pushButton_filter")
        self.horizontalLayout_filter.addWidget(self.pushButton_filter)
        
        self.lineEdit_filter = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_filter.setObjectName("lineEdit_filter")
        self.horizontalLayout_filter.addWidget(self.lineEdit_filter)
        
        
#         self.filter_list_view = QtWidgets.QListWidget(self.tab)
#         self.filter_list_view.setObjectName("filter_list_view")
#         self.horizontalLayout_filter.addWidget(self.filter_list_view)
        
        
#         self.filter_list_view.addItem('Creat New Filter')
#         self.filter_list_view.setCurrentRow(0)

#         self.filter_dict = {}
#         self.filter_count = -1

        # add tree view

        self.treeView = QtWidgets.QTreeView(self.tab)
        
        self.layout_vertical_filecontrol.addWidget(self.treeView)
#         self.horizontalLayout_filter.addWidget(self.treeView)
    
        self.treeView.setHeaderHidden(True)
        self.treeModel = QStandardItemModel()
        self.treeView.setExpandsOnDoubleClick(False)
        

        
        self.tree_dic = {}

#         self.tree_dic[(0,)] = StandardItem('Create graph', 12, set_bold=True)
#         self.treeModel.appendRow(self.tree_dic[(0,)])

        self.tree_dic[(0,)] = {}
        self.tree_dic[(0,)]['tree_standarditem'] = StandardItem('Create graph', 12, set_bold=True)
        self.treeModel.appendRow(self.tree_dic[(0,)]['tree_standarditem'])

        self.tree_dic[(0,0)] = {}
        self.tree_dic[(0,0)]['tree_standarditem'] = StandardItem('test branch', 10, set_bold=True)
        self.tree_dic[(0,)]['tree_standarditem'].appendRow(self.tree_dic[(0,0)]['tree_standarditem'])
    
        # 1st window, 1st tree index
            

        self.tree_index = (0,)
        self.dialog = window_filter(self)
        self.tree_dic[(0,)]['tree_windowfilter'] = self.dialog
    
        
        self.treeView.setModel(self.treeModel)
        self.treeView.expandAll()
        self.treeView.doubleClicked.connect(self.getValue)
  

# two extra buttons

#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")

#         self.button_copy = QtWidgets.QPushButton(self.centralwidget)
#         self.button_copy.setMinimumSize(QtCore.QSize(50, 0))
#         self.button_copy.setMaximumSize(QtCore.QSize(80, 16777215))
#         self.button_copy.setObjectName("button_copy")

#         self.horizontalLayout.addWidget(self.button_copy)

#         self.button_paste = QtWidgets.QPushButton(self.centralwidget)
#         self.button_paste.setMinimumSize(QtCore.QSize(50, 0))
#         self.button_paste.setMaximumSize(QtCore.QSize(80, 16777215))
#         self.button_paste.setObjectName("button_paste")

#         self.horizontalLayout.addWidget(self.button_paste)

#         self.layout_vertical_filecontrol.addLayout(self.horizontalLayout)
    
    
    
        
        self.gridLayout_filter.addLayout(self.horizontalLayout_filter, 0, 0, 1, 1)
        self.tab_widgets_main.addTab(self.tab, "")

        
        
        
        self.pushButton_filter.clicked.connect(self.openwindow_filter)

        self.test_number = 0




### Peak Height tab

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
#         self.gridLayout_6.setContentsMargins(10, 10, -1, 10)
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
        self.lineEdit_scatterxvoltage.setMinimumSize(QtCore.QSize(110, 0))
        self.lineEdit_scatterxvoltage.setMaximumSize(QtCore.QSize(80, 16777215)) 
        self.lineEdit_scatterxvoltage.setObjectName("lineEdit_scatterxvoltage")
        self.gridLayout_6.addWidget(self.lineEdit_scatterxvoltage, 1, 1, 1, 1)
        self.lineEdit_scatteryvoltage = QtWidgets.QLineEdit(self.subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_scatteryvoltage.sizePolicy().hasHeightForWidth())
        self.lineEdit_scatteryvoltage.setSizePolicy(sizePolicy)
        self.lineEdit_scatteryvoltage.setMinimumSize(QtCore.QSize(110, 0))
        self.lineEdit_scatteryvoltage.setMaximumSize(QtCore.QSize(80, 16777215)) 
        self.lineEdit_scatteryvoltage.setObjectName("lineEdit_scatteryvoltage")
        self.gridLayout_6.addWidget(self.lineEdit_scatteryvoltage, 2, 1, 1, 1)
        
        ### threshold subgating               
        
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
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem20, 0, 2, 1, 1)
        

        self.polygon_inside_label_30 = QtWidgets.QLabel(self.subtab_scatter)
        self.polygon_inside_label_30.setFont(font)
        self.polygon_inside_label_30.setObjectName("polygon_inside_label_30")
        self.gridLayout_4.addWidget(self.polygon_inside_label_30, 0, 0, 1, 1)
        
        self.polygon_inside_label_29 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.polygon_inside_label_29.setFont(font)
        self.polygon_inside_label_29.setObjectName("polygon_inside_label_29")
        self.gridLayout_4.addWidget(self.polygon_inside_label_29, 1, 0, 1, 1)
    
        self.pushButton_9 = QtWidgets.QPushButton(self.subtab_scatter)
        self.pushButton_9.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_4.addWidget(self.pushButton_9, 1, 1, 1, 1)
#         self.horizontalLayout_32.addWidget(self.pushButton_9)
        

        self.pushButton_10 = QtWidgets.QPushButton(self.subtab_scatter)
        self.pushButton_10.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton_10.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_4.addWidget(self.pushButton_10, 1, 2, 1, 1)
       
        self.pushButton_12 = QtWidgets.QPushButton(self.subtab_scatter)
        self.pushButton_12.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_4.addWidget(self.pushButton_12, 1, 3, 1, 1)    
    
        self.line_13 = QtWidgets.QFrame(self.subtab_scatter)
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.gridLayout_4.addWidget(self.line_13, 2, 0, 1, 4)
        
        self.pushButton_11 = QtWidgets.QPushButton(self.subtab_scatter)
        self.pushButton_11.setMinimumSize(QtCore.QSize(110, 0))
        self.pushButton_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_4.addWidget(self.pushButton_11, 3, 2, 1, 1)
      
        self.label_density_adjust2 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_density_adjust2.setFont(font)
        self.label_density_adjust2.setObjectName("label_density_adjust2")
        self.gridLayout_4.addWidget(self.label_density_adjust2, 4, 0, 1, 1)
        
        self.lineEdit_second_layer_density_adjust = QtWidgets.QLineEdit(self.subtab_scatter)
#         self.lineEdit_second_layer_density_adjust.setMinimumSize(QtCore.QSize(110, 0))
#         self.lineEdit_second_layer_density_adjust.setMaximumSize(QtCore.QSize(80, 16777215)) 
        self.lineEdit_second_layer_density_adjust.setObjectName("lineEdit_second_layer_density_adjust")
        self.gridLayout_4.addWidget(self.lineEdit_second_layer_density_adjust, 4, 1, 1, 1)
        self.lineEdit_second_layer_density_adjust.setText("1")
        
        self.verticalLayout_9.addLayout(self.gridLayout_4)
        

                
               

        
        self.label_36 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.verticalLayout_9.addWidget(self.label_36)        
        self.tableView_scatterquadrants = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatterquadrants.setObjectName("tableView_scatterquadrants")
        self.tableView_scatterquadrants.setMinimumSize(QtCore.QSize(500, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_scatterquadrants.sizePolicy().hasHeightForWidth())
        self.tableView_scatterquadrants.setSizePolicy(sizePolicy)   
        
        self.verticalLayout_9.addWidget(self.tableView_scatterquadrants)
        self.label_37 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_9.addWidget(self.label_37)
        self.tableView_scatterxaxis = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatterxaxis.setObjectName("tableView_scatterxaxis")
        self.tableView_scatterxaxis.setMinimumSize(QtCore.QSize(500, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_scatterxaxis.sizePolicy().hasHeightForWidth())
        self.tableView_scatterxaxis.setSizePolicy(sizePolicy) 
        
        self.verticalLayout_9.addWidget(self.tableView_scatterxaxis)
        self.label_38 = QtWidgets.QLabel(self.subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.verticalLayout_9.addWidget(self.label_38)
        self.tableView_scatteryaxis = QtWidgets.QTableWidget(self.subtab_scatter)
        self.tableView_scatteryaxis.setObjectName("tableView_scatteryaxis")
        self.tableView_scatteryaxis.setMinimumSize(QtCore.QSize(500, 100))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_scatteryaxis.sizePolicy().hasHeightForWidth())
        self.tableView_scatteryaxis.setSizePolicy(sizePolicy) 
        
        self.verticalLayout_9.addWidget(self.tableView_scatteryaxis)

        ### Quadrants table
        # set row count
        self.tableView_scatterquadrants.setRowCount(4)
        # set column count
        self.tableView_scatterquadrants.setColumnCount(7)
        self.tableView_scatterquadrants.setHorizontalHeaderLabels(('Count', '% Total Peaks', '% Total Droplets', 'X Single Peak %',
                                                                   'Y Single Peak %', 'X Multi Peak %', 'Y Multi Peak %'))
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
#         self.data_line = self.graphWidget.plot([0, 1], [1, 1],
#                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
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


### subgating
        self.tab_subgating = QtWidgets.QWidget()
        self.tab_subgating.setObjectName("tab_subgating")

#         self.verticalLayout_4 = QtWidgets.QVBoxLayout(tab_subgating)
        self.subgating_verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_subgating)
        self.subgating_verticalLayout_4.setObjectName("subgating_verticalLayout_4")
        self.tab_widgets_subgating = QtWidgets.QTabWidget(self.tab_subgating)
        self.tab_widgets_subgating.setObjectName("tab_widgets_subgating")

        self.subgating_subtab_scatter = QtWidgets.QWidget()
        self.subgating_subtab_scatter.setObjectName("subgating_subtab_scatter")
        self.subgating_horizontalLayout_29 = QtWidgets.QHBoxLayout(self.subgating_subtab_scatter)
        self.subgating_horizontalLayout_29.setObjectName("subgating_horizontalLayout_29")
        self.subgating_verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.subgating_verticalLayout_9.setContentsMargins(10, -1, -1, -1)
        self.subgating_verticalLayout_9.setObjectName("subgating_verticalLayout_9")
        self.subgating_gridLayout_6 = QtWidgets.QGridLayout()
#         self.subgating_gridLayout_6.setContentsMargins(10, 10, -1, 10)
        self.subgating_gridLayout_6.setObjectName("subgating_gridLayout_6")
        self.subgating_label_30 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.subgating_label_30.setFont(font)
        self.subgating_label_30.setObjectName("subgating_label_30")
        self.subgating_gridLayout_6.addWidget(self.subgating_label_30, 0, 1, 1, 1)
        self.subgating_horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.subgating_horizontalLayout_30.setObjectName("subgating_horizontalLayout_30")
        self.subgating_label_31 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        self.subgating_label_31.setObjectName("subgating_label_31")
        self.subgating_horizontalLayout_30.addWidget(self.subgating_label_31)
        
        self.subgating_preselect_comboBox = QtWidgets.QComboBox(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_preselect_comboBox.sizePolicy().hasHeightForWidth())
        self.subgating_preselect_comboBox.setSizePolicy(sizePolicy)
        self.subgating_preselect_comboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.subgating_preselect_comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.subgating_preselect_comboBox.setObjectName("subgating_comboBox")
        self.subgating_preselect_comboBox.addItem("")
        self.subgating_preselect_comboBox.addItem("")
        self.subgating_horizontalLayout_30.addWidget(self.subgating_preselect_comboBox)
        
        
        
        self.subgating_comboBox = QtWidgets.QComboBox(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_comboBox.sizePolicy().hasHeightForWidth())
        self.subgating_comboBox.setSizePolicy(sizePolicy)
        self.subgating_comboBox.setMinimumSize(QtCore.QSize(80, 0))
        self.subgating_comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.subgating_comboBox.setObjectName("subgating_comboBox")
        self.subgating_comboBox.addItem("")
        self.subgating_comboBox.addItem("")
        self.subgating_comboBox.addItem("")
        self.subgating_comboBox.addItem("")
        self.subgating_horizontalLayout_30.addWidget(self.subgating_comboBox)
        self.subgating_gridLayout_6.addLayout(self.subgating_horizontalLayout_30, 1, 0, 1, 1)
        
        self.subgating_lineEdit_scatterxvoltage = QtWidgets.QLineEdit(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_lineEdit_scatterxvoltage.sizePolicy().hasHeightForWidth())
        self.subgating_lineEdit_scatterxvoltage.setSizePolicy(sizePolicy)
        self.subgating_lineEdit_scatterxvoltage.setMinimumSize(QtCore.QSize(60, 0))
        self.subgating_lineEdit_scatterxvoltage.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_lineEdit_scatterxvoltage.setObjectName("subgating_lineEdit_scatterxvoltage")
        self.subgating_gridLayout_6.addWidget(self.subgating_lineEdit_scatterxvoltage, 1, 1, 1, 1)
        self.subgating_lineEdit_scatteryvoltage = QtWidgets.QLineEdit(self.subgating_subtab_scatter)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_lineEdit_scatteryvoltage.sizePolicy().hasHeightForWidth())
        self.subgating_lineEdit_scatteryvoltage.setSizePolicy(sizePolicy)
        self.subgating_lineEdit_scatteryvoltage.setMinimumSize(QtCore.QSize(60, 0))
        self.subgating_lineEdit_scatteryvoltage.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_lineEdit_scatteryvoltage.setObjectName("lsubgating_ineEdit_scatteryvoltage")
        self.subgating_gridLayout_6.addWidget(self.subgating_lineEdit_scatteryvoltage, 2, 1, 1, 1)
        self.subgating_horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.subgating_horizontalLayout_31.setObjectName("subgating_horizontalLayout_31")
        self.subgating_label_32 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        self.subgating_label_32.setObjectName("subgating_label_32")
        self.subgating_horizontalLayout_31.addWidget(self.subgating_label_32)
        
        self.subgating_preselect_comboBox_2 = QtWidgets.QComboBox(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_preselect_comboBox_2.sizePolicy().hasHeightForWidth())
        self.subgating_preselect_comboBox_2.setSizePolicy(sizePolicy)
        self.subgating_preselect_comboBox_2.setMinimumSize(QtCore.QSize(80, 0))
        self.subgating_preselect_comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.subgating_preselect_comboBox_2.setObjectName("subgating_comboBox")
        self.subgating_preselect_comboBox_2.addItem("")
        self.subgating_preselect_comboBox_2.addItem("")
        self.subgating_horizontalLayout_31.addWidget(self.subgating_preselect_comboBox_2)
        
        
        self.subgating_comboBox_2 = QtWidgets.QComboBox(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_comboBox_2.sizePolicy().hasHeightForWidth())
        self.subgating_comboBox_2.setSizePolicy(sizePolicy)
        self.subgating_comboBox_2.setMinimumSize(QtCore.QSize(80, 0))
        self.subgating_comboBox_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.subgating_comboBox_2.setObjectName("subgating_comboBox_2")
        self.subgating_comboBox_2.addItem("")
        self.subgating_comboBox_2.addItem("")
        self.subgating_comboBox_2.addItem("")
        self.subgating_comboBox_2.addItem("")
        self.subgating_horizontalLayout_31.addWidget(self.subgating_comboBox_2)
        self.subgating_gridLayout_6.addLayout(self.subgating_horizontalLayout_31, 2, 0, 1, 1)
        self.subgating_label_29 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.subgating_label_29.setFont(font)
        self.subgating_label_29.setObjectName("subgating_label_29")
        self.subgating_gridLayout_6.addWidget(self.subgating_label_29, 0, 0, 1, 1)
        self.subgating_verticalLayout_9.addLayout(self.subgating_gridLayout_6)
        self.subgating_line_14 = QtWidgets.QFrame(self.subgating_subtab_scatter)
        self.subgating_line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.subgating_line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.subgating_line_14.setObjectName("subgating_line_14")
        self.subgating_verticalLayout_9.addWidget(self.subgating_line_14)
        self.subgating_gridLayout_4 = QtWidgets.QGridLayout()
        self.subgating_gridLayout_4.setObjectName("subgating_gridLayout_4")
        subgating_spacerItem20 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.subgating_gridLayout_4.addItem(subgating_spacerItem20, 0, 2, 1, 1)
                
 
        self.subgating_polygon_inside_label_30 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        self.subgating_polygon_inside_label_30.setFont(font)
        self.subgating_polygon_inside_label_30.setObjectName("polygon_inside_label_30")
        self.subgating_gridLayout_4.addWidget(self.subgating_polygon_inside_label_30, 0, 0, 1, 1)  
        
        self.subgating_polygon_inside_label_29 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.subgating_polygon_inside_label_29.setFont(font)
        self.subgating_polygon_inside_label_29.setObjectName("polygon_inside_label_29")
        self.subgating_gridLayout_4.addWidget(self.subgating_polygon_inside_label_29, 1, 0, 1, 1)                
    
        self.subgating_pushButton_9 = QtWidgets.QPushButton(self.subgating_subtab_scatter)
        self.subgating_pushButton_9.setMinimumSize(QtCore.QSize(110, 0))
        self.subgating_pushButton_9.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_pushButton_9.setObjectName("subgating_pushButton_9")
        self.subgating_gridLayout_4.addWidget(self.subgating_pushButton_9, 1, 1, 1, 1)
#         self.horizontalLayout_32.addWidget(self.pushButton_9)
        

        self.subgating_pushButton_10 = QtWidgets.QPushButton(self.subgating_subtab_scatter)
        self.subgating_pushButton_10.setMinimumSize(QtCore.QSize(110, 0))
        self.subgating_pushButton_10.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_pushButton_10.setObjectName("subgating_pushButton_10")
        self.subgating_gridLayout_4.addWidget(self.subgating_pushButton_10, 1, 2, 1, 1)
   
        self.subgating_pushButton_11 = QtWidgets.QPushButton(self.subgating_subtab_scatter)
        self.subgating_pushButton_11.setMinimumSize(QtCore.QSize(110, 0))
        self.subgating_pushButton_11.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_pushButton_11.setObjectName("subgating_pushButton_11")
        self.subgating_gridLayout_4.addWidget(self.subgating_pushButton_11, 1, 3, 1, 1)
        
        self.subgating_line_13 = QtWidgets.QFrame(self.subgating_subtab_scatter)
        self.subgating_line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.subgating_line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.subgating_line_13.setObjectName("subgating_line_13")
        self.subgating_gridLayout_4.addWidget(self.subgating_line_13, 2, 0, 1, 4)
        
        self.subgating_pushButton_12 = QtWidgets.QPushButton(self.subgating_subtab_scatter)
#         self.subgating_pushButton_12.setMinimumSize(QtCore.QSize(110, 0))
#         self.subgating_pushButton_12.setMaximumSize(QtCore.QSize(80, 16777215))
        self.subgating_pushButton_12.setObjectName("subgating_pushButton_11")
        self.subgating_gridLayout_4.addWidget(self.subgating_pushButton_12, 3, 1, 1, 2)        
        
        
        
        self.label_density_adjust3 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_density_adjust3.setFont(font)
        self.label_density_adjust3.setObjectName("label_density_adjust3")
        self.subgating_gridLayout_4.addWidget(self.label_density_adjust3, 4, 0, 1, 1)
        
        self.lineEdit_third_layer_density_adjust = QtWidgets.QLineEdit(self.subgating_subtab_scatter)
        self.lineEdit_third_layer_density_adjust.setMinimumSize(QtCore.QSize(110, 0))
        self.lineEdit_third_layer_density_adjust.setMaximumSize(QtCore.QSize(80, 16777215)) 
        self.lineEdit_third_layer_density_adjust.setObjectName("lineEdit_third_layer_density_adjust")
        self.subgating_gridLayout_4.addWidget(self.lineEdit_third_layer_density_adjust, 4, 1, 1, 1)
        self.lineEdit_third_layer_density_adjust.setText("1")        
        
        
        
        
        self.subgating_verticalLayout_9.addLayout(self.subgating_gridLayout_4)

        
        self.subgating_label_36 = QtWidgets.QLabel(self.subgating_subtab_scatter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.subgating_label_36.setFont(font)
        self.subgating_label_36.setObjectName("subgating_label_36")
        self.subgating_verticalLayout_9.addWidget(self.subgating_label_36)
        self.subgating_tableView_scatterquadrants = QtWidgets.QTableWidget(self.subgating_subtab_scatter)
        self.subgating_tableView_scatterquadrants.setObjectName("subgating_tableView_scatterquadrants")
        self.subgating_tableView_scatterquadrants.setMinimumSize(QtCore.QSize(20, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_tableView_scatterquadrants.sizePolicy().hasHeightForWidth())
        self.subgating_tableView_scatterquadrants.setSizePolicy(sizePolicy) 
        
        self.subgating_verticalLayout_9.addWidget(self.subgating_tableView_scatterquadrants)
        
                ### Quadrants table
        # set row count
        self.subgating_tableView_scatterquadrants.setRowCount(1)
        # set column count
        self.subgating_tableView_scatterquadrants.setColumnCount(7)
        self.subgating_tableView_scatterquadrants.setHorizontalHeaderLabels(('Count', '% Total Peaks', '% Total Droplets', 'X Single Peak %',
                                                                   'Y Single Peak %', 'X Multi Peak %', 'Y Multi Peak %'))





        subgating_spacerItem_bottom = QtWidgets.QSpacerItem(60, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.subgating_verticalLayout_9.addItem(subgating_spacerItem_bottom)
        
        self.subgating_horizontalLayout_29.addLayout(self.subgating_verticalLayout_9)

        self.subgating_line_7 = QtWidgets.QFrame(self.subgating_subtab_scatter)
        self.subgating_line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.subgating_line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.subgating_line_7.setObjectName("subgating_line_7")
        self.subgating_horizontalLayout_29.addWidget(self.subgating_line_7)
        
        
        ### graphwidget in subgating tab
        
        self.subgating_graphWidget = PlotWidget(self.subgating_subtab_scatter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subgating_graphWidget.sizePolicy().hasHeightForWidth())
        self.subgating_graphWidget.setSizePolicy(sizePolicy)
        self.subgating_graphWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.subgating_graphWidget.setObjectName("subgating_graphWidget")
        self.subgating_horizontalLayout_29.addWidget(self.subgating_graphWidget)
        self.subgating_graphWidget.setTitle("test scatter plot", color="w", size="30pt")
        styles = {"color": "r", "font-size": "20px"}
        self.subgating_graphWidget.setBackground('w')

        self.subgating_graphWidget.setLabel('left', 'Green', **styles)
        self.subgating_graphWidget.setLabel('bottom', 'Far Red', **styles)
        

            
        self.tab_widgets_main.addTab(self.tab_subgating, "")
        self.subgating_verticalLayout_4.addWidget(self.tab_widgets_subgating)
        self.tab_widgets_subgating.addTab(self.subgating_subtab_scatter, "")

        ### threshold in subgating tab
        
        # threshold

        self.subgating_lineEdit_scatterxvoltage.setText("0")
        self.subgating_lineEdit_scatteryvoltage.setText("0")

        self.subgating_data_line_x = self.subgating_graphWidget.plot([0, 1], [1, 1],
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.subgating_data_line_y = self.subgating_graphWidget.plot([1, 1], [0, 1],
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))

        self.subgating_lineEdit_scatterxvoltage.editingFinished.connect(self.subgating_thresholdUpdated_2)
        self.subgating_lineEdit_scatteryvoltage.editingFinished.connect(self.subgating_thresholdUpdated_2)
        # threshold end
        

        

#### subtab polygon linear graph
        
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_151 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_151.setObjectName("horizontalLayout_151")
        self.verticalLayout_52 = QtWidgets.QVBoxLayout()
        self.verticalLayout_52.setContentsMargins(5, -1, 5, -1)
        self.verticalLayout_52.setObjectName("verticalLayout_52")
        self.gridLayout_42 = QtWidgets.QGridLayout()
        self.gridLayout_42.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.label_181 = QtWidgets.QLabel(self.tab_4)
        self.label_181.setAlignment(QtCore.Qt.AlignCenter)
        self.label_181.setObjectName("label_181")
        self.gridLayout_42.addWidget(self.label_181, 0, 0, 1, 2)
        self.label_183 = QtWidgets.QLabel(self.tab_4)
        self.label_183.setAlignment(QtCore.Qt.AlignCenter)
        self.label_183.setObjectName("label_183")
        self.gridLayout_42.addWidget(self.label_183, 7, 0, 1, 2)
        
        #pushbutton5
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_6.setObjectName("pushButton_6")
#         self.gridLayout_42.addWidget(self.pushButton_5, 8, 0, 1, 2)
        self.gridLayout_42.addWidget(self.pushButton_6, 8, 0, 1, 2)
        
#         self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_4)
    
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_42.addWidget(self.pushButton_7, 12, 0, 1, 2)
        self.label_180 = QtWidgets.QLabel(self.tab_4)
        self.label_180.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_270.setObjectName("label_270")
        self.label_180.setObjectName("label_180")
    
        self.gridLayout_42.addWidget(self.label_180, 3, 0, 1, 1)
        self.label_182 = QtWidgets.QLabel(self.tab_4)
        self.label_182.setAlignment(QtCore.Qt.AlignCenter)
        self.label_182.setObjectName("label_182")
        self.gridLayout_42.addWidget(self.label_182, 5, 0, 1, 1)
        
#         self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_4)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_42.addWidget(self.pushButton_8, 11, 0, 1, 2)
        
#         self.lineEdit_32 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_36 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_36.sizePolicy().hasHeightForWidth())
        self.lineEdit_36.setSizePolicy(sizePolicy)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.gridLayout_42.addWidget(self.lineEdit_36, 3, 1, 1, 1)
        
        
        
        
#         self.lineEdit_35 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_37 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_37.sizePolicy().hasHeightForWidth())
        self.lineEdit_37.setSizePolicy(sizePolicy)
        self.lineEdit_37.setObjectName("lineEdit_37")
        self.gridLayout_42.addWidget(self.lineEdit_37, 6, 1, 1, 1)
        
        self.label_188 = QtWidgets.QLabel(self.tab_4)
        self.label_188.setAlignment(QtCore.Qt.AlignCenter)
#         self.label_278.setObjectName("label_278")
        self.label_188.setObjectName("label_188")
        self.gridLayout_42.addWidget(self.label_188, 6, 0, 1, 1)
        
        
        
        
#         self.comboBox_13 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_14 = QtWidgets.QComboBox(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_14.sizePolicy().hasHeightForWidth())
        self.comboBox_14.setSizePolicy(sizePolicy)
        self.comboBox_14.setObjectName("comboBox_13")
#         self.comboBox_14.addItem("Ch1 ")
#         self.comboBox_14.addItem("Ch2 ")
#         self.comboBox_14.addItem("Ch3 ")
#         self.comboBox_14.addItem("Ch1-2")
#         self.comboBox_14.addItem("Ch1-3")
#         self.comboBox_14.addItem("Ch2-3")
#         self.comboBox_14.addItem("Peak Record")
        self.gridLayout_42.addWidget(self.comboBox_14, 1, 0, 1, 2)
        
        
#         self.lineEdit_31 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_38 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_38.sizePolicy().hasHeightForWidth())
        self.lineEdit_38.setSizePolicy(sizePolicy)
        self.lineEdit_38.setObjectName("lineEdit_38")
        self.gridLayout_42.addWidget(self.lineEdit_38, 5, 1, 1, 1)
        

        self.lineEdit_36.setText("0")
        self.lineEdit_38.setText("5")
        self.lineEdit_37.setText("0")
        
        
        
#         self.layout_vertical_checkbox_2 = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox_3 = QtWidgets.QVBoxLayout()
        self.layout_vertical_checkbox_3.setObjectName("layout_vertical_checkbox_3")
        
        self.polygon_channel_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.polygon_channel_1.setObjectName("self.polygon_channel_1")
        
        self.polygon_channel_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.polygon_channel_2.setObjectName("self.polygon_channel_2")
  
        self.polygon_channel_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.polygon_channel_3.setObjectName("self.polygon_channel_3")
        
        self.polygon_channel_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.polygon_channel_4.setObjectName("self.polygon_channel_4")
        
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_1)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_2)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_3)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_4)

        self.polygon_channel_1.setChecked(True)
        self.polygon_channel_2.setChecked(True)
        self.polygon_channel_3.setChecked(True)
        self.polygon_channel_4.setChecked(True)

        self.gridLayout_42.addItem(self.layout_vertical_checkbox_3, 14, 0, 1,2 )
        
        
#         self.label_277 = QtWidgets.QLabel(self.tab_3)
        self.label_187 = QtWidgets.QLabel(self.tab_4)
        self.label_187.setAlignment(QtCore.Qt.AlignCenter)
        self.label_187.setObjectName("label_187")
        self.gridLayout_42.addWidget(self.label_187, 15, 0, 1, 2)
        
        self.polygon_Smooth_enable = QtWidgets.QCheckBox(self.tab_4)
        self.polygon_Smooth_enable.setObjectName("polygon_Smooth_enable")
        self.gridLayout_42.addWidget(self.polygon_Smooth_enable, 16, 0, 1, 2)        
        
        
        
#         self.lineEdit_33 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_39 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_39.sizePolicy().hasHeightForWidth())
        self.lineEdit_39.setSizePolicy(sizePolicy)
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.gridLayout_42.addWidget(self.lineEdit_39, 17, 1, 1, 1)

        

#         self.lineEdit_34 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_40 = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_40.sizePolicy().hasHeightForWidth())
        self.lineEdit_40.setSizePolicy(sizePolicy)
        self.lineEdit_40.setObjectName("lineEdit_40")
        self.gridLayout_42.addWidget(self.lineEdit_40, 18, 1, 1, 1)

        
#         self.lineEdit_33.setText("7")
#         self.lineEdit_34.setText("29")
        self.lineEdit_39.setText("7")
        self.lineEdit_40.setText("29")
        
        
        
#         self.label_275 = QtWidgets.QLabel(self.tab_3)
        self.label_185 = QtWidgets.QLabel(self.tab_4)
        self.label_185.setAlignment(QtCore.Qt.AlignCenter)
        self.label_185.setObjectName("label_185")
        self.gridLayout_42.addWidget(self.label_185, 17, 0, 1, 1)
#         self.label_276 = QtWidgets.QLabel(self.tab_3)
        self.label_186 = QtWidgets.QLabel(self.tab_4)
        self.label_186.setAlignment(QtCore.Qt.AlignCenter)
        self.label_186.setObjectName("label_186")
        self.gridLayout_42.addWidget(self.label_186, 18, 0, 1, 1)  

        
        
        spacerItem28 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_42.addItem(spacerItem28, 13, 0, 1, 2)        
        
        spacerItem27 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_42.addItem(spacerItem27, 9, 0, 1, 2)
        
#         self.label_274 = QtWidgets.QLabel(self.tab_3)
        self.label_184 = QtWidgets.QLabel(self.tab_4)
        self.label_184.setAlignment(QtCore.Qt.AlignCenter)
        self.label_184.setObjectName("label_184")
        self.gridLayout_42.addWidget(self.label_184, 10, 0, 1, 2)
        self.verticalLayout_52.addLayout(self.gridLayout_42)
        
        spacerItem29 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_52.addItem(spacerItem29)
        
        self.horizontalLayout_151.addLayout(self.verticalLayout_52)
        
        self.line_101 = QtWidgets.QFrame(self.tab_4)
        self.line_101.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_101.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_101.setObjectName("line_101")
        self.horizontalLayout_151.addWidget(self.line_101)
        
#         self.widget_28 = QtWidgets.QWidget(self.tab_3)
        self.widget_29 = PlotWidget(self.tab_4)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_29.sizePolicy().hasHeightForWidth())
        self.widget_29.setSizePolicy(sizePolicy)
        self.widget_29.setMinimumSize(QtCore.QSize(500, 500))
        self.widget_29.setObjectName("widget_29")
        self.horizontalLayout_151.addWidget(self.widget_29)
        
        

        styles = {"color": "r", "font-size": "20px"}
        self.widget_29.setLabel('left', 'Height', **styles)
        self.widget_29.setBackground('w')
        
        self.tab_widgets_subgating.addTab(self.tab_4, "")
#### polygon linear end


        
###### subtab sweep        
        self.tab_sweep = QtWidgets.QWidget()
        self.tab_sweep.setObjectName("tab_sweep")
#         self.tab_sweep = QtWidgets.QWidget()
#         self.tab_sweep.setObjectName("tab_sweep")

        
        self.tab_widgets_subgating.addTab(self.tab_sweep, "")          
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
        self.comboBox_option1.addItem("Green")
        self.comboBox_option1.addItem("Red")
        self.comboBox_option1.addItem("Blue")
        self.comboBox_option1.addItem("Orange")   
        
        
        
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
        self.comboBox_option2.addItem("Green")
        self.comboBox_option2.addItem("Red")
        self.comboBox_option2.addItem("Blue")
        self.comboBox_option2.addItem("Orange")  
        
        
        
        
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

        


        # report tab

        self.tab_report = QtWidgets.QWidget()
        self.tab_report.setObjectName("tab_report")
        
        self.horizontalLayout_report_tab = QtWidgets.QHBoxLayout(self.tab_report)
        self.horizontalLayout_report_tab.setObjectName("horizontalLayout_report_tab")

        self.textEdit = QtWidgets.QTextEdit(self.tab_report)
        self.textEdit.setObjectName("textEdit")

        self.horizontalLayout_report_tab.addWidget(self.textEdit)
        self.tab_widgets_main.addTab(self.tab_report, "")  
        
        self.textbox = "Current version: Amberlab V1.23" + "\n" + "you can find logs here:"
        self.textEdit.setPlainText(self.textbox)
        
     
        
        ### tab end
        

        
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
        
    # save project
        self.actionAdd_Save = QtWidgets.QAction(MainWindow)
        self.actionAdd_Save.setObjectName("actionAdd_Save")
        self.actionAdd_Load = QtWidgets.QAction(MainWindow)
        self.actionAdd_Load.setObjectName("actionAdd_Load")
        
        self.menuFiles.addAction(self.actionAdd_Save)
        self.menuFiles.addAction(self.actionAdd_Load)
       
    # save single file
        self.actionAdd_SaveSingleFile = QtWidgets.QAction(MainWindow)
        self.actionAdd_SaveSingleFile.setObjectName("actionAdd_SaveSingleFile")

        
        self.menuFiles.addAction(self.actionAdd_SaveSingleFile)    
    
    
    # save parameters
        self.actionAdd_SaveParameters = QtWidgets.QAction(MainWindow)
        self.actionAdd_SaveParameters.setObjectName("actionAdd_SaveParameters")
        self.actionAdd_LoadParameters = QtWidgets.QAction(MainWindow)
        self.actionAdd_LoadParameters.setObjectName("actionAdd_LoadParameters")

        self.menuFiles.addAction(self.actionAdd_SaveParameters)
        self.menuFiles.addAction(self.actionAdd_LoadParameters)
        
        
#         self.menuFiles.addAction(self.Save)
        self.menuFiles.addAction(self.actionClose)
        self.menubar.addAction(self.menuFiles.menuAction())

        # list of all connected functions
        self.actionImport.triggered.connect(self.openfolder)
        self.actionAdd_New.triggered.connect(self.add)
        self.actionAdd_Save.triggered.connect(self.save)
        self.actionAdd_Load.triggered.connect(self.load)
        self.actionAdd_SaveParameters.triggered.connect(self.save_parameters)
        self.actionAdd_LoadParameters.triggered.connect(self.load_parameters)
        
        self.actionAdd_SaveSingleFile.triggered.connect(self.save_single)

        
        self.button_update.clicked.connect(self.pressed)
        self.button_update_2.clicked.connect(self.filter_width_table)
        self.pushButton_5.clicked.connect(self.reset_linear_plot)
        self.pushButton_4.clicked.connect(self.last_page)
        self.pushButton_3.clicked.connect(self.next_page)
        
        self.pushButton_6.clicked.connect(self.polygon_reset_linear_plot)
        self.pushButton_8.clicked.connect(self.polygon_last_page)
        self.pushButton_7.clicked.connect(self.polygon_next_page)        
        
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

#         self.file_list_view.itemChanged.connect(self.update_names)
        self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)
        self.lineEdit_binwidth_2.editingFinished.connect(self.update_sweep_graphs)
        self.lineEdit_binwidth.editingFinished.connect(self.draw)

#         self.file_list_view.itemChanged.connect(self.update_names)
        self.lineEdit_gatevoltageminimum.editingFinished.connect(self.sweep_update_low)
        self.lineEdit_gatevoltagemaximum.editingFinished.connect(self.sweep_update_high)
        
        self.lineEdit_5.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_6.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_7.editingFinished.connect(self.lr_peak_width_plot)
        self.lineEdit_8.editingFinished.connect(self.lr_peak_width_plot)


        self.channel_1.stateChanged.connect(self.linear_plot)
        self.channel_2.stateChanged.connect(self.linear_plot)
        self.channel_3.stateChanged.connect(self.linear_plot)
        self.channel_4.stateChanged.connect(self.linear_plot)
        
        self.polygon_channel_1.stateChanged.connect(self.polygon_linear_plot)
        self.polygon_channel_2.stateChanged.connect(self.polygon_linear_plot)
        self.polygon_channel_3.stateChanged.connect(self.polygon_linear_plot)
        self.polygon_channel_4.stateChanged.connect(self.polygon_linear_plot)
        
        self.recalculate_peak_dataset = True

        self.lr_x_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)
        self.lr_y_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)

#         self.comboBox_6.currentIndexChanged.connect(self.width_scatter_channel_to_histogram_channel)
#         self.comboBox_5.currentIndexChanged.connect(self.width_scatter_channel_to_histogram_channel)
#         self.listView_channels_3.currentItemChanged.connect(self.width_histogram_channel_to_scatter_channel)
#         self.lineEdit_gatevoltage_2.editingFinished.connect(self.width_histogram_channel_to_scatter_channel)
#         self.lineEdit_gatevoltage_4.editingFinished.connect(self.width_histogram_channel_to_scatter_channel)
        
        self.comboBox_option1.currentIndexChanged.connect(self.update_sweep_1)
        self.comboBox_option2.currentIndexChanged.connect(self.update_sweep_2)
        
        self.w = OtherWindow(self)
        self.pushButton_resample.clicked.connect(self.openWindow)
        


        self.x = []
        self.y = []
        self.polygon = []
        self.points_inside = []
        self.graphWidget.scene().sigMouseClicked.connect(self.onMouseMoved) 


        
        self.subgating_x = []
        self.subgating_y = []
        self.subgating_polygon = []
        self.final_subgating_sweep_data = [[], [], [], []]
        self.subgating_sweep_data = [[], [], [], []]        
        self.subgating_graphWidget.scene().sigMouseClicked.connect(self.subgating_onMouseMoved) 
        
        self.polygon_trigger = False
        self.subgating_polygon_trigger = False    
        
        self.pushButton_9.clicked.connect(self.polygon_triggering)
        self.pushButton_10.clicked.connect(self.polygon_clean)
        self.pushButton_11.clicked.connect(lambda:self.subgating_scatter(switch_tab = True))
        
        
        self.subgating_pushButton_9.clicked.connect(self.subgating_polygon_triggering)
        self.subgating_pushButton_10.clicked.connect(self.subgating_polygon_clean)
        self.subgating_pushButton_12.clicked.connect(self.polygon_linear_plot_triggered_from_scatter_subtab)

        self.pushButton_12.clicked.connect(self.edit_polygon_shape)
        self.stop_edit_trigger = True
        
        self.subgating_pushButton_11.clicked.connect(self.subgating_edit_polygon_shape)
        self.subgating_stop_edit_trigger = True
        
    # check box trigger
        self.checkbox_ch1.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 1 state changed to ", 
                                                                           afterchange = self.checkbox_ch1.isChecked()))
        self.checkbox_ch2.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 2 state changed to ", 
                                                                           afterchange = self.checkbox_ch2.isChecked()))
        self.checkbox_ch3.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 3 state changed to ", 
                                                                           afterchange = self.checkbox_ch3.isChecked()))
        self.checkbox_ch12.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 1-2 state changed to ", 
                                                                           afterchange = self.checkbox_ch12.isChecked()))
        self.checkbox_ch13.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 1-3 state changed to ", 
                                                                           afterchange = self.checkbox_ch13.isChecked()))
        self.checkbox_ch23.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Channel 2-3 state changed to ", 
                                                                           afterchange = self.checkbox_ch23.isChecked()))
        self.checkbox_Droplet_Record.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox Droplet_Record state changed to ", 
                                                                           afterchange = self.checkbox_Droplet_Record.isChecked()))
        self.checkBox_7.stateChanged.connect(lambda:self.textbox_trigger(change = "checkbox All Channel state changed to ", 
                                                                           afterchange = self.checkBox_7.isChecked()))

        self.channel_1.stateChanged.connect(lambda:self.textbox_trigger(change = "Raw data viewer channel_1 state changed to ", 
                                                                           afterchange = self.channel_1.isChecked()))
        self.channel_2.stateChanged.connect(lambda:self.textbox_trigger(change = "Raw data viewer channel_2 state changed to ", 
                                                                           afterchange = self.channel_2.isChecked()))
        self.channel_3.stateChanged.connect(lambda:self.textbox_trigger(change = "Raw data viewer channel_3 state changed to ", 
                                                                           afterchange = self.channel_3.isChecked()))
        self.channel_4.stateChanged.connect(lambda:self.textbox_trigger(change = "Raw data viewer channel_4 state changed to ", 
                                                                           afterchange = self.channel_4.isChecked()))

        self.polygon_channel_1.stateChanged.connect(lambda:self.textbox_trigger(change = "User define linear graph channel_1 state changed to ", 
                                                                           afterchange = self.polygon_channel_1.isChecked()))
        self.polygon_channel_2.stateChanged.connect(lambda:self.textbox_trigger(change = "User define linear graph channel_2 state changed to ", 
                                                                           afterchange = self.polygon_channel_2.isChecked()))
        self.polygon_channel_3.stateChanged.connect(lambda:self.textbox_trigger(change = "User define linear graph channel_3 state changed to ", 
                                                                           afterchange = self.polygon_channel_3.isChecked()))
        self.polygon_channel_4.stateChanged.connect(lambda:self.textbox_trigger(change = "User define linear graph channel_4 state changed to ", 
                                                                           afterchange = self.polygon_channel_4.isChecked()))
        
    # combobox trigger
        self.comboBox_5.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter scatter plot x-axis changed to ", 
                                                                           afterchange = self.comboBox_5.currentText()))

        self.comboBox_6.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter scatter plot y-axis changed to ", 
                                                                           afterchange = self.comboBox_6.currentText())) 
        
        self.comboBox_peak_num_1.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating channel Green condition changed to ", 
                                                                           afterchange = self.comboBox_peak_num_1.currentText())) 
        self.comboBox_peak_num_2.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating channel Red condition changed to ", 
                                                                           afterchange = self.comboBox_peak_num_2.currentText()))  
        self.comboBox_peak_num_3.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating channel Blue condition changed to ", 
                                                                           afterchange = self.comboBox_peak_num_3.currentText())) 
        self.comboBox_peak_num_4.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating channel Orange condition changed to ", 
                                                                           afterchange = self.comboBox_peak_num_4.currentText())) 

        self.comboBox.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "2nd filter Quadrant Gating x-axis channel changed to ", 
                                                                           afterchange = self.comboBox.currentText()))
        self.comboBox_2.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "2nd filter Quadrant Gating y-axis channel changed to ", 
                                                                           afterchange = self.comboBox_2.currentText()))

        self.subgating_comboBox.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "3rd filter scatter plot x-axis channel changed to ", 
                                                                           afterchange = self.subgating_comboBox.currentText()))
        self.subgating_comboBox_2.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "3rd filter scatter plot y-axis channel changed to ", 
                                                                           afterchange = self.subgating_comboBox_2.currentText()))
        self.subgating_preselect_comboBox.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "3rd filter scatter plot x-axis arrtibute changed to ", 
                                                                           afterchange = self.subgating_preselect_comboBox.currentText()))
        self.subgating_preselect_comboBox_2.currentIndexChanged.connect(lambda:self.textbox_trigger(change = "3rd filter scatter plot y-axis arrtibute changed to ", 
                                                                           afterchange = self.subgating_preselect_comboBox_2.currentText()))
                        
    # listview trigger
        self.listView_channels_2.currentItemChanged.connect(lambda:self.textbox_trigger(change = "Sweept channel selection changed to ", 
                                                                           afterchange = self.listView_channels_2.currentItem().text()))
    
        self.listView_channels_3.currentItemChanged.connect(lambda:self.textbox_trigger(change = "1st filter histogram channel selection changed to ", 
                                                                           afterchange = self.listView_channels_3.currentItem().text()))

        self.listView_channels.currentItemChanged.connect(lambda:self.textbox_trigger(change = "2nd filter histogram channel selection changed to ", 
                                                                           afterchange = self.listView_channels.currentItem().text()))

        self.file_list_view.currentItemChanged.connect(lambda:self.textbox_trigger(change = "loading file changed to ", 
                                                                           afterchange = self.file_list_view.currentItem().text()))


    # lineedit trigger (editingFinished or textChanged)
        self.lineEdit_gatevoltage_2.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter histogram Min Width threshold changed to ", 
                                                                           afterchange = self.lineEdit_gatevoltage_2.text()))  
        self.lineEdit_gatevoltage_4.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter histogram Max Width threshold changed to ", 
                                                                           afterchange = self.lineEdit_gatevoltage_4.text()))   
        
        self.lineEdit_gatevoltagemaximum.textChanged.connect(lambda:self.textbox_trigger(change = "Sweep gating threshold voltage maximum changed to ", 
                                                                           afterchange = self.lineEdit_gatevoltagemaximum.text())) 
        self.lineEdit_gatevoltageminimum.textChanged.connect(lambda:self.textbox_trigger(change = "Sweep gating threshold voltage minimum change to ", 
                                                                           afterchange = self.lineEdit_gatevoltageminimum.text())) 
        self.lineEdit_increments.textChanged.connect(lambda:self.textbox_trigger(change = "Sweep gating threshold increments changed to ", 
                                                                           afterchange = self.lineEdit_increments.text()))       

        

        self.lineEdit_binwidth_2.textChanged.connect(lambda:self.textbox_trigger(change = "Sweep tab bin width changed to ", 
                                                                           afterchange = self.lineEdit_binwidth_2.text()))
        self.lineEdit_binwidth_3.textChanged.connect(lambda:self.textbox_trigger(change = "1nd filter histogram bin width changed to ", 
                                                                           afterchange = self.lineEdit_binwidth_3.text()))
        self.lineEdit_binwidth.textChanged.connect(lambda:self.textbox_trigger(change = "2nd filter histogram bin width changed to ", 
                                                                           afterchange = self.lineEdit_binwidth.text())) 
        self.lineEdit_gatevoltage.textChanged.connect(lambda:self.textbox_trigger(change = "2nd filter histogram gate voltage changed to ", 
                                                                                   afterchange = self.lineEdit_gatevoltage.text())) 
        

        
        self.lineEdit_5.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter Scatter plot x-axis min changed to ", 
                                                                           afterchange = self.lineEdit_5.text())) 
        self.lineEdit_6.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter Scatter plot y-axis min changed to ", 
                                                                           afterchange = self.lineEdit_6.text())) 
        self.lineEdit_7.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter Scatter plot x-axis max changed to ", 
                                                                           afterchange = self.lineEdit_7.text())) 
        self.lineEdit_8.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter Scatter plot y-axis max changed to ", 
                                                                           afterchange = self.lineEdit_8.text())) 
       
        self.lineEdit_9.textChanged.connect(lambda:self.textbox_trigger(change = "Voltage Threshold Green(V) changed to ", 
                                                                           afterchange = self.lineEdit_9.text())) 
        self.lineEdit_10.textChanged.connect(lambda:self.textbox_trigger(change = "Voltage Threshold Far Red(V) changed to ", 
                                                                           afterchange = self.lineEdit_10.text()))
        self.lineEdit_11.textChanged.connect(lambda:self.textbox_trigger(change = "Voltage Threshold Ultra Violet(V) changed to ", 
                                                                           afterchange = self.lineEdit_11.text()))
        self.lineEdit_12.textChanged.connect(lambda:self.textbox_trigger(change = "Voltage Threshold Orange(V) changed to ", 
                                                                           afterchange = self.lineEdit_12.text()))
        
        self.lineEdit_peak_num_1.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating # of peaks in channel Orange changed to ", 
                                                                           afterchange = self.lineEdit_peak_num_1.text()))
        self.lineEdit_peak_num_2.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating # of peaks in channel Orange changed to ", 
                                                                           afterchange = self.lineEdit_peak_num_2.text()))
        self.lineEdit_peak_num_3.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating # of peaks in channel Orange changed to ", 
                                                                           afterchange = self.lineEdit_peak_num_3.text()))
        self.lineEdit_peak_num_4.textChanged.connect(lambda:self.textbox_trigger(change = "1st filter multi peaks gating # of peaks in channel Orange changed to ", 
                                                                           afterchange = self.lineEdit_peak_num_4.text()))
        
        self.lineEdit_scatterxvoltage.textChanged.connect(lambda:self.textbox_trigger(change = "2nd filter quadrant gating x-axis gate voltage changed to ", 
                                                                           afterchange = self.lineEdit_scatterxvoltage.text()))
        self.lineEdit_scatteryvoltage.textChanged.connect(lambda:self.textbox_trigger(change = "2nd filter quadrant gating y-axis gate voltage changed to ", 
                                                                           afterchange = self.lineEdit_scatteryvoltage.text()))
        
        
        
        try:
            self.file_list_view.itemChanged.connect(lambda:self.chart_title_change(change = self.file_list_view.currentItem().text()))
        except:
            self.file_list_view.setCurrentRow(0)
            self.file_list_view.itemChanged.connect(lambda:self.chart_title_change(change = self.file_list_view.currentItem().text()))
            
            
        self.load = False
        
        # add default parameters

        self.inside2 = []
        self.polygon_for_edit = []
        self.points = []
        
        self.points_inside_list = []

        self.subgating_inside2 = []
        self.subgating_points_inside = []

        self.subgating_polygon = []
        self.subgating_polygon_for_edit = []
        self.subgating_polygon_trigger = []
        self.subgating_points = []
        self.subgating_points_inside_list = []        
        
        
        
    def openwindow_filter(self):
        # self.dialog is the current creating filter
        # self.window_filter is the list contain all the filter tabs, use show() to show
        # self.filter_count count how many filters created
        # self.filter_list_view is the list view
        # self.filter_dict is the dict contain filter name and index, use name to find index, show in self.window_filter

        if self.filter_list_view.currentRow() == 0:
            self.dialog = window_filter(self)
            self.window_filter.append(self.dialog)

            self.filter_count = self.filter_count + 1 
            filter_name = "filter " + str(self.filter_count)
            self.filter_list_view.addItem(filter_name)

            self.filter_dict[filter_name] = int(self.filter_count)

            self.dialog.show()
        else:
            name = self.filter_list_view.currentItem().text()
            list_number = self.filter_dict[name]
            self.window_filter[list_number].show()
            
    def getValue(self, val):
        # add tree view
        current_branch = val
        self.tree_index = (val.row(),)
        
        while current_branch.parent().row() != -1:    
            self.tree_index += (current_branch.parent().row(),)
            current_branch = current_branch.parent()
        print(self.tree_index)

#         self.window_filter[self.tree_index].show()
        self.tree_dic[self.tree_index]['tree_windowfilter'].show()
    
#         if self.tree_index == (0,):
#             # assign a valid key to new branch
#             find_a_key = False
#             key_count = 0
#             while not find_a_key:         
#                 new_index = (key_count,) + self.tree_index
#                 if new_index in self.tree_dic:
#                     key_count += 1
#                 else:
#                     find_a_key = True

#             self.tree_dic[new_index] = StandardItem('New graph', 12 - len(new_index))
#             self.tree_dic[self.tree_index].appendRow(self.tree_dic[new_index])

#             self.treeView.expandAll()
            
#             # open a new window for the new branch
            
#             # reassign tree_index, new window need index to create child branch
#             self.tree_index = new_index
            
#             self.dialog = window_filter(self)
#             self.window_filter[new_index] = self.dialog

#             self.dialog.show()
            
#         else:
#             self.window_filter[self.tree_index].show()
            

    def chart_title_change(self, change):
        if len(str(change)) > 30:
            change = str(change)[0:30]
            
        self.graphWidget.setTitle(str(change), color="b", size="10pt")
        self.graphWidget_width_scatter.setTitle(str(change), color="b", size="10pt")
        self.widget_28.setTitle(str(change), color="b", size="10pt")
        self.histogram_graphWidget_3.setTitle(str(change), color="b", size="10pt")
        self.histogram_graphWidget.setTitle(str(change), color="b", size="10pt")
        self.subgating_graphWidget.setTitle(str(change), color="b", size="10pt")
        self.widget_29.setTitle(str(change), color="b", size="10pt")
        
        
#         = PlotWidget(self.tab_gating)

    def textbox_trigger(self,change, afterchange):
        # record change in the log
        self.textbox = self.textbox + "\n" + str(change) +  str(afterchange)

        
        self.textEdit.setPlainText(self.textbox)   
        # done
        
        
        
    def subgating_scatter(self,switch_tab = False, pressed_function_redo = False):
        if pressed_function_redo == True:
            self.subgating_polygon_clean()
            self.polygon_clean()   
            
        # load parameters
        if self.load == True: 

            with open(str(self.loadname), 'rb') as filehandle:
                # read the data as binary data stream
                parameters = pickle.load(filehandle)

            self.inside2 = parameters[53]
            self.points_inside = parameters[54]
            self.polygon_inside_label_29.setText(parameters[55])
            self.polygon = parameters[56]
            self.polygon_for_edit = parameters[57]
            polygon_lines = parameters[57]
            polygon_points = parameters[57]
            self.polygon_trigger = parameters[58]
            self.points = parameters[59]
            self.points_inside_list = parameters[60]
                
            if self.polygon_for_edit != []:
                        
                self.polygon_lines = []

                for i in range(len(polygon_lines)):
                    self.polygon_lines.append([])
                    if polygon_lines[i]!= []:
                        self.polygon_lines[i].append(self.graphWidget.plot([polygon_lines[i][0][0],polygon_lines[i][0][0]], 
                                                                                  [polygon_lines[i][0][1],polygon_lines[i][0][1]],
                                                                                  pen=pg.mkPen(color=('r'), width=5, 
                                                                                          style=QtCore.Qt.DashLine)))
                    for ii in range(len(polygon_lines[i])-1):
                        self.polygon_lines[-1].append(self.graphWidget.plot([polygon_lines[i][ii][0],polygon_lines[i][ii+1][0]], 
                                                                          [polygon_lines[i][ii][1],polygon_lines[i][ii+1][1]],
                                                                          pen=pg.mkPen(color=('r'), width=5, 
                                                                                  style=QtCore.Qt.DashLine)))


                for i in range(len(polygon_lines)):  
                    if polygon_lines[i]!= []:
                        self.polygon_lines[i].append(self.graphWidget.plot([polygon_lines[i][0][0],polygon_lines[i][-1][0]], 
                                                                                  [polygon_lines[i][0][1],polygon_lines[i][-1][1]],
                                                                                  pen=pg.mkPen(color=('r'), width=5, 
                                                                                          style=QtCore.Qt.DashLine)))
                self.polygon_points = []

                for i in range(len(polygon_points)):
                    self.polygon_points.append([])
                    if polygon_points[i]!= []:
                        self.polygon_points[i].append(self.graphWidget.plot([polygon_points[i][0][0],polygon_points[i][0][0]], 
                                                                      [polygon_points[i][0][1],polygon_points[i][0][1]],
                                                                      pen=None, symbol='o'))
                    for ii in range(len(polygon_points[i])-1):
                        self.polygon_points[-1].append(self.graphWidget.plot([polygon_points[i][ii][0],polygon_points[i][ii+1][0]], 
                                                                      [polygon_points[i][ii][1],polygon_points[i][ii+1][1]],
                                                                      pen=None, symbol='o'))
                for i in range(len(polygon_points)):
                    if polygon_points[i]!= []:
                        self.polygon_points[i].append(self.graphWidget.plot([polygon_points[i][0][0],polygon_points[i][-1][0]], 
                                                                      [polygon_points[i][0][1],polygon_points[i][-1][1]],
                                                                      pen=None, symbol='o'))
            # laod end
            
        if switch_tab == True:
            self.tab_widgets_main.setCurrentIndex(4)
            self.tab_widgets_subgating.setCurrentIndex(0)
            
        if self.polygon_trigger == False:
            subgating_plot_update, self.textbox = self.ui_state.subgating_replot_check(self.points_inside_square, self.quadrant1_list,
                                                             self.subgating_comboBox.currentText(), 
                                                             self.subgating_comboBox_2.currentText(), 
                                                             self.subgating_preselect_comboBox.currentText(), 
                                                             self.subgating_preselect_comboBox_2.currentText(),
                                                             self.textbox,
                                                            self.lineEdit_third_layer_density_adjust.text())
            try:
                if subgating_plot_update:
                    self.points_inside = list(compress(self.points_inside_square, self.quadrant1_list))
            except:
                subgating_plot_update = False
                print("no points extracted")
        else:
            self.polygon_triggering()
            subgating_plot_update, self.textbox = self.ui_state.subgating_replot_check(self.points_inside_square, self.points_inside,
                                             self.subgating_comboBox.currentText(), 
                                             self.subgating_comboBox_2.currentText(), 
                                             self.subgating_preselect_comboBox.currentText(), 
                                             self.subgating_preselect_comboBox_2.currentText(),
                                             self.textbox,
                                             self.lineEdit_third_layer_density_adjust.text())

        
        self.checkA = time.time()
        if subgating_plot_update or pressed_function_redo:


            self.lineEdit_38.setText(str(5)) 


            if self.subgating_preselect_comboBox.currentIndex() == 0:
                data_in_subgating_x = self.working_data[self.subgating_comboBox.currentIndex()]  
            else:
                data_in_subgating_x = self.peak_width_working_data[self.subgating_comboBox.currentIndex()]             

            if self.subgating_preselect_comboBox_2.currentIndex() == 0:
                data_in_subgating_y = self.working_data[self.subgating_comboBox_2.currentIndex()] 
            else:
                data_in_subgating_y = self.peak_width_working_data[self.subgating_comboBox_2.currentIndex()] 


            x_axis_channel = self.subgating_comboBox.currentIndex()
            y_axis_channel = self.subgating_comboBox_2.currentIndex()
            x_axis_name = self.subgating_preselect_comboBox.currentText() + " " + self.subgating_comboBox.currentText()
            y_axis_name = self.subgating_preselect_comboBox_2.currentText() + " " + self.subgating_comboBox_2.currentText()
            self.subgating_sweep_data = [[], [], [], []]


            if len(self.points_inside) !=0:
                self.subgating_graphWidget.clear()

                self.subgating_graphWidget.setLabel('left', y_axis_name, color='b')
                self.subgating_graphWidget.setLabel('bottom', x_axis_name, color='b')

    #             self.subgating_Ch1_channel0 = subgating_data[x_axis_channel]
    #             self.subgating_Ch1_channel1 = subgating_data[y_axis_channel]

                self.subgating_Ch1_channel0 = [ data_in_subgating_x[i] for i in self.points_inside]
                self.subgating_Ch1_channel1 = [ data_in_subgating_y[i] for i in self.points_inside]

                
                for ch in range(len(self.working_data)):
                    self.subgating_sweep_data[ch] = [self.working_data[ch][i] for i in self.points_inside]

                max_voltage = 12
                bins = 1000
                steps = max_voltage / bins

                # all data is first sorted into a histogram
                histo, _, _ = np.histogram2d(self.subgating_Ch1_channel0, self.subgating_Ch1_channel1, bins,
                                             [[0, max_voltage], [0, max_voltage]],
                                             density=True)
                max_density = histo.max()
                print('histo',histo)
                percentage_coefficient = int(self.lineEdit_third_layer_density_adjust.text())
                
                # made empty array to hold the sorted data according to density
                density_listx = []
                density_listy = []
                for i in range(6):
                    density_listx.append([])
                    density_listy.append([])
                    
                    
                self.checkB = time.time()
# Transparency            
#                 self.subgating_graphWidget.plot(self.subgating_Ch1_channel0, self.subgating_Ch1_channel1, symbol='p', pen=None, symbolPen=None,
#                                       symbolSize=5, symbolBrush=(255,0,0,50))
#                 self.subgating_graphWidget.autoRange()
                
                for i in range(len(self.subgating_Ch1_channel0)):
                    x = self.subgating_Ch1_channel0[i]
                    y = self.subgating_Ch1_channel1[i]
                    a = int(x / steps)
                    b = int(y / steps)
                    if a >= 12:
                        a = 11
                    if b >= 12:
                        b = 11

                    # checking for density, the value divided by steps serves as the index
                    density = histo[a][b]
                    
                    percentage = density / max_density * 100 *percentage_coefficient

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


                    self.subgating_graphWidget.plot(density_listx[i], density_listy[i], symbol='p', pen=None, symbolPen=None,
                                          symbolSize=5, symbolBrush=(red, blue, green))
                    
                    
                self.checkC = time.time()
                
                self.subgating_thresholdUpdated_2()
                self.subgating_graphWidget.autoRange()
                # fill quadrant table
                try:
                    droplets = float(self.lineEdit_totaldroplets.text())
                    totalpercent1 = round(len(self.Ch1_channel0) / droplets * 100, 2)
                except:
                    totalpercent1 = 0

                view1 = str(round(100 * len(self.points_inside) / len(self.Ch1_channel0), 2))
                single_peak_count_channel0 = 0
                multi_peak_count_channel0 = 0
                single_peak_count_channel1 = 0
                multi_peak_count_channel1 = 0
                

                a = list(set(self.points_inside).intersection(set(self.points_inside_square)))
 
                self.checkC1 = time.time()
#                 for i in a:
                for i in range(len(a)):
                    if self.Ch1_channel0_peak_num[i] == 1:
                        single_peak_count_channel0 += 1
                    elif self.Ch1_channel0_peak_num[i] > 1:
                        multi_peak_count_channel0 += 1
                    if self.Ch1_channel1_peak_num[i] == 1:
                        single_peak_count_channel1 += 1
                    elif self.Ch1_channel1_peak_num[i] > 1:
                        multi_peak_count_channel1 += 1
                            
                self.checkC2 = time.time()
                x_single_1 = str(round(100 * single_peak_count_channel0 / len(self.points_inside), 2))
                y_single_1 = str(round(100 * single_peak_count_channel1 / len(self.points_inside), 2))
                x_multi_1 = str(round(100 * multi_peak_count_channel0 / len(self.points_inside), 2))
                y_multi_1 = str(round(100 * multi_peak_count_channel1 / len(self.points_inside), 2))
                
                self.checkC3 = time.time()
                self.subgating_tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(len(self.points_inside))))
                self.subgating_tableView_scatterquadrants.setItem(0, 1, QTableWidgetItem(view1))
                self.subgating_tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
                self.subgating_tableView_scatterquadrants.setItem(0, 3, QTableWidgetItem(x_single_1))
                self.subgating_tableView_scatterquadrants.setItem(0, 4, QTableWidgetItem(y_single_1))
                self.subgating_tableView_scatterquadrants.setItem(0, 5, QTableWidgetItem(x_multi_1))
                self.subgating_tableView_scatterquadrants.setItem(0, 6, QTableWidgetItem(y_multi_1))

                
                self.checkD = time.time()
                # load parameters
                if self.load == True:  
                    self.load = False

                    with open(str(self.loadname), 'rb') as filehandle:
                        # read the data as binary data stream
                        parameters = pickle.load(filehandle)

                    self.subgating_inside2 = parameters[60]
                    self.subgating_points_inside = parameters[61]
                    self.subgating_polygon_inside_label_29.setText(parameters[63])
                    self.subgating_polygon = parameters[64]
                    self.subgating_polygon_for_edit = parameters[65]
                    subgating_polygon_lines = parameters[65]
                    subgating_polygon_points = parameters[65]
                    self.subgating_polygon_for_edit = parameters[65]
                    self.subgating_polygon_trigger = parameters[66]
                    self.subgating_points = parameters[67]
                    self.subgating_points_inside_list = parameters[68]

                    if self.subgating_polygon != [[]]: 
                        self.subgating_polygon_lines = []

                        for i in range(len(subgating_polygon_lines)):
                            self.subgating_polygon_lines.append([])
                            if subgating_polygon_lines[i]!= []:
                                self.subgating_polygon_lines[i].append(self.subgating_graphWidget.plot([subgating_polygon_lines[i][0][0],subgating_polygon_lines[i][0][0]], 
                                                                                          [subgating_polygon_lines[i][0][1],subgating_polygon_lines[i][0][1]],
                                                                                          pen=pg.mkPen(color=('r'), width=5, 
                                                                                                  style=QtCore.Qt.DashLine)))
                            for ii in range(len(subgating_polygon_lines[i])-1):
                                self.subgating_polygon_lines[-1].append(self.subgating_graphWidget.plot([subgating_polygon_lines[i][ii][0],subgating_polygon_lines[i][ii+1][0]], 
                                                                                  [subgating_polygon_lines[i][ii][1],subgating_polygon_lines[i][ii+1][1]],
                                                                                  pen=pg.mkPen(color=('r'), width=5, 
                                                                                          style=QtCore.Qt.DashLine)))


                        for i in range(len(subgating_polygon_lines)):  
                            if subgating_polygon_lines[i]!= []:
                                self.subgating_polygon_lines[i].append(self.subgating_graphWidget.plot([subgating_polygon_lines[i][0][0],subgating_polygon_lines[i][-1][0]], 
                                                                                          [subgating_polygon_lines[i][0][1],subgating_polygon_lines[i][-1][1]],
                                                                                          pen=pg.mkPen(color=('r'), width=5, 
                                                                                                  style=QtCore.Qt.DashLine)))
                        self.subgating_polygon_points = []

                        for i in range(len(subgating_polygon_points)):
                            self.subgating_polygon_points.append([])
                            if subgating_polygon_points[i]!= []:
                                self.subgating_polygon_points[i].append(self.subgating_graphWidget.plot([subgating_polygon_points[i][0][0],subgating_polygon_points[i][0][0]], 
                                                                              [subgating_polygon_points[i][0][1],subgating_polygon_points[i][0][1]],
                                                                              pen=None, symbol='o'))
                            for ii in range(len(subgating_polygon_points[i])-1):
                                self.subgating_polygon_points[-1].append(self.subgating_graphWidget.plot([subgating_polygon_points[i][ii][0],subgating_polygon_points[i][ii+1][0]], 
                                                                              [subgating_polygon_points[i][ii][1],subgating_polygon_points[i][ii+1][1]],
                                                                              pen=None, symbol='o'))
                        for i in range(len(subgating_polygon_points)):
                            if subgating_polygon_points[i]!= []:
                                self.subgating_polygon_points[i].append(self.subgating_graphWidget.plot([subgating_polygon_points[i][0][0],subgating_polygon_points[i][-1][0]], 
                                                                              [subgating_polygon_points[i][0][1],subgating_polygon_points[i][-1][1]],
                                                                              pen=None, symbol='o'))

                        self.widget_29.autoRange()

                        self.polygon_linear_plot_triggered_from_scatter_subtab()
                        
                        #load end

            elif len(self.points_inside) ==0:
                self.subgating_graphWidget.clear()
                self.subgating_Ch1_channel0  = []
                self.subgating_Ch1_channel1 = []


        
    def polygon_triggering(self):
        if self.polygon_trigger == False:
            self.polygon_trigger = True
            self.points = list(zip(self.Ch1_channel0,self.Ch1_channel1))

            self.polygon_points = [[]]
            self.polygon_lines = [[]]
            self.points_inside = []
            self.polygon = [[]]
            self.polygon_for_edit = [[]]
            self.points_inside_list = []
        elif self.polygon[-1] == [] and self.x == []:
            print("Polygon button clicked")
        else:
                                
            path = mpltPath.Path(self.polygon[-1])
            self.inside2 = path.contains_points(self.points)

            start_end_dot_x = [self.x[0],self.x[-1]]
            start_end_dot_y = [self.y[0],self.y[-1]]            
            self.polygon_lines[-1].append(self.graphWidget.plot(start_end_dot_x, start_end_dot_y,pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
            self.polygon_points[-1].append(self.graphWidget.plot(start_end_dot_x, start_end_dot_y, pen=None, symbol='o'))
            
            
            # show the dots have index before the first filter
#             self.points_inside.extend(list(compress(self.points_inside_square, self.inside2)))

            self.points_inside_list.append(list(compress(self.points_inside_square, self.inside2)))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func=lambda arr:set(arr) 
            self.points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.points_inside))
            self.polygon_inside_label_29.setText(points_inside) 
     
            self.polygon.append([])
            self.polygon_points.append([])
            self.polygon_lines.append([])
            self.polygon_for_edit.append([])
            self.x = []
            self.y = []
 
    def subgating_polygon_triggering(self):
#         self.polygon_trigger = True
        if self.subgating_polygon_trigger == False:
            self.subgating_polygon_trigger = True
            self.subgating_points = list(zip(self.subgating_Ch1_channel0,self.subgating_Ch1_channel1))
            
            self.subgating_polygon_points = [[]]
            self.subgating_polygon_for_edit = [[]]
            self.subgating_points_inside_list = []
            
            
            self.subgating_polygon_lines = [[]]
            self.subgating_points_inside = [[]]
            self.subgating_polygon = [[]]
            
            self.final_subgating_sweep_data = [[],[],[],[]]
            
        elif self.subgating_polygon[-1] == [] and self.subgating_x == []:
            print("Polygon button clicked")
        else:
            if self.subgating_polygon != []:
                path = mpltPath.Path(self.subgating_polygon[-1])
                self.subgating_inside2 = path.contains_points(self.subgating_points)

                
                # compare the T,F with last step T,F
                
                start_end_dot_x = [self.subgating_x[0],self.subgating_x[-1]]
                start_end_dot_y = [self.subgating_y[0],self.subgating_y[-1]]  
                
                self.subgating_polygon_lines[-1].append(self.subgating_graphWidget.plot(start_end_dot_x, start_end_dot_y,pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
                self.subgating_polygon_points[-1].append(self.subgating_graphWidget.plot(start_end_dot_x, start_end_dot_y, pen=None, symbol='o'))
           
                # show the dots have index before the first filter
#                 self.subgating_points_inside.extend(list(compress(self.points_inside, self.subgating_inside2)))


                # if create multipul filtering, use points_inside and subgating_points_inside, those unwraped the list inside list
                self.subgating_points_inside_list.append(list(compress(self.points_inside, self.subgating_inside2)))
    

#                 print('self.points_inside_square',self.points_inside_square)

    

                arr = []
                for i in self.subgating_points_inside_list:
                    for ii in i:
                        arr.append(ii)
                # remove duplicate points
                rem_duplicate_func=lambda arr:set(arr) 
                self.subgating_points_inside = list(rem_duplicate_func(arr))
                
                print('self.subgating_points_inside',self.subgating_points_inside)

            
                points_inside = 'Inside: ' + str(len(self.subgating_points_inside))
                self.subgating_polygon_inside_label_29.setText(points_inside)
     
            

                for ch in range(len(self.working_data)):
                    self.final_subgating_sweep_data[ch] = [self.working_data[ch][i] for i in self.subgating_points_inside]

                self.subgating_polygon.append([])
                self.subgating_polygon_points.append([])
                self.subgating_polygon_lines.append([])
                self.subgating_polygon_for_edit.append([])
                self.subgating_x = []
                self.subgating_y = []
        
    def subgating_polygon_clean(self):
        self.subgating_polygon_inside_label_29.setText('Inside: 0') 
        self.subgating_x = []
        self.subgating_y = []
        self.subgating_polygon = [[]]
        self.subgating_points_inside = [[]]
#         try:
#             self.subgating_graphWidget.removeItem(self.subgating_polygon_points)
            
#             for i in range(len(self.subgating_polygon_lines)):
#                 self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[i])

#         except:
#             print("no subgating_polygon drawed")
#         self.subgating_polygon_trigger = False 
        try:
            for i_list in range(len(self.subgating_polygon_points)):
                for i in range(len(self.subgating_polygon_points[i_list])):
                    self.subgating_graphWidget.removeItem(self.subgating_polygon_points[i_list][i])
                    self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[i_list][i])

        except:
            print("no subgating_polygon drawed")
        self.subgating_polygon_trigger = False
                


    def polygon_clean(self):
        self.polygon_inside_label_29.setText('Inside: 0') 
        self.x = []
        self.y = []
        self.polygon = [[]]
        self.points_inside = [[]]
        try:
            for i_list in range(len(self.polygon_points)):
                for i in range(len(self.polygon_points[i_list])):
                    self.graphWidget.removeItem(self.polygon_points[i_list][i])
                    self.graphWidget.removeItem(self.polygon_lines[i_list][i])

        except:
            print("no polygon drawed")
        self.polygon_trigger = False

        
    def subgating_onMouseMoved(self,point):
        if self.subgating_stop_edit_trigger and self.subgating_polygon_trigger:

            p = self.subgating_graphWidget.plotItem.vb.mapSceneToView(point.scenePos())

            self.subgating_x.append(p.x())
            self.subgating_y.append(p.y())
            
            self.subgating_polygon_points[-1].append(self.subgating_graphWidget.plot(self.subgating_x[-2:len(self.subgating_x)], self.subgating_y[-2:len(self.subgating_y)], pen=None, symbol='o'))
            self.subgating_polygon_lines[-1].append(self.subgating_graphWidget.plot(self.subgating_x[-2:len(self.subgating_x)], self.subgating_y[-2:len(self.subgating_y)],pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
            self.subgating_polygon[-1].append([p.x(),p.y()])
            self.subgating_polygon_for_edit[-1].append([p.x(),p.y()])
 

        elif self.subgating_stop_edit_trigger == False:
            p = self.subgating_graphWidget.plotItem.vb.mapSceneToView(point.scenePos())     
            
            nearest_distance = 20
            
            
            nearest_index = 0
            nearest_list = 0
            
            list_count = 0
            for i_list in self.subgating_polygon_for_edit:
                count = 0
                for i in i_list:
                    diff_x = abs(i[0] - p.x())
                    diff_y = abs(i[1] - p.y())
                    diff_total = sqrt(diff_x*diff_x + diff_y*diff_y)
                    if diff_total < nearest_distance:           
                        nearest_distance = diff_total
                        nearest_index = count
                        nearest_list = list_count
                    count += 1
                list_count += 1


            # remove points

            if nearest_index == 0:
                self.subgating_graphWidget.removeItem(self.subgating_polygon_points[nearest_list][-1])
            

            self.subgating_graphWidget.removeItem(self.subgating_polygon_points[nearest_list][nearest_index])
            self.subgating_graphWidget.removeItem(self.subgating_polygon_points[nearest_list][nearest_index+1])
            # change points  
            # bug: when use in unfinished polygon, line will couse error
            self.subgating_polygon_for_edit[nearest_list][nearest_index] = [p.x(),p.y()]
            



                          
            if nearest_index == 0:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.subgating_polygon_points[nearest_list][nearest_index-1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            
                edit_x = [p.x(),p.x()]
                edit_y = [p.y(), p.y()]
                
                self.subgating_polygon_points[nearest_list][nearest_index] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o') 
            else:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.subgating_polygon_points[nearest_list][nearest_index] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')                
                
            if nearest_index == len(self.subgating_polygon_for_edit[nearest_list])-1:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][0][1], p.y()]

                self.subgating_polygon_points[nearest_list][nearest_index+1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            else:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.subgating_polygon_points[nearest_list][nearest_index+1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')





            # remove lines
            if nearest_index == 0:
                self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[nearest_list][-1])
            self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[nearest_list][nearest_index])
            self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[nearest_list][nearest_index+1])
            
            # change lines  
            # bug: when use in unfinished polygon, line will couse error
            
            if nearest_index == 0:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.subgating_polygon_lines[nearest_list][nearest_index-1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
                
                
            else:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.subgating_polygon_lines[nearest_list][nearest_index] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
                          

            if nearest_index == len(self.subgating_polygon_for_edit[nearest_list])-1:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][0][1], p.y()]

                self.subgating_polygon_lines[nearest_list][nearest_index+1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))

                
            else:
                edit_x = [self.subgating_polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.subgating_polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.subgating_polygon_lines[nearest_list][nearest_index+1] = self.subgating_graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
                

            self.subgating_nearest_list = nearest_list
            


            
    def onMouseMoved(self,point):
        if self.stop_edit_trigger and self.polygon_trigger:

            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())

            self.x.append(p.x())
            self.y.append(p.y())

            self.polygon_points[-1].append(self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)], pen=None, symbol='o'))
            self.polygon_lines[-1].append(self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)],pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)))
            self.polygon[-1].append([p.x(),p.y()])
            self.polygon_for_edit[-1].append([p.x(),p.y()])

        elif self.stop_edit_trigger == False:
            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())     
            
            nearest_distance = 20
            
            
            nearest_index = 0
            nearest_list = 0
            
            list_count = 0
            for i_list in self.polygon_for_edit:
                count = 0
                for i in i_list:
                    diff_x = abs(i[0] - p.x())
                    diff_y = abs(i[1] - p.y())
                    diff_total = sqrt(diff_x*diff_x + diff_y*diff_y)
                    if diff_total < nearest_distance:           
                        nearest_distance = diff_total
                        nearest_index = count
                        nearest_list = list_count
                    count += 1
                list_count += 1

            # remove points

            if nearest_index == 0:
                self.graphWidget.removeItem(self.polygon_points[nearest_list][-1])
            

            self.graphWidget.removeItem(self.polygon_points[nearest_list][nearest_index])
            self.graphWidget.removeItem(self.polygon_points[nearest_list][nearest_index+1])
            # change points  
            # bug: when use in unfinished polygon, line will couse error
            self.polygon_for_edit[nearest_list][nearest_index] = [p.x(),p.y()]
            



                          
            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.polygon_points[nearest_list][nearest_index-1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            
                edit_x = [p.x(),p.x()]
                edit_y = [p.y(), p.y()]
                
                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o') 
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1],p.y()]

                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')                
                
            if nearest_index == len(self.polygon_for_edit[nearest_list])-1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_points[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.polygon_points[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=None, symbol='o')





            # remove lines
            if nearest_index == 0:
                self.graphWidget.removeItem(self.polygon_lines[nearest_list][-1])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index+1])
            
            # change lines  
            # bug: when use in unfinished polygon, line will couse error
            
            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index-1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
                

            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index-1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index-1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
            

            if nearest_index == len(self.polygon_for_edit[nearest_list])-1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index+1][0],p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index+1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index+1] = self.graphWidget.plot(edit_x, edit_y,
                                      pen=pg.mkPen(color=('b'), width=5, style=QtCore.Qt.DashLine))

            self.nearest_list = nearest_list
            
            
    def subgating_edit_polygon_shape(self):
        
        print("subgating_edit_polygon_shape activate")
        if self.subgating_stop_edit_trigger == True:
            self.subgating_polygon_triggering()
            self.subgating_stop_edit_trigger = False
            self.subgating_polygon_temp = []
#             self.polygon_temp = []
#             self.subgating_polygon_temp = self.subgating_polygon_lines
        else:
        
                
            self.subgating_stop_edit_trigger = True
            
            for ii in range(len(self.subgating_polygon_lines)):
                for i in range(len(self.subgating_polygon_lines[ii])):
                    self.subgating_graphWidget.removeItem(self.subgating_polygon_lines[ii][i])     
                    
            for ii in range(len(self.subgating_polygon_lines)-1):
                for i in range(1,len(self.subgating_polygon_lines[ii])-1):
                    list_x = [self.subgating_polygon_for_edit[ii][i][0],self.subgating_polygon_for_edit[ii][i-1][0]]
                    list_y = [self.subgating_polygon_for_edit[ii][i][1],self.subgating_polygon_for_edit[ii][i-1][1]]
                    self.subgating_polygon_lines[ii][i] = self.subgating_graphWidget.plot(list_x, 
                                                                      list_y,
                                                                      pen=pg.mkPen(color=('r'), 
                                                                                   width=5, 
                                                                                   style=QtCore.Qt.DashLine)) 

            for ii in range(len(self.subgating_polygon_lines)-1):
                list_x = [self.subgating_polygon_for_edit[ii][0][0],self.subgating_polygon_for_edit[ii][-1][0]]
                list_y = [self.subgating_polygon_for_edit[ii][0][1],self.subgating_polygon_for_edit[ii][-1][1]]                    
                self.subgating_polygon_lines[ii][-1] = self.subgating_graphWidget.plot(list_x, list_y,
                                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)) 

                
                    
            for i in range(len(self.subgating_polygon_for_edit)-1):
                path = mpltPath.Path(self.subgating_polygon_for_edit[i])
                self.subgating_inside2 = path.contains_points(self.subgating_points)
                # show the dots have index before the first filter
                # bug fix: shows the dots have index from first layer
                self.subgating_points_inside = list(compress(self.points_inside, self.subgating_inside2))
                self.subgating_points_inside_list[i] = list(compress(self.points_inside, self.subgating_inside2))
#                 self.subgating_points_inside = list(compress(self.points_inside_square, self.subgating_inside2))
#                 self.subgating_points_inside_list[i] = list(compress(self.points_inside_square, self.subgating_inside2))

                print('self.subgating_points_inside',self.subgating_points_inside)
                print('self.subgating_points_inside_list[i]',self.subgating_points_inside_list)
                

            arr = []
            for i in self.subgating_points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func=lambda arr:set(arr) 
            self.subgating_points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.subgating_points_inside))
            self.subgating_polygon_inside_label_29.setText(points_inside)
     
            
            for ch in range(len(self.working_data)):
                self.final_subgating_sweep_data[ch] = [self.working_data[ch][i] for i in self.subgating_points_inside]

    def edit_polygon_shape(self):
        
        print("edit_polygon_shape activate")
        if self.stop_edit_trigger == True:
            self.polygon_triggering()
            self.stop_edit_trigger = False
        else:
            self.stop_edit_trigger = True
            
            
            
            for ii in range(len(self.polygon_lines)):
                for i in range(len(self.polygon_lines[ii])):
                    self.graphWidget.removeItem(self.polygon_lines[ii][i])     
                    
            for ii in range(len(self.polygon_lines)-1):
                for i in range(1,len(self.polygon_lines[ii])-1):
                    list_x = [self.polygon_for_edit[ii][i][0],self.polygon_for_edit[ii][i-1][0]]
                    list_y = [self.polygon_for_edit[ii][i][1],self.polygon_for_edit[ii][i-1][1]]
                    self.polygon_lines[ii][i] = self.graphWidget.plot(list_x, list_y,
                                                                      pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)) 
                    
            for ii in range(len(self.polygon_lines)-1):
                list_x = [self.polygon_for_edit[ii][0][0],self.polygon_for_edit[ii][-1][0]]
                list_y = [self.polygon_for_edit[ii][0][1],self.polygon_for_edit[ii][-1][1]]                    
                self.polygon_lines[ii][-1] = self.graphWidget.plot(list_x, list_y,
                                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine)) 


                    
            for i in range(len(self.polygon_for_edit)-1):
                path = mpltPath.Path(self.polygon_for_edit[i])
                self.inside2 = path.contains_points(self.points)
                self.points_inside = list(compress(self.points_inside_square, self.inside2))
                self.points_inside_list[i] = list(compress(self.points_inside_square, self.inside2))
                
#                 path = mpltPath.Path(self.polygon_for_edit[self.nearest_list])
#                 self.inside2 = path.contains_points(self.points)
                
            # show the dots have index before the first filter
#             self.points_inside = list(compress(self.points_inside_square, self.inside2))
            
#             self.points_inside_list[self.nearest_list] = list(compress(self.points_inside_square, self.inside2))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func=lambda arr:set(arr) 
            self.points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.points_inside))
            self.polygon_inside_label_29.setText(points_inside)         
        
        
        
        
    def polygon_linear_plot_triggered_from_scatter_subtab(self):
        self.reset_comboBox = True
        self.polygon_linear_plot()
        
    def polygon_linear_plot(self):
        self.tab_widgets_subgating.setCurrentIndex(1)
        self.subgating_polygon_triggering() 
        self.polygon_trigger == False
        
        self.widget_29.clear()

                    

        ####
        
        ## add item only contain points inside, into the combobox in polygon filtered linear plot
        if self.reset_comboBox == True:
            self.comboBox_14.clear() 

            for list_index in self.comboBox_14_list:
                list_text = self.comboBox_14_list[list_index]
                
                polygon_length = 0
                for i in range(list_index):
                    polygon_length += len(self.analog[self.current_file_dict[self.comboBox_14_list[i]]][0][0])

                polygon_length_end = polygon_length + len(self.analog[self.current_file_dict[list_text]][0][0])                       
                index_in_all_selected_channel = [x for x, x in enumerate(self.subgating_points_inside) if x > polygon_length and x <= polygon_length_end]

                if index_in_all_selected_channel != []:
                    self.comboBox_14.addItem(str(list_text))  

        self.reset_comboBox = False
        ## end
        
        
        key_list = list(self.comboBox_14_list.keys())
        val_list = list(self.comboBox_14_list.values())

        # print key with val 100
        position = val_list.index(self.comboBox_14.currentText())
        polygon_index = key_list[position]
        polygon_text = self.comboBox_14.currentText()
        
        polygon_length = 0
        
        for i in range(polygon_index):
            polygon_length += len(self.analog[self.current_file_dict[self.comboBox_14_list[i]]][0][0])
               
        polygon_length_end = polygon_length + len(self.analog[self.current_file_dict[polygon_text]][0][0])
        
        index_in_all_selected_channel = [x for x, x in enumerate(self.subgating_points_inside) if x >= polygon_length and x <= polygon_length_end]


        index_in_current_channel = [x - polygon_length for x in index_in_all_selected_channel]

        
        # find data in csv file
        text1 = self.comboBox_14.currentText()
        
        header = 0
        
# plotted sample size fore lineaar plot, use self.chunksize 
# chunksize = 1000/undersample facor, calculated under sub:pressed
        try:
            if int(self.lineEdit_37.text())>0:
                sample_size = int(self.lineEdit_37.text())
                if text1 == "Peak Record":
                    header = 2
            else:
                sample_size = self.chunksize
                if text1 == "Peak Record":
                    header = 2
                    sample_size = 200
        except:
            sample_size = 200
            if text1 == "Peak Record":
                header = 2
                sample_size = 200
    

        upper_bond = int(self.lineEdit_38.text())
        lower_bond = int(self.lineEdit_36.text())
        if lower_bond < len(index_in_current_channel):
            
            # fix exceeded upper bond
            if len(index_in_current_channel) < upper_bond :
                upper_bond  = len(index_in_current_channel)
                self.lineEdit_38.setText(str(upper_bond))
            nrows = upper_bond - lower_bond
            
            if nrows>15:
                self.lineEdit_38.setText(str(lower_bond + 15))
                nrows = 15        
            self.main_file_select = self.file_list_view.currentRow()
            self.subgating_file_dict = self.file_dict_list[self.main_file_select]
            os.chdir(self.subgating_file_dict["Root Folder"])
            file = self.subgating_file_dict[text1]    



            data = pd.DataFrame({0: [],1: [], 2: [],3: []},)

            print("index_in_current_channel",len(index_in_current_channel),':',index_in_current_channel)

            for x in range(lower_bond,upper_bond):
                i = index_in_current_channel[x]
                skip_rows = i * sample_size 
                polygon_data = pd.read_csv(file, skiprows = skip_rows, nrows=sample_size, header=header) 
                length = len(polygon_data.columns) 
                polygon_data.columns = list(range(0,length))
                data = pd.concat([data,polygon_data])

    #         print(polygon_data)


            height_data = data[0].values.tolist()
            height_index = list(range(len(height_data)))

            poly_degree = int(self.lineEdit_39.text())
            window_length = int(self.lineEdit_40.text())//2 *2-1
            self.widget_29.addLegend()  


            for i in range(0,sample_size * nrows,sample_size):         
                self.widget_29.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))


            if self.polygon_Smooth_enable.isChecked():
                if self.polygon_channel_1.isChecked():
                    height_data = savgol_filter(data[0], window_length, poly_degree)
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    height_data = savgol_filter(data[1], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    height_data = savgol_filter(data[2], window_length, poly_degree)
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index,height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            else:
                if self.polygon_channel_1.isChecked():
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index,data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index,data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index,data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index,data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
        else: 
            print("Enter a new lower bond value")
            
            

        self.widget_29.autoRange()
        
    def polygon_reset_linear_plot(self):
        self.polygon_linear_plot()
        self.widget_29.autoRange()
        
    def polygon_last_page(self):
        lower_bond = int(self.lineEdit_36.text())
        upper_bond = int(self.lineEdit_38.text())
        nrows = upper_bond - lower_bond        
        
        self.lineEdit_36.setText(str(lower_bond - nrows))
        self.lineEdit_38.setText(str(upper_bond - nrows))
        
        self.polygon_linear_plot()
        
    def polygon_next_page(self):
        lower_bond = int(self.lineEdit_36.text())
        upper_bond = int(self.lineEdit_38.text())
        nrows = upper_bond - lower_bond        
        
        self.lineEdit_36.setText(str(lower_bond + nrows))
        self.lineEdit_38.setText(str(upper_bond + nrows))

        self.polygon_linear_plot()        
                
        
        
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
            if int(self.lineEdit_35.text())>0:
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
        if nrows>15:
            self.lineEdit_31.setText(str(lower_bond + 15))
            nrows = 15
            
        
        self.main_file_select = self.file_list_view.currentRow()
        self.polygon_file_dict = self.file_dict_list[self.main_file_select]
        os.chdir(self.polygon_file_dict["Root Folder"])
        file = self.polygon_file_dict[text1]      
        

        data = pd.read_csv(file, skiprows = sample_size * lower_bond, nrows=sample_size * nrows, header=header)  
        length = len(data.columns) 

        data.columns = list(range(0,length))
        
        height_data = data[0].values.tolist()
        height_index = list(range(len(height_data)))

        poly_degree = int(self.lineEdit_33.text())
        window_length = int(self.lineEdit_34.text())//2 *2-1
        self.widget_28.addLegend()  
        
        
        for i in range(0,sample_size * nrows,sample_size):         
            self.widget_28.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))

#                     self.data_line_y = self.graphWidget.plot([1, 1], [0, 1],
#                                                  pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
                
        if self.Smooth_enable.isChecked():
            if self.channel_1.isChecked():
                height_data = savgol_filter(data[0], window_length, poly_degree)
                pen = pg.mkPen(color=(83, 229, 29), width=2)
                self.widget_28.plot(height_index,height_data, name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_2.isChecked():
                height_data = savgol_filter(data[1], window_length, poly_degree)
                pen = pg.mkPen(color=(238, 17, 47), width=2)
                self.widget_28.plot(height_index,height_data, name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_3.isChecked():
                height_data = savgol_filter(data[2], window_length, poly_degree)
                pen = pg.mkPen(color=(48, 131, 240), width=2)
                self.widget_28.plot(height_index,height_data, name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_4.isChecked():
                height_data = savgol_filter(data[3], window_length, poly_degree)
                pen = pg.mkPen(color=(238, 134, 30), width=2)
                self.widget_28.plot(height_index,height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
        else:
            if self.channel_1.isChecked():
                pen = pg.mkPen(color=(83, 229, 29), width=2)
                self.widget_28.plot(height_index,data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_2.isChecked():
                pen = pg.mkPen(color=(238, 17, 47), width=2)
                self.widget_28.plot(height_index,data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_3.isChecked():
                pen = pg.mkPen(color=(48, 131, 240), width=2)
                self.widget_28.plot(height_index,data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))
            if self.channel_4.isChecked():
                pen = pg.mkPen(color=(238, 134, 30), width=2)
                self.widget_28.plot(height_index,data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o', symbolSize=0, symbolBrush=('m'))

        
#     def width_scatter_channel_to_histogram_channel(self):
#         self.listView_channels_3.setCurrentRow(self.comboBox_5.currentIndex())
#         self.recalculate_peak_dataset = True
    
#     def width_histogram_channel_to_scatter_channel(self):
#         self.comboBox_5.setCurrentIndex(self.listView_channels_3.currentRow())
#         self.lineEdit_5.setText(self.lineEdit_gatevoltage_2.text())
#         self.lineEdit_7.setText(self.lineEdit_gatevoltage_4.text())
#         self.lr_peak_width_plot()
#         self.recalculate_peak_dataset = True
        
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
        self.listWidget_sampingrate.addItem("Droplet Record:"+ str(self.chunksize))
        self.listWidget_sampingrate.addItem("All Hit:1000")
#         self.listWidget_sampingrate.setCurrentRow(0)
        
        
#     def update_names(self):
#         """update the name of the sweep dropboxes"""
#         self.comboBox_option1.clear()
#         self.comboBox_option2.clear()
#         self.comboBox_option1.addItem("Current Data")
#         self.comboBox_option2.addItem("Current Data")
#         self.comboBox_option1.addItem("Current Data post Width/Peaks # Filter")
#         self.comboBox_option2.addItem("Current Data post Width/Peaks # Filter")
#         self.comboBox_option1.addItem("Current Data post 2nd Filter")
#         self.comboBox_option2.addItem("Current Data post 2nd Filter")
#         for i in range(self.file_list_view.count()):
#             self.comboBox_option1.addItem(self.file_list_view.item(i).text())
#             self.comboBox_option2.addItem(self.file_list_view.item(i).text())

    def update_working_data(self):
#         try: print("Ui_MainWindow.reset:", Ui_MainWindow.reset)
#         except : print("Ui_MainWindow.reset: FALSE")


        print('self.update',self.update)
        print('self.reanalysis',self.reanalysis)
        if self.update or self.reanalysis:
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
            if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict['Droplet Record'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Droplet Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Droplet Record']][2][i]
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Peak Record']][2][i]

            if len(self.peak_width_working_data) == 0:
                for i in range(4):
                    self.peak_width_working_data[i] += self.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.analog[self.current_file_dict['Peak Record']][2][i]
            self.peak_num_filter()

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
                    
            if self.checkbox_Droplet_Record.isChecked() and self.current_file_dict['Droplet Record'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Droplet Record']][0][i]
                    
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]
            if len(self.working_data) == 0:
                for i in range(4):
                    self.working_data[i] += self.analog[self.current_file_dict['Peak Record']][0][i]

            ### filter data by using min and max width

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

                        

            
        print("0,self.recalculate_peak_dataset",self.recalculate_peak_dataset)   
        if self.recalculate_peak_dataset == True:
            ## x-axis
            if self.comboBox_5.currentIndex() == 0:
                self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if
                                     x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex() == 0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if
                                         x >= max(float(self.lineEdit_5.text()), float(self.lineEdit_6.text()))
                                         and x <= min(float(self.lineEdit_7.text()), float(self.lineEdit_8.text()))]
                elif self.comboBox_6.currentIndex() == 1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

            elif self.comboBox_5.currentIndex() == 1:
                self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if
                                     x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex() == 0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if
                                         x >= max(float(self.lineEdit_5.text()), float(self.lineEdit_6.text()))
                                         and x <= min(float(self.lineEdit_7.text()), float(self.lineEdit_8.text()))]
                elif self.comboBox_6.currentIndex() == 2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

            elif self.comboBox_5.currentIndex() == 2:
                self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if
                                     x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex() == 0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if
                                         x >= max(float(self.lineEdit_5.text()), float(self.lineEdit_6.text()))
                                         and x <= min(float(self.lineEdit_7.text()), float(self.lineEdit_8.text()))]
                elif self.comboBox_6.currentIndex() == 3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]

            elif self.comboBox_5.currentIndex() == 3:
                self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if
                                     x >= float(self.lineEdit_5.text()) and x <= float(self.lineEdit_7.text())]
                if self.comboBox_6.currentIndex() == 0:
                    self.width_index0 = [i for i, x in enumerate(self.peak_width_working_data[0]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 1:
                    self.width_index1 = [i for i, x in enumerate(self.peak_width_working_data[1]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 2:
                    self.width_index2 = [i for i, x in enumerate(self.peak_width_working_data[2]) if
                                         x >= float(self.lineEdit_6.text()) and x <= float(self.lineEdit_8.text())]
                elif self.comboBox_6.currentIndex() == 3:
                    self.width_index3 = [i for i, x in enumerate(self.peak_width_working_data[3]) if
                                         x >= max(float(self.lineEdit_5.text()), float(self.lineEdit_6.text()))
                                         and x <= min(float(self.lineEdit_7.text()), float(self.lineEdit_8.text()))]


            self.recalculate_peak_dataset = False

            self.data_updated = True

            

            
            
    def update_statistic(self):
        """update the statistic table"""
        if self.update:
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


        if len(self.width)!=0:
            filtered_gate_voltage_x = [x for x in self.width if x > text_x]
            percentage = round(100 * len(filtered_gate_voltage_x) / len(self.width), 2)
        else:
            percentage = "NA"
            
        self.lineEdit_percentage.setText(str(percentage))
        


        
    def update_sweep_graphs(self, bypass=False):
        self.sweep_bins = float(self.lineEdit_binwidth_2.text())
#         update1, update2, data_updated = self.ui_state.sweep_update(channel_select=self.sweep_channel,
#                                                                     file1=self.sweep_file_1,
#                                                                     file2=self.sweep_file_2, bins=self.sweep_bins)
        update1 = update2 = data_updated = True
        if update1:
            self.update_sweep_1(data_updated)
        elif bypass:
            self.update_sweep_1(bypass)
        if update2:
            self.update_sweep_2(data_updated)
        elif bypass:
            self.update_sweep_2(bypass)

#     def update_sweep_1(self, data_updated=False):
#         self.widget_sweepparam2.clear()
#         channel = self.listView_channels_2.currentRow()
#         if channel == -1:
#             self.listView_channels_2.setCurrentRow(0)
#         axis_name = self.listView_channels_2.currentItem().text()
#         self.widget_sweepparam2.setLabel('bottom', axis_name)
#         print("update sweep 1")
#         r, g, b = Helper.rgb_select(channel)
#         if data_updated or len(self.sweep_1_data) == 0:
#             #self.sweep_1_data = self.working_data[channel]
#             self.sweep_1_data = []
#             if self.comboBox_option1.currentIndex() == 0:
#                 try:
#                     # sweep data left
# #                     self.sweep_1_data = self.final_subgating_sweep_data[channel]
#                     self.sweep_1_data = self.sweep_left[channel]
#                 except:
#                     self.sweep_1_data = [[], [], [], []]
#             elif self.comboBox_option1.currentIndex() == 1:
#                 self.sweep_1_data = self.filtered_working_data[channel]
#             elif self.comboBox_option1.currentIndex() == 2:
#                 self.sweep_1_data = self.subgating_sweep_data[channel]
#             else:
#                 if self.checkBox_7.isChecked() and self.sweep_1_dict['Peak Record'] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Peak Record']][0][channel]
#                 if self.checkbox_ch1.isChecked() and self.sweep_1_dict['Ch1 '] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1 ']][0][channel]
#                 if self.checkbox_ch2.isChecked() and self.sweep_1_dict['Ch2 '] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch2 ']][0][channel]
#                 if self.checkbox_ch3.isChecked() and self.sweep_1_dict['Ch3 '] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch3 ']][0][channel]
#                 if self.checkbox_ch12.isChecked() and self.sweep_1_dict['Ch1-2'] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1-2']][0][channel]
#                 if self.checkbox_ch13.isChecked() and self.sweep_1_dict['Ch1-3'] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch1-3']][0][channel]
#                 if self.checkbox_ch23.isChecked() and self.sweep_1_dict['Ch2-3'] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Ch2-3']][0][channel]
#                 if self.checkbox_Droplet_Record.isChecked() and self.sweep_1_dict['Droplet Record'] != '':
#                     self.sweep_1_data += self.analog[self.sweep_1_dict['Droplet Record']][0][channel]
#         try:
#             range_width = int(max(self.sweep_1_data)) + 1
#         except:
#             range_width = 1
#         bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
#         y, x = np.histogram(self.sweep_1_data, bins=bin_edge)
#         separate_y = [0] * len(y)
#         for i in range(len(y)):
#             separate_y = [0] * len(y)
#             separate_y[i] = y[i]
#             self.widget_sweepparam2.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
#         self.widget_sweepparam2.setXRange(0, max(x), padding=0)
#         self.widget_sweepparam2.setYRange(0, max(y), padding=0)
#         self.label_39.setText(self.comboBox_option1.currentText())


    def update_sweep_1(self, data_updated=False):
        self.widget_sweepparam2.clear()
        channel = self.comboBox_option1.currentIndex()
        if channel == -1:
            self.comboBox_option1.setCurrentIndex(0)
        axis_name = self.comboBox_option1.currentText()
        self.widget_sweepparam2.setLabel('bottom', axis_name)
        print("update sweep 1")
        r, g, b = Helper.rgb_select(channel)
        if data_updated or len(self.sweep_1_data) == 0:
            try:
                self.sweep_1_data = self.sweep_left[channel]
            except:
                self.sweep_1_data = [[], [], [], []]

        try:
            range_width = int(max(self.sweep_1_data)) + 1
        except:
            range_width = 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
        y, x = np.histogram(self.sweep_1_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam2.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam2.setXRange(0, max(x), padding=0)
        self.widget_sweepparam2.setYRange(0, max(y), padding=0)
        self.label_39.setText(self.comboBox_option1.currentText())

    def update_sweep_2(self, data_updated=False):
        self.widget_sweepparam1.clear()
        channel = self.comboBox_option2.currentIndex()
        if channel == -1:
            self.comboBox_option2.setCurrentIndex(0)
        axis_name = self.comboBox_option2.currentText()
        self.widget_sweepparam1.setLabel('bottom', axis_name)
        r, g, b = Helper.rgb_select(channel)
        print("update sweep 2")
        if data_updated or len(self.sweep_2_data) == 0:
            try:
                self.sweep_2_data = self.sweep_right[channel]
            except:
                self.sweep_2_data = [[],[],[],[]]

        try:
            range_width = int(max(self.sweep_2_data)) + 1
        except:
            range_width = 1
        bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
        y, x = np.histogram(self.sweep_2_data, bins=bin_edge)
        separate_y = [0] * len(y)
        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.widget_sweepparam1.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
        self.widget_sweepparam1.setXRange(0, max(x), padding=0)
        self.widget_sweepparam1.setYRange(0, max(y), padding=0)
        self.label_65.setText(self.comboBox_option2.currentText())
        
#     def update_sweep_2(self, data_updated=False):
#         self.widget_sweepparam1.clear()
#         channel = self.listView_channels_2.currentRow()
#         if channel == -1:
#             self.listView_channels_2.setCurrentRow(0)
#         axis_name = self.listView_channels_2.currentItem().text()
#         self.widget_sweepparam1.setLabel('bottom', axis_name)
#         r, g, b = Helper.rgb_select(channel)
#         print("update sweep 2")
#         if data_updated or len(self.sweep_2_data) == 0:
#             # self.sweep_2_data = self.working_data[channel]
#             self.sweep_2_data = []
#             if self.comboBox_option2.currentIndex() == 0 and len(self.final_subgating_sweep_data) > 0:
#                 try:
# #                     self.sweep_2_data = self.final_subgating_sweep_data[channel]
#                     self.sweep_2_data = self.sweep_right[channel]
#                 except:
#                     self.sweep_2_data = [[],[],[],[]]
#             elif self.comboBox_option2.currentIndex() == 1:
#                 self.sweep_2_data = self.filtered_working_data[channel]
#             elif self.comboBox_option2.currentIndex() == 2:
#                 self.sweep_2_data = self.subgating_sweep_data[channel]
#             else:
#                 if self.checkBox_7.isChecked() and self.sweep_2_dict['Peak Record'] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Peak Record']][0][channel]
#                     print("self.analog[self.sweep_2_dict['Peak Record']][0][channel]",self.analog[self.sweep_2_dict['Peak Record']][0][channel])
#                 if self.checkbox_ch1.isChecked() and self.sweep_2_dict['Ch1 '] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1 ']][0][channel]
#                 if self.checkbox_ch2.isChecked() and self.sweep_2_dict['Ch2 '] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch2 ']][0][channel]
#                 if self.checkbox_ch3.isChecked() and self.sweep_2_dict['Ch3 '] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch3 ']][0][channel]
#                 if self.checkbox_ch12.isChecked() and self.sweep_2_dict['Ch1-2'] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1-2']][0][channel]
#                 if self.checkbox_ch13.isChecked() and self.sweep_2_dict['Ch1-3'] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch1-3']][0][channel]
#                 if self.checkbox_ch23.isChecked() and self.sweep_2_dict['Ch2-3'] != '':
#                     self.sweep_2_data += self.analog[self.sweep_2_dict['Ch2-3']][0][channel]
#         try:
#             range_width = int(max(self.sweep_2_data)) + 1
#         except:
#             range_width = 1
#         bin_edge = Helper.histogram_bin(range_width, float(self.lineEdit_binwidth_2.text()))
#         y, x = np.histogram(self.sweep_2_data, bins=bin_edge)
#         separate_y = [0] * len(y)
#         for i in range(len(y)):
#             separate_y = [0] * len(y)
#             separate_y[i] = y[i]
#             self.widget_sweepparam1.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True, brush=(r, g, b))
#         self.widget_sweepparam1.setXRange(0, max(x), padding=0)
#         self.widget_sweepparam1.setYRange(0, max(y), padding=0)
#         self.label_65.setText(self.comboBox_option2.currentText())


    def draw_peak_width(self, data_updated=False):
        
        self.histo_bins_peak_width = float(self.lineEdit_binwidth_3.text())
        update = self.ui_state.width_gating_update(channel_select=self.peak_width_channel, bins=self.peak_width_bins)

        
        if update:
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

            self.peak_width = [x for x in self.full_peak_width if x >= x_low and x <= x_high]

            try:
                range_width = int(max(self.peak_width)) + 1
            except:
                print("No dots inside")
                range_width = 1

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
        '''1st layer scatter plot'''
                
        update = self.ui_state.width_scatter_update(x_select=self.width_scatter_channelx, y_select=self.width_scatter_channely,
                                                    density_adjust_1= self.lineEdit_first_layer_density_adjust.text())

        
        if self.filter_update or data_updated or update:

            x_axis_channel = self.comboBox_5.currentIndex()
            y_axis_channel = self.comboBox_6.currentIndex()
            x_axis_name = self.comboBox_5.currentText()
            y_axis_name = self.comboBox_6.currentText()

            self.graphWidget_width_scatter.clear()

            self.graphWidget_width_scatter.setLabel('left', y_axis_name, color='b')
            self.graphWidget_width_scatter.setLabel('bottom', x_axis_name, color='b')

            self.Ch1_channel0_width = self.peak_width_working_data[x_axis_channel]
            self.Ch1_channel1_width = self.peak_width_working_data[y_axis_channel]

            
            # max should be bigger than the lagest dot number
            # try bins
            max_voltage = 1000
            bins = 1000
            steps = max_voltage / bins
            # all data is first sorted into a histogram
            histo, _, _ = np.histogram2d(self.Ch1_channel0_width, self.Ch1_channel1_width, bins,
                                         [[0, max_voltage], [0, max_voltage]],
                                         density=True)
            max_density = histo.max()
            percentage_coefficient = int(self.lineEdit_first_layer_density_adjust.text())
    
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
                
#                 print('a',a)
#                 print('b',b)
                
                if a >= 100:
                    a = 99
                if b >= 100:
                    b = 99
                    
                # checking for density, the value divided by steps serves as the index
                density = histo[a][b]

                
                percentage = density / max_density * 100 * percentage_coefficient
                if percentage > 100:
                    percentage = 100
#                 print('percentage',percentage)

                
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
 
            
            # update square selection without trigger data update
            self.graphWidget_width_scatter.removeItem(self.lr_x_axis)
            self.graphWidget_width_scatter.removeItem(self.lr_y_axis)

            x_low = float(self.lineEdit_5.text())
            y_low = float(self.lineEdit_6.text())
            x_high = float(self.lineEdit_7.text())
            y_high = float(self.lineEdit_8.text())

            self.lineEdit_gatevoltage_2.setText(str(round(x_low,2)))
            self.lineEdit_gatevoltage_4.setText(str(round(x_high,2)))

            self.lr_x_axis = pg.LinearRegionItem([x_low,x_high])
            self.lr_y_axis = pg.LinearRegionItem([y_low,y_high], orientation = 1)
            self.graphWidget_width_scatter.addItem(self.lr_x_axis)
            self.graphWidget_width_scatter.addItem(self.lr_y_axis)        

            # no trigger data update
#             self.recalculate_peak_dataset = True

            self.lr_x_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)
            self.lr_y_axis.sigRegionChangeFinished.connect(self.lr_peak_width_change)  



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
        self.lr_y_axis = pg.LinearRegionItem([y_low,y_high], orientation = 1)
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

        
        points_inside_square = list(set(width_index1).intersection(set(width_index2)))
        
        self.lineEdit_gatevoltage_5.setText(str(len(points_inside_square)))
        
        


        
    def draw(self, data_updated=False):

        self.histo_bins = float(self.lineEdit_binwidth.text())
        update = self.ui_state.gating_update(channel_select=self.histo_channel, bins=self.histo_bins)
        

        if update:
            print("update draw")

            self.width = self.filtered_working_data[self.listView_channels.currentRow()]
            self.lineEdit_count.setText(str(len(self.width)))
            if len(self.width)!=0:

                channel = self.listView_channels.currentRow()
                if channel == -1:
                    self.listView_channels.setCurrentRow(0)
                self.histogram_graphWidget.clear()
                r, g, b = Helper.rgb_select(channel)
                styles = {"color": "r", "font-size": "20px"}
                axis_name = self.listView_channels.currentItem().text()
                self.histogram_graphWidget.setLabel('bottom', axis_name, **styles)

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

                # after 1st map so the line layer will appear in front of the histogram
                self.data_line = self.histogram_graphWidget.plot([0, 0], [0, 0],
                                                                 pen=pg.mkPen(color=('r'), width=5,
                                                                              style=QtCore.Qt.DashLine))
                self.thresholdUpdated()

    def draw_2(self, data_updated=False):
        """2nd layer scatter plot"""
        

        
        self.draw_2_update = self.ui_state.scatter_update(x_select=self.scatter_channelx, y_select=self.scatter_channely,
                                                          x_gate=self.lineEdit_scatterxvoltage.text(), 
                                                          y_gate=self.lineEdit_scatteryvoltage.text(),
                                                         density_adjust_2 = self.lineEdit_second_layer_density_adjust.text())
        if self.draw_2_update or data_updated:
            print("update draw2")

            if self.comboBox.currentIndex() == 0:
                if self.comboBox_2.currentIndex() == 0:
                    points_inside_square = self.width_index0
                elif self.comboBox_2.currentIndex() == 1:
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index1)))

                elif self.comboBox_2.currentIndex() == 2:
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index2)))

                elif self.comboBox_2.currentIndex() == 3:
                    points_inside_square = list(set(self.width_index0).intersection(set(self.width_index3)))


            elif self.comboBox.currentIndex() == 1:
                if self.comboBox_2.currentIndex() == 0:
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index0)))

                elif self.comboBox_2.currentIndex() == 1:
                    points_inside_square = self.width_index1
                elif self.comboBox_2.currentIndex() == 2:
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index2)))

                elif self.comboBox_2.currentIndex() == 3:
                    points_inside_square = list(set(self.width_index1).intersection(set(self.width_index3)))


            elif self.comboBox.currentIndex() == 2:
                if self.comboBox_2.currentIndex() == 0:
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index0)))


                elif self.comboBox_2.currentIndex() == 1:
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index1)))

                elif self.comboBox_2.currentIndex() == 2:
                    points_inside_square = self.width_index2
                elif self.comboBox_2.currentIndex() == 3:
                    points_inside_square = list(set(self.width_index2).intersection(set(self.width_index3)))

            elif self.comboBox.currentIndex() == 3:
                if self.comboBox_2.currentIndex() == 0:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index0)))

                elif self.comboBox_2.currentIndex() == 1:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index1)))

                elif self.comboBox_2.currentIndex() == 2:
                    points_inside_square = list(set(self.width_index3).intersection(set(self.width_index2)))

                elif self.comboBox_2.currentIndex() == 3:
                    points_inside_square = self.width_index3
                 
            self.check3A2 = time.time()

            points_inside_square = list(set(points_inside_square).intersection(set(self.peak_num_filtered_index)))
            self.points_inside_square = points_inside_square
#             peak_data_x = self.working_data[self.comboBox.currentIndex()]
#             peak_data_y = self.working_data[self.comboBox_2.currentIndex()]
            peak_num_data_x = self.peak_num_working_data[self.comboBox.currentIndex()]
            peak_num_data_y = self.peak_num_working_data[self.comboBox_2.currentIndex()]

            self.check3A3 = time.time()
            
            if len(points_inside_square) != 0:

                self.filtered_working_data[0] = [self.working_data[0][i] for i in points_inside_square]
                self.filtered_working_data[1] = [self.working_data[1][i] for i in points_inside_square]
                self.filtered_working_data[2] = [self.working_data[2][i] for i in points_inside_square]
                self.filtered_working_data[3] = [self.working_data[3][i] for i in points_inside_square]
                
                
                
                
                self.filtered_peak_num_working_data[0] = [self.peak_num_working_data[0][i] for i in points_inside_square]
                self.filtered_peak_num_working_data[1] = [self.peak_num_working_data[1][i] for i in points_inside_square]
                self.filtered_peak_num_working_data[2] = [self.peak_num_working_data[2][i] for i in points_inside_square]
                self.filtered_peak_num_working_data[3] = [self.peak_num_working_data[3][i] for i in points_inside_square]


            else:
                self.filtered_working_data[0] = []
                self.filtered_working_data[1] = []
                self.filtered_working_data[2] = []
                self.filtered_working_data[3] = []
                
                self.filtered_peak_num_working_data[0] = []
                self.filtered_peak_num_working_data[1] = []
                self.filtered_peak_num_working_data[2] = []
                self.filtered_peak_num_working_data[3] = []


            
            x_axis_channel = self.comboBox.currentIndex()
            y_axis_channel = self.comboBox_2.currentIndex()
            x_axis_name = self.comboBox.currentText()
            y_axis_name = self.comboBox_2.currentText()


            try:
                print("x", len(self.filtered_working_data[x_axis_channel]), "y",
                      len(self.filtered_working_data[y_axis_channel]))
            except:
                print("x", 0, "y", 0)

            self.graphWidget.clear()

            self.check3A4 = time.time()
            
            if len(self.filtered_working_data[x_axis_channel]) != 0 and len(
                    self.filtered_working_data[y_axis_channel]) != 0:

                self.graphWidget.setLabel('left', y_axis_name, color='b')
                self.graphWidget.setLabel('bottom', x_axis_name, color='b')

                self.Ch1_channel0 = self.filtered_working_data[x_axis_channel]
                self.Ch1_channel1 = self.filtered_working_data[y_axis_channel]
                self.Ch1_channel0_peak_num = self.filtered_peak_num_working_data[x_axis_channel]
                self.Ch1_channel1_peak_num = self.filtered_peak_num_working_data[y_axis_channel]

                max_voltage = 12
                bins = 1000
                steps = max_voltage / bins

                # all data is first sorted into a histogram
                histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins,
                                             [[0, max_voltage], [0, max_voltage]],
                                             density=True)
                max_density = histo.max()
                percentage_coefficient = int(self.lineEdit_second_layer_density_adjust.text())/10
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
                    percentage = density / max_density * 100 *percentage_coefficient
                    if percentage > 100:
                        percentage = 100
                    
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
#                     #test 
#                     self.tree_dic[(0,)]['tree_windowfilter'].graphWidget.plot(density_listx[i], density_listy[i], symbol='p', pen=None, symbolPen=None,
#                                           symbolSize=5, symbolBrush=(red, blue, green))

                #    >0%    0,0,1   blue
                #    >15%   0,1,1  cyan
                #    >30%   0,1,0  green
                #    >45%   1,1,0  yellow
                #    >60%   1,0,0   red
                #    >75%   1,1,1   white

                print("draw2 end")
                # threshold
                self.thresholdUpdated_2()
            else:
                self.Ch1_channel0 = []
                self.Ch1_channel1 = []
                self.Ch1_channel0_peak_num = []
                self.Ch1_channel1_peak_num = []
                self.thresholdUpdated_2()

                
                
                
    def subgating_thresholdUpdated_2(self):
        self.subgating_graphWidget.removeItem(self.subgating_data_line_y)
        self.subgating_graphWidget.removeItem(self.subgating_data_line_x)

        text_x = float(self.subgating_lineEdit_scatterxvoltage.text())
        text_y = float(self.subgating_lineEdit_scatteryvoltage.text())

        # x
        line_xx = [text_x, text_x]

        try:
            line_yy = [0, max(self.subgating_Ch1_channel1)+10]
        except:
            line_yy = [0, 1]

        self.subgating_data_line_x.setData(line_xx, line_yy)
        # y
        try:
            line_x = [0, max(self.subgating_Ch1_channel0)+10]
        except:
            line_x = [0, 1]

        line_y = [text_y, text_y]

        self.subgating_data_line_y.setData(line_x, line_y)
        self.subgating_data_line_x = self.subgating_graphWidget.plot(line_xx, line_yy,
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        self.subgating_data_line_y = self.subgating_graphWidget.plot(line_x, line_y,
                                                 pen=pg.mkPen(color=('r'), width=5, style=QtCore.Qt.DashLine))
        
    def thresholdUpdated_2(self):
        self.graphWidget.removeItem(self.data_line_y)
        self.graphWidget.removeItem(self.data_line_x)

        text_x = float(self.lineEdit_scatterxvoltage.text())
        text_y = float(self.lineEdit_scatteryvoltage.text())

        # x
        line_xx = [text_x, text_x]

        try:
            line_yy = [0, max(self.Ch1_channel1)]
        except:
            line_yy = [0, 1]

        self.data_line_x.setData(line_xx, line_yy)
        # y
        try:
            line_x = [0, max(self.Ch1_channel0)]
        except:
            line_x = [0, 1]

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
            
        # filter peak number into single peak, multipeak
        multipeak = [x for x in self.Ch1_channel0_peak_num]

        count_quadrant1 = 0
        count_quadrant2 = 0
        count_quadrant3 = 0
        count_quadrant4 = 0

        #peak count for the two selected channel will be stored in an array, array holds q1 - q4
        single_peak_count_channel0 = [0, 0, 0, 0]
        single_peak_count_channel1 = [0, 0, 0, 0]
        multi_peak_count_channel0 = [0, 0, 0, 0]
        multi_peak_count_channel1 = [0, 0, 0, 0]

        channel0_list_quadrant1 = []
        channel1_list_quadrant1 = []
        channel0_list_quadrant2 = []
        channel1_list_quadrant2 = []
        channel0_list_quadrant3 = []
        channel1_list_quadrant3 = []
        channel0_list_quadrant4 = []
        channel1_list_quadrant4 = []

        
        
        if self.polygon_trigger == False:
            
            self.quadrant1_list = [False] * len(a)

            for i in range(len(a)):
                if a[i] and c[i]:
                    self.quadrant1_list[i] = True
                    channel0_list_quadrant1.append(self.Ch1_channel0[i])
                    channel1_list_quadrant1.append(self.Ch1_channel1[i])
                    count_quadrant1 += 1
                    if self.Ch1_channel0_peak_num[i] == 1:
                        single_peak_count_channel0[0] += 1
                    elif self.Ch1_channel0_peak_num[i] > 1:
                        multi_peak_count_channel0[0] += 1
                    if self.Ch1_channel1_peak_num[i] == 1:
                        single_peak_count_channel1[0] += 1
                    elif self.Ch1_channel1_peak_num[i] > 1:
                        multi_peak_count_channel1[0] += 1


                elif not a[i] and c[i]:
                    channel0_list_quadrant2.append(self.Ch1_channel0[i])
                    channel1_list_quadrant2.append(self.Ch1_channel1[i])
                    count_quadrant2 += 1
                    if self.Ch1_channel0_peak_num[i] == 1:
                        single_peak_count_channel0[1] += 1
                    elif self.Ch1_channel0_peak_num[i] > 1:
                        multi_peak_count_channel0[1] += 1
                    if self.Ch1_channel1_peak_num[i] == 1:
                        single_peak_count_channel1[1] += 1
                    elif self.Ch1_channel1_peak_num[i] > 1:
                        multi_peak_count_channel1[1] += 1
                elif not a[i] and not c[i]:
                    channel0_list_quadrant3.append(self.Ch1_channel0[i])
                    channel1_list_quadrant3.append(self.Ch1_channel1[i])
                    count_quadrant3 += 1
                    if self.Ch1_channel0_peak_num[i] == 1:
                        single_peak_count_channel0[2] += 1
                    elif self.Ch1_channel0_peak_num[i] > 1:
                        multi_peak_count_channel0[2] += 1
                    if self.Ch1_channel1_peak_num[i] == 1:
                        single_peak_count_channel1[2] += 1
                    elif self.Ch1_channel1_peak_num[i] > 1:
                        multi_peak_count_channel1[2] += 1
                elif a[i] and not c[i]:
                    channel0_list_quadrant4.append(self.Ch1_channel0[i])
                    channel1_list_quadrant4.append(self.Ch1_channel1[i])
                    count_quadrant4 += 1
                    if self.Ch1_channel0_peak_num[i] == 1:
                        single_peak_count_channel0[3] += 1
                    elif self.Ch1_channel0_peak_num[i] > 1:
                        multi_peak_count_channel0[3] += 1
                    if self.Ch1_channel1_peak_num[i] == 1:
                        single_peak_count_channel1[3] += 1
                    elif self.Ch1_channel1_peak_num[i] > 1:
                        multi_peak_count_channel1[3] += 1
  
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
            
        if len(self.Ch1_channel0)!=0:
            view1 = str(round(100 * count_quadrant1 / len(self.Ch1_channel0), 2))
            view2 = str(round(100 * count_quadrant2 / len(self.Ch1_channel0), 2))
            view3 = str(round(100 * count_quadrant3 / len(self.Ch1_channel0), 2))
            view4 = str(round(100 * count_quadrant4 / len(self.Ch1_channel0), 2))
            if count_quadrant1 > 0:
                x_single_1 = str(round(100 * single_peak_count_channel0[0] / count_quadrant1, 2))
                y_single_1 = str(round(100 * single_peak_count_channel1[0] / count_quadrant1, 2))
                x_multi_1 = str(round(100 * multi_peak_count_channel0[0] / count_quadrant1, 2))
                y_multi_1 = str(round(100 * multi_peak_count_channel1[0] / count_quadrant1, 2))
            else:
                x_single_1 = '0'
                y_single_1 = '0'
                x_multi_1 = '0'
                y_multi_1 = '0'
            if count_quadrant2 > 0:
                x_single_2 = str(round(100 * single_peak_count_channel0[1] / count_quadrant2, 2))
                y_single_2 = str(round(100 * single_peak_count_channel1[1] / count_quadrant2, 2))
                x_multi_2 = str(round(100 * multi_peak_count_channel0[1] / count_quadrant2, 2))
                y_multi_2 = str(round(100 * multi_peak_count_channel1[1] / count_quadrant2, 2))
            else:
                x_single_2 = '0'
                y_single_2 = '0'
                x_multi_2 = '0'
                y_multi_2 = '0'
            if count_quadrant3 > 0:
                x_single_3 = str(round(100 * single_peak_count_channel0[2] / count_quadrant3, 2))
                y_single_3 = str(round(100 * single_peak_count_channel1[2] / count_quadrant3, 2))
                x_multi_3 = str(round(100 * multi_peak_count_channel0[2] / count_quadrant3, 2))
                y_multi_3 = str(round(100 * multi_peak_count_channel1[2] / count_quadrant3, 2))
            else:
                x_single_3 = '0'
                y_single_3 = '0'
                x_multi_3 = '0'
                y_multi_3 = '0'
            if count_quadrant4 > 0:
                x_single_4 = str(round(100 * single_peak_count_channel0[3] / count_quadrant4, 2))
                y_single_4 = str(round(100 * single_peak_count_channel1[3] / count_quadrant4, 2))
                x_multi_4 = str(round(100 * multi_peak_count_channel0[3] / count_quadrant4, 2))
                y_multi_4 = str(round(100 * multi_peak_count_channel1[3] / count_quadrant4, 2))
            else:
                x_single_4 = '0'
                y_single_4 = '0'
                x_multi_4 = '0'
                y_multi_4 = '0'

        else:
            view1 = 0
            view2 = 0
            view3 = 0
            view4 = 0
            x_single_1 = '0'
            x_single_2 = '0'
            x_single_3 = '0'
            x_single_4 = '0'
            y_single_1 = '0'
            y_single_2 = '0'
            y_single_3 = '0'
            y_single_4 = '0'
            x_multi_1 = '0'
            x_multi_2 = '0'
            x_multi_3 = '0'
            x_multi_4 = '0'
            y_multi_1 = '0'
            y_multi_2 = '0'
            y_multi_3 = '0'
            y_multi_4 = '0'


        self.tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(count_quadrant1)))
        self.tableView_scatterquadrants.setItem(0, 1, QTableWidgetItem(view1))
        self.tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
        self.tableView_scatterquadrants.setItem(0, 3, QTableWidgetItem(x_single_1))
        self.tableView_scatterquadrants.setItem(0, 4, QTableWidgetItem(y_single_1))
        self.tableView_scatterquadrants.setItem(0, 5, QTableWidgetItem(x_multi_1))
        self.tableView_scatterquadrants.setItem(0, 6, QTableWidgetItem(y_multi_1))
        self.tableView_scatterquadrants.setItem(1, 0, QTableWidgetItem(str(count_quadrant2)))
        self.tableView_scatterquadrants.setItem(1, 1, QTableWidgetItem(view2))
        self.tableView_scatterquadrants.setItem(1, 2, QTableWidgetItem(str(totalpercent2)))
        self.tableView_scatterquadrants.setItem(1, 3, QTableWidgetItem(x_single_2))
        self.tableView_scatterquadrants.setItem(1, 4, QTableWidgetItem(y_single_2))
        self.tableView_scatterquadrants.setItem(1, 5, QTableWidgetItem(x_multi_2))
        self.tableView_scatterquadrants.setItem(1, 6, QTableWidgetItem(y_multi_2))
        self.tableView_scatterquadrants.setItem(2, 0, QTableWidgetItem(str(count_quadrant3)))
        self.tableView_scatterquadrants.setItem(2, 1, QTableWidgetItem(view3))
        self.tableView_scatterquadrants.setItem(2, 2, QTableWidgetItem(str(totalpercent3)))
        self.tableView_scatterquadrants.setItem(2, 3, QTableWidgetItem(x_single_3))
        self.tableView_scatterquadrants.setItem(2, 4, QTableWidgetItem(y_single_3))
        self.tableView_scatterquadrants.setItem(2, 5, QTableWidgetItem(x_multi_3))
        self.tableView_scatterquadrants.setItem(2, 6, QTableWidgetItem(y_multi_3))
        self.tableView_scatterquadrants.setItem(3, 0, QTableWidgetItem(str(count_quadrant4)))
        self.tableView_scatterquadrants.setItem(3, 1, QTableWidgetItem(view4))
        self.tableView_scatterquadrants.setItem(3, 2, QTableWidgetItem(str(totalpercent4)))
        self.tableView_scatterquadrants.setItem(3, 3, QTableWidgetItem(x_single_4))
        self.tableView_scatterquadrants.setItem(3, 4, QTableWidgetItem(y_single_4))
        self.tableView_scatterquadrants.setItem(3, 5, QTableWidgetItem(x_multi_4))
        self.tableView_scatterquadrants.setItem(3, 6, QTableWidgetItem(y_multi_4))

#         ### mid table

#         try:
#             self.tableView_scatterxaxis.setItem(0, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel0_list_quadrant1), 2))))
#             self.tableView_scatterxaxis.setItem(0, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel0_list_quadrant1), 2))))
#             self.tableView_scatterxaxis.setItem(0, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel0_list_quadrant1), 2))))
#         except:
#             self.tableView_scatterxaxis.setItem(0, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(0, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(0, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatterxaxis.setItem(1, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel0_list_quadrant2), 2))))
#             self.tableView_scatterxaxis.setItem(1, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel0_list_quadrant2), 2))))
#             self.tableView_scatterxaxis.setItem(1, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel0_list_quadrant2), 2))))
#         except:
#             self.tableView_scatterxaxis.setItem(1, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(1, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(1, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatterxaxis.setItem(2, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel0_list_quadrant3), 2))))
#             self.tableView_scatterxaxis.setItem(2, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel0_list_quadrant3), 2))))
#             self.tableView_scatterxaxis.setItem(2, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel0_list_quadrant3), 2))))
#         except:
#             self.tableView_scatterxaxis.setItem(2, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(2, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(2, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatterxaxis.setItem(3, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel0_list_quadrant4), 2))))
#             self.tableView_scatterxaxis.setItem(3, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel0_list_quadrant4), 2))))
#             self.tableView_scatterxaxis.setItem(3, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel0_list_quadrant4), 2))))
#         except:
#             self.tableView_scatterxaxis.setItem(3, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(3, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatterxaxis.setItem(3, 2, QTableWidgetItem('NaN'))

#         # bottom

#         try:
#             self.tableView_scatteryaxis.setItem(0, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel1_list_quadrant1), 2))))
#             self.tableView_scatteryaxis.setItem(0, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel1_list_quadrant1), 2))))
#             self.tableView_scatteryaxis.setItem(0, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel1_list_quadrant1), 2))))
#         except:
#             self.tableView_scatteryaxis.setItem(0, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(0, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(0, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatteryaxis.setItem(1, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel1_list_quadrant2), 2))))
#             self.tableView_scatteryaxis.setItem(1, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel1_list_quadrant2), 2))))
#             self.tableView_scatteryaxis.setItem(1, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel1_list_quadrant2), 2))))
#         except:
#             self.tableView_scatteryaxis.setItem(1, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(1, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(1, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatteryaxis.setItem(2, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel1_list_quadrant3), 2))))
#             self.tableView_scatteryaxis.setItem(2, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel1_list_quadrant3), 2))))
#             self.tableView_scatteryaxis.setItem(2, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel1_list_quadrant3), 2))))
#         except:
#             self.tableView_scatteryaxis.setItem(2, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(2, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(2, 2, QTableWidgetItem('NaN'))

#         try:
#             self.tableView_scatteryaxis.setItem(3, 0, QTableWidgetItem(
#                 str(round(statistics.mean(channel1_list_quadrant4), 2))))
#             self.tableView_scatteryaxis.setItem(3, 1, QTableWidgetItem(
#                 str(round(statistics.stdev(channel1_list_quadrant4), 2))))
#             self.tableView_scatteryaxis.setItem(3, 2, QTableWidgetItem(
#                 str(round(statistics.median(channel1_list_quadrant4), 2))))
#         except:
#             self.tableView_scatteryaxis.setItem(3, 0, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(3, 1, QTableWidgetItem('NaN'))
#             self.tableView_scatteryaxis.setItem(3, 2, QTableWidgetItem('NaN'))


#         ###  


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
        self.checkbox_Droplet_Record.setText(_translate("MainWindow", "Droplet Record"))
        self.checkBox_7.setText(_translate("MainWindow", "All Channel"))
        
        self.channel_1.setText(_translate("MainWindow", "Channel 1"))
        self.channel_2.setText(_translate("MainWindow", "Channel 2"))
        self.channel_3.setText(_translate("MainWindow", "Channel 3"))
        self.channel_4.setText(_translate("MainWindow", "Channel 4"))
        
        
        self.button_update.setText(_translate("MainWindow", "Update"))
#         self.label_2.setText(_translate("MainWindow", "Gate Voltages"))
#         self.button_copy.setText(_translate("MainWindow", "Copy"))
#         self.button_paste.setText(_translate("MainWindow", "Paste"))
#         self.button_screenshot.setText(_translate("MainWindow", "Screenshot"))
#         self.pushButton_2.setText(_translate("MainWindow", "Save"))
#         self.pushButton.setText(_translate("MainWindow", "Load"))
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
        self.label_29.setText(_translate("MainWindow", "Quadrant Gating"))
        
        self.polygon_inside_label_29.setText(_translate("MainWindow", "Inside: 0"))
        self.polygon_inside_label_30.setText(_translate("MainWindow", "Polygonal Gating"))
        
        
        self.label_36.setText(_translate("MainWindow", "Quadrants"))
        self.label_37.setText(_translate("MainWindow", "X Axis"))
        self.label_38.setText(_translate("MainWindow", "Y Axis"))
        self.tab_widgets_scatter.setTabText(self.tab_widgets_scatter.indexOf(self.subtab_scatter),
                                            _translate("MainWindow", "Scatter"))
        self.tab_widgets_scatter.setTabText(self.tab_widgets_scatter.indexOf(self.tab_gating),
                                         _translate("MainWindow", "Histogram"))        

       

        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_scatter),
                                         _translate("MainWindow", "Peak Height Subgating"))
        
        
        
        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_subgating),
                                         _translate("MainWindow", "Subgating Results"))        
        self.tab_widgets_subgating.setTabText(self.tab_widgets_subgating.indexOf(self.subgating_subtab_scatter),
                                            _translate("MainWindow", "Scatter"))        
        self.tab_widgets_subgating.setTabText(self.tab_widgets_subgating.indexOf(self.tab_sweep), 
                                              _translate("MainWindow", "Sweep"))   
        
        self.subgating_label_30.setText(_translate("MainWindow", "Gate Voltages"))
        self.subgating_label_31.setText(_translate("MainWindow", "X-Axis"))
        self.subgating_comboBox.setItemText(0, _translate("MainWindow", "Green"))
        self.subgating_comboBox.setItemText(1, _translate("MainWindow", "Far Red"))
        self.subgating_comboBox.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.subgating_comboBox.setItemText(3, _translate("MainWindow", "Orange"))

        self.subgating_preselect_comboBox.setItemText(0, _translate("MainWindow", "Height"))
        self.subgating_preselect_comboBox.setItemText(1, _translate("MainWindow", "Width"))

        
        self.subgating_polygon_inside_label_29.setText(_translate("MainWindow", "Inside: 0"))
        self.subgating_polygon_inside_label_30.setText(_translate("MainWindow", "Linear Plot Selection"))
        
        self.subgating_label_32.setText(_translate("MainWindow", "Y-Axis"))

        self.subgating_preselect_comboBox_2.setItemText(0, _translate("MainWindow", "Height"))
        self.subgating_preselect_comboBox_2.setItemText(1, _translate("MainWindow", "Width"))

        
        self.subgating_comboBox_2.setItemText(0, _translate("MainWindow", "Green"))
        self.subgating_comboBox_2.setItemText(1, _translate("MainWindow", "Far Red"))
        self.subgating_comboBox_2.setItemText(2, _translate("MainWindow", "Ultra Violet"))
        self.subgating_comboBox_2.setItemText(3, _translate("MainWindow", "Orange"))
        self.subgating_label_29.setText(_translate("MainWindow", "Scatter Plot Axes"))        
        
        self.subgating_pushButton_9.setText(_translate("MainWindow", "Polygon"))
        self.subgating_pushButton_10.setText(_translate("MainWindow", "Clear"))
        self.subgating_pushButton_12.setText(_translate("MainWindow", "Extract Linear Plot"))

        self.pushButton_12.setText(_translate("MainWindow", "Shape Edit"))
        self.subgating_pushButton_11.setText(_translate("MainWindow", "Shape Edit"))
        
        self.pushButton_11.setText(_translate("MainWindow", "Extract"))
        
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
        self.label_84.setText(_translate("MainWindow", "Selected/Total"))
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
        self.label_93.setText(_translate("MainWindow", "Selected Data"))
        
        self.label_num_peak_1.setText(_translate("MainWindow", "Channel"))
        self.label_num_peak_2.setText(_translate("MainWindow", "Condition"))
        self.label_num_peak_3.setText(_translate("MainWindow", "# of Peaks"))
        self.label_num_peak_4.setText(_translate("MainWindow", "Green"))
        self.label_num_peak_5.setText(_translate("MainWindow", "Red"))
        self.label_num_peak_6.setText(_translate("MainWindow", "Blue"))
        self.label_num_peak_7.setText(_translate("MainWindow", "Orange"))
        self.label_num_peak_title.setText(_translate("MainWindow", "Multi Peaks Gating"))
        self.comboBox_peak_num_1.setItemText(0, _translate("MainWindow", ">="))
        self.comboBox_peak_num_1.setItemText(1, _translate("MainWindow", "=="))
        self.comboBox_peak_num_1.setItemText(2, _translate("MainWindow", "<="))
        self.comboBox_peak_num_2.setItemText(0, _translate("MainWindow", ">="))
        self.comboBox_peak_num_2.setItemText(1, _translate("MainWindow", "=="))
        self.comboBox_peak_num_2.setItemText(2, _translate("MainWindow", "<="))
        self.comboBox_peak_num_3.setItemText(0, _translate("MainWindow", ">="))
        self.comboBox_peak_num_3.setItemText(1, _translate("MainWindow", "=="))
        self.comboBox_peak_num_3.setItemText(2, _translate("MainWindow", "<="))
        self.comboBox_peak_num_4.setItemText(0, _translate("MainWindow", ">="))
        self.comboBox_peak_num_4.setItemText(1, _translate("MainWindow", "=="))
        self.comboBox_peak_num_4.setItemText(2, _translate("MainWindow", "<="))
        self.lineEdit_peak_num_1.setText("0")
        self.lineEdit_peak_num_2.setText("0")
        self.lineEdit_peak_num_3.setText("0")
        self.lineEdit_peak_num_4.setText("0")

        self.tab_widget_peak_width.setTabText(self.tab_widget_peak_width.indexOf(self.sub_tab_width_scatter), 
                                              _translate("MainWindow", "Scatter"))
        self.tab_widget_peak_width.setTabText(self.tab_widget_peak_width.indexOf(self.sub_tab_width_histogram), 
                                              _translate("MainWindow", "Histogram")) 
        self.label_271.setText(_translate("MainWindow", "Channel Selection"))
        
        self.label_180.setText(_translate("MainWindow", "Start Peak"))
        self.label_181.setText(_translate("MainWindow", "Channel Selection"))
        self.label_182.setText(_translate("MainWindow", "End Peak"))
        self.label_183.setText(_translate("MainWindow", "*Peak difference < 15"))
        self.label_184.setText(_translate("MainWindow", "Last/Next"))
        self.label_185.setText(_translate("MainWindow", "Polynomial Order"))
        self.label_186.setText(_translate("MainWindow", "Smooth Level"))
        self.label_187.setText(_translate("MainWindow", "Smoothing"))
        self.label_188.setText(_translate("MainWindow", "Custom Sample Size"))
        self.polygon_Smooth_enable.setText(_translate("MainWindow", "Enable smooth?"))
        self.pushButton_6.setText(_translate("MainWindow", "Generate Plot"))
        self.pushButton_7.setText(_translate("MainWindow", "Next Page"))
        self.pushButton_8.setText(_translate("MainWindow", "Last Page"))
        self.polygon_channel_1.setText(_translate("MainWindow", "Channel 1"))
        self.polygon_channel_2.setText(_translate("MainWindow", "Channel 2"))
        self.polygon_channel_3.setText(_translate("MainWindow", "Channel 3"))
        self.polygon_channel_4.setText(_translate("MainWindow", "Channel 4"))
        self.tab_widgets_subgating.setTabText(self.tab_widgets_subgating.indexOf(self.tab_4), _translate("MainWindow", "User defined linear graph"))
                        
        self.pushButton_9.setText(_translate("MainWindow", "Polygon"))
        self.pushButton_10.setText(_translate("MainWindow", "Clear"))

        
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
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_3), _translate("MainWindow", "Raw Data Viewer"))               
        
        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_peakwidth),
                                         _translate("MainWindow", "Peak Width/Number Subgating"))
        
        self.tab_widgets_main.setTabText(self.tab_widgets_main.indexOf(self.tab_report),
                                         _translate("MainWindow", "Log"))
        self.label_54.setText(_translate("MainWindow", "Channels"))
        self.pushButton_saveplot_2.setText(_translate("MainWindow", "Save Plot"))
        self.label_59.setText(_translate("MainWindow", "Peak Width Threshold"))
        self.label_60.setText(_translate("MainWindow", "Min Width"))
#         self.label_76.setText(_translate("MainWindow", "V"))
        self.label_77.setText(_translate("MainWindow", "Percentage"))
        self.label_78.setText(_translate("MainWindow", "%"))
        self.label_79.setText(_translate("MainWindow", "Bin Width"))
        self.label_density_adjust1.setText(_translate("MainWindow", "Density Level"))
        self.label_density_adjust2.setText(_translate("MainWindow", "Density Level"))
        self.label_density_adjust3.setText(_translate("MainWindow", "Density Level"))
        
        self.menuFiles.setTitle(_translate("MainWindow", "Projects"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionAdd_New.setText(_translate("MainWindow", "Add New"))
        self.actionAdd_Save.setText(_translate("MainWindow", "Save"))
        self.actionAdd_Load.setText(_translate("MainWindow", "Load"))
        self.actionAdd_SaveSingleFile.setText(_translate("MainWindow", "Save Single File"))
        self.actionAdd_SaveParameters.setText(_translate("MainWindow", "Save Parameters"))
        self.actionAdd_LoadParameters.setText(_translate("MainWindow", "Load Parameters"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        
        self.label_filter.setText(_translate("MainWindow", "test"))

    def pressed(self):
        print('pressed')
        check0 = time.time()
        
        
        # load parameters
        if self.load ==True:
            with open(str(self.loadname), 'rb') as filehandle:
                # read the data as binary data stream
                parameters = pickle.load(filehandle)

            # check box
            self.checkbox_ch1.setChecked(parameters[0])
            self.checkbox_ch2.setChecked(parameters[1])
            self.checkbox_ch3.setChecked(parameters[2])
            self.checkbox_ch12.setChecked(parameters[3])
            self.checkbox_ch13.setChecked(parameters[4])
            self.checkbox_ch23.setChecked(parameters[5])
            self.checkBox_7.setChecked(parameters[6])
            self.channel_1.setChecked(parameters[7])
            self.channel_2.setChecked(parameters[8])
            self.channel_3.setChecked(parameters[9])
            self.channel_4.setChecked(parameters[10])
            self.polygon_channel_1.setChecked(parameters[11])
            self.polygon_channel_2.setChecked(parameters[12])
            self.polygon_channel_3.setChecked(parameters[13])
            self.polygon_channel_4.setChecked(parameters[14])

            # combobox 
            self.comboBox_5.setCurrentIndex(parameters[15]) 
            self.comboBox_6.setCurrentIndex(parameters[16])
            self.comboBox_peak_num_1.setCurrentIndex(parameters[17])
            self.comboBox_peak_num_2.setCurrentIndex(parameters[18])
            self.comboBox_peak_num_3.setCurrentIndex(parameters[19])
            self.comboBox_peak_num_4.setCurrentIndex(parameters[20])
            self.comboBox.setCurrentIndex(parameters[21])
            self.comboBox_2.setCurrentIndex(parameters[22])
            self.subgating_comboBox.setCurrentIndex(parameters[23])
            self.subgating_comboBox_2.setCurrentIndex(parameters[24])
            self.subgating_preselect_comboBox.setCurrentIndex(parameters[25])
            self.subgating_preselect_comboBox_2.setCurrentIndex(parameters[26])

            # lineedit 
            self.lineEdit_gatevoltage_2.setText(parameters[27])
            self.lineEdit_gatevoltage_4.setText(parameters[28])
            self.lineEdit_gatevoltagemaximum.setText(parameters[29])
            self.lineEdit_gatevoltageminimum.setText(parameters[30])
            self.lineEdit_increments.setText(parameters[31])
            self.lineEdit_binwidth_2.setText(parameters[32])
            self.lineEdit_binwidth_3.setText(parameters[33])
            self.lineEdit_binwidth.setText(parameters[34])
            self.lineEdit_gatevoltage.setText(parameters[35])
            self.lineEdit_5.setText(parameters[36])
            self.lineEdit_6.setText(parameters[37])
            self.lineEdit_7.setText(parameters[38])
            self.lineEdit_8.setText(parameters[39])
            self.lineEdit_9.setText(parameters[40])
            self.lineEdit_10.setText(parameters[41])
            self.lineEdit_11.setText(parameters[42])
            self.lineEdit_12.setText(parameters[43])
            self.lineEdit_peak_num_1.setText(parameters[44])
            self.lineEdit_peak_num_2.setText(parameters[45])
            self.lineEdit_peak_num_3.setText(parameters[46])
            self.lineEdit_peak_num_4.setText(parameters[47])
            self.lineEdit_scatterxvoltage.setText(parameters[48])
            self.lineEdit_scatteryvoltage.setText(parameters[49])
            self.file_dict_list = parameters[50]
            list_name = parameters[51]
            self.save_a = parameters[52]
            self.checkbox_Droplet_Record.setChecked(parameters[69])

            # reset file list box on left top
            self.analog = {}
            self.file_list_view.clear()
#             self.comboBox_option1.clear()
#             self.comboBox_option2.clear()

            for i in range(len(list_name)):
                f = list_name[i]
                # for i in range
                self.file_list_view.addItem(f)
#                 self.comboBox_option1.addItem(f)
#                 self.comboBox_option2.addItem(f)

                # record change in the log
                self.textbox = self.textbox + "\n" + "open file:" + str(f)
                self.textEdit.setPlainText(self.textbox)  

            for i in range(self.file_list_view.count()):
                item = self.file_list_view.item(i)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.file_list_view.setCurrentRow(0)  
            
#             self.thresholdUpdated()
            try:
                self.thresholdUpdated_2()
            except:
                print("threshold_2 updated")
        
        
        elif self.load_parameters == True:
            with open(str(self.loadname), 'rb') as filehandle:
                # read the data as binary data stream
                parameters = pickle.load(filehandle)

            # check box
            self.checkbox_ch1.setChecked(parameters[0])
            self.checkbox_ch2.setChecked(parameters[1])
            self.checkbox_ch3.setChecked(parameters[2])
            self.checkbox_ch12.setChecked(parameters[3])
            self.checkbox_ch13.setChecked(parameters[4])
            self.checkbox_ch23.setChecked(parameters[5])
            self.checkBox_7.setChecked(parameters[6])
            self.channel_1.setChecked(parameters[7])
            self.channel_2.setChecked(parameters[8])
            self.channel_3.setChecked(parameters[9])
            self.channel_4.setChecked(parameters[10])
            self.polygon_channel_1.setChecked(parameters[11])
            self.polygon_channel_2.setChecked(parameters[12])
            self.polygon_channel_3.setChecked(parameters[13])
            self.polygon_channel_4.setChecked(parameters[14])

            # combobox 
            self.comboBox_5.setCurrentIndex(parameters[15]) 
            self.comboBox_6.setCurrentIndex(parameters[16])
            self.comboBox_peak_num_1.setCurrentIndex(parameters[17])
            self.comboBox_peak_num_2.setCurrentIndex(parameters[18])
            self.comboBox_peak_num_3.setCurrentIndex(parameters[19])
            self.comboBox_peak_num_4.setCurrentIndex(parameters[20])
            self.comboBox.setCurrentIndex(parameters[21])
            self.comboBox_2.setCurrentIndex(parameters[22])
            self.subgating_comboBox.setCurrentIndex(parameters[23])
            self.subgating_comboBox_2.setCurrentIndex(parameters[24])
            self.subgating_preselect_comboBox.setCurrentIndex(parameters[25])
            self.subgating_preselect_comboBox_2.setCurrentIndex(parameters[26])

            # lineedit 
            self.lineEdit_gatevoltage_2.setText(parameters[27])
            self.lineEdit_gatevoltage_4.setText(parameters[28])
            self.lineEdit_gatevoltagemaximum.setText(parameters[29])
            self.lineEdit_gatevoltageminimum.setText(parameters[30])
            self.lineEdit_increments.setText(parameters[31])
            self.lineEdit_binwidth_2.setText(parameters[32])
            self.lineEdit_binwidth_3.setText(parameters[33])
            self.lineEdit_binwidth.setText(parameters[34])
            self.lineEdit_gatevoltage.setText(parameters[35])
            self.lineEdit_5.setText(parameters[36])
            self.lineEdit_6.setText(parameters[37])
            self.lineEdit_7.setText(parameters[38])
            self.lineEdit_8.setText(parameters[39])
            self.lineEdit_9.setText(parameters[40])
            self.lineEdit_10.setText(parameters[41])
            self.lineEdit_11.setText(parameters[42])
            self.lineEdit_12.setText(parameters[43])
            self.lineEdit_peak_num_1.setText(parameters[44])
            self.lineEdit_peak_num_2.setText(parameters[45])
            self.lineEdit_peak_num_3.setText(parameters[46])
            self.lineEdit_peak_num_4.setText(parameters[47])
            self.lineEdit_scatterxvoltage.setText(parameters[48])
            self.lineEdit_scatteryvoltage.setText(parameters[49])
            self.checkbox_Droplet_Record(parameters[50])
            
            
        
        

        try:
            self.chart_title_change(change = self.file_list_view.currentItem().text())
        except:
            self.file_list_view.setCurrentRow(0)
            self.chart_title_change(change = self.file_list_view.currentItem().text())     
        
        # global Ch1,Ch2,Ch3,Ch1_2,Ch1_3,Ch2_3,Locked,Raw_Time_Log,current_file_dict
        self.main_file_select = self.file_list_view.currentRow()
        self.ch1_checkbox = self.checkbox_ch1.isChecked()
        self.ch2_checkbox = self.checkbox_ch2.isChecked()
        self.ch3_checkbox = self.checkbox_ch3.isChecked()
        self.ch12_checkbox = self.checkbox_ch12.isChecked()
        self.ch13_checkbox = self.checkbox_ch13.isChecked()
        self.ch23_checkbox = self.checkbox_ch23.isChecked()
        self.Droplet_Record_checkbox = self.checkbox_Droplet_Record.isChecked()
        self.all_checkbox = self.checkBox_7.isChecked()

        

            
        self.histo_channel = self.listView_channels.currentRow()
        self.histo_bins = float(self.lineEdit_binwidth.text())
        self.peak_width_channel = self.listView_channels_3.currentRow()
        self.peak_width_bins = float(self.lineEdit_binwidth_3.text())
        self.scatter_channelx = self.comboBox.currentIndex()
        self.scatter_channely = self.comboBox_2.currentIndex()
        self.width_scatter_channelx = self.comboBox_5.currentIndex()
        self.width_scatter_channely = self.comboBox_6.currentIndex()
        self.peak_num_mode = []
        self.peak_num_in = []
        self.peak_num_mode.append(self.comboBox_peak_num_1.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_2.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_3.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_4.currentIndex())
        self.peak_num_in.append(int(self.lineEdit_peak_num_1.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_2.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_3.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_4.text()))

        self.sweep_channel = self.listView_channels_2.currentRow()
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
        self.sweep_bins = float(self.lineEdit_binwidth_2.text())
        self.current_file_dict = self.file_dict_list[self.main_file_select]



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



        
        #         start = time.time()
        if stats.under_sample_factor == "":
            under_sample = 1
        else:
            under_sample = stats.under_sample_factor
        
        channel = self.peak_width_channel
        width_enable = True

        try:
            self.chunksize = self.chunk_resample
        except:
#             self.chunksize = int(1000 / float(under_sample))
            self.chunksize = 200

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

        ### check Voltage threshold(V)  
        threshold = [self.lineEdit_9.text(),self.lineEdit_10.text(),self.lineEdit_11.text(),self.lineEdit_12.text()]
        peaks_threshold = []
        width_threshold = []
        width_min = [0,0,0,0]
        width_max = [500,500,500,500]

        if self.current_file_dict["Param"] != "":
            with open(self.current_file_dict["Param"]) as param_file:
                stats_reader = csv.reader(param_file, delimiter=",")
                location = [[0,0],[0,0]]
                param_holder = []
                for x, lines in enumerate(stats_reader):
                    param_holder.append(lines)
                    for y, field in enumerate(lines):
                        if field == "Peak Threshold (V)":
                            location[0] = [x,y]
                        if field == "BG Threshold (V)":
                            location[1] = [x, y]
                try:
                    for i in range(1,5):
                        peaks_threshold.append(float(param_holder[location[0][0]+i][location[0][1]]))
                        width_threshold.append(float(param_holder[location[1][0]+i][location[1][1]]))
                        print("Peaks Threshold Found: ", peaks_threshold)
                        print("Width Threshold Found: ", width_threshold)
                except:
                    print("Peaks Threshold Not Found")
        if len(peaks_threshold) == 0:
            peaks_threshold = [1, 1, 1, 1]

        try:
            # test if numbers entered in threshold
            for i in range(4):
                threshold[i] = float(threshold[i])
        except:
            # if not, find in parameter file
            if len(width_threshold) == 0:
                threshold = [1, 1, 1, 1]
            else:
                threshold = width_threshold
                
        self.lineEdit_9.setText(str(threshold[0]))
        self.lineEdit_10.setText(str(threshold[1]))
        self.lineEdit_11.setText(str(threshold[2]))
        self.lineEdit_12.setText(str(threshold[3]))    

        self.width_update, self.reanalysis = self.ui_state.peak_width_update(channel_select=self.peak_width_channel,
                                                                             bins=self.peak_width_bins,
                                                                             peak_width_threshold=self.lineEdit_gatevoltage_2.text(),
                                                                             voltage_threshold=threshold)

        ### check end
        
        
        
        try:
            self.update = self.ui_state.working_file_update_check(file=self.current_file_dict, chall=self.all_checkbox,
                                                                  ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                                  ch3=self.ch3_checkbox,
                                                                  ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                                  ch2_3=self.ch23_checkbox, Droplet_Record=self.Droplet_Record_checkbox,
                                                                  reset=Ui_MainWindow.reset)
            print('file',self.main_file_select)
        except:
            self.update = self.ui_state.working_file_update_check(file=self.current_file_dict, chall=self.all_checkbox,
                                                                  ch1=self.ch1_checkbox, ch2=self.ch2_checkbox,
                                                                  ch3=self.ch3_checkbox,
                                                                  ch1_2=self.ch12_checkbox, ch1_3=self.ch13_checkbox,
                                                                  ch2_3=self.ch23_checkbox, Droplet_Record=self.Droplet_Record_checkbox)
            print('file',self.main_file_select)
        self.filter_update = self.ui_state.filter_peak_update(x_axis_channel_number=int(self.comboBox_5.currentIndex()),
                                                              y_axis_channel_number=int(self.comboBox_6.currentIndex()),
                                                              x_axis_channel_min=float(self.lineEdit_5.text()),
                                                              x_axis_channel_max=float(self.lineEdit_7.text()),
                                                              y_axis_channel_min=float(self.lineEdit_6.text()),
                                                              y_axis_channel_max=float(self.lineEdit_8.text()),
                                                              peak_num_in=self.peak_num_in,
                                                              peak_num_mode=self.peak_num_mode)

        threshold_check = self.ui_state.threshold_check(threshold = threshold)

        if self.update or threshold_check:
            peak_enable =True
        else:
            peak_enable = False
        print("peak recalculate enable check is :",peak_enable) 
        print("resample parameter self.reset check is :",reset) 
        print("filter condition change check is :",self.filter_update)
        print("threshold check is:",self.reanalysis, ", current threshold is:", threshold)
            
            
        self.data_updated = False
               
            
        check1 = time.time()
        
        if self.current_file_dict["Peak Record"] in self.analog and not reset and not self.reanalysis and not self.load:
            print("--------------------------------------------------------not reset")
            self.tab_widgets_main.currentIndex
            
            check2 = time.time()
            self.update_working_data()
            check2A = time.time()
            if self.data_updated == True:
                self.draw(True)
                check3 = time.time()
                self.draw_2(True)
                check3A = time.time()
                self.update_sweep_graphs(True)
            else:
                self.draw()
                check3 = time.time()
                self.draw_2()
                
            check4 = time.time()
            
            self.draw_peak_width()
            check4A = time.time()
            self.draw_peak_width_2()
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
            self.update_sampling_Rate()
            check5 = time.time()
            
            self.subgating_scatter(pressed_function_redo = self.draw_2_update)

        else:
            print("--------------------------------------------------------reset")
            if self.load == False:

                a = Analysis.file_extracted_data_Qing(self.current_file_dict,threshold, 
                                                      peaks_threshold, width_min, width_max, 
                                                      width_enable, peak_enable, channel, self.chunksize,
                                                     0, stats.ch1_hit, stats.ch2_hit, stats.ch3_hit, stats.ch12_hit, 
                                                      stats.ch13_hit,
                                                      stats.ch23_hit, stats.Droplet_Record_hit,
                                                      stats.total_sorted)
                
                print("data extration complete, drawing....")
    
                self.analog.update(a.analog_file)

                self.save_a = self.analog
            else:
                # load
                self.analog = self.save_a
                print("data loading complete, drawing....")
            
            check2 = time.time()
            
            self.update_working_data()
            
            # direct everything into window filters
            # self.draw is histogram
            # self.draw_2 triggers 2nd and 3rd filter
            if self.data_updated == True:
                self.draw(True)
                self.draw_2(True)
                self.update_sweep_graphs(True)
            else:   
                self.draw()
                self.draw_2()
                
            
#             check4 = time.time()
            
            self.draw_peak_width()
#             check4A = time.time()
#             self.draw_peak_width_2()
#             check4B = time.time()
            
#             self.update_sweep_graphs()
#             check4C = time.time()
#             self.sweep_update_high()
#             check4D = time.time()
#             self.sweep_update_low()
#             check4E = time.time()
#             self.sweep_update()
#             check4F = time.time()
            
#             self.update_statistic()
#             check4G = time.time()
#             self.update_sampling_Rate()
            
#             check5 = time.time()
#             Ui_MainWindow.reset = False
            
                    # add item to polygon linear plot tab
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
            if self.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] != '':
                self.comboBox_14_list[len(self.comboBox_14_list)] = "Peak Record"
            ### End
            
            self.subgating_scatter(pressed_function_redo = True) 
            print("complete!")
        check6 = time.time()

               
                


    def add(self):
        name, _ = QFileDialog.getOpenFileNames(self.mainwindow, 'Open File', filter="*peak*")
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
#             self.comboBox_option1.addItem(f)
#             self.comboBox_option2.addItem(f)
        for i in range(self.file_list_view.count()):
            item = self.file_list_view.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def openfolder(self):
        self.analog = {}
        self.file_list_view.clear()
        self.file_dict_list.clear()
#         self.comboBox_option1.clear()
#         self.comboBox_option2.clear()
        name, _ = QFileDialog.getOpenFileNames(self.mainwindow, 'Open File', filter="*peak*")
        for f in name:
            print(f)
            self.file_dict_list.append(Helper.project_namelist(f))
            self.file_list_view.addItem(f)
#             self.comboBox_option1.addItem(f)
#             self.comboBox_option2.addItem(f)
            
            # record change in the log
            self.textbox = self.textbox + "\n" + "open file:" + str(f)
            self.textEdit.setPlainText(self.textbox)   
            
        for i in range(self.file_list_view.count()):
            item = self.file_list_view.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def save(self):
        
        name,_ = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File')
        try: 
            list_name = []
            for i in range(self.file_list_view.count()):
                self.file_list_view.setCurrentRow(i)
                list_name.append(self.file_list_view.currentItem().text())
                
            dict_list = self.file_dict_list
            parameters = [self.checkbox_ch1.isChecked(), self.checkbox_ch2.isChecked(), self.checkbox_ch3.isChecked(),
                         self.checkbox_ch12.isChecked(), self.checkbox_ch13.isChecked(), self.checkbox_ch23.isChecked(),
                         self.checkBox_7.isChecked(), self.channel_1.isChecked(), self.channel_2.isChecked(), 
                          self.channel_3.isChecked(), 
                         self.channel_4.isChecked(), self.polygon_channel_1.isChecked(), self.polygon_channel_2.isChecked(),
                         self.polygon_channel_3.isChecked(), self.polygon_channel_4.isChecked(),
                          self.comboBox_5.currentIndex(),
                        self.comboBox_6.currentIndex(),
                        self.comboBox_peak_num_1.currentIndex(),
                        self.comboBox_peak_num_2.currentIndex(),
                        self.comboBox_peak_num_3.currentIndex(),
                        self.comboBox_peak_num_4.currentIndex(),
                        self.comboBox.currentIndex(),
                        self.comboBox_2.currentIndex(),
                        self.subgating_comboBox.currentIndex(),
                        self.subgating_comboBox_2.currentIndex(),
                        self.subgating_preselect_comboBox.currentIndex(),
                        self.subgating_preselect_comboBox_2.currentIndex(),
                        self.lineEdit_gatevoltage_2.text(),
                        self.lineEdit_gatevoltage_4.text(),
                        self.lineEdit_gatevoltagemaximum.text(),
                        self.lineEdit_gatevoltageminimum.text(),
                        self.lineEdit_increments.text(),
                        self.lineEdit_binwidth_2.text(),
                        self.lineEdit_binwidth_3.text(),
                        self.lineEdit_binwidth.text(),
                        self.lineEdit_gatevoltage.text(),
                        self.lineEdit_5.text(),
                        self.lineEdit_6.text(),
                        self.lineEdit_7.text(),
                        self.lineEdit_8.text(),
                        self.lineEdit_9.text(),
                        self.lineEdit_10.text(),
                        self.lineEdit_11.text(),
                        self.lineEdit_12.text(),
                        self.lineEdit_peak_num_1.text(),
                        self.lineEdit_peak_num_2.text(),
                        self.lineEdit_peak_num_3.text(),
                        self.lineEdit_peak_num_4.text(),
                        self.lineEdit_scatterxvoltage.text(),
                        self.lineEdit_scatteryvoltage.text(),
                        # file list
                        dict_list,
                        list_name,
                        self.save_a,
                        # polygon 
                        self.inside2,
                        self.points_inside,
                        self.polygon_inside_label_29.text(),
                        self.polygon,
                        self.polygon_for_edit,
                        self.polygon_trigger,
                        self.points,
                        self.points_inside_list,
                         #subgating polygon
                        self.subgating_inside2,
                        self.subgating_points_inside,
                        self.subgating_polygon_inside_label_29.text(),
                        self.subgating_polygon,
                        self.subgating_polygon_for_edit,
                        self.subgating_polygon_trigger,
                        self.subgating_points,
                        self.subgating_points_inside_list,
                        self.checkbox_Droplet_Record.isChecked()]


            with open(str(name.split("/")[-1]), 'wb') as filehandle:
                pickle.dump(parameters, filehandle)
          
        except:
            print("nothing to save")
            
    def load(self):
        name,_= QFileDialog.getOpenFileNames(self.mainwindow, 'Open File')
        if name != []:
            b = ''
            for i in name[0].split("/")[0:-1]:
                b = b + i + "/"
            os.chdir(str(b[0:-1]))
            self.load = True
            self.loadname = name[0].split("/")[-1]
            self.pressed()
    
    def save_single(self):
        
        name,_ = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File')

        list_name = []
        list_name.append(self.file_list_view.currentItem().text())
        
        dict_list = []
        row = self.file_list_view.currentRow() 
        dict_list.append(self.file_dict_list[row])

        
        parameters = [self.checkbox_ch1.isChecked(), self.checkbox_ch2.isChecked(), self.checkbox_ch3.isChecked(),
                     self.checkbox_ch12.isChecked(), self.checkbox_ch13.isChecked(), self.checkbox_ch23.isChecked(),
                     self.checkBox_7.isChecked(), self.channel_1.isChecked(), self.channel_2.isChecked(), 
                      self.channel_3.isChecked(), 
                     self.channel_4.isChecked(), self.polygon_channel_1.isChecked(), self.polygon_channel_2.isChecked(),
                     self.polygon_channel_3.isChecked(), self.polygon_channel_4.isChecked(),
                      self.comboBox_5.currentIndex(),
                    self.comboBox_6.currentIndex(),
                    self.comboBox_peak_num_1.currentIndex(),
                    self.comboBox_peak_num_2.currentIndex(),
                    self.comboBox_peak_num_3.currentIndex(),
                    self.comboBox_peak_num_4.currentIndex(),
                    self.comboBox.currentIndex(),
                    self.comboBox_2.currentIndex(),
                    self.subgating_comboBox.currentIndex(),
                    self.subgating_comboBox_2.currentIndex(),
                    self.subgating_preselect_comboBox.currentIndex(),
                    self.subgating_preselect_comboBox_2.currentIndex(),
                    self.lineEdit_gatevoltage_2.text(),
                    self.lineEdit_gatevoltage_4.text(),
                    self.lineEdit_gatevoltagemaximum.text(),
                    self.lineEdit_gatevoltageminimum.text(),
                    self.lineEdit_increments.text(),
                    self.lineEdit_binwidth_2.text(),
                    self.lineEdit_binwidth_3.text(),
                    self.lineEdit_binwidth.text(),
                    self.lineEdit_gatevoltage.text(),
                    self.lineEdit_5.text(),
                    self.lineEdit_6.text(),
                    self.lineEdit_7.text(),
                    self.lineEdit_8.text(),
                    self.lineEdit_9.text(),
                    self.lineEdit_10.text(),
                    self.lineEdit_11.text(),
                    self.lineEdit_12.text(),
                    self.lineEdit_peak_num_1.text(),
                    self.lineEdit_peak_num_2.text(),
                    self.lineEdit_peak_num_3.text(),
                    self.lineEdit_peak_num_4.text(),
                    self.lineEdit_scatterxvoltage.text(),
                    self.lineEdit_scatteryvoltage.text(),
                    # file list
                    dict_list,
                    list_name,
                    self.save_a,
                    # polygon 
                    self.inside2,
                    self.points_inside,
                    self.polygon_inside_label_29.text(),
                    self.polygon,
                    self.polygon_for_edit,
                    self.polygon_trigger,
                    self.points,
                    self.points_inside_list,
                     #subgating polygon
                    self.subgating_inside2,
                    self.subgating_points_inside,
                    self.subgating_polygon_inside_label_29.text(),
                    self.subgating_polygon,
                    self.subgating_polygon_for_edit,
                    self.subgating_polygon_trigger,
                    self.subgating_points,
                    self.subgating_points_inside_list,
                    self.checkbox_Droplet_Record.isChecked()]

        print("save Location:", name)
        with open(str(name.split("/")[-1]), 'wb') as filehandle:
            pickle.dump(parameters, filehandle)
          
#         except:
#             print("nothing to save")
     
    def load_parameters(self):
        name,_= QFileDialog.getOpenFileNames(self.mainwindow, 'Open File')
        if name != []:
            b = ''
            for i in name[0].split("/")[0:-1]:
                b = b + i + "/"
            os.chdir(str(b[0:-1]))
            self.load_parameters = True
            self.loadname = name[0].split("/")[-1]
            self.pressed()
            
    def save_parameters(self):
        name,_ = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File')
        try: 
            parameters = [self.checkbox_ch1.isChecked(), self.checkbox_ch2.isChecked(), self.checkbox_ch3.isChecked(),
                         self.checkbox_ch12.isChecked(), self.checkbox_ch13.isChecked(), self.checkbox_ch23.isChecked(),
                         self.checkBox_7.isChecked(), self.channel_1.isChecked(), self.channel_2.isChecked(), 
                          self.channel_3.isChecked(), 
                         self.channel_4.isChecked(), self.polygon_channel_1.isChecked(), self.polygon_channel_2.isChecked(),
                         self.polygon_channel_3.isChecked(), self.polygon_channel_4.isChecked(),
                          self.comboBox_5.currentIndex(),
                        self.comboBox_6.currentIndex(),
                        self.comboBox_peak_num_1.currentIndex(),
                        self.comboBox_peak_num_2.currentIndex(),
                        self.comboBox_peak_num_3.currentIndex(),
                        self.comboBox_peak_num_4.currentIndex(),
                        self.comboBox.currentIndex(),
                        self.comboBox_2.currentIndex(),
                        self.subgating_comboBox.currentIndex(),
                        self.subgating_comboBox_2.currentIndex(),
                        self.subgating_preselect_comboBox.currentIndex(),
                        self.subgating_preselect_comboBox_2.currentIndex(),
                        self.lineEdit_gatevoltage_2.text(),
                        self.lineEdit_gatevoltage_4.text(),
                        self.lineEdit_gatevoltagemaximum.text(),
                        self.lineEdit_gatevoltageminimum.text(),
                        self.lineEdit_increments.text(),
                        self.lineEdit_binwidth_2.text(),
                        self.lineEdit_binwidth_3.text(),
                        self.lineEdit_binwidth.text(),
                        self.lineEdit_gatevoltage.text(),
                        self.lineEdit_5.text(),
                        self.lineEdit_6.text(),
                        self.lineEdit_7.text(),
                        self.lineEdit_8.text(),
                        self.lineEdit_9.text(),
                        self.lineEdit_10.text(),
                        self.lineEdit_11.text(),
                        self.lineEdit_12.text(),
                        self.lineEdit_peak_num_1.text(),
                        self.lineEdit_peak_num_2.text(),
                        self.lineEdit_peak_num_3.text(),
                        self.lineEdit_peak_num_4.text(),
                        self.lineEdit_scatterxvoltage.text(),
                        self.lineEdit_scatteryvoltage.text(),
                        self.checkbox_Droplet_Record.isChecked()]


            with open(str(name.split("/")[-1]), 'wb') as filehandle:
                pickle.dump(parameters, filehandle)
          
        except:
            print("nothing to save")
            
    def peak_num_comp(self, number_of_peak, mode, num_in):
        """function to do comparison for peak number filter"""
        if mode == 0:
            if number_of_peak >= num_in:
                return True
            else:
                return False
        elif mode == 1:
            if number_of_peak == num_in:
                return True
            else:
                return False
        elif mode == 2:
            if number_of_peak <= num_in:
                return True
            else:
                return False
        return False

    def peak_num_filter(self):
        """function for peak num filter, mode 0 is >=, mode 1 is ==, mode 2 is =< """
        self.peak_num_filtered_index = []
        holder = [[],[],[],[]]
        for ch in range(4):
            holder[ch] = [i for i, x in enumerate(self.peak_num_working_data[ch])
                          if self.peak_num_comp(x, self.peak_num_mode[ch], self.peak_num_in[ch])]
        self.peak_num_filtered_index = list(set(holder[0]).intersection(set(holder[1]), set(holder[2]), set(holder[3])))


if __name__ == "__main__":
    freeze_support()
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
