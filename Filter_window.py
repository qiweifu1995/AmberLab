from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtCore
from pyqtgraph import PlotWidget
from PyQt5.Qt import QStandardItem
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import os
from scipy.signal import savgol_filter
import Helper
import numpy as np
from itertools import compress
import matplotlib.path as mpltPath
import time
from math import sqrt
import math
from PyQt5.QtGui import QFont, QColor
import Stats_window
import Time_log_selection_window
import logging
import sys
from pyqtgraph import colormap
from Helper import ThreadState
from functools import partial
from pathlib import Path
import csv

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


class RectQuadrant(pg.GraphicsObject):
    """class for drawing the rectangle to show selected quadrant"""

    def __init__(self, rect, parent=None):
        super().__init__(parent)
        self._rect = rect
        self.picture = QtGui.QPicture()
        self._generate_picture()

    @property
    def rect(self):
        return self._rect

    def _generate_picture(self):
        painter = QtGui.QPainter(self.picture)
        painter.setPen(pg.mkPen("w"))
        painter.setBrush(pg.mkBrush((0, 0, 140, 30)))
        painter.drawRect(self.rect)
        painter.end()

    def paint(self, painter, option, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

    def resize(self, rect):
        self._rect = rect
        self.picture = QtGui.QPicture()
        self._generate_picture()


class window_filter(QWidget):
    CHANNEL_NAME = ["488nm Green", "638nm Red", "405nm Blue", "561nm Orange", "Ch5", "Ch6"]

    def __init__(self, parent, current_file_dict=None, working_data=None, peak_width_working_data=None,
                 peak_num_working_data=None, linear_plot_channel_list={}, multi_file=None, multi_file_index=None,
                 root=None, saved_data=None, extracted_ratio_data=None):
        super().__init__()

        self.line_thickness = 4
        self.axis_font_size = 12
        self.legend_font_size = 12
        self.axis_thickness = 3
        self.axis_font = QFont('Times')
        self.axis_font.setPointSize(21)
        self.axis_pen = pg.mkPen(QColor(0, 0, 0), width=self.axis_thickness)

        self.setupUI()
        print(saved_data)
        if saved_data is None:
            self.ui = parent
            self.ch_select = ChannelSelectWindow(self)
            self.legacy_mode = False
            # tree_index saved the index number for all filters, include its parent and child branch
            # ex. index = 0,1,1 means: select filter index is "No.1", under parent "No.1", upder grand-parent "No.0"
            self.linear_plot_channel_list = linear_plot_channel_list
            self.tree_index = self.ui.tree_index
            self.current_file_dict = current_file_dict
            self.working_data = working_data
            self.filter_out_list = []
            self.peak_width_working_data = []
            self.peak_num_working_data = []
            self.peak_time_working_data = []
            self.extracted_ratio_data = []
            self.points_inside_square = []
            # root will hold the file index for the root file if true, else None
            self.root = root
            self.selected_quadrant = 1
            self.rect_trigger = False
            self.reset_comboBox = True
            self.multi_file = multi_file
            self.multi_file_index = multi_file_index

            self.x = []
            self.y = []
            self.polygon = []
            self.points_inside = []
            self.x_quadrant_data = [[] for i in range(6)]
            self.y_quadrant_data = [[] for i in range(6)]
            self.Ch1_channel0 = []
            self.Ch1_channel1 = []
            self.Ch1_channel0_peak_num = []
            self.Ch1_channel1_peak_num = []

            # plot setting
            self.line_thickness = 4
            self.axis_font_size = 12
            self.legend_font_size = 12
            self.axis_thickness = 3
            self.axis_font = QFont('Times')
            self.axis_font.setPointSize(21)
            self.axis_pen = pg.mkPen(QColor(0, 0, 0), width=self.axis_thickness)

            # linear plot data
            self.index_in_all_selected_channel = []

            # export parent index
            # ex. index = 0,1,1 ; parent index = 0,1
            if len(self.tree_index) > 1:
                parent_index = self.tree_index[1:]
                self.points_inside_square = self.ui.tree_dic[parent_index]['quadrant1_list_or_polygon']
                self.peak_width_working_data = peak_width_working_data
                self.peak_num_working_data = peak_num_working_data
                self.extracted_ratio_data = extracted_ratio_data
                self.root = None
                self.comboBox_ch_select.setDisabled(True)
                self.button_channel_select.setDisabled(True)
            # sets up the stats window
            self.stats_window = Stats_window.StatsWindow()

            # set up plot data
            self.spots = []
            self.scatter = pg.ScatterPlotItem()

        else:
            self.ui = parent
            self.ch_select = ChannelSelectWindow(self)
            # tree_index saved the index number for all filters, include its parent and child branch
            # ex. index = 0,1,1 means: select filter index is "No.1", under parent "No.1", upder grand-parent "No.0"
            self.legacy_mode = False
            self.linear_plot_channel_list = saved_data.linear_plot_channel_list
            self.tree_index = saved_data.tree_index
            self.current_file_dict = saved_data.current_file_dict
            self.working_data = saved_data.working_data
            self.filter_out_list = saved_data.filter_out_list
            self.peak_width_working_data = saved_data.peak_width_working_data
            self.peak_num_working_data = saved_data.peak_num_working_data
            self.peak_time_working_data = saved_data.peak_time_working_data
            self.points_inside_square = saved_data.points_inside_square
            # root will hold the file index for the root file if true, else None
            self.root = saved_data.root
            self.selected_quadrant = 1
            self.rect_trigger = False
            self.reset_comboBox = True
            self.multi_file = saved_data.multi_file
            self.multi_file_index = saved_data.multi_file_index

            self.x = []
            self.y = []
            self.polygon = saved_data.polygon
            self.points_inside = saved_data.points_inside
            self.x_quadrant_data = [[] for i in range(6)]
            self.y_quadrant_data = [[] for i in range(6)]

            self.Ch1_channel0 = saved_data.Ch1_channel0
            self.Ch1_channel1 = saved_data.Ch1_channel1
            self.Ch1_channel0_peak_num = saved_data.Ch1_channel0_peak_num
            self.Ch1_channel1_peak_num = saved_data.Ch1_channel1_peak_num

            # ui element update
            self.comboBox_3.setCurrentIndex(saved_data.window_setting["x_color"])
            self.comboBox_4.setCurrentIndex(saved_data.window_setting["y_color"])
            self.comboBox_1.setCurrentIndex(saved_data.window_setting["x_mode"])
            self.comboBox_2.setCurrentIndex(saved_data.window_setting["y_mode"])
            self.GateVoltage_x.setText(saved_data.window_setting["GateVoltage_x"])
            self.GateVoltage_y.setText(saved_data.window_setting["GateVoltage_y"])
            self.comboBox_peak_num_1.setCurrentIndex(saved_data.window_setting["ch1_peak_num_mode"])
            self.comboBox_peak_num_2.setCurrentIndex(saved_data.window_setting["ch2_peak_num_mode"])
            self.comboBox_peak_num_3.setCurrentIndex(saved_data.window_setting["ch3_peak_num_mode"])
            self.comboBox_peak_num_4.setCurrentIndex(saved_data.window_setting["ch4_peak_num_mode"])
            self.comboBox_peak_num_5.setCurrentIndex(saved_data.window_setting["ch5_peak_num_mode"])
            self.comboBox_peak_num_6.setCurrentIndex(saved_data.window_setting["ch6_peak_num_mode"])
            self.lineEdit_peak_num_1.setText(saved_data.window_setting["ch1_peak_num"])
            self.lineEdit_peak_num_2.setText(saved_data.window_setting["ch2_peak_num"])
            self.lineEdit_peak_num_3.setText(saved_data.window_setting["ch3_peak_num"])
            self.lineEdit_peak_num_4.setText(saved_data.window_setting["ch4_peak_num"])
            self.lineEdit_peak_num_5.setText(saved_data.window_setting["ch5_peak_num"])
            self.lineEdit_peak_num_6.setText(saved_data.window_setting["ch6_peak_num"])

            # plot setting
            self.line_thickness = 4
            self.axis_font_size = 12
            self.legend_font_size = 12
            self.axis_thickness = 3
            self.axis_font = QFont('Times')
            self.axis_font.setPointSize(21)
            self.axis_pen = pg.mkPen(QColor(0, 0, 0), width=self.axis_thickness)

            # linear plot data
            self.index_in_all_selected_channel = saved_data.index_in_all_selected_channel

            # sets up the stats window
            self.stats_window = Stats_window.StatsWindow()

            # set up plot data
            self.spots = saved_data.spots
            logging.info(self.spots)
            self.scatter = pg.ScatterPlotItem()
            self.scatter.addPoints(self.spots)
            self.graphWidget.addItem(self.scatter)

            pen = pg.mkPen(color='r', width=5, style=QtCore.Qt.DashLine)
            self.lr_x_axis.setValue(float(self.GateVoltage_x.text()))
            self.lr_y_axis.setValue(float(self.GateVoltage_y.text()))

            self.lr_x_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
            self.lr_x_axis.sigPositionChangeFinished.connect(self.quadrant_rect_resize)
            self.lr_x_axis.sigPositionChanged.connect(self.quadrant_rect_resize)
            self.lr_y_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
            self.lr_y_axis.sigPositionChanged.connect(self.quadrant_rect_resize)
            self.lr_y_axis.sigPositionChangeFinished.connect(self.quadrant_rect_resize)
            # reset threshold # test
            if len(self.tree_index) > 1:
                self.comboBox_ch_select.setDisabled(True)
                self.button_channel_select.setDisabled(True)
            self.infiniteline_table_update()

    def setupUI(self):
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
        Scatter_plot_layout.addWidget(self.lineedit_filter_name, 1, 1, 1, 2)

        self.line_filter_name = QtWidgets.QFrame()
        self.line_filter_name.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_filter_name.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_filter_name, 2, 0, 1, 7)

        # some thresholds
        self.label_Axes = QLabel("Scatter Plot Axes")
        sizePolicy.setHeightForWidth(self.label_Axes.sizePolicy().hasHeightForWidth())
        self.label_Axes.setSizePolicy(sizePolicy)
        Scatter_plot_layout.addWidget(self.label_Axes, 3, 0, 1, 1)

        self.label_x_Axis = QLabel("X-Axis")
        Scatter_plot_layout.addWidget(self.label_x_Axis, 4, 0, 1, 1)

        self.label_y_Axis = QLabel("Y-Axis")
        Scatter_plot_layout.addWidget(self.label_y_Axis, 5, 0, 1, 1)

        self.label_channel_select = QLabel("Select Ch")
        Scatter_plot_layout.addWidget(self.label_channel_select, 3, 5, 1, 1)

        self.button_channel_select = QPushButton("Legacy Ch Select")
        Scatter_plot_layout.addWidget(self.button_channel_select, 5, 5, 1, 1)

        self.spacerItem_ch_select = QtWidgets.QSpacerItem(50, 1, QtWidgets.QSizePolicy.Minimum,
                                                          QtWidgets.QSizePolicy.Minimum)
        Scatter_plot_layout.addItem(self.spacerItem_ch_select, 5, 6, 1, 1)

        ### Check box layout
        self.comboBox_1 = QtWidgets.QComboBox()
        self.comboBox_1.addItem("Height")
        self.comboBox_1.addItem("Width")
        self.comboBox_1.addItem("Ratio")

        self.comboBox_2 = QtWidgets.QComboBox()
        self.comboBox_2.addItem("Height")
        self.comboBox_2.addItem("Width")
        self.comboBox_2.addItem("Ratio")

        self.comboBox_3 = QtWidgets.QComboBox()
        for channel_name in self.CHANNEL_NAME:
            self.comboBox_3.addItem(channel_name)

        self.comboBox_4 = QtWidgets.QComboBox()
        for channel_name in self.CHANNEL_NAME:
            self.comboBox_4.addItem(channel_name)

        self.comboBox_ch_select = QtWidgets.QComboBox()
        self.comboBox_ch_select.addItem("All Droplets")
        self.comboBox_ch_select.addItem("Sorted Positives")
        self.comboBox_ch_select.addItem("All Positives")
        self.comboBox_ch_select.addItem("Locked Positives")

        Scatter_plot_layout.addWidget(self.comboBox_1, 4, 1, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_2, 5, 1, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_3, 4, 2, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_4, 5, 2, 1, 1)
        Scatter_plot_layout.addWidget(self.comboBox_ch_select, 4, 5, 1, 1)

        self.GateVoltage_x = QtWidgets.QLineEdit('0')
        Scatter_plot_layout.addWidget(self.GateVoltage_x, 4, 3, 1, 1)
        self.GateVoltage_y = QtWidgets.QLineEdit('0')
        Scatter_plot_layout.addWidget(self.GateVoltage_y, 5, 3, 1, 1)

        self.line_Scatter_plot = QtWidgets.QFrame()
        self.line_Scatter_plot.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Scatter_plot.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_Scatter_plot, 6, 0, 1, 7)

        self.line_ch_select = QtWidgets.QFrame()
        self.line_ch_select.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_ch_select.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_ch_select, 3, 4, 3, 1)

        ######## Multi_peaks_layout grid

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

        # adding the channel name in a loop
        self.label_num_peak_list = []
        for channel_name in self.CHANNEL_NAME:
            self.label_num_peak_list.append(QtWidgets.QLabel(channel_name))

        Multi_peaks_layout.addWidget(self.label_num_peak_1, 1, 0)
        Multi_peaks_layout.addWidget(self.label_num_peak_2, 1, 1)
        Multi_peaks_layout.addWidget(self.label_num_peak_3, 1, 2)

        # add all the labels using loop
        for i, ch in enumerate(self.label_num_peak_list):
            Multi_peaks_layout.addWidget(ch, i+2, 0)

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

        self.comboBox_peak_num_5 = QtWidgets.QComboBox()
        self.comboBox_peak_num_5.addItem(">=")
        self.comboBox_peak_num_5.addItem("==")
        self.comboBox_peak_num_5.addItem("<=")

        self.comboBox_peak_num_6 = QtWidgets.QComboBox()
        self.comboBox_peak_num_6.addItem(">=")
        self.comboBox_peak_num_6.addItem("==")
        self.comboBox_peak_num_6.addItem("<=")

        Multi_peaks_layout.addWidget(self.comboBox_peak_num_1, 2, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_2, 3, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_3, 4, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_4, 5, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_5, 6, 1)
        Multi_peaks_layout.addWidget(self.comboBox_peak_num_6, 7, 1)

        self.lineEdit_peak_num_1 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_2 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_3 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_4 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_5 = QtWidgets.QLineEdit('0')
        self.lineEdit_peak_num_6 = QtWidgets.QLineEdit('0')

        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_1, 2, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_2, 3, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_3, 4, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_4, 5, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_5, 6, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_6, 7, 2, 1, 1)

        self.line_Multi_peaks = QtWidgets.QFrame()
        self.line_Multi_peaks.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Multi_peaks.setFrameShadow(QtWidgets.QFrame.Sunken)
        Multi_peaks_layout.addWidget(self.line_Multi_peaks, 8, 0, 1, 3)

        ######## Multi peak end

        self.label_dots_inside_polygon = QLabel("Inside : 0")
        sizePolicy.setHeightForWidth(self.label_dots_inside_polygon.sizePolicy().hasHeightForWidth())
        self.label_dots_inside_polygon.setSizePolicy(sizePolicy)
        #         self.label_8.setMinimumSize(QtCore.QSize(80, 0))
        #         self.label_8.setMaximumSize(QtCore.QSize(100, 16777215))
        #         self.label_8.setObjectName("label_8")
        layout.addWidget(self.label_dots_inside_polygon, 9, 0, 1, 1)

        self.polygon_button_1 = QPushButton('Polygon')
        self.polygon_button_2 = QPushButton('Clear')
        self.polygon_button_3 = QPushButton('Shape Edit')

        #         self.button_rename.setSizePolicy(sizePolicy)

        layout.addWidget(self.polygon_button_1, 10, 0, 1, 1)
        layout.addWidget(self.polygon_button_2, 10, 1, 1, 1)
        layout.addWidget(self.polygon_button_3, 10, 2, 1, 1)

        # confirm buttons

        self.pushButton_confirm = QPushButton('Update')
        layout.addWidget(self.pushButton_confirm, 8, 0, 1, 1)

        # density label
        self.label_density = QLabel("Plot Density")
        layout.addWidget(self.label_density, 8, 1, 1, 1)
        self.density_line_edit = QtWidgets.QDoubleSpinBox()
        self.density_line_edit.setValue(0.1)
        layout.addWidget(self.density_line_edit, 8, 2, 1, 1)

        self.pushButton_1 = QPushButton('Next Filter')
        self.pushButton_2 = QPushButton('Stats')
        self.pushButton_3 = QPushButton('Linear Plot')

        layout.addWidget(self.pushButton_1, 11, 0, 1, 1)
        layout.addWidget(self.pushButton_2, 11, 1, 1, 1)
        layout.addWidget(self.pushButton_3, 11, 2, 1, 1)

        self.pushButton_4 = QPushButton('Export to Sweep1')
        layout.addWidget(self.pushButton_4, 12, 0, 1, 1)
        self.pushButton_5 = QPushButton('Export to Sweep2')
        layout.addWidget(self.pushButton_5, 12, 1, 1, 1)

        self.pushButton_timelog = QPushButton('Export Time Log')
        layout.addWidget(self.pushButton_timelog, 12, 2, 1, 1)

        ### Quadrants table

        self.tableView_scatterquadrants = QtWidgets.QTableWidget()
        #         self.tableView_scatterquadrants.setObjectName("tableView_scatterquadrants")
        self.tableView_scatterquadrants.setMinimumSize(QtCore.QSize(500, 80))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_scatterquadrants.sizePolicy().hasHeightForWidth())
        self.tableView_scatterquadrants.setSizePolicy(sizePolicy)
        self.tableView_scatterquadrants.setSizePolicy(sizePolicy)

        layout.addWidget(self.tableView_scatterquadrants, 13, 0, 1, 4)

        # set row count
        self.tableView_scatterquadrants.setRowCount(4)
        # set column count
        self.tableView_scatterquadrants.setColumnCount(7)
        self.tableView_scatterquadrants.setHorizontalHeaderLabels(
            ('Count', '% Total Peaks', '% Total Droplets', 'X Single Peak %',
             'Y Single Peak %', 'X Multi Peak %', 'Y Multi Peak %'))
        self.tableView_scatterquadrants.setVerticalHeaderLabels(
            ('Top Right', 'Top Left', 'Bottom Left', 'Bottom Right'))

        self.tableView_scatterquadrants.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #         self.tableView_scatterquadrants.verticalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        ### graph
        self.graphWidget = PlotWidget(title=' ')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setMinimumSize(QtCore.QSize(500, 500))
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Green')
        self.graphWidget.setLabel('bottom', 'Far Red')
        self.graphWidget.disableAutoRange()

        # plot setting

        self.graphWidget.getAxis('left').setPen(self.axis_pen)
        self.graphWidget.getAxis('left').setTextPen(self.axis_pen)
        self.graphWidget.getAxis('left').setStyle(tickFont=self.axis_font)
        self.graphWidget.getAxis('bottom').setPen(self.axis_pen)
        self.graphWidget.getAxis('bottom').setTextPen(self.axis_pen)
        self.graphWidget.getAxis('bottom').setStyle(tickFont=self.axis_font)

        # add threshold
        pen = pg.mkPen(color='r', width=5, style=QtCore.Qt.DashLine)
        self.lr_x_axis = pg.InfiniteLine(0, movable=True, pen=pen)
        self.graphWidget.addItem(self.lr_x_axis)
        self.lr_y_axis = pg.InfiniteLine(0, movable=True, pen=pen, angle=0)
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
        self.tab_widgets_main.addTab(self.tab_1, 'Scatter Plot')

        Scatter_layout = QtWidgets.QHBoxLayout(self.tab_1)
        Scatter_layout.addWidget(self.graphWidget)

        self.v_line_scatter = QtWidgets.QFrame(self.tab_1)
        self.v_line_scatter.setFrameShape(QtWidgets.QFrame.VLine)
        self.v_line_scatter.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_layout.addWidget(self.v_line_scatter)

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
        self.pushButton_2.clicked.connect(self.stats_clicked)
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
        self.histogram_comboBox_1.addItem("Ratio")

        # adding all the channel names using a loop
        self.histogram_comboBox_2 = QtWidgets.QComboBox()
        for channel_name in self.CHANNEL_NAME:
            self.histogram_comboBox_2.addItem(channel_name)

        # adding all the channel names using a loop
        self.histogram_comboBox_3 = QtWidgets.QComboBox()
        for channel_name in self.CHANNEL_NAME:
            self.histogram_comboBox_3.addItem(channel_name)

        self.histogram_label_1 = QtWidgets.QLabel("Mode: ")
        self.histogram_label_2 = QtWidgets.QLabel("Channel: ")
        self.histogram_label_3 = QtWidgets.QLabel("Channel: ")

        control_sub_layout = QtWidgets.QGridLayout()
        control_sub_layout.addWidget(self.histogram_comboBox_2, 0, 1, 1, 1)
        control_sub_layout.addWidget(self.histogram_comboBox_3, 1, 1, 1, 1)
        control_sub_layout.addWidget(self.histogram_label_2, 0, 0, 1, 1)
        control_sub_layout.addWidget(self.histogram_label_3, 1, 0, 1, 1)

        Control_layout.addWidget(self.histogram_label_1, 0, 0, 1, 1)

        Control_layout.addWidget(self.histogram_comboBox_1, 0, 1, 1, 1)

        Control_layout.addLayout(control_sub_layout, 1, 0, 2, 2)
        self.histogram_comboBox_3.hide()
        self.histogram_label_3.hide()

        self.line_histo_2 = QtWidgets.QFrame(self.tab_2)
        self.line_histo_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_histo_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        Control_layout.addWidget(self.line_histo_2, 2, 0, 1, 2)

        # graph parameters adjust
        self.label_bin_width = QLabel("Binwidth")
        Control_layout.addWidget(self.label_bin_width, 3, 0, 1, 1)

        self.histogram_binwidth = QtWidgets.QLineEdit('0.1')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram_binwidth.sizePolicy().hasHeightForWidth())
        self.histogram_binwidth.setSizePolicy(sizePolicy)

        Control_layout.addWidget(self.histogram_binwidth, 3, 1, 1, 1)

        # gate voltage
        self.label_gate_voltage = QLabel("Gate Voltage")
        Control_layout.addWidget(self.label_gate_voltage, 4, 0, 1, 1)

        self.histogram_gate_voltage = QtWidgets.QLineEdit('0')
        self.histogram_gate_voltage.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.histogram_gate_voltage, 4, 1, 1, 1)
        self.histogram_gate_voltage.editingFinished.connect(self.histo_text_changed)

        self.line_histo_3 = QtWidgets.QFrame(self.tab_2)
        self.line_histo_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_histo_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        Control_layout.addWidget(self.line_histo_3, 5, 0, 1, 2)

        self.label_histo_mean = QLabel("Mean:   ")
        self.label_histo_mean.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_histo_mean, 6, 0, 1, 2)

        self.label_histo_std = QLabel("Standard Deviation:   ")
        self.label_histo_std.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_histo_std, 7, 0, 1, 2)

        # percentage
        self.label_percentage = QLabel("Percentage (Total Peaks):   %")
        self.label_percentage.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_percentage, 8, 0, 1, 2)

        self.label_percentage_all = QLabel("Percentage (Total Droplets):   %")
        self.label_percentage_all.setSizePolicy(sizePolicy)
        Control_layout.addWidget(self.label_percentage_all, 9, 0, 1, 2)

        self.line_histo_4 = QtWidgets.QFrame(self.tab_2)
        self.line_histo_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_histo_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        Control_layout.addWidget(self.line_histo_4, 10, 0, 1, 2)

        # buttons
        self.histogram_pushButton_1 = QPushButton('Update')

        Control_layout.addWidget(self.histogram_pushButton_1, 11, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(5, 400, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        Control_layout.addItem(spacerItem, 12, 0, 1, 1)
        # Finish layouts

        pen = pg.mkPen(color='r', width=5, style=QtCore.Qt.DashLine)
        self.histo_threshold_line = pg.InfiniteLine(0, movable=True, pen=pen)
        self.histogram_graphWidget.addItem(self.histo_threshold_line)
        self.histo_threshold_line.sigPositionChangeFinished.connect(self.histo_line_moved)

        Histogram_layout = QtWidgets.QHBoxLayout(self.tab_2)
        Histogram_layout.addWidget(self.histogram_graphWidget)

        self.line_histo = QtWidgets.QFrame(self.tab_2)
        self.line_histo.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_histo.setFrameShadow(QtWidgets.QFrame.Sunken)
        Histogram_layout.addWidget(self.line_histo)

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
        self.polygon_channel_5 = QtWidgets.QCheckBox("Channel_5")
        self.polygon_channel_6 = QtWidgets.QCheckBox("Channel_6")

        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_1)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_2)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_3)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_4)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_5)
        self.layout_vertical_checkbox_3.addWidget(self.polygon_channel_6)

        self.polygon_channel_1.setChecked(True)
        self.polygon_channel_2.setChecked(True)
        self.polygon_channel_3.setChecked(True)
        self.polygon_channel_4.setChecked(True)
        self.polygon_channel_5.setChecked(True)
        self.polygon_channel_6.setChecked(True)

        self.gridLayout_42.addItem(self.layout_vertical_checkbox_3, 14, 0, 1, 2)

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

        self.label_plot_options = QtWidgets.QLabel("Plot Options")
        self.label_plot_options.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_plot_options, 19, 0, 1, 2)

        self.label_line_thickness = QtWidgets.QLabel("Line Thickness")
        self.label_line_thickness.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_line_thickness, 20, 0, 1, 1)

        self.lineEdit_line_thickness = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_line_thickness.sizePolicy().hasHeightForWidth())
        self.lineEdit_line_thickness.setSizePolicy(sizePolicy)
        self.lineEdit_line_thickness.setObjectName("lineEdit_line_thickness")
        self.lineEdit_line_thickness.setText("3")
        line_thickness_valid = QtGui.QIntValidator(1, 40, self)
        self.lineEdit_line_thickness.setValidator(line_thickness_valid)
        self.gridLayout_42.addWidget(self.lineEdit_line_thickness, 20, 1, 1, 1)
        self.lineEdit_line_thickness.editingFinished.connect(self.update_fonts)

        self.label_legend_font = QtWidgets.QLabel("Legend Font")
        self.label_legend_font.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_legend_font, 21, 0, 1, 1)

        self.lineEdit_legend_font = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_legend_font.sizePolicy().hasHeightForWidth())
        self.lineEdit_legend_font.setSizePolicy(sizePolicy)
        self.lineEdit_legend_font.setObjectName("lineEdit_legend_font")
        self.lineEdit_legend_font.setText("12")
        legend_font_valid = QtGui.QIntValidator(1, 40, self)
        self.lineEdit_legend_font.setValidator(legend_font_valid)
        self.gridLayout_42.addWidget(self.lineEdit_legend_font, 21, 1, 1, 1)
        self.lineEdit_legend_font.editingFinished.connect(self.update_fonts)

        self.label_axis_thickness = QtWidgets.QLabel("Axis Thickness")
        self.label_axis_thickness.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_axis_thickness, 22, 0, 1, 1)

        self.lineEdit_axis_thickness = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_axis_thickness.sizePolicy().hasHeightForWidth())
        self.lineEdit_axis_thickness.setSizePolicy(sizePolicy)
        self.lineEdit_axis_thickness.setObjectName("lineEdit_axis_thickness")
        self.lineEdit_axis_thickness.setText("3")
        axis_thickness_valid = QtGui.QIntValidator(1, 40, self)
        self.lineEdit_axis_thickness.setValidator(axis_thickness_valid)
        self.gridLayout_42.addWidget(self.lineEdit_axis_thickness, 22, 1, 1, 1)
        self.lineEdit_axis_thickness.editingFinished.connect(self.update_fonts)

        self.label_axis_font = QtWidgets.QLabel("Axis Font")
        self.label_axis_font.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_42.addWidget(self.label_axis_font, 23, 0, 1, 1)

        self.lineEdit_axis_font = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_axis_font.sizePolicy().hasHeightForWidth())
        self.lineEdit_axis_font.setSizePolicy(sizePolicy)
        self.lineEdit_axis_font.setObjectName("lineEdit_axis_font")
        self.lineEdit_axis_font.setText("12")
        axis_font_valid = QtGui.QIntValidator(1, 40, self)
        self.lineEdit_axis_font.setValidator(axis_font_valid)
        self.gridLayout_42.addWidget(self.lineEdit_axis_font, 23, 1, 1, 1)
        self.lineEdit_axis_font.editingFinished.connect(self.update_fonts)

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

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
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
        self.widget_29.getAxis('left').setPen(self.axis_pen)
        self.widget_29.getAxis('left').setTextPen(self.axis_pen)
        self.widget_29.getAxis('left').setStyle(tickFont=self.axis_font)
        self.widget_29.getAxis('bottom').setPen(self.axis_pen)
        self.widget_29.getAxis('bottom').setTextPen(self.axis_pen)
        self.widget_29.getAxis('bottom').setStyle(tickFont=self.axis_font)

        # triggers
        self.pushButton_6.clicked.connect(self.polygon_reset_linear_plot)
        self.pushButton_8.clicked.connect(self.polygon_last_page)
        self.pushButton_7.clicked.connect(self.polygon_next_page)
        self.pushButton_timelog.clicked.connect(self.time_log_clicked)
        self.button_channel_select.clicked.connect(self.channel_select_clicked)

        self.graphWidget.sigRangeChanged.connect(self.quadrant_rect_resize)

        ##########################################################################################

    def update_fonts(self):
        print("update fonts")
        if self.lineEdit_line_thickness.hasAcceptableInput():
            self.line_thickness = int(self.lineEdit_line_thickness.text())

        if self.lineEdit_axis_font.hasAcceptableInput():
            self.axis_font_size = int(self.lineEdit_axis_font.text())
            self.axis_font.setPointSize(self.axis_font_size)
            self.widget_29.getAxis('left').setStyle(tickFont=self.axis_font)
            self.widget_29.getAxis('bottom').setStyle(tickFont=self.axis_font)
            self.graphWidget.getAxis('left').setStyle(tickFont=self.axis_font)
            self.graphWidget.getAxis('bottom').setStyle(tickFont=self.axis_font)

        if self.lineEdit_legend_font.hasAcceptableInput():
            self.legend_font_size = self.lineEdit_legend_font.text()

        if self.lineEdit_axis_thickness.hasAcceptableInput():
            self.axis_thickness = int(self.lineEdit_axis_thickness.text())
            self.axis_pen = pg.mkPen(QColor(0, 0, 0), width=self.axis_thickness)
            self.widget_29.getAxis('left').setPen(self.axis_pen)
            self.widget_29.getAxis('left').setTextPen(self.axis_pen)
            self.widget_29.getAxis('bottom').setPen(self.axis_pen)
            self.widget_29.getAxis('bottom').setTextPen(self.axis_pen)
            self.graphWidget.getAxis('left').setPen(self.axis_pen)
            self.graphWidget.getAxis('left').setTextPen(self.axis_pen)
            self.graphWidget.getAxis('bottom').setPen(self.axis_pen)
            self.graphWidget.getAxis('bottom').setTextPen(self.axis_pen)

    # update the left and right sweep graphs on the sweep tab
    def update_sweep_left(self):
        self.ui.sweep_left = [[], [], [], []]
        for ch in range(len(self.working_data)):
            self.ui.sweep_left[ch] = [self.working_data[ch][i] for i in self.points_inside]
        self.ui.update_sweep_1(data_updated=True)

    def update_sweep_right(self):
        self.ui.sweep_right = [[], [], [], []]
        for ch in range(len(self.working_data)):
            self.ui.sweep_right[ch] = [self.working_data[ch][i] for i in self.points_inside]
        self.ui.update_sweep_2(data_updated=True)

    # two ways to trigger the linear plot:
    # 1. from the linear plot tab, "generate plot" button, (more like a "reset" button)
    # 2. from main filter tab, "export leaner plot button"
    # This is the trigger 2 from the main filter tab

    def channel_list_update(self, linear_plot_channel_list=None):
        """function call to update the channel list used for linear plot"""
        if linear_plot_channel_list is not None:
            self.linear_plot_channel_list = linear_plot_channel_list
        else:
            self.linear_plot_channel_list = {}
            if self.comboBox_ch_select.currentIndex() == 0:
                """case for droplet file"""
                if self.current_file_dict['Droplet Record'] != '':
                    self.linear_plot_channel_list[len(self.linear_plot_channel_list)] = "Droplet Record"
            elif self.comboBox_ch_select.currentIndex() == 1:
                """case for sorted positive file"""
                if self.current_file_dict['Peak Record'] != '':
                    self.linear_plot_channel_list[len(self.linear_plot_channel_list)] = "Peak Record"
            elif self.comboBox_ch_select.currentIndex() == 2:
                """case for all positive file"""
                if self.current_file_dict['Peak Record'] != '':
                    self.linear_plot_channel_list[len(self.linear_plot_channel_list)] = "Peak Record"
                if self.current_file_dict['Locked Out Peaks'] != '':
                    self.linear_plot_channel_list[len(self.linear_plot_channel_list)] = "Locked Out Peaks"
            else:
                """case for locked out file"""
                if self.current_file_dict['Locked Out Peaks'] != '':
                    self.linear_plot_channel_list[len(self.linear_plot_channel_list)] = "Locked Out Peaks"

    def tree_index_update(self, new_index):
        """update index function call, usually called after a filter was removed to update the dict"""
        self.tree_index = new_index

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
            self.index_in_all_selected_channel = []
            if not self.multi_file:
                multi_file_holder = [0]
            else:
                multi_file_holder = self.multi_file
            for file in multi_file_holder:
                if len(multi_file_holder) > 1:
                    self.current_file_dict = self.ui.file_dict_list[file]
                for list_index in self.linear_plot_channel_list:
                    list_text = self.linear_plot_channel_list[list_index]
                    polygon_length = 0
                    for i in range(list_index):
                        polygon_length += len(
                            self.ui.analog[self.current_file_dict[self.linear_plot_channel_list[i]]][0][0])

                    polygon_length_end = polygon_length + len(self.ui.analog[self.current_file_dict[list_text]][0][0])
                    if list_index >= len(self.index_in_all_selected_channel) or len(multi_file_holder) == 1:
                        # if first file, append to list , and add channel is not empty
                        self.index_in_all_selected_channel.append([x for x, x in enumerate(self.points_inside) if
                                                                   polygon_length < x <= polygon_length_end])
                    else:
                        self.index_in_all_selected_channel[list_index].extend(
                            [x for x, x in enumerate(self.points_inside)
                             if polygon_length < x <= polygon_length_end])
            # cycle the list again to sort and populate the combo box
            for list_index in self.linear_plot_channel_list:
                if self.index_in_all_selected_channel[list_index]:
                    self.index_in_all_selected_channel[list_index].sort()
                    self.comboBox_14.addItem(str(self.linear_plot_channel_list[list_index]))

        self.reset_comboBox = False

        key_list = list(self.linear_plot_channel_list.keys())
        val_list = list(self.linear_plot_channel_list.values())

        position = val_list.index(self.comboBox_14.currentText())
        polygon_index = key_list[position]
        polygon_text = self.comboBox_14.currentText()

        polygon_length = 0

        for i in range(polygon_index):
            polygon_length += len(self.ui.analog[self.current_file_dict[self.linear_plot_channel_list[i]]][0][0])

        polygon_length_end = polygon_length + len(self.ui.analog[self.current_file_dict[polygon_text]][0][0])

        ### trace end

        # get the points after filtering
        index_in_current_channel = [x - polygon_length for x in self.index_in_all_selected_channel[polygon_index]]

        ### find data in csv file
        text1 = self.comboBox_14.currentText()
        header = 0

        # custom sample size in linear tab, allow user to switch sample size in the filter tab
        try:
            if int(self.lineEdit_37.text()) > 0:
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
            if len(index_in_current_channel) < upper_bond:
                upper_bond = len(index_in_current_channel)
                self.lineEdit_38.setText(str(upper_bond))
            nrows = upper_bond - lower_bond

            if nrows > 15:
                self.lineEdit_38.setText(str(lower_bond + 15))
                nrows = 15

            self.subgating_file_dict = self.ui.file_dict_list[self.tree_index[len(self.tree_index) - 1]]
            os.chdir(self.subgating_file_dict["Root Folder"])
            file = self.subgating_file_dict[text1]

            data = pd.DataFrame({0: [], 1: [], 2: [], 3: []}, )

            # print("index_in_current_channel", len(index_in_current_channel), ':', index_in_current_channel)

            for x in range(lower_bond, upper_bond):
                current_droplet_index = index_in_current_channel[x]
                file_droplet_index = current_droplet_index
                if self.multi_file:
                    for count, index in enumerate(self.multi_file_index):
                        if current_droplet_index > index:
                            self.subgating_file_dict = self.ui.file_dict_list[self.multi_file[count]]
                            os.chdir(self.subgating_file_dict["Root Folder"])
                            file = self.subgating_file_dict[text1]
                            file_droplet_index -= index
                        else:
                            break

                skip_rows = file_droplet_index * sample_size
                polygon_data = pd.read_csv(file, skiprows=skip_rows, nrows=sample_size, header=header)
                length = len(polygon_data.columns)
                polygon_data.columns = list(range(0, length))
                data = pd.concat([data, polygon_data])
            if sample_size == 1000:
                print("Graph will be undersampled to 200")
                data = data.iloc[::5, :]

            height_data = data[0].values.tolist()
            height_index = list(range(len(height_data)))
            height_index = [i / 100 for i in height_index]

            poly_degree = int(self.lineEdit_39.text())
            window_length = int(self.lineEdit_40.text()) // 2 * 2 - 1

            self.widget_29.addLegend()
            self.widget_29.plotItem.legend.setLabelTextColor(QColor(0, 0, 0))
            self.widget_29.plotItem.legend.setLabelTextSize(str(self.legend_font_size) + 'pt')

            self.plot_width = self.line_thickness

            for i in range(0, 2 * nrows, 2):
                self.widget_29.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))

            if self.polygon_Smooth_enable.isChecked():
                if self.polygon_channel_1.isChecked():
                    height_data = savgol_filter(data[0], window_length, poly_degree)
                    pen = pg.mkPen(color=(83, 229, 29), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='ZsGreen', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    height_data = savgol_filter(data[1], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 17, 47), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='E2-Crimson', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    height_data = savgol_filter(data[2], window_length, poly_degree)
                    pen = pg.mkPen(color=(48, 131, 240), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='CellTrace Violet', pen=pen, symbol='o',
                                        symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_5.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='Channel_5', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_6.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, height_data, name='Channel_6', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
            else:
                if self.polygon_channel_1.isChecked():
                    pen = pg.mkPen(color=(83, 229, 29), width=self.plot_width)
                    self.widget_29.plot(height_index, data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    pen = pg.mkPen(color=(238, 17, 47), width=self.plot_width)
                    self.widget_29.plot(height_index, data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    pen = pg.mkPen(color=(48, 131, 240), width=self.plot_width)
                    self.widget_29.plot(height_index, data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_5.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, data[3].values.tolist(), name='Channel_5', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_6.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=self.plot_width)
                    self.widget_29.plot(height_index, data[3].values.tolist(), name='Channel_6', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
        else:
            print("Enter a new lower bond value")

        self.widget_29.autoRange()

        # histogram tab main function

    def histo_line_moved(self):
        """connect when histo line move"""
        threshold = round(self.histo_threshold_line.value(), 3)
        self.histogram_gate_voltage.setText(str(threshold))
        self.update_histo_threshold(threshold)

    def histo_text_changed(self):
        """connect when histo gate voltage text change"""
        threshold = round(float(self.histogram_gate_voltage.text()), 3)
        self.histo_threshold_line.setValue(threshold)
        self.update_histo_threshold(threshold)

    def update_histo_threshold(self, threshold):
        """this funciton handles when the threshold of the histogram changes from the line"""

        self.width = [x for x in self.full_width if x >= float(threshold)]

        width_count_filtered = round(100 * len(self.width) / len(self.full_width), 2)
        width_count = "" + str(width_count_filtered) + '% of filtered points ' + str(
            len(self.width)) + '/' + str(len(self.full_width))
        self.label_percentage.setText(width_count)

        percentage_all_count = round(100 * len(self.width) / len(self.working_data[0]), 2)
        percentage_all = "" + str(percentage_all_count) + '% of all points ' + str(
            len(self.width)) + '/' + str(len(self.working_data[0]))
        self.label_percentage_all.setText(percentage_all)

        histo_mean = round(np.mean(self.width), 3)
        histo_mean_string = "Mean:   " + str(histo_mean)
        self.label_histo_mean.setText(histo_mean_string)

        histo_stdev = round(np.std(self.width), 3)
        histo_stdev_string = "Standard Deviation:   " + str(histo_stdev)
        self.label_histo_std.setText(histo_stdev_string)

    def draw_histogram(self):
        try:
            points_inside_square = self.points_inside_square
        except:
            self.draw_graphwidget()

        if self.histogram_comboBox_1.currentIndex() == 0:
            self.width = self.working_data[self.histogram_comboBox_2.currentIndex()]
        elif self.histogram_comboBox_1.currentIndex() == 1:
            self.width = self.peak_width_working_data[self.histogram_comboBox_2.currentIndex()]
        else:
            self.width = self.extracted_ratio_data

        self.full_width = [self.width[i] for i in self.points_inside_square]

        self.width = [x for x in self.full_width if x >= float(self.histogram_gate_voltage.text())]

        width_count_filtered = round(100 * len(self.width) / len(self.full_width), 2)
        width_count = "" + str(width_count_filtered) + '% of filtered points ' + str(
            len(self.width)) + '/' + str(len(self.full_width))
        self.label_percentage.setText(width_count)

        percentage_all_count = round(100 * len(self.width) / len(self.working_data[0]), 2)
        percentage_all = "" + str(percentage_all_count) + '% of all points ' + str(
            len(self.width)) + '/' + str(len(self.working_data[0]))
        self.label_percentage_all.setText(percentage_all)

        histo_mean = round(np.mean(self.width), 3)
        histo_mean_string = "Mean:   " + str(histo_mean)
        self.label_histo_mean.setText(histo_mean_string)

        histo_stdev = round(np.std(self.width), 3)
        histo_stdev_string = "Standard Deviation:   " + str(histo_stdev)
        self.label_histo_std.setText(histo_stdev_string)

        channel = self.histogram_comboBox_2.currentIndex()

        self.histogram_graphWidget.clear()
        r, g, b = Helper.rgb_select(channel)
        styles = {"color": "r", "font-size": "20px"}
        axis_name = self.histogram_comboBox_2.currentText()
        self.histogram_graphWidget.addItem(self.histo_threshold_line)
        self.histogram_graphWidget.setLabel('bottom', axis_name, **styles)

        range_width = int(max(self.full_width)) + 1
        # test binwidth
        bin_edge = Helper.histogram_bin(range_width, float(self.histogram_binwidth.text()))
        y, x = np.histogram(self.full_width, bins=bin_edge)
        separate_y = [0] * len(y)

        for i in range(len(y)):
            separate_y = [0] * len(y)
            separate_y[i] = y[i]
            self.histogram_graphWidget.plot(x, separate_y, stepMode=True, fillLevel=0, fillOutline=True,
                                            brush=(r, g, b))

        self.histogram_graphWidget.setXRange(float(self.histogram_gate_voltage.text()), max(x), padding=0)
        self.histogram_graphWidget.setYRange(0, max(y), padding=0)

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
        holder = [[], [], [], []]
        for ch in range(6):
            holder[ch] = [i for i, x in enumerate(self.peak_num_working_data[ch])
                          if self.peak_num_comp(x, self.peak_num_mode[ch], self.peak_num_in[ch])]
        self.peak_num_filtered_index = list(set(holder[0]).intersection(set(holder[1]), set(holder[2]), set(holder[3])))
        # print('holder[0]', holder[0])
        # print('self.peak_num_filtered_index', self.peak_num_filtered_index)

    ### drawing function for main tab scatter pot

    def draw_graphwidget(self):
        # "update" clicked
        # prepare data
        start = time.time()
        if len(self.tree_index) == 1:
            # this is for root data extraction

            self.peak_width_working_data = []
            self.peak_num_working_data = []
            self.working_data = []
            self.peak_time_working_data = []
            self.extracted_ratio_data = []

            for i in range(6):
                self.working_data.append([])
                self.peak_width_working_data.append([])
                self.peak_num_working_data.append([])

            if self.multi_file is None:
                """if file is single"""
                if len(self.tree_index) > 1 or self.ui.extraction_thread_state[self.root] is ThreadState.FINISHED:
                    self.peak_width_working_data = []
                    self.peak_num_working_data = []
                    self.working_data = []
                    self.peak_time_working_data = []

                    for i in range(6):
                        self.working_data.append([])
                        self.peak_width_working_data.append([])
                        self.peak_num_working_data.append([])

                    if self.legacy_mode:
                        if self.ch_select.checkbox_ch1.isChecked() and self.current_file_dict[
                            'Ch1 '] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1 ']][3]
                        if self.ch_select.checkbox_ch2.isChecked() and self.current_file_dict[
                            'Ch2 '] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch2 ']][3]
                        if self.ch_select.checkbox_ch3.isChecked() and self.current_file_dict[
                            'Ch3 '] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch3 ']][3]
                        if self.ch_select.checkbox_ch12.isChecked() and self.current_file_dict[
                            'Ch1-2'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1-2']][3]
                        if self.ch_select.checkbox_ch13.isChecked() and self.current_file_dict[
                            'Ch1-3'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1-3']][3]
                        if self.ch_select.checkbox_ch23.isChecked() and self.current_file_dict[
                            'Ch2-3'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][0][i]
                                self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][1][i]
                                self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch2-3']][3]
                        if self.ch_select.checkbox_Droplet_Record.isChecked() and self.current_file_dict[
                            'Droplet Record'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][0][i]
                                self.peak_width_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Droplet Record']][1][i]
                                self.peak_num_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Droplet Record']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Droplet Record']][3]
                        if self.ch_select.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict[
                            'Locked Out Peaks'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                self.peak_num_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][
                                    i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]
                        if self.ch_select.checkBox_7.isChecked() and self.current_file_dict[
                            'Peak Record'] in self.ui.analog.keys():
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                self.peak_width_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                                self.peak_num_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]
                        if len(self.peak_width_working_data) == 0:
                            for i in range(6):
                                self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                self.peak_width_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                                self.peak_num_working_data[i] += \
                                self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                            self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]
                        points_inside_square = [i for i in range(len(self.working_data[0]))]

                    else:
                        if self.comboBox_ch_select.currentIndex() == 0:
                            if self.current_file_dict['Droplet Record'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][0][
                                        i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Droplet Record']][1][
                                        i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Droplet Record']][2][i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Droplet Record']][
                                    3]
                                self.extracted_ratio_data += self.ui.analog[self.current_file_dict['Droplet Record']][4]
                            points_inside_square = [i for i in range(len(self.working_data[0]))]
                        elif self.comboBox_ch_select.currentIndex() == 1:
                            """Case for positive sorted droplet"""
                            if self.current_file_dict['Peak Record'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]
                                self.extracted_ratio_data += self.ui.analog[self.current_file_dict['Droplet Record']][4]
                            points_inside_square = [i for i in range(len(self.working_data[0]))]

                        elif self.comboBox_ch_select.currentIndex() == 2:
                            if self.current_file_dict['Peak Record'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]
                                self.extracted_ratio_data += self.ui.analog[self.current_file_dict['Droplet Record']][4]
                            if self.current_file_dict['Locked Out Peaks'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                    self.peak_width_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][
                                        i]
                                self.peak_time_working_data += \
                                self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]
                                self.extracted_ratio_data += self.ui.analog[self.current_file_dict['Droplet Record']][4]
                            points_inside_square = [i for i in range(len(self.working_data[0]))]

                        elif self.comboBox_ch_select.currentIndex() == 3:
                            if self.current_file_dict['Locked Out Peaks'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                    self.peak_width_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][
                                        i]
                                self.peak_time_working_data += \
                                self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]
                                self.extracted_ratio_data += self.ui.analog[self.current_file_dict['Droplet Record']][4]
                            points_inside_square = [i for i in range(len(self.working_data[0]))]
                        self.channel_list_update()
                else:
                    show_dialog("File not extracted or out of date, please extract file and try again.", "Error")
                    return False

            else:
                """case for multiple file"""
                # check all the files and see if extraction finished
                file_ready_list = [self.ui.extraction_thread_state[x] == ThreadState.FINISHED for x in self.multi_file]
                if False not in file_ready_list:

                    self.peak_width_working_data = []
                    self.peak_num_working_data = []
                    self.working_data = []
                    self.peak_time_working_data = []

                    for i in range(6):
                        self.working_data.append([])
                        self.peak_width_working_data.append([])
                        self.peak_num_working_data.append([])

                    self.multi_file_index = []
                    file_index_holder = 0
                    for file in self.multi_file:
                        """iterate through all index and add them all to the working data."""
                        self.current_file_dict = self.ui.file_dict_list[file]
                        if self.legacy_mode:
                            if self.ch_select.checkbox_ch1.isChecked() and self.current_file_dict[
                                'Ch1 '] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch1 ']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1 ']][3]
                            if self.ch_select.checkbox_ch2.isChecked() and self.current_file_dict[
                                'Ch2 '] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch2 ']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch2 ']][3]
                            if self.ch_select.checkbox_ch3.isChecked() and self.current_file_dict[
                                'Ch3 '] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch3 ']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch3 ']][3]
                            if self.ch_select.checkbox_ch12.isChecked() and self.current_file_dict[
                                'Ch1-2'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch1-2']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1-2']][3]
                            if self.ch_select.checkbox_ch13.isChecked() and self.current_file_dict[
                                'Ch1-3'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch1-3']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch1-3']][3]
                            if self.ch_select.checkbox_ch23.isChecked() and self.current_file_dict[
                                'Ch2-3'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Ch2-3']][1][i]
                                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][2][
                                        i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Ch2-3']][3]
                            if self.ch_select.checkbox_Droplet_Record.isChecked() and self.current_file_dict[
                                'Droplet Record'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][0][
                                        i]
                                    self.peak_width_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][1][i]
                                    self.peak_num_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][2][i]
                                self.peak_time_working_data += \
                                    self.ui.analog[self.current_file_dict['Droplet Record']][3]
                            if self.ch_select.checkbox_Locked_Out_Peaks.isChecked() and self.current_file_dict[
                                'Locked Out Peaks'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                    self.peak_width_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                    self.peak_num_working_data[i] += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][i]
                                self.peak_time_working_data += \
                                    self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]

                            if self.ch_select.checkBox_7.isChecked() and self.current_file_dict[
                                'Peak Record'] in self.ui.analog.keys():
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][1][
                                        i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]

                            if len(self.peak_width_working_data) == 0:
                                for i in range(6):
                                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                    self.peak_width_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][1][
                                        i]
                                    self.peak_num_working_data[i] += \
                                    self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                self.peak_time_working_data += self.ui.analog[self.current_file_dict['Peak Record']][3]
                            points_inside_square = [i for i in range(len(self.working_data[0]))]
                            self.multi_file_index.append(file_index_holder)
                            file_index_holder = len(points_inside_square)
                        else:
                            if self.comboBox_ch_select.currentIndex() == 0:
                                """All droplet case"""
                                if self.current_file_dict['Droplet Record'] in self.ui.analog.keys():
                                    for i in range(6):
                                        self.working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Droplet Record']][0][i]
                                        self.peak_width_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Droplet Record']][1][i]
                                        self.peak_num_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Droplet Record']][2][i]
                                    self.peak_time_working_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][3]
                                    self.extracted_ratio_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][4]

                                points_inside_square = [i for i in range(len(self.working_data[0]))]
                                self.multi_file_index.append(file_index_holder)
                                file_index_holder = len(points_inside_square)
                            elif self.comboBox_ch_select.currentIndex() == 1:
                                if self.current_file_dict['Peak Record'] in self.ui.analog.keys():
                                    for i in range(6):
                                        self.working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                        self.peak_width_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][1][
                                                i]
                                        self.peak_num_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                    self.peak_time_working_data += \
                                        self.ui.analog[self.current_file_dict['Peak Record']][3]
                                    self.extracted_ratio_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][4]
                                points_inside_square = [i for i in range(len(self.working_data[0]))]
                                self.multi_file_index.append(file_index_holder)
                                file_index_holder = len(points_inside_square)
                            elif self.comboBox_ch_select.currentIndex() == 2:
                                """All Positive"""
                                if self.current_file_dict['Peak Record'] in self.ui.analog.keys():
                                    for i in range(6):
                                        self.working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                                        self.peak_width_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][1][
                                                i]
                                        self.peak_num_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Peak Record']][2][i]
                                    self.peak_time_working_data += \
                                        self.ui.analog[self.current_file_dict['Peak Record']][3]
                                    self.extracted_ratio_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][4]
                                if self.current_file_dict['Locked Out Peaks'] in self.ui.analog.keys():
                                    for i in range(6):
                                        self.working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                        self.peak_width_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                        self.peak_num_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][i]
                                    self.peak_time_working_data += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]
                                    self.extracted_ratio_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][4]
                                points_inside_square = [i for i in range(len(self.working_data[0]))]
                                self.multi_file_index.append(file_index_holder)
                                file_index_holder = len(points_inside_square)
                            elif self.comboBox_ch_select.currentIndex() == 3:
                                """Locked Positive"""
                                if self.current_file_dict['Locked Out Peaks'] in self.ui.analog.keys():
                                    for i in range(6):
                                        self.working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][0][i]
                                        self.peak_width_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][1][i]
                                        self.peak_num_working_data[i] += \
                                            self.ui.analog[self.current_file_dict['Locked Out Peaks']][2][i]
                                    self.peak_time_working_data += \
                                        self.ui.analog[self.current_file_dict['Locked Out Peaks']][3]
                                    self.extracted_ratio_data += \
                                        self.ui.analog[self.current_file_dict['Droplet Record']][4]
                                points_inside_square = [i for i in range(len(self.working_data[0]))]
                                self.multi_file_index.append(file_index_holder)
                                file_index_holder = len(points_inside_square)

                            self.channel_list_update()

                else:
                    show_dialog("Not all files extracted or up to date, please extract files and try again.", "Error")
                    return False

        else:
            points_inside_square = self.points_inside_square

        # edit filter name
        logging.info("Data collection time pt1: " + str(time.time() - start))
        start = time.time()
        # updatename to y vs.  x axis
        if self.lineedit_filter_name.text() == '':
            self_brach_name = str(self.comboBox_2.currentText() + " " + self.comboBox_4.currentText() + 'VS. ' +
                                  self.comboBox_1.currentText() + " " + self.comboBox_3.currentText())
            self.ui.tree_dic[self.tree_index]['tree_standarditem'].setText(self_brach_name)
            self.setWindowTitle(self_brach_name)
        else:
            self_brach_name = str(self.lineedit_filter_name.text())
            self.ui.tree_dic[self.tree_index]['tree_standarditem'].setText(self_brach_name)
            self.setWindowTitle(self_brach_name)

            # check peak number filter
        self.peak_num_mode = []
        self.peak_num_in = []
        self.peak_num_mode.append(self.comboBox_peak_num_1.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_2.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_3.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_4.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_5.currentIndex())
        self.peak_num_mode.append(self.comboBox_peak_num_6.currentIndex())
        self.peak_num_in.append(int(self.lineEdit_peak_num_1.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_2.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_3.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_4.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_5.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_6.text()))

        if self.peak_num_mode != [0, 0, 0, 0, 0, 0] or self.peak_num_in != [0, 0, 0, 0, 0, 0]:
            self.peak_num_filter()
            points_inside_square = list(set(points_inside_square).intersection(set(self.peak_num_filtered_index)))

        self.points_inside_square = points_inside_square
        # peak number filter end

        if self.comboBox_1.currentIndex() == 0:
            data_in_subgating_x = self.working_data[self.comboBox_3.currentIndex()]
        elif self.comboBox_1.currentIndex() == 1:
            data_in_subgating_x = self.peak_width_working_data[self.comboBox_3.currentIndex()]
        else:
            data_in_subgating_x = self.extracted_ratio_data

        if self.comboBox_2.currentIndex() == 0:
            data_in_subgating_y = self.working_data[self.comboBox_4.currentIndex()]
        elif self.comboBox_2.currentIndex() == 1:
            data_in_subgating_y = self.peak_width_working_data[self.comboBox_4.currentIndex()]
        else:
            data_in_subgating_y = self.extracted_ratio_data

        peak_num_in_subgating_x = self.peak_num_working_data[self.comboBox_3.currentIndex()]
        peak_num_in_subgating_y = self.peak_num_working_data[self.comboBox_4.currentIndex()]

        x_axis_channel = self.comboBox_3.currentIndex()
        y_axis_channel = self.comboBox_4.currentIndex()
        x_axis_name = self.comboBox_1.currentText() + " " + self.comboBox_3.currentText()
        y_axis_name = self.comboBox_2.currentText() + " " + self.comboBox_4.currentText()

        self.graphWidget.clear()
        self.graphWidget.setLabel('left', y_axis_name, color='b')
        self.graphWidget.setLabel('bottom', x_axis_name, color='b')

        self.Ch1_channel0 = [data_in_subgating_x[i] for i in self.points_inside_square]
        self.Ch1_channel0_peak_num = [peak_num_in_subgating_x[i] for i in self.points_inside_square]
        self.Ch1_channel1 = [data_in_subgating_y[i] for i in self.points_inside_square]
        self.Ch1_channel1_peak_num = [peak_num_in_subgating_y[i] for i in self.points_inside_square]

        logging.info("Data collection time pt2: " + str(time.time() - start))
        start = time.time()

        # test color setup
        max_voltage = 12
        bins = 2000
        steps = max_voltage / bins

        # all data is first sorted into a histogram
        histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins,
                                     [[0, max_voltage], [0, max_voltage]],
                                     density=False)
        max_density = histo.max()
        percentage_coefficient = self.density_line_edit.value()

        logging.info("Data plotting density generation time: " + str(time.time() - start))
        start = time.time()

        # made empty array to hold the sorted data according to density
        self.start_plot_update(steps, histo, max_density, percentage_coefficient)
        self.setEnabled(False)

        # temporary function to show the average of ratio and standard deviation
        ratio_avergae = np.mean(self.extracted_ratio_data)
        ratio_stdev = np.std(self.extracted_ratio_data)
        print(f"Mean of the Fret Ratio is: {ratio_avergae}")
        print(f"Std of the Fret Ratio is: {ratio_stdev}")

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
        """yodate the gate voltage filter"""
        single_peak_count_channel0 = [0, 0, 0, 0]
        single_peak_count_channel1 = [0, 0, 0, 0]
        multi_peak_count_channel0 = [0, 0, 0, 0]
        multi_peak_count_channel1 = [0, 0, 0, 0]
        count_quadrant = [0, 0, 0, 0]
        quadrant_values_array = []
        for i in range(4):
            quadrant_values_array.append([])

        # pass the threshold value to next window
        text_x = self.lr_x_axis.value()
        text_y = self.lr_y_axis.value()
        self.quadrant_indexs = [[], [], [], []]
        a = (np.array(self.Ch1_channel0) > text_x).tolist()
        c = (np.array(self.Ch1_channel1) > text_y).tolist()

        self.quadrant1_list = [False] * len(a)
        self.quadrant2_list = [False] * len(a)
        self.quadrant3_list = [False] * len(a)
        self.quadrant4_list = [False] * len(a)

        for i in range(len(a)):
            """determine each quadrant values"""
            if a[i] and c[i]:
                quadrant = 0
                self.quadrant1_list[i] = True
                self.quadrant_indexs[0].append(i)
            elif not a[i] and c[i]:
                quadrant = 1
                self.quadrant2_list[i] = True
                self.quadrant_indexs[1].append(i)
            elif not a[i] and not c[i]:
                quadrant = 2
                self.quadrant3_list[i] = True
                self.quadrant_indexs[2].append(i)
            else:
                quadrant = 3
                self.quadrant4_list[i] = True
                self.quadrant_indexs[3].append(i)

            count_quadrant[quadrant] += 1
            if self.Ch1_channel0_peak_num[i] == 1:
                single_peak_count_channel0[quadrant] += 1
            elif self.Ch1_channel0_peak_num[i] > 1:
                multi_peak_count_channel0[quadrant] += 1
            if self.Ch1_channel1_peak_num[i] == 1:
                single_peak_count_channel1[quadrant] += 1
            elif self.Ch1_channel1_peak_num[i] > 1:
                multi_peak_count_channel1[quadrant] += 1
        try:
            droplets = float(self.ui.lineEdit_totaldroplets.text())
        except:
            droplets = 1

        for i in range(4):

            if len(self.Ch1_channel0) != 0:
                view1 = str(round(100 * count_quadrant[i] / len(self.Ch1_channel0), 2))
                totalpercent = str(round(100 * count_quadrant[i] / droplets, 2))
                if count_quadrant[i] > 0:
                    x_single_1 = str(round(100 * single_peak_count_channel0[i] / count_quadrant[i], 2))
                    y_single_1 = str(round(100 * single_peak_count_channel1[i] / count_quadrant[i], 2))
                    x_multi_1 = str(round(100 * multi_peak_count_channel0[i] / count_quadrant[i], 2))
                    y_multi_1 = str(round(100 * multi_peak_count_channel1[i] / count_quadrant[i], 2))
                else:
                    x_single_1 = '0'
                    y_single_1 = '0'
                    x_multi_1 = '0'
                    y_multi_1 = '0'
            else:
                view1 = 0
                totalpercent = '0'
                x_single_1 = '0'
                y_single_1 = '0'
                x_multi_1 = '0'
                y_multi_1 = '0'

            self.tableView_scatterquadrants.setItem(i, 0, QTableWidgetItem(str(count_quadrant[i])))
            self.tableView_scatterquadrants.setItem(i, 1, QTableWidgetItem(view1))
            self.tableView_scatterquadrants.setItem(i, 2, QTableWidgetItem(str(totalpercent)))
            self.tableView_scatterquadrants.setItem(i, 3, QTableWidgetItem(x_single_1))
            self.tableView_scatterquadrants.setItem(i, 4, QTableWidgetItem(y_single_1))
            self.tableView_scatterquadrants.setItem(i, 5, QTableWidgetItem(x_multi_1))
            self.tableView_scatterquadrants.setItem(i, 6, QTableWidgetItem(y_multi_1))

    def quadrant_rect_click_handle(self):
        """update the quadrant rectangle when mouse is clicked, remove or add the box as needed"""
        print("redraw square")
        y_axis = self.graphWidget.getAxis('left')
        x_axis = self.graphWidget.getAxis('bottom')
        x_range = x_axis.range
        y_range = y_axis.range
        x_threshold = self.lr_x_axis.value()
        y_threshold = self.lr_y_axis.value()
        # calls the custom function
        if self.rect_trigger:
            self.graphWidget.removeItem(self.quad_rect)
            self.rect_trigger = False
            return
        self.rect_trigger = True

        if self.selected_quadrant == 0:
            if x_threshold < x_range[1] and y_threshold < y_range[1]:
                x_width = x_range[1] - x_threshold
                y_width = y_range[1] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 1:
            if x_threshold > x_range[0] and y_threshold < y_range[1]:
                x_width = x_range[0] - x_threshold
                y_width = y_range[1] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 2:
            if x_threshold > x_range[0] and y_threshold > y_range[0]:
                x_width = x_range[0] - x_threshold
                y_width = y_range[0] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 3:
            if x_threshold < x_range[1] and y_threshold > y_range[0]:
                x_width = x_range[1] - x_threshold
                y_width = y_range[0] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)

        self.quad_rect = RectQuadrant(rect_object)
        self.graphWidget.addItem(self.quad_rect)
        self.graphWidget.disableAutoRange()

    def quadrant_rect_resize(self):
        """update the quadrant rectangle"""
        print("redraw square")
        y_axis = self.graphWidget.getAxis('left')
        x_axis = self.graphWidget.getAxis('bottom')
        x_range = x_axis.range
        y_range = y_axis.range
        x_threshold = self.lr_x_axis.value()
        y_threshold = self.lr_y_axis.value()
        # calls the custom function
        if self.rect_trigger:
            self.graphWidget.removeItem(self.quad_rect)

        self.rect_trigger = True

        if self.selected_quadrant == 0:
            if x_threshold < x_range[1] and y_threshold < y_range[1]:
                x_width = x_range[1] - x_threshold
                y_width = y_range[1] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 1:
            if x_threshold > x_range[0] and y_threshold < y_range[1]:
                x_width = x_range[0] - x_threshold
                y_width = y_range[1] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 2:
            if x_threshold > x_range[0] and y_threshold > y_range[0]:
                x_width = x_range[0] - x_threshold
                y_width = y_range[0] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)
        elif self.selected_quadrant == 3:
            if x_threshold < x_range[1] and y_threshold > y_range[0]:
                x_width = x_range[1] - x_threshold
                y_width = y_range[0] - y_threshold
                rect_object = QtCore.QRectF(x_threshold, y_threshold, x_width, y_width)
            else:
                rect_object = QtCore.QRectF(x_threshold, y_threshold, 0, 0)

        self.quad_rect = RectQuadrant(rect_object)
        self.graphWidget.addItem(self.quad_rect)
        self.graphWidget.disableAutoRange()

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
                self.points = list(zip(self.Ch1_channel0, self.Ch1_channel1))
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

            start_end_dot_x = [self.x[0], self.x[-1]]
            start_end_dot_y = [self.y[0], self.y[-1]]
            self.polygon_lines[-1].append(self.graphWidget.plot(start_end_dot_x, start_end_dot_y,
                                                                pen=pg.mkPen(color=('r'), width=5,
                                                                             style=QtCore.Qt.DashLine)))
            self.polygon_points[-1].append(
                self.graphWidget.plot(start_end_dot_x, start_end_dot_y, pen=None, symbol='o'))

            # show the dots have index before the first filter
            #             self.points_inside.extend(list(compress(self.points_inside_square, self.inside2)))

            self.points_inside_list.append(list(compress(self.points_inside_square, self.inside2)))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func = lambda arr: set(arr)
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
                droplets = float(self.ui.lineEdit_totaldroplets.text())
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
            self.tableView_scatterquadrants.setItem(0, 0, QTableWidgetItem(str(len(self.points_inside))))
            self.tableView_scatterquadrants.setItem(0, 1, QTableWidgetItem(view1))
            self.tableView_scatterquadrants.setItem(0, 2, QTableWidgetItem(str(totalpercent1)))
            self.tableView_scatterquadrants.setItem(0, 3, QTableWidgetItem(x_single_1))
            self.tableView_scatterquadrants.setItem(0, 4, QTableWidgetItem(y_single_1))
            self.tableView_scatterquadrants.setItem(0, 5, QTableWidgetItem(x_multi_1))
            self.tableView_scatterquadrants.setItem(0, 6, QTableWidgetItem(y_multi_1))

    # step 2,3
    def onMouseMoved(self, point):
        """handle the mouse click event"""
        if not self.polygon_trigger and point.button() == 1:
            """this will handle the quandrant selection, where polygonal gating is off"""
            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())
            x = p.x()
            y = p.y()
            y_axis = self.graphWidget.getAxis('left')
            x_axis = self.graphWidget.getAxis('bottom')
            x_range = x_axis.range
            y_range = y_axis.range
            if x > x_range[0] and y > y_range[0]:
                """check to ensure mouse click is on plot"""
                gate_x = self.lr_x_axis.value()
                gate_y = self.lr_y_axis.value()
                print("x: " + str(x))
                print("y: " + str(y))
                x_sign = x >= gate_x
                y_sign = y >= gate_y
                if x_sign and y_sign:
                    self.selected_quadrant = 0
                elif not x_sign and y_sign:
                    self.selected_quadrant = 1
                elif not x_sign and not y_sign:
                    self.selected_quadrant = 2
                elif x_sign and not y_sign:
                    self.selected_quadrant = 3
                print("Selected Quandrant: " + str(self.selected_quadrant))
                try:
                    """output the selected qudrant to the output array"""
                    if self.selected_quadrant == 0:
                        self.points_inside = list(compress(self.points_inside_square, self.quadrant1_list))
                    elif self.selected_quadrant == 1:
                        self.points_inside = list(compress(self.points_inside_square, self.quadrant2_list))
                    elif self.selected_quadrant == 2:
                        self.points_inside = list(compress(self.points_inside_square, self.quadrant3_list))
                    elif self.selected_quadrant == 3:
                        self.points_inside = list(compress(self.points_inside_square, self.quadrant4_list))
                except:
                    self.points_inside = []
                self.quadrant_rect_click_handle()

        elif self.stop_edit_trigger and self.polygon_trigger and point.button() == 1:

            self.graphWidget.removeItem(self.quad_rect)

            p = self.graphWidget.plotItem.vb.mapSceneToView(point.scenePos())

            self.x.append(p.x())
            self.y.append(p.y())

            self.polygon_points[-1].append(
                self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)], pen=None, symbol='o'))
            self.polygon_lines[-1].append(self.graphWidget.plot(self.x[-2:len(self.x)], self.y[-2:len(self.y)],
                                                                pen=pg.mkPen(color=('r'), width=5,
                                                                             style=QtCore.Qt.DashLine)))
            self.polygon[-1].append([p.x(), p.y()])
            self.polygon_for_edit[-1].append([p.x(), p.y()])

        # some redundent functions, used to fix some error. Didn't have time to simplify
        elif self.stop_edit_trigger == False and point.button() == 1:

            self.graphWidget.removeItem(self.quad_rect)
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
                    diff_total = sqrt(diff_x * diff_x + diff_y * diff_y)
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
            self.graphWidget.removeItem(self.polygon_points[nearest_list][nearest_index + 1])
            # change points

            self.polygon_for_edit[nearest_list][nearest_index] = [p.x(), p.y()]

            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index - 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index - 1][1], p.y()]

                self.polygon_points[nearest_list][nearest_index - 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                             pen=None, symbol='o')

                edit_x = [p.x(), p.x()]
                edit_y = [p.y(), p.y()]

                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                                                                         pen=None, symbol='o')
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index - 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index - 1][1], p.y()]

                self.polygon_points[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                                                                         pen=None, symbol='o')

            if nearest_index == len(self.polygon_for_edit[nearest_list]) - 1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_points[nearest_list][nearest_index + 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                             pen=None, symbol='o')
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index + 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index + 1][1], p.y()]

                self.polygon_points[nearest_list][nearest_index + 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                             pen=None, symbol='o')

            # remove lines
            if nearest_index == 0:
                self.graphWidget.removeItem(self.polygon_lines[nearest_list][-1])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index])
            self.graphWidget.removeItem(self.polygon_lines[nearest_list][nearest_index + 1])

            # change lines
            # bug: when use in unfinished polygon, line will couse error

            if nearest_index == 0:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index - 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index - 1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index - 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                            pen=pg.mkPen(color=('b'),
                                                                                                         width=5,
                                                                                                         style=QtCore.Qt.DashLine))


            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index - 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index - 1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index] = self.graphWidget.plot(edit_x, edit_y,
                                                                                        pen=pg.mkPen(color=('b'),
                                                                                                     width=5,
                                                                                                     style=QtCore.Qt.DashLine))

            if nearest_index == len(self.polygon_for_edit[nearest_list]) - 1:
                edit_x = [self.polygon_for_edit[nearest_list][0][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][0][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index + 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                            pen=pg.mkPen(color=('b'),
                                                                                                         width=5,
                                                                                                         style=QtCore.Qt.DashLine))
            else:
                edit_x = [self.polygon_for_edit[nearest_list][nearest_index + 1][0], p.x()]
                edit_y = [self.polygon_for_edit[nearest_list][nearest_index + 1][1], p.y()]

                self.polygon_lines[nearest_list][nearest_index + 1] = self.graphWidget.plot(edit_x, edit_y,
                                                                                            pen=pg.mkPen(color=('b'),
                                                                                                         width=5,
                                                                                                         style=QtCore.Qt.DashLine))

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

            for ii in range(len(self.polygon_lines) - 1):
                for i in range(1, len(self.polygon_lines[ii]) - 1):
                    list_x = [self.polygon_for_edit[ii][i][0], self.polygon_for_edit[ii][i - 1][0]]
                    list_y = [self.polygon_for_edit[ii][i][1], self.polygon_for_edit[ii][i - 1][1]]
                    self.polygon_lines[ii][i] = self.graphWidget.plot(list_x, list_y,
                                                                      pen=pg.mkPen(color=('r'), width=5,
                                                                                   style=QtCore.Qt.DashLine))

            for ii in range(len(self.polygon_lines) - 1):
                list_x = [self.polygon_for_edit[ii][0][0], self.polygon_for_edit[ii][-1][0]]
                list_y = [self.polygon_for_edit[ii][0][1], self.polygon_for_edit[ii][-1][1]]
                self.polygon_lines[ii][-1] = self.graphWidget.plot(list_x, list_y,
                                                                   pen=pg.mkPen(color=('r'), width=5,
                                                                                style=QtCore.Qt.DashLine))

            for i in range(len(self.polygon_for_edit) - 1):
                path = mpltPath.Path(self.polygon_for_edit[i])
                self.inside2 = path.contains_points(self.points)
                self.points_inside = list(compress(self.points_inside_square, self.inside2))
                self.points_inside_list[i] = list(compress(self.points_inside_square, self.inside2))

            arr = []
            for i in self.points_inside_list:
                for ii in i:
                    arr.append(ii)
            # remove duplicate points
            rem_duplicate_func = lambda arr: set(arr)
            self.points_inside = list(rem_duplicate_func(arr))

            points_inside = 'Inside: ' + str(len(self.points_inside))
            self.label_dots_inside_polygon.setText(points_inside)

            # close the filter tab

    def channel_select_clicked(self):
        """for when channel selected is clicked"""
        self.ch_select.show()

    def stats_clicked(self):
        """ypdate stats window"""
        self.x_quadrant_data = [[] for i in range(4)]
        self.y_quadrant_data = [[] for i in range(4)]

        for i in range(4):
            if len(self.quadrant_indexs[i]) > 0:
                for j in range(len(self.quadrant_indexs[i])):
                    self.x_quadrant_data[i].append(self.Ch1_channel0[self.quadrant_indexs[i][j]])
                    self.y_quadrant_data[i].append(self.Ch1_channel1[self.quadrant_indexs[i][j]])

        self.stats_window.update(self.windowTitle, self.x_quadrant_data, self.y_quadrant_data)
        self.stats_window.show()
        self.stats_window.activateWindow()
        # "Next filiter" button on the main filter tab, pass the filtered value to next window0

    # and assign a index number to next filter
    def ok_clicked(self):
        # incase user forgot to click polygon again to finish polygon

        if self.polygon_trigger == False:
            """
            text_x = self.lr_x_axis.value()
            text_y = self.lr_y_axis.value()
            a = (np.array(self.Ch1_channel0) > text_x).tolist()
            c = (np.array(self.Ch1_channel1) > text_y).tolist()

            self.quadrant1_list = [False] * len(a)

            for i in range(len(a)):
                if a[i] and c[i]:
                    self.quadrant1_list[i] = True
            """
            if self.selected_quadrant == 0:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant1_list))
            elif self.selected_quadrant == 1:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant2_list))
            elif self.selected_quadrant == 2:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant3_list))
            elif self.selected_quadrant == 3:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant4_list))

            self.filter_out_list = self.points_inside
        else:
            # run trigger again incase user forgot to finish the shape
            self.polygon_triggering()
            # pass polygon value to next window
            self.filter_out_list = self.points_inside

        # use self.tree_index instead ui to prevent potential bugs

        find_a_key = False
        key_count = 0
        while not find_a_key:
            new_index = (key_count,) + self.tree_index
            if new_index in self.ui.tree_dic:
                key_count += 1
            else:
                find_a_key = True

        # tree_dic[self.tree_index]['tree_standarditem'] append the codes for bottom left tree view in main window
        # tree_dic[self.tree_index]['quadrant1_list_or_polygon'] append the filter information

        self.ui.tree_dic[new_index] = {}
        self.ui.tree_dic[new_index]['tree_standarditem'] = StandardItem('New graph', 12 - len(new_index))
        self.ui.tree_dic[self.tree_index]['tree_standarditem'].appendRow(
            self.ui.tree_dic[new_index]['tree_standarditem'])
        self.ui.tree_dic[self.tree_index]['quadrant1_list_or_polygon'] = self.filter_out_list
        # ('self.quadrant1_list_or_polygon', self.filter_out_list)
        self.ui.treeView.expandAll()

        # reassign tree_index, new window need this index to create child branch
        self.ui.tree_index = new_index

        # open a new window for the new branch
        self.ui.dialog = window_filter(self.ui, self.current_file_dict, self.working_data, self.peak_width_working_data,
                                       self.peak_num_working_data, self.linear_plot_channel_list, self.multi_file,
                                       self.multi_file_index, None, None, self.extracted_ratio_data)
        #         self.ui.window_filter[new_index] = self.ui.dialog
        self.ui.tree_dic[new_index]['tree_windowfilter'] = self.ui.dialog
        self.ui.dialog.show()
        print(self.ui.tree_dic.keys())

    def export_clicked(self):
        self.ui.lineEdit_filter.setText(self.lineEdit.text())
        self.close()

    def time_log_clicked(self):
        """this function handles when user clicks the export time log, create a timelog window"""

        if self.polygon_trigger == False:
            if self.selected_quadrant == 0:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant1_list))
            elif self.selected_quadrant == 1:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant2_list))
            elif self.selected_quadrant == 2:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant3_list))
            elif self.selected_quadrant == 3:
                self.points_inside = list(compress(self.points_inside_square, self.quadrant4_list))

            self.filter_out_list = self.points_inside
        else:
            # run trigger again incase user forgot to finish the shape
            self.polygon_triggering()
            # pass polygon value to next window
            self.filter_out_list = self.points_inside

        current_file_counter = 0
        time_list_holder = []
        # time list will hold the data for all the file, each file is one list
        self.time_list = []
        # file list index holds the file index for each of the time list entry
        file_list_index = []
        # indices holds the number of iteration for each file
        indices = [0]
        print(self.multi_file_index)

        if self.root is not None:
            file_list_index.append(self.root)
            time_list_holder = [self.peak_time_working_data[x] for x in self.filter_out_list]
            self.time_list.append(time_list_holder.copy())
            time_list_holder.clear()

        elif len(self.multi_file_index) > 1:
            # handles cases where multi file index is true and has more than 1 file index
            counter = 0
            for index in self.multi_file_index:
                file_exist = False
                low = index
                if len(self.multi_file_index) > current_file_counter + 1:
                    high = self.multi_file_index[current_file_counter + 1]
                else:
                    high = self.filter_out_list[-1] + 1
                while counter < len(self.filter_out_list):
                    x = self.filter_out_list[counter]
                    if low <= x < high and file_exist is False:
                        file_exist = True
                        file_list_index.append(self.multi_file[current_file_counter])
                    elif x >= high:
                        current_file_counter += 1
                        break
                    counter += 1
                if file_exist:
                    indices.append(counter)

            for i in range(len(indices) - 1):
                lower_bound = indices[i]
                upper_bound = indices[i + 1]
                for j in range(lower_bound, upper_bound):
                    x = self.filter_out_list[j]
                    time_list_holder.append(self.peak_time_working_data[x])
                self.time_list.append(time_list_holder.copy())
                time_list_holder.clear()

        elif len(self.multi_file_index) == 1 and self.root is None:
            # handle when there is only 1 file, but not a root file
            file_list_index.append(self.multi_file[0])
            time_list_holder = [self.peak_time_working_data[x] for x in self.filter_out_list]
            self.time_list.append(time_list_holder.copy())
            time_list_holder.clear()

        # this list is for transfering the data to timeLog
        dataframe_list = []

        for file_time_data in self.time_list:

            minutes_list = []
            counts_list = []
            for i in range(1, file_time_data[-1] + 1):
                minutes_list.append(i)
                counts_list.append(file_time_data.count(i))
            dataframe = pd.DataFrame({"Minutes": minutes_list, "Total Sorted": counts_list})
            dataframe_list.append(dataframe)

        self.time_log_window = Time_log_selection_window.TimeLogPopUpWindow(self.ui.time_log_window, self.windowTitle(),
                                                                            dataframe_list, file_list_index)
        self.time_log_window.show()

    def start_plot_update(self, steps, histo, max_density, percentage_coefficient):
        """method to create threads to do plot update"""
        self.loading_bar = LoadingScreen()
        self.scatter = pg.ScatterPlotItem()
        self.thread = QtCore.QThread()
        self.worker = PlotGenerationWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(partial(self.worker.run, self, steps, histo, max_density, percentage_coefficient))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.plot_finalization)
        self.worker.progress.connect(self.loading_bar.update)
        self.thread.start()

    def plot_finalization(self):
        """call this function when the worker finish updating plot data"""
        # self.scatter = pg.ScatterPlotItem()
        # self.scatter.addPoints(self.spotss)
        # self.graphWidget.addItem(self.scatter)
        self.setEnabled(True)
        self.loading_bar.hide()
        self.graphWidget.removeItem(self.lr_x_axis)
        self.graphWidget.removeItem(self.lr_y_axis)

        pen = pg.mkPen(color='r', width=5, style=QtCore.Qt.DashLine)
        self.lr_x_axis = pg.InfiniteLine(0, movable=True, pen=pen)
        self.graphWidget.addItem(self.lr_x_axis)
        self.lr_y_axis = pg.InfiniteLine(0, movable=True, pen=pen, angle=0)
        self.graphWidget.addItem(self.lr_y_axis)
        self.lr_x_axis.setValue(float(self.GateVoltage_x.text()))
        self.lr_y_axis.setValue(float(self.GateVoltage_y.text()))

        self.lr_x_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        self.lr_x_axis.sigPositionChangeFinished.connect(self.quadrant_rect_resize)
        self.lr_x_axis.sigPositionChanged.connect(self.quadrant_rect_resize)
        self.lr_y_axis.sigPositionChangeFinished.connect(self.infiniteline_update)
        self.lr_y_axis.sigPositionChanged.connect(self.quadrant_rect_resize)
        self.lr_y_axis.sigPositionChangeFinished.connect(self.quadrant_rect_resize)
        # reset threshold # test
        self.infiniteline_table_update()

    def filter_export(self):
        """function calls to export data needed to recreate filter"""
        window_setting = {"x_color": self.comboBox_3.currentIndex(),
                          "y_color": self.comboBox_4.currentIndex(),
                          "x_mode": self.comboBox_1.currentIndex(),
                          "y_mode": self.comboBox_2.currentIndex(),
                          "GateVoltage_x": self.GateVoltage_x.text(),
                          "GateVoltage_y": self.GateVoltage_y.text(),
                          "ch1_peak_num_mode": self.comboBox_peak_num_1.currentIndex(),
                          "ch2_peak_num_mode": self.comboBox_peak_num_2.currentIndex(),
                          "ch3_peak_num_mode": self.comboBox_peak_num_3.currentIndex(),
                          "ch4_peak_num_mode": self.comboBox_peak_num_4.currentIndex(),
                          "ch1_peak_num": self.lineEdit_peak_num_1.text(),
                          "ch2_peak_num": self.lineEdit_peak_num_2.text(),
                          "ch3_peak_num": self.lineEdit_peak_num_3.text(),
                          "ch4_peak_num": self.lineEdit_peak_num_4.text(),
                          }

        output = FilterData(self.linear_plot_channel_list, self.tree_index, self.current_file_dict,
                            self.working_data, self.points_inside_square, self.points_inside, self.filter_out_list,
                            self.peak_width_working_data,
                            self.peak_num_working_data, self.peak_time_working_data, self.root, self.multi_file,
                            self.multi_file_index, self.index_in_all_selected_channel, self.spots, self.Ch1_channel0,
                            self.Ch1_channel1, self.Ch1_channel0_peak_num, self.Ch1_channel1_peak_num, window_setting)
        return output


