# this is the file contains all the helper functions
# all functions that serves a generic purpose should be implemented here

import os


def project_namelist(file_dir):
    """function for loading all file names for the project, returns as dictionary"""
    name_dict = {"Ch1": "",
                 "Ch2": "",
                 "Ch3": "",
                 "Ch1-2": "",
                 "Ch1-3": "",
                 "Ch2-3": ""}
    if os.path.isfile(file_dir) and file_dir.rfind("Peak Record") > 1:
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

