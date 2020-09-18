# this is the file contains all the helper functions
# all functions that serves a generic purpose should be implemented here

import os, csv


def project_namelist(file_dir):
    """function for loading all file names for the project, returns as dictionary"""
    name_dict = {"Ch1 ": "",
                 "Ch2 ": "",
                 "Ch3 ": "",
                 "Ch1-2": "",
                 "Ch1-3": "",
                 "Ch2-3": "",
                 "Locked": "",
                 "Param": "",
                 "Summary": "",
                 "Peak Record": "",
                 "Raw Time Log": "",
                 "Time Log": "",
                 "Root Folder": ""
                 }
    if os.path.isfile(file_dir) and file_dir.rfind("Peak Record") >= 0:
        root_folder = os.path.dirname(file_dir)
        file_name = os.path.basename(file_dir)
        time_stamp = file_name[0:13]
        file_list = os.listdir(root_folder)
        name_dict["Peak Record"] = file_name
        name_dict["Root Folder"] = root_folder
        for file in file_list:
            if file.rfind(str(time_stamp)) >= 0:
                for key in name_dict:
                    if file.rfind(key) >= 0:
                        name_dict[key] = file
    return name_dict.copy()


class Stats:
    """this class holds all the parameter"""
    def __init__(self, file_path):
        print(file_path)
        stats_dict = {"Starting Time": "",
                      "Ending  Time": "",
                      "Total Run Time": "",
                      "Total Sorted  ": "",
                      "Total Droplets": "",
                      "Total Lost From Lockout": "",
                      "Sorting Positive Rate": "",
                      "DT Total Cells": "",
                      "UnderSample Factor": "",
                      "Negative Ch 1 Hit": "",
                      "Negative Ch 2 Hit": "",
                      "Negative Ch 3 Hit": "",
                      "Negative Ch 1-2 Hit": "",
                      "Negative CH 1-3 Hit": "",
                      "Negative Ch 2-3 Hit": "",
                      "Total Dispensed ": "",
                      "Dispense Missed": ""}
        if os.path.isfile(file_path) and file_path.rfind("Summary") >= 0:
            print("run")
            with open(file_path) as param_file:
                cell_name = []
                stats_reader = csv.reader(param_file, delimiter=",")
                for lines in stats_reader:
                    # reading all the lines in the file. append all key word into array
                    # if not keyword then append empty string
                    # line after key word is where param data is read
                    if len(cell_name) == 0:
                        for field in lines:
                            if field in stats_dict:
                                cell_name.append(field)
                            else:
                                cell_name.append("")
                        if cell_name.count("") == len(cell_name):
                            cell_name.clear()
                    else:
                        for data in lines:
                            stats_key = cell_name.pop(0)
                            if stats_key in stats_dict:
                                stats_dict[stats_key] = data
                        cell_name.clear()
        self.start_time = stats_dict["Starting Time"]
        self.end_time = stats_dict["Ending  Time"]
        self.total_runtime = stats_dict["Total Run Time"]
        self.total_droplets = stats_dict["Total Droplets"]
        self.total_sorted = stats_dict["Total Sorted  "]
        self.total_lost = stats_dict["Total Lost From Lockout"]
        self.ch1_hit = stats_dict["Negative Ch 1 Hit"]
        self.ch2_hit = stats_dict["Negative Ch 2 Hit"]
        self.ch3_hit = stats_dict["Negative Ch 3 Hit"]
        self.ch12_hit = stats_dict["Negative Ch 1-2 Hit"]
        self.ch13_hit = stats_dict["Negative CH 1-3 Hit"]
        self.ch23_hit = stats_dict["Negative Ch 2-3 Hit"]
        self.under_sample_factor = stats_dict["UnderSample Factor"]
        self.total_dispensed = stats_dict["Total Dispensed "]
        self.dispense_missed = stats_dict["Dispense Missed"]


def rgb_select(channel):
    if channel == 0:
        r = 0
        g = 255
        b = 0
    elif channel == 1:
        r = 255
        g = 0
        b = 0
    elif channel == 2:
        r = 0
        g = 0
        b = 255
    elif channel == 3:
        r = 255
        g = 165
        b = 0
    else:
        r = 0
        g = 255
        b = 0
    return r, g, b


def histogram_bin(range_max, increment):
    """funciton that return the bin"""
    x_holder = 0
    bin_edge = []
    increment = increment
    while x_holder < range_max:
        bin_edge.append(x_holder)
        x_holder += increment
    bin_edge.append(x_holder)
    return bin_edge