class FilterData:
    """this class will hold all the data to reconstruct a filter"""

    def __init__(self, linear_plot_channel_list, tree_index, current_file_dict, working_data, points_inside_square,
                 points_inside, filter_out_list,
                 peak_width_working_data, peak_num_working_data, peak_time_working_data, root, multi_file,
                 multi_file_index, index_in_all_selected_channel, spots, Ch1_channel0, Ch1_channel1,
                 Ch1_channel0_peak_num, Ch1_channel1_peak_num, window_setting):
        # tree_index saved the index number for all filters, include its parent and child branch
        # ex. index = 0,1,1 means: select filter index is "No.1", under parent "No.1", upder grand-parent "No.0"
        self.linear_plot_channel_list = linear_plot_channel_list
        self.tree_index = tree_index
        self.current_file_dict = current_file_dict
        self.working_data = working_data
        self.filter_out_list = filter_out_list
        self.peak_width_working_data = peak_width_working_data
        self.peak_num_working_data = peak_num_working_data
        self.peak_time_working_data = peak_time_working_data
        self.points_inside_square = points_inside_square
        self.points_inside = points_inside
        # root will hold the file index for the root file if true, else None
        self.root = root

        self.multi_file = multi_file
        self.multi_file_index = multi_file_index

        self.polygon = []
        self.points_inside = []

        # linear plot data
        self.index_in_all_selected_channel = index_in_all_selected_channel

        # set up plot data
        self.spots = spots
        self.Ch1_channel0 = Ch1_channel0
        self.Ch1_channel1 = Ch1_channel1
        self.Ch1_channel0_peak_num = Ch1_channel0_peak_num
        self.Ch1_channel1_peak_num = Ch1_channel1_peak_num
        self.window_setting = window_setting


