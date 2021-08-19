from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial
import os
from PyQt5.Qt import QStandardItem
from multiprocessing import freeze_support
import Filter_window
import pandas as pd
import random
import datetime
import pyqtgraph as pg
from enum import Enum


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=Qt.QColor(0, 0, 0)):
        super().__init__()

        fnt = Qt.QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class Time_log_functions(Enum):
    """This class holds the enum for time log functions"""
    TOTAL_SORTED = 0
    TOTAL_LOST = 1
    TOTAL_DROPLETS = 2
    POSITIVE_RATE = 3
    DROPLET_FREQUENCY = 4
    SORTED_RATE = 5
    LOCKED_OUT = 6


class TimeLogFileSelectionWindow(QWidget):
    """Class that allows user to select the files for syringes, also handles UI for file combine of filters"""

    def __init__(self, file_list: QListWidget, file_model: Qt.QStandardItemModel, file_index: list, tree_dict: dict
                 , tree_model: Qt.QStandardItemModel, parent: QMainWindow, file_dict: list, top_graph: pg.PlotWidget
                 , bot_graph: pg.PlotWidget):
        super().__init__()
        self.setupUI()
        self.main_file_list = file_list
        self.file_model = file_model
        self.file_index = file_index
        self.tree_model = tree_model
        self.ui = parent
        self.file_dict = file_dict

        # time_log_data holds the raw data from time log files, organized in a 1D list
        self.time_log_data = []

        self.file_names_top = []
        self.file_names_bot = []

        # file_time_data holds the time stamp of all the file in time log data, one to one
        self.file_time_data = []

        # mode saves the list of dictionary, only exist for the parent node
        self.mode = []

        self.top_processed_data = pd.DataFrame()
        self.bot_processed_data = pd.DataFrame()
        self.top_graph = top_graph
        self.bot_graph = bot_graph

        # self.filter_index = tree_index

        # caller keeps track of which file index to work on, 0 for filter, 1 for log files
        self.caller = 1
        self.spawned_filter_counter = 1
        self.tree_dict = tree_dict
        self.load_files()

        self.ch1_name = "Green"
        self.ch2_name = "Red"
        self.ch3_name = "Blue"
        self.ch4_name = "Orange"

    def setupUI(self):
        """call this function when setting up UI"""
        self.setWindowTitle("Syringe File Selection")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setMaximumSize(400, 400)
        self.setSizePolicy(sizePolicy)

        layout = QVBoxLayout()
        self.label = QLabel("Syringe Name")
        layout.addWidget(self.label)

        self.line_edit_name = QLineEdit("Syringe 1")
        layout.addWidget(self.line_edit_name)

        self.file_list = QtWidgets.QListWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.file_list.setSizePolicy(sizePolicy)
        self.file_list.setMinimumSize(QtCore.QSize(100, 100))
        self.file_list.setMaximumSize(QtCore.QSize(400, 400))
        self.file_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(self.file_list)

        self.line_divider = QtWidgets.QFrame(self)
        self.line_divider.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_divider.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_divider.setObjectName("line_top_vertical")
        layout.addWidget(self.line_divider)

        self.ch_selection_text = QtWidgets.QLabel("Channel Selection (Only for Time Log)")

        layout.addWidget(self.ch_selection_text)

        self.ch_1_checkbox = QtWidgets.QCheckBox("Green")
        self.ch_1_checkbox.setTristate()
        self.ch_1_checkbox.setToolTip("Check to include Positives from this Ch, Box to exclude positives containing "
                                      "this Ch")
        self.ch_2_checkbox = QtWidgets.QCheckBox("Red")
        self.ch_2_checkbox.setTristate()
        self.ch_2_checkbox.setToolTip("Check to include Positives from this Ch, Box to exclude positives containing "
                                      "this Ch")
        self.ch_3_checkbox = QtWidgets.QCheckBox("Blue")
        self.ch_3_checkbox.setTristate()
        self.ch_3_checkbox.setToolTip("Check to include Positives from this Ch, Box to exclude positives containing "
                                      "this Ch")
        self.ch_4_checkbox = QtWidgets.QCheckBox("Orange")
        self.ch_4_checkbox.setTristate()
        self.ch_4_checkbox.setToolTip("Check to include Positives from this Ch, Box to exclude positives containing "
                                      "this Ch")

        layout_box = QGridLayout()
        layout_box.addWidget(self.ch_1_checkbox, 0, 0)
        layout_box.addWidget(self.ch_2_checkbox, 0, 1)
        layout_box.addWidget(self.ch_3_checkbox, 1, 0)
        layout_box.addWidget(self.ch_4_checkbox, 1, 1)

        layout.addLayout(layout_box)

        self.line_divider_2 = QtWidgets.QFrame(self)
        self.line_divider_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_divider_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_divider_2.setObjectName("line_top_vertical")
        layout.addWidget(self.line_divider_2)

        self.time_divide_label = QLabel("Time Point Division (Only for Time Log)")
        layout.addWidget(self.time_divide_label)

        self.time_divide_checkbox = QtWidgets.QCheckBox("Time point every ")

        self.time_spinbox = QtWidgets.QSpinBox()
        self.time_spinbox.setMinimum(1)

        self.time_combobox = QtWidgets.QComboBox()
        self.time_combobox.addItem("Minutes")
        self.time_combobox.addItem("Hours")

        layout_time_divide = QHBoxLayout()
        layout_time_divide.addWidget(self.time_divide_checkbox)
        layout_time_divide.addWidget(self.time_spinbox)
        layout_time_divide.addWidget(self.time_combobox)

        layout.addLayout(layout_time_divide)

        layout_h = QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        layout_h.addWidget(self.ok_button)
        layout_h.addWidget(self.cancel_button)

        layout.addLayout(layout_h)

        self.setLayout(layout)

        self.ch_1_checkbox.clicked.connect(self.checkbox_handle)
        self.ch_2_checkbox.clicked.connect(self.checkbox_handle)
        self.ch_3_checkbox.clicked.connect(self.checkbox_handle)
        self.ch_4_checkbox.clicked.connect(self.checkbox_handle)
        self.ok_button.clicked.connect(self.ok_clicked)
        self.cancel_button.clicked.connect(self.close_clicked)

    def checkbox_handle(self):
        sender = self.sender()
        if sender.checkState() == 1:
            sender.setCheckState(2)
        elif sender.checkState() == 0:
            sender.setCheckState(1)
        elif sender.checkState() == 2:
            sender.setCheckState(0)

    def populate_list(self):
        """function to populate the file list with updated information, also update all other elements"""
        self.file_list.clear()
        for i in range(self.main_file_list.count()):
            item = self.main_file_list.item(i).text()
            self.file_list.addItem(item)
        # update the automatic default name for syringe
        if self.caller == 1:
            # fetch syringe name for time_log_call
            syringe_number = self.file_model.rowCount() + 1
            self.line_edit_name.setText("Syringe " + str(syringe_number))
            self.ch_1_checkbox.setCheckState(0)
            self.ch_2_checkbox.setCheckState(0)
            self.ch_3_checkbox.setCheckState(0)
            self.ch_4_checkbox.setCheckState(0)
            self.ch_1_checkbox.setEnabled(True)
            self.ch_2_checkbox.setEnabled(True)
            self.ch_3_checkbox.setEnabled(True)
            self.ch_4_checkbox.setEnabled(True)
            self.time_combobox.setEnabled(True)
            self.time_spinbox.setEnabled(True)
            self.time_divide_checkbox.setEnabled(True)

        else:
            # fetech syringe name for filter call

            self.line_edit_name.setText("Syringe " + str(self.spawned_filter_counter))
            self.ch_1_checkbox.setCheckState(0)
            self.ch_2_checkbox.setCheckState(0)
            self.ch_3_checkbox.setCheckState(0)
            self.ch_4_checkbox.setCheckState(0)
            self.ch_1_checkbox.setEnabled(False)
            self.ch_2_checkbox.setEnabled(False)
            self.ch_3_checkbox.setEnabled(False)
            self.ch_4_checkbox.setEnabled(False)
            self.time_combobox.setEnabled(False)
            self.time_spinbox.setEnabled(False)
            self.time_divide_checkbox.setEnabled(False)

    def load_files(self):
        """function call to load the file after filelist is loaded"""
        for file in self.file_dict:
            # check if file exist
            if file["Time Log"]:
                os.chdir(file["Root Folder"])
                data = pd.read_csv(file["Time Log"])
                self.file_time_data.append(datetime.datetime.strptime(file["Time Log"][0:13], "%y%m%d_%H%M%S"))
                data.fillna(0, inplace=True)
                data.replace(0, int(random.randrange(150, 200, 1)), True)
                # follow function for testing use only, when file is not good
                for col in data.columns.values:
                    for i in data.index.values:
                        data.loc[i, col] = int(random.randrange(1, 200, 1))
                self.time_log_data.append(data)
                # print(data)
        # print(self.file_time_data)

    def time_log_process_data(self, index_items, caller):
        """function used to combine and load data of the time log"""
        if caller == 0:
            self.top_processed_data = []
            self.file_names_top = []
        else:
            self.bot_processed_data = []
            self.file_names_bot = []
        for item in index_items:
            # check for valid input
            index = [item.parent().row(), item.row()]
            if caller == 0:
                self.file_names_top.append(item.data())
            else:
                self.file_names_bot.append(item.data())

            if len(index) != 2:
                return

            # parent node, combine all internal syringes
            time_gap = []
            current_data = pd.DataFrame()
            time_col = []

            if index[0] < 0:
                for i, current_index in enumerate(self.file_index[index[1]]):
                    # extract the time different between files, first file difference is 0
                    delta_in_minutes = 0
                    if i > 0:
                        current_data = current_data.append(self.time_log_data[current_index], ignore_index=True)
                        delta = self.file_time_data[current_index] - self.file_time_data[
                            self.file_index[index[1]][i - 1]]
                        delta_in_minutes = int(delta.total_seconds() // 60)
                        time_gap.append(delta_in_minutes)
                        time_col.extend(
                            [x + sum(time_gap) + 1 for x in range(len(self.time_log_data[current_index].index))])
                    else:
                        current_data = self.time_log_data[current_index]
                        time_gap.append(delta_in_minutes)
                        time_col = [x + 1 for x in range(len(current_data.index))]

            else:
                current_data = self.time_log_data[self.file_index[index[0]][index[1]]]
                time_col = [x + 1 for x in range(len(current_data.index))]
                current_data['Minutes'] = time_col
            current_data['Minutes'] = time_col
            if caller == 0:
                self.top_processed_data.append(current_data)
            else:
                self.bot_processed_data.append(current_data)
        print(self.top_processed_data)
        print(self.file_names_top)

    def data_transform(self, caller: int, function: Time_log_functions):
        """this function will change the data into the list accepted by plot widget"""
        line_thickness = 4
        if caller == 0:
            data_list = self.top_processed_data
            plot_widget = self.top_graph
            file_name = self.file_names_top
        else:
            data_list = self.bot_processed_data
            plot_widget = self.bot_graph
            file_name = self.file_names_bot
        plot_widget.clear()
        plot_widget.addLegend()
        plot_widget.plotItem.legend.setLabelTextColor(Qt.QColor(0, 0, 0))
        if function is Time_log_functions.TOTAL_SORTED:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Droplets")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        y = data["Total Sorted"].cumsum()
                        x = data["Minutes"]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Sorted Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.TOTAL_LOST:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Droplets")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        y = data["Total Lost From Lockout"].cumsum()
                        x = data["Minutes"]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Lost From Lockout Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.TOTAL_DROPLETS:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Droplets")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        y = data["Total Droplets"].cumsum()
                        x = data["Minutes"]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Droplets Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.POSITIVE_RATE:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Percentage(%)")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        droplets = data["Total Droplets"].cumsum()
                        positive = data["Total Sorted"].cumsum()
                        y = [i / j for i, j in zip(positive, droplets)]
                        x = data["Minutes"]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Droplets or Total Sorted Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.DROPLET_FREQUENCY:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Droplet/min")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        droplets = data["Total Droplets"].cumsum()
                        x = data["Minutes"]
                        y = [i / j for i, j in zip(droplets, x)]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Droplets Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.SORTED_RATE:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Sorted/min")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        y = data["Total Sorted"]
                        x = data["Minutes"]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Droplets Not in Log")
                else:
                    print("No Syringe Selected")
        elif function is Time_log_functions.LOCKED_OUT:
            plot_widget.setLabel('bottom', "Time(min)")
            plot_widget.setLabel('left', "Locked Out/min")
            for count, data in enumerate(data_list):
                color = pg.intColor(count)
                name = file_name[count]
                if data is not pd.DataFrame.empty:
                    try:
                        lost = data["Total Lost From Lockout"].cumsum()
                        x = data["Minutes"]
                        y = [i / j for i, j in zip(lost, x)]
                        plot_widget.addItem(pg.PlotDataItem(x, y, name=name, pen=pg.mkPen(color, width=line_thickness)))
                    except:
                        print("Total Lost Not in Log")
                else:
                    print("No Syringe Selected")

    def remove_item(self, index: list):
        """function for removing syringe or file"""
        # check for valid input
        if len(index) != 2:
            return

        # check if parent node
        if index[0] < 0:
            self.file_index.pop(index[1])
            self.file_model.removeRow(index[1])
            self.mode.pop(index[1])

        # child node
        else:
            del self.file_index[index[0]][index[1]]
            self.file_model.item(index[0]).removeRow(index[1])

            # delete syringe group if empty
            if not self.file_index[index[0]]:
                self.file_index.pop(index[0])
                self.file_model.removeRow(index[0])
                self.mode.pop(index[0])

        print(self.file_index)
        print(self.mode)

    def ok_clicked(self):
        """handler for ok clicked"""
        index_holder = []
        for item in self.file_list.selectedIndexes():
            # find all the index of selected item
            index_holder.append(item.row())
        index_holder.sort()
        if self.caller == 1:
            # this case handles the call request by time log

            if len(index_holder) > 0:
                # first add the syringe with the name
                syringe = Qt.QStandardItem(self.line_edit_name.text())
                self.file_model.appendRow(syringe)
                syringe_number = self.file_model.rowCount() - 1
                self.extract_mode_data(index_holder)
                for i in range(len(index_holder)):
                    item = Qt.QStandardItem(self.main_file_list.item(i).text())
                    self.file_model.item(syringe_number).appendRow(item)
                self.file_index.append(index_holder)
            self.hide()

        elif self.caller == 0:
            # this case handles the call request by window filters
            self.spawned_filter_counter += 1
            #  the number of root keys, and create new index
            new_index = (len([key for key in self.tree_dict.keys() if len(key) == 1]),)
            self.tree_dict[new_index] = {}
            self.tree_dict[new_index]['tree_standarditem'] = StandardItem(self.line_edit_name.text(), 12, set_bold=True)
            self.tree_dict[new_index]['tree_windowfilter'] = Filter_window.window_filter(self.ui, None, None,
                                                                                         None, None,
                                                                                         self.ui.comboBox_14_list,
                                                                                         index_holder)
            self.tree_model.appendRow(self.tree_dict[new_index]['tree_standarditem'])

    def close_clicked(self):
        """handle close button clicked"""
        self.hide()

    def extract_mode_data(self, index):
        """this function checks for the channels user selected, and add the dictionary entry into the mode variable"""
        checkbox_mode_list = [self.ch_1_checkbox.checkState(), self.ch_2_checkbox.checkState(),
                              self.ch_3_checkbox.checkState(), self.ch_4_checkbox.checkState()]
        channel_holder = []
        time_divide = ()
        units_multiplier = lambda text: 1 if text == "Minutes" else 60
        time_increment_raw = self.time_spinbox.value() * units_multiplier(self.time_combobox.currentText())
        # time delta used to divide files into its own time division
        time_delta = datetime.timedelta(hours=time_increment_raw//60, minutes=time_increment_raw%60)
        self.mode.append({})
        if sum(checkbox_mode_list) > 0:
            # this is when any checkbox is not default unchecked

            for count, checkbox_mode in enumerate(checkbox_mode_list):
                # unchecked case does not need to go into the dictionary
                if checkbox_mode == 1:
                    # this case handle when the user selects negative state for the channel
                    channel_holder.append((str(count + 1), False))
                elif checkbox_mode == 2:
                    # this case handle when user select this channel as positive
                    channel_holder.append((str(count + 1), True))

        if self.time_divide_checkbox.isChecked():
            self.mode[len(self.mode) - 1]["Time Divide Data"] = []
            time_divide = (self.time_spinbox.value(), self.time_combobox.currentText())
            self.mode[len(self.mode) - 1]["Time Divide"] = time_divide
            time_list = [self.file_time_data[i] for i in index]
            file_data = [self.time_log_data[i] for i in index]
            starting_time = time_list[0]
            # data holder hserve as the buffer for single time points, each file time point start at 0
            data_holder = pd.DataFrame()
            # syringe data holder serve as the holder for the entire syringe cluster, with scaled time column
            syringe_data_holder = pd.DataFrame()
            # time col holds the time data, append to the dataframe at the end
            time_col = []
            number_of_increment = 0
            for time, data in zip(time_list, file_data):
                # while loop for incrementing the counter
                time_from_start = time - starting_time
                time_divide_in_minutes = time_delta.seconds // 60
                while time_delta*number_of_increment <= time_from_start < time_delta*(number_of_increment+1):
                    # reset data holder and add the increment by 1
                    number_of_increment += 1
                    data_holder = pd.DataFrame()
                if len(data_holder.index) == 0:
                    # data holder is empty, new time point, start time point time at 0 minutes

                    number_of_loop = len(data.index) // time_divide_in_minutes + 1
                    for i in range(number_of_loop):
                        # for loop with more than 1 iteration, it means file longer than a time point, aka split the
                        # the files into multiple time point
                        if number_of_loop-1 == i:
                            # last iteration, check for end of length, do not clear the data holder, next file might
                            # be in the same slot
                            data_holder.append(data.iloc[i * time_divide_in_minutes:len(data.index)])
                            syringe_data_holder.append(data_holder)
                            data_holder["Minutes"] = [j + 1 for j in range(len(data_holder.index))]
                            self.mode[len(self.mode) - 1]["Time Divide Data"].append(data_holder)
                            time_col.append([i * time_divide_in_minutes + 1 + j for j in len(data_holder.index)])
                            # add the entry to the list
                            if self.time_combobox.currentText() == "Minutes":
                                entry_name = "T-" + str(number_of_increment*time_divide_in_minutes) + "Minutes"
                            else:
                                entry_name = "T-" + str(number_of_increment * self.time_spinbox.value()) + "Hours"
                            item = Qt.QStandardItem(entry_name)
                            self.file_model.item(self.file_model.rowCount() - 1).appendRow(item)
                        else:
                            # not last iteration, create a child node every loop, increment the counter
                            data_holder = data.iloc[i*time_divide_in_minutes:(i+1)*time_divide_in_minutes]

                            # add the temp data into the main file
                            syringe_data_holder.append(data_holder)
                            data_holder["Minutes"] = [j + 1 for j in range(len(data_holder.index))]
                            self.mode[len(self.mode) - 1]["Time Divide Data"].append(data_holder)

                            # append the time data into the time_col before clearing temp data
                            time_col.append([i * time_divide_in_minutes + 1 + j for j in len(data_holder.index)])
                            data_holder = pd.DataFrame()

                            # add the time point into the file model
                            if self.time_combobox.currentText() == "Minutes":
                                entry_name = "T-" + str(number_of_increment*time_divide_in_minutes) + "Minutes"
                            else:
                                entry_name = "T-" + str(number_of_increment * self.time_spinbox.value()) + "Hours"
                            item = Qt.QStandardItem(entry_name)
                            self.file_model.item(self.file_model.rowCount() - 1).appendRow(item)
                            number_of_increment += 1
                else:
                    # this case is when current data is not empty, thus the time point can possibly include more data
                    # the while loop before also checks to ensure that the file starts in this time slot
                    start_index = len(data_holder.index)
                    time_from_start - time_delta*number_of_increment
                    if len(data.index) > time_divide_in_minutes - start_index:


        if channel_holder:
            self.mode[len(self.mode)-1]["Positive Channels"] = channel_holder

        if time_divide:
            self.mode[len(self.mode)-1]["Time Divide"] = time_divide

        print(self.mode)


if __name__ == "__main__":
    freeze_support()
    import sys

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    ui = TimeLogFileSelectionWindow()
    ui.show()
    sys.exit(app.exec_())