class ui_state:
    """this class holds all the current state of the UI"""
    def __init__(self):
        self.all_check = False
        self.ch1_check = False
        self.ch2_check = False
        self.ch3_check = False
        self.ch1_2_check = False
        self.ch1_3_check = False
        self.ch2_3_check = False
        self.file_select = -1
        self.gating_channel_select = -1
        self.gating_bins = 0
        self.gating_voltage = 0
        self.scatter_channel_select_x = -1
        self.scatter_channel_select_y = -1
        self.scatter_gate_voltage_x = 0
        self.scatter_gate_voltage_y = 0
        self.sweep_channel_select = -1
        self.sweep_bins = 0
        self.sweep_file_1 = -1
        self.sweep_file_2 = -1

    def working_file_update_check(self, update_state=True, file=None, chall=None, ch1=None, ch2=None,
                                  ch3=None, ch1_2=None, ch1_3=None, ch2_3=None):
        """checks if checkbox are updated and needs to be refreshed"""
        changed = False
        if file is not None and self.file_select != file:
            changed = True
        elif chall is not None and self.all_check != chall:
            changed = True
        elif ch1 is not None and self.ch1_check != ch1:
            changed = True
        elif ch2 is not None and self.ch2_check != ch2:
            changed = True
        elif ch3 is not None and self.ch3_check != ch3:
            changed = True
        elif ch1_2 is not None and self.ch1_2_check != ch1_2:
            changed = True
        elif ch1_3 is not None and self.ch1_3_check != ch1_3:
            changed = True
        elif ch2_3 is not None and self.ch2_3_check != ch2_3:
            changed = True
        if update_state:
            if file is not None:
                self.file_select = file
            if chall is not None:
                self.all_check = chall
            if ch1 is not None:
                self.ch1_check = ch1
            if ch2 is not None:
                self.ch2_check = ch2
            if ch3 is not None:
                self.ch3_check = ch3
            if ch1_2 is not None:
                self.ch1_2_check = ch1_2
            if ch1_3 is not None:
                self.ch1_3_check = ch1_3
            if ch2_3 is not None:
                self.ch2_3_check = ch2_3
        return changed

    def gating_update(self, update_state=True, channel_select=None, bins=None, gate_voltage=None):
        """keeps track of states in gating"""
        replot, recalculate = False
        if channel_select is not None and channel_select != self.gating_channel_select:
            replot = True
        elif bins is not None and bins != self.gating_bins:
            replot = True
        if gate_voltage is not None and gate_voltage != self.gating_voltage:
            recalculate = True
        if update_state:
            if channel_select is not None:
                self.gating_channel_select = channel_select
            if bins is not None:
                self.gating_bins = bins
            if gate_voltage is not None:
                self.gating_voltage = gate_voltage
        return replot, recalculate

    def scatter_update(self, update_state=True, x_select=None, y_select=None, x_gate=None, y_gate=None):
        """keep track of state in scatter tab"""
        replot, recalculate = False
        if x_select is not None and x_select != self.scatter_channel_select_x:
            replot = True
        elif y_select is not None and y_select != self.scatter_channel_select_y:
            replot = True
        if x_gate is not None and x_gate != self.scatter_gate_voltage_x:
            recalculate = True
        elif y_gate is not None and y_gate != self.scatter_gate_voltage_y:
            recalculate = True
        if update_state:
            if x_select is not None:
                self.scatter_channel_select_x = x_select
            if y_select is not None:
                self.scatter_channel_select_y = y_select
            if x_gate is not None:
                self.scatter_gate_voltage_x = x_gate
            if y_gate is not None:
                self.scatter_gate_voltage_y = y_gate
        return replot, recalculate

    def sweep_update(self, update_state=False, channel_select=None, bins=None, file1=None, file2=None):
        """keep track of state in sweep tab"""
        replot1, replot2 = False
        if file1 is not None and file1 != self.sweep_file_1:
            replot1 = True
        if file2 is not None and file2 != self.sweep_file_2:
            replot2 = True
        if channel_select is not None and channel_select != self.sweep_channel_select:
            replot1 = True
            replot2 = True
        elif bins is not None and bins != self.sweep_bins:
            replot1 = True
            replot2 = True
        if update_state:
            if channel_select is not None:
                self.sweep_channel_select = channel_select
            if bins is not None:
                self.sweep_bins = bins
            if file1 is not None:
                self.sweep_file_1 = file1
            if file2 is not None:
                self.sweep_file_2 = file2
        return replot1, replot2




if __name__ == "__main__":
    state = ui_state()
    update = state.checkbox_update_check(True,ch2=True)
    print(update)
    print(state.ch2_check)
    print(state.ch1_check)





