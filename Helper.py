# this is the file contains all the helper functions
# all functions that serves a generic purpose should be implemented here

import os, csv


def project_namelist(file_dir):
    """function for loading all file names for the project, returns as dictionary"""
    name_dict = {"Ch1": "",
                 "Ch2": "",
                 "Ch3": "",
                 "Ch1-2": "",
                 "Ch1-3": "",
                 "Ch2-3": "",
                 "Locked": "",
                 "Param": "",
                 "Summary": "",
                 }
    if os.path.isfile(file_dir) and file_dir.rfind("Peak Record") >= 0:
        root_folder = os.path.dirname(file_dir)
        file_name = os.path.basename(file_dir)
        time_stamp = file_name[0:13]
        file_list = os.listdir(root_folder)
        for file in file_list:
            if file.rfind(str(time_stamp)) >= 0:
                for key in name_dict:
                    if file.rfind(key) >= 0:
                        name_dict[key] = file
    return name_dict.copy()


class Stats:
    """this class holds all the parameter"""
    def __int__(self, file_path):
        print(file_path)
        stats_dict = {"Starting Time": "",
                      "Ending  Time": "",
                      "Total Run Time": "",
                      "Total Sorted": "",
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
                      "Total Dispensed": "",
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
        self.total_sorted = stats_dict["Total Sorted"]
        self.total_lost = stats_dict["Total Lost From Lockout"]
        self.ch1_hit = stats_dict["Negative Ch 1 Hit"]
        self.ch2_hit = stats_dict["Negative Ch 2 Hit"]
        self.ch3_hit = stats_dict["Negative Ch 3 Hit"]
        self.ch12_hit = stats_dict["Negative Ch 1-2 Hit"]
        self.ch13_hit = stats_dict["Negative CH 1-3 Hit"]
        self.ch23_hit = stats_dict["Negative Ch 2-3 Hit"]
        self.undersample_factor = stats_dict["UnderSample Factor"]


if __name__ == "__main__":
    import Helper
    print(project_namelist(r"D:\Users\QIwei Fu\Downloads\EXP200601-2\EXP200601-2/200601_130231 AFB Peak Record.csv"))
    stats = Helper.Stats()
    stats.__int__(r"D:\Users\QIwei Fu\Downloads\EXP200601-2\EXP200601-2/200601_130231 AFB Summary.csv")
    print(stats.total_runtime)