class PlotGenerationWorker(QtCore.QObject):
    """worker to handle plot color generation"""
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(list)

    def run(self, parent, steps, histo, max_density, percentage_coefficient):
        parent.spots = []
        print(os.getcwd())
        step = [i / 256 for i in range(255)]
        colors = []
        with open(os.path.dirname(os.path.realpath(__file__)) + '/CET-R2.csv', newline='') as f:
            reader = csv.reader(f)
            for line in reader:
                colors.append([float(x) * 256 for x in line])
        print(colors)
        cm = pg.ColorMap(pos=step, color=colors)
        # cm = colormap.get("CET-R2.csv")
        progress_percent = 0
        data_size = len(parent.Ch1_channel0)
        for i in range(data_size):
            x = parent.Ch1_channel0[i]
            y = parent.Ch1_channel1[i]

            a = int(x / steps)
            b = int(y / steps)
            if a >= 1000:
                a = 999
            if b >= 1000:
                b = 999

            # checking for density, the value divided by steps serves as the index
            density = histo[a][b]
            percentage = density / max_density * 100 * percentage_coefficient
            if percentage <= 0 or math.isnan(percentage):
                percentage = 0.1
            elif percentage > 1:
                percentage = 1
            spot_dic = {'pos': (x, y), 'size': 3,
                        'pen': None,
                        'symbol': 'p',
                        'brush': cm.map(percentage, mode=pg.ColorMap.QCOLOR)}
            parent.spots.append(spot_dic.copy())
            # calculate current percentage, this stage max at 80
            if i * 100 // data_size != progress_percent:
                progress_percent = i * 80 // data_size
                signal_string = "Processing data points: " + str(i) + "/" + str(data_size)
                self.progress.emit([progress_percent, signal_string])
            # parent.graphWidget.plot(density_listx[i], density_listy[i], symbol='p', pen=None, symbolPen=None,
            #                     symbolSize=5, symbolBrush=(red, blue, green))
        self.progress.emit([85, "Assigning density to data..."])
        parent.scatter.addPoints(parent.spots)
        self.progress.emit([95, "Plotting data..."])
        parent.graphWidget.addItem(parent.scatter)
        self.progress.emit([100, "Finished"])
        self.finished.emit()


