from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QTableWidgetItem
from pyqtgraph.Qt import QtCore
from pyqtgraph import PlotWidget
from PyQt5.Qt import QStandardItem
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
from PyQt5.QtGui import QFont, QColor


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class window_filter(QWidget):
    def __init__(self, parent, current_file_dict, working_data, peak_width_working_data, peak_num_working_data,
                 linear_plot_channel_list={}):
        super().__init__()
        self.ui = parent
        # tree_index saved the index number for all filters, include its parent and child branch
        # ex. index = 0,1,1 means: select filter index is "No.1", under parent "No.1", upder grand-parent "No.0"
        self.linear_plot_channel_list = linear_plot_channel_list
        self.tree_index = self.ui.tree_index
        self.current_file_dict = current_file_dict
        self.working_data = working_data
        self.filter_out_list = []
        self.peak_width_working_data = []
        self.peak_num_working_data = []
        self.points_inside_square = []

        # export parent index
        # ex. index = 0,1,1 ; parent index = 0,1
        if len(self.tree_index) > 1:
            parent_index = self.tree_index[1:]
            self.points_inside_square = self.ui.tree_dic[parent_index]['quadrant1_list_or_polygon']
            self.peak_width_working_data = peak_width_working_data
            self.peak_num_working_data = peak_num_working_data

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

        self.GateVoltage_x = QtWidgets.QLineEdit('0')
        Scatter_plot_layout.addWidget(self.GateVoltage_x, 4, 3, 1, 1)
        self.GateVoltage_y = QtWidgets.QLineEdit('0')
        Scatter_plot_layout.addWidget(self.GateVoltage_y, 5, 3, 1, 1)

        self.line_Scatter_plot = QtWidgets.QFrame()
        self.line_Scatter_plot.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Scatter_plot.setFrameShadow(QtWidgets.QFrame.Sunken)
        Scatter_plot_layout.addWidget(self.line_Scatter_plot, 6, 0, 1, 4)

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

        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_1, 2, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_2, 3, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_3, 4, 2, 1, 1)
        Multi_peaks_layout.addWidget(self.lineEdit_peak_num_4, 5, 2, 1, 1)

        self.line_Multi_peaks = QtWidgets.QFrame()
        self.line_Multi_peaks.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_Multi_peaks.setFrameShadow(QtWidgets.QFrame.Sunken)
        Multi_peaks_layout.addWidget(self.line_Multi_peaks, 6, 0, 1, 3)

        ######## Multi peak end

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

        self.polygon_button_1 = QPushButton('Polygon')
        self.polygon_button_2 = QPushButton('Clear')
        self.polygon_button_3 = QPushButton('Shape Edit')

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

        # add threshold
        pen = pg.mkPen(color=(0, 120, 180), width=5)
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

        # triggers
        self.pushButton_6.clicked.connect(self.polygon_reset_linear_plot)
        self.pushButton_8.clicked.connect(self.polygon_last_page)
        self.pushButton_7.clicked.connect(self.polygon_next_page)

        self.reset_comboBox = True

        #### linear end
        ##########################################################################################

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

    def channel_list_update(self, linear_plot_channel_list):
        self.linear_plot_channel_list = linear_plot_channel_list

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

            for list_index in self.linear_plot_channel_list:
                list_text = self.linear_plot_channel_list[list_index]

                polygon_length = 0
                for i in range(list_index):
                    polygon_length += len(
                        self.ui.analog[self.current_file_dict[self.linear_plot_channel_list[i]]][0][0])

                polygon_length_end = polygon_length + len(self.ui.analog[self.current_file_dict[list_text]][0][0])
                index_in_all_selected_channel = [x for x, x in enumerate(self.points_inside) if
                                                 x > polygon_length and x <= polygon_length_end]

                if index_in_all_selected_channel != []:
                    self.comboBox_14.addItem(str(list_text))

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
        index_in_all_selected_channel = [x for x, x in enumerate(self.points_inside) if
                                         x >= polygon_length and x <= polygon_length_end]
        index_in_current_channel = [x - polygon_length for x in index_in_all_selected_channel]

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
            self.subgating_file_dict = self.ui.file_dict_list[self.tree_index[len(self.tree_index)-1]]
            os.chdir(self.subgating_file_dict["Root Folder"])
            file = self.subgating_file_dict[text1]

            data = pd.DataFrame({0: [], 1: [], 2: [], 3: []}, )

            print("index_in_current_channel", len(index_in_current_channel), ':', index_in_current_channel)

            for x in range(lower_bond, upper_bond):
                i = index_in_current_channel[x]
                skip_rows = i * sample_size
                polygon_data = pd.read_csv(file, skiprows=skip_rows, nrows=sample_size, header=header)
                length = len(polygon_data.columns)
                polygon_data.columns = list(range(0, length))
                data = pd.concat([data, polygon_data])

            height_data = data[0].values.tolist()
            height_index = list(range(len(height_data)))

            poly_degree = int(self.lineEdit_39.text())
            window_length = int(self.lineEdit_40.text()) // 2 * 2 - 1
            self.widget_29.addLegend()

            for i in range(0, sample_size * nrows, sample_size):
                self.widget_29.plot([i, i], [0, 3], pen=pg.mkPen(color=('r'), width=1, style=QtCore.Qt.DashLine))

            if self.polygon_Smooth_enable.isChecked():
                if self.polygon_channel_1.isChecked():
                    height_data = savgol_filter(data[0], window_length, poly_degree)
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index, height_data, name='Channel_1', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    height_data = savgol_filter(data[1], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index, height_data, name='Channel_2', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    height_data = savgol_filter(data[2], window_length, poly_degree)
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index, height_data, name='Channel_3', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    height_data = savgol_filter(data[3], window_length, poly_degree)
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index, height_data, name='Channel_4', pen=pen, symbol='o', symbolSize=0,
                                        symbolBrush=('m'))
            else:
                if self.polygon_channel_1.isChecked():
                    pen = pg.mkPen(color=(83, 229, 29), width=2)
                    self.widget_29.plot(height_index, data[0].values.tolist(), name='Channel_1', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_2.isChecked():
                    pen = pg.mkPen(color=(238, 17, 47), width=2)
                    self.widget_29.plot(height_index, data[1].values.tolist(), name='Channel_2', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_3.isChecked():
                    pen = pg.mkPen(color=(48, 131, 240), width=2)
                    self.widget_29.plot(height_index, data[2].values.tolist(), name='Channel_3', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
                if self.polygon_channel_4.isChecked():
                    pen = pg.mkPen(color=(238, 134, 30), width=2)
                    self.widget_29.plot(height_index, data[3].values.tolist(), name='Channel_4', pen=pen, symbol='o',
                                        symbolSize=0, symbolBrush=('m'))
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
            self.width = self.working_data[self.histogram_comboBox_2.currentIndex()]
        else:
            self.width = self.peak_width_working_data[self.histogram_comboBox_2.currentIndex()]

        self.full_width = [self.width[i] for i in self.points_inside_square]

        self.width = [x for x in self.full_width if x >= float(self.histogram_gate_voltage.text())]

        width_count_filtered = round(100 * len(self.width) / len(self.full_width), 2)
        width_count = "Percentage: " + str(width_count_filtered) + '% of filtered points ' + str(
            len(self.width)) + '/' + str(len(self.full_width))
        self.label_percentage.setText(width_count)

        percentage_all_count = round(100 * len(self.width) / len(self.working_data[0]), 2)
        percentage_all = "Percentage: " + str(percentage_all_count) + '% of all points ' + str(
            len(self.width)) + '/' + str(len(self.working_data[0]))
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
        holder = [[], [], [], []]
        for ch in range(4):
            holder[ch] = [i for i, x in enumerate(self.peak_num_working_data[ch])
                          if self.peak_num_comp(x, self.peak_num_mode[ch], self.peak_num_in[ch])]
        self.peak_num_filtered_index = list(set(holder[0]).intersection(set(holder[1]), set(holder[2]), set(holder[3])))
        print('holder[0]', holder[0])
        print('self.peak_num_filtered_index', self.peak_num_filtered_index)

    ### drawing function for main tab scatter pot

    def draw_graphwidget(self):
        # "update" clicked
        # prepare data

        if not self.points_inside_square:
            # this is for root data extraction
            self.peak_width_working_data = []
            self.peak_num_working_data = []
            self.working_data = []

            for i in range(4):
                self.working_data.append([])
                self.peak_width_working_data.append([])
                self.peak_num_working_data.append([])

            if self.ui.checkbox_ch1.isChecked() and self.current_file_dict['Ch1 '] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1 ']][2][i]
            if self.ui.checkbox_ch2.isChecked() and self.current_file_dict['Ch2 '] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2 ']][2][i]
            if self.ui.checkbox_ch3.isChecked() and self.current_file_dict['Ch3 '] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch3 ']][2][i]
            if self.ui.checkbox_ch12.isChecked() and self.current_file_dict['Ch1-2'] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-2']][2][i]
            if self.ui.checkbox_ch13.isChecked() and self.current_file_dict['Ch1-3'] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch1-3']][2][i]
            if self.ui.checkbox_ch23.isChecked() and self.current_file_dict['Ch2-3'] in self.ui.analog.s():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Ch2-3']][2][i]
            if self.ui.checkbox_Droplet_Record.isChecked() and self.current_file_dict[
                'Droplet Record'] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Droplet Record']][2][i]
            if self.ui.checkBox_7.isChecked() and self.current_file_dict['Peak Record'] in self.ui.analog.keys():
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][2][i]

            if len(self.peak_width_working_data) == 0:
                for i in range(4):
                    self.working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][0][i]
                    self.peak_width_working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][1][i]
                    self.peak_num_working_data[i] += self.ui.analog[self.current_file_dict['Peak Record']][2][i]
            points_inside_square = [i for i in range(len(self.working_data[0]))]
        else:
            points_inside_square = self.points_inside_square

        # edit filter name

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
        self.peak_num_in.append(int(self.lineEdit_peak_num_1.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_2.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_3.text()))
        self.peak_num_in.append(int(self.lineEdit_peak_num_4.text()))

        if self.peak_num_mode != [0, 0, 0, 0] or self.peak_num_in != [0, 0, 0, 0]:
            self.peak_num_filter()
            points_inside_square = list(set(points_inside_square).intersection(set(self.peak_num_filtered_index)))

        self.points_inside_square = points_inside_square
        # peak number filter end

        if self.comboBox_1.currentIndex() == 0:
            data_in_subgating_x = self.working_data[self.comboBox_3.currentIndex()]
        else:
            data_in_subgating_x = self.peak_width_working_data[self.comboBox_3.currentIndex()]

        if self.comboBox_2.currentIndex() == 0:
            data_in_subgating_y = self.working_data[self.comboBox_4.currentIndex()]
        else:
            data_in_subgating_y = self.peak_width_working_data[self.comboBox_4.currentIndex()]

        x_axis_channel = self.comboBox_3.currentIndex()
        y_axis_channel = self.comboBox_4.currentIndex()
        x_axis_name = self.comboBox_1.currentText() + " " + self.comboBox_3.currentText()
        y_axis_name = self.comboBox_2.currentText() + " " + self.comboBox_4.currentText()

        self.graphWidget.clear()
        self.graphWidget.setLabel('left', y_axis_name, color='b')
        self.graphWidget.setLabel('bottom', x_axis_name, color='b')

        self.Ch1_channel0 = [data_in_subgating_x[i] for i in self.points_inside_square]
        self.Ch1_channel1 = [data_in_subgating_y[i] for i in self.points_inside_square]

        # test color setup
        max_voltage = 12
        bins = 1000
        steps = max_voltage / bins

        # all data is first sorted into a histogram
        histo, _, _ = np.histogram2d(self.Ch1_channel0, self.Ch1_channel1, bins,
                                     [[0, max_voltage], [0, max_voltage]],
                                     density=True)
        max_density = histo.max()
        percentage_coefficient = int(1) / 10
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
            percentage = density / max_density * 100 * percentage_coefficient
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

        pen = pg.mkPen(color=(0, 120, 180), width=5)
        self.lr_x_axis = pg.InfiniteLine(0, movable=True, pen=pen)
        self.graphWidget.addItem(self.lr_x_axis)
        self.lr_y_axis = pg.InfiniteLine(0, movable=True, pen=pen, angle=0)
        self.graphWidget.addItem(self.lr_y_axis)
        self.lr_x_axis.setValue(float(self.GateVoltage_x.text()))
        self.lr_y_axis.setValue(float(self.GateVoltage_y.text()))

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
                if self.ui.Ch1_channel0_peak_num[i] == 1:
                    single_peak_count_channel0 += 1
                elif self.ui.Ch1_channel0_peak_num[i] > 1:
                    multi_peak_count_channel0 += 1
                if self.ui.Ch1_channel1_peak_num[i] == 1:
                    single_peak_count_channel1 += 1
                elif self.ui.Ch1_channel1_peak_num[i] > 1:
                    multi_peak_count_channel1 += 1

        try:
            droplets = float(self.ui.lineEdit_totaldroplets.text())
            totalpercent1 = round(count_quadrant1 / droplets * 100, 2)
        except:
            totalpercent1 = 0

        if len(self.Ch1_channel0) != 0:
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
                if self.ui.Ch1_channel0_peak_num[i] == 1:
                    single_peak_count_channel0 += 1
                elif self.ui.Ch1_channel0_peak_num[i] > 1:
                    multi_peak_count_channel0 += 1
                if self.ui.Ch1_channel1_peak_num[i] == 1:
                    single_peak_count_channel1 += 1
                elif self.ui.Ch1_channel1_peak_num[i] > 1:
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
        if self.stop_edit_trigger and self.polygon_trigger:

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

            self.filter_out_list = list(compress(self.points_inside_square, self.quadrant1_list))
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
        print('self.quadrant1_list_or_polygon', self.filter_out_list)
        self.ui.treeView.expandAll()

        # reassign tree_index, new window need this index to create child branch
        self.ui.tree_index = new_index

        # open a new window for the new branch
        self.ui.dialog = window_filter(self.ui, self.current_file_dict, self.working_data, self.peak_width_working_data,
                                       self.peak_num_working_data, self.linear_plot_channel_list)
        #         self.ui.window_filter[new_index] = self.ui.dialog
        self.ui.tree_dic[new_index]['tree_windowfilter'] = self.ui.dialog
        self.ui.dialog.show()

    def export_clicked(self):
        self.ui.lineEdit_filter.setText(self.lineEdit.text())
        self.close()
