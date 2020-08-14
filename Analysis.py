# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here


class Droplet(object):
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __int__(self):
        self.width = 0
        self.peak_voltage = [0.0, 0.0, 0.0, 0.0]


def peak_detect():
    """this function detects if a peak exist in for each droplet data set"""


def width_detect(threshold, min, max):
    """this function calculate the width specified at a given voltage and size"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import os
import Helper
import time
from itertools import islice
import numpy as np



# os.chdir('C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/EXP200225-6')
# Ch = pd.read_csv('200225_171057 AFB AFB Ch2 Hit.csv',header = None)

os.chdir('C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/Test_file_1')
Ch = pd.read_csv('200225_171057 AFA Peak Record.csv',header = 2)
Ch.columns =[0,1,2,3] 

start = time.time()

under_sample_factor = 1
under_sample_range = int(1000 / under_sample_factor)
# select channel and threshold
threshold = 2


Ch = Ch -threshold
peak_total = []
width_total = []

for channel in range(4):
    sign = Ch[channel].map(np.sign)
    diff1 = sign.diff(periods=1).fillna(0)
    df1 = Ch[channel].loc[diff1[diff1 != 0].index]
    index_list = df1.index

#     sample_size = 100
    sample_size = under_sample_range
    current_width = 0
    peak = []
    width = []



    for i in range(len(index_list)):
        print(sample_size,"/",len(Ch),", channel",channel)

        if index_list[i] > sample_size:  
            peak.append(round((Ch[channel][sample_size - under_sample_range:sample_size].max() + threshold),3))
            width.append(current_width)
            current_width = 0
            sample_size = sample_size + under_sample_range
            # check if 0 width exist
            for x in range((index_list[i] - sample_size) // under_sample_range):
                peak.append(round((Ch[channel][sample_size - under_sample_range:sample_size].max() + threshold),3))
                width.append(0)
                sample_size = sample_size + under_sample_range

        if df1[index_list[i-1]] >= 0:
            if df1[index_list[i]] <= 0:
                current_width = max(index_list[i] - index_list[i-1],current_width)

    # append the last few peaks and widths
    peak.append(round((Ch[channel][sample_size - under_sample_range:sample_size].max() + threshold),3))
    width.append(current_width)   
    print(sample_size,"/",len(Ch),", channel",channel)
    
    # append widths lower then threshold at last, and peaks
    for x in range((len(Ch) - sample_size) // under_sample_range):
        sample_size = sample_size + under_sample_range
        print(sample_size,"/",len(Ch),", channel",channel)
        peak.append(round((Ch[channel][sample_size - under_sample_range:sample_size].max() + threshold),3))
        width.append(0)
    

    peak_total.append(peak)
    width_total.append(width)

end = time.time()
print(end - start)
# print(width_total)
# print(peak_total)