class LoadingScreen(QWidget):
    """This class is the pop up window for when graph is loading"""

    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.bar_text = QtWidgets.QLabel(self)
        self.bar_text.setText("Updating plot...")
        self.layout.addWidget(self.bar_text)
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 400, 25)
        self.pbar.setValue(0)
        self.layout.addWidget(self.pbar)
        self.setWindowTitle("Plot Updating")
        self.setLayout(self.layout)
        self.setFixedSize(500, 80)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.show()

    def update(self, progress: int):
        """Call this function when progress signal is emited"""
        self.bar_text.setText(progress[1])
        self.pbar.setValue(progress[0])


class ChannelSelectWindow(QWidget):
    """this class will pop up for legacy channel selection"""

    def __init__(self, parent: window_filter):
        super(ChannelSelectWindow, self).__init__()
        self.comboBox_14_list = {}
        self.parent = parent
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Channel Selection")
        self.setFixedSize(200, 300)
        self.layout_vertical_checkbox = QtWidgets.QVBoxLayout()

        self.line = QtWidgets.QFrame()
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.label = QtWidgets.QLabel("Please select channels: ")
        self.layout_vertical_checkbox.addWidget(self.label)

        self.layout_vertical_checkbox.addWidget(self.line)

        self.layout_vertical_checkbox.setObjectName("layout_vertical_checkbox")
        self.checkbox_ch1 = QtWidgets.QCheckBox("Channel 1")
        self.checkbox_ch1.setObjectName("checkbox_ch1")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch1)
        self.checkbox_ch2 = QtWidgets.QCheckBox("Channel 2")
        self.checkbox_ch2.setObjectName("checkbox_ch2")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch2)
        self.checkbox_ch3 = QtWidgets.QCheckBox("Channel 3")
        self.checkbox_ch3.setObjectName("checkbox_ch3")
        # elf.layout_vertical_checkbox.addWidget(self.checkbox_ch3)
        self.checkbox_ch12 = QtWidgets.QCheckBox("Channel 1-2")
        self.checkbox_ch12.setObjectName("checkbox_ch12")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch12)
        self.checkbox_ch13 = QtWidgets.QCheckBox("Channel 1-3")
        self.checkbox_ch13.setObjectName("checkbox_ch13")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch13)
        self.checkbox_ch23 = QtWidgets.QCheckBox("Channel 2-3")
        self.checkbox_ch23.setObjectName("checkbox_ch23")
        self.layout_vertical_checkbox.addWidget(self.checkbox_ch23)

        self.checkbox_Droplet_Record = QtWidgets.QCheckBox("Droplet Record")
        self.checkbox_Droplet_Record.setObjectName("checkbox_Droplet_Record")
        self.layout_vertical_checkbox.addWidget(self.checkbox_Droplet_Record)

        self.checkbox_Locked_Out_Peaks = QtWidgets.QCheckBox("Locked Out Peaks")
        self.checkbox_Locked_Out_Peaks.setObjectName("checkbox_Locked_Out_Peaks")
        self.layout_vertical_checkbox.addWidget(self.checkbox_Locked_Out_Peaks)

        self.checkBox_7 = QtWidgets.QCheckBox("Sorted Peaks")
        self.checkBox_7.setObjectName("checkBox_7")
        self.layout_vertical_checkbox.addWidget(self.checkBox_7)

        self.layout_horizontal_checkbox = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.reset_button = QtWidgets.QPushButton("Reset")

        self.line_2 = QtWidgets.QFrame()
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.layout_vertical_checkbox.addWidget(self.line_2)

        self.layout_horizontal_checkbox.addWidget(self.ok_button)
        self.layout_horizontal_checkbox.addWidget(self.reset_button)
        self.layout_vertical_checkbox.addLayout(self.layout_horizontal_checkbox)

        self.setLayout(self.layout_vertical_checkbox)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

        self.ok_button.pressed.connect(self.update_channels)
        self.reset_button.pressed.connect(self.reset)

    def update_channels(self):
        self.comboBox_14_list = {}
        if self.checkbox_ch1.isChecked() and self.parent.current_file_dict['Ch1 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1 "
        if self.checkbox_ch2.isChecked() and self.parent.current_file_dict['Ch2 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2 "
        if self.checkbox_ch3.isChecked() and self.parent.current_file_dict['Ch3 '] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch3 "
        if self.checkbox_ch12.isChecked() and self.parent.current_file_dict['Ch1-2'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-2"
        if self.checkbox_ch13.isChecked() and self.parent.current_file_dict['Ch1-3'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch1-3"
        if self.checkbox_ch23.isChecked() and self.parent.current_file_dict['Ch2-3'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Ch2-3"
        if self.checkbox_Droplet_Record.isChecked() and self.parent.current_file_dict['Droplet Record'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Droplet Record"
        if self.checkbox_Locked_Out_Peaks.isChecked() and self.parent.current_file_dict['Locked Out Peaks'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Locked Out Peaks"
        if self.checkBox_7.isChecked() and self.parent.current_file_dict['Peak Record'] != '':
            self.comboBox_14_list[len(self.comboBox_14_list)] = "Peak Record"

        if len(self.comboBox_14_list.keys()) > 0:
            self.parent.legacy_mode = True
            self.parent.button_channel_select.setCheckable(True)
            self.parent.button_channel_select.setDown(True)
            self.parent.linear_plot_channel_list = self.comboBox_14_list.copy()
            self.parent.button_channel_select.repaint()
        else:
            self.parent.legacy_mode = False
            self.parent.button_channel_select.setCheckable(True)
            self.parent.button_channel_select.setDown(False)
            self.parent.button_channel_select.repaint()
        self.parent.channel_list_update(self.comboBox_14_list)
        self.hide()

    def reset(self):
        self.checkbox_ch1.setCheckState(0)
        self.checkbox_ch2.setCheckState(0)
        self.checkbox_ch3.setCheckState(0)
        self.checkbox_ch12.setCheckState(0)
        self.checkbox_ch13.setCheckState(0)
        self.checkbox_ch23.setCheckState(0)
        self.checkbox_Droplet_Record.setCheckState(0)
        self.checkbox_Locked_Out_Peaks.setCheckState(0)
        self.checkBox_7.setCheckState(0)


def show_dialog(text: str, window_title: str):
    """this function is used to present user with a dialog"""
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle(window_title)
    layout = QtWidgets.QVBoxLayout(dialog)
    dialog_text = QLabel()
    dialog_text.setText(text)
    layout.addWidget(dialog_text)
    ok_btn = QPushButton("Ok")
    ok_btn.setMaximumSize(100, 50)
    layout.addWidget(ok_btn, alignment=Qt.AlignCenter)
    ok_btn.clicked.connect(dialog.hide)
    dialog.setLayout(layout)
    dialog.exec_()


if __name__ == '__main__':
    # create pyqt5 app
    App = QtWidgets.QApplication(sys.argv)
    # create the instance of our Window
    window = ChannelSelectWindow()
    window.show()

    # start the app
    sys.exit(App.exec())
