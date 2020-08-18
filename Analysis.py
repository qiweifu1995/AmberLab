# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here
import pandas as pd
import time
import numpy as np

class Droplet:
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __init__(self, width, peaks):
        self.width = width
        self.peak_voltage = peaks



class file_extracted_data_Qing:
    def __init__(self, current_file_dict, threshold=0, width_enable=True, channel=0, chunksize=1000, header=2):
        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            self.Ch1list, self.Ch1width = self.extract(current_file_dict["Ch1 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            self.Ch2list, self.Ch2width = self.extract(current_file_dict["Ch2 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            self.Ch3list, self.Ch3width = self.extract(current_file_dict["Ch3 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            self.Ch12list, self.Ch12width = self.extract(current_file_dict["Ch1-2"], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            self.Ch13list, self.Ch13width = self.extract(current_file_dict["Ch1-3"], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch2-3"] != "":
            self.Ch23list, self.Ch23width = self.extract(current_file_dict["Ch2-3"], threshold, width_enable, channel, chunksize, header)
        
        print("Extracting Peak...")
        self.Peaklist, self.Peakwidth = self.extract(current_file_dict["Peak Record"], threshold, width_enable, channel, 1000 , 2)
        
        print("Done")
            
    def extract(self, file, threshold=1, width_enable=True, channel=0, chunksize=100, header=0):

        # select channel and threshold
        peak = []
        width =[]

        for Ch in pd.read_csv(file, chunksize=chunksize, header=header):
            Ch.columns =[0,1,2,3] 
            sign = Ch - threshold
            sign[sign > 0] = 1
            sign[sign < 0] = -1

            diff1 = sign[channel].diff(periods=1).fillna(0)
            df1 = sign[channel].loc[diff1[diff1 != 0].index]
            index_list = df1.index


            peak.append(round(Ch[channel].max(),3))

            if width_enable == True:
                current_width = 0

                for i in range(len(index_list)):
                    if df1[index_list[i-1]] >= 0:
                        if df1[index_list[i]] <= 0:
                            current_width = max(index_list[i] - index_list[i-1],current_width)

                if current_width == 0:
                    width.append(0)
                else:
                    width.append(current_width)
                    current_width = 0
        return (peak, width)

    
    
class file_extracted_data:
    def __init__(self, current_file_dict, threshold=0, width_enable=True, channel=0, chunksize=1000, header=0):

        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            self.stats_Ch1 = self.extract(current_file_dict["Ch1 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            self.stats_Ch2 = self.extract(current_file_dict["Ch2 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            self.stats_Ch3 = self.extract(current_file_dict["Ch3 "], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            self.stats_Ch12 = self.extract(current_file_dict["Ch1-2"], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            self.stats_Ch13 = self.extract(current_file_dict["Ch1-3"], threshold, width_enable, channel, chunksize, header)
        if current_file_dict["Ch2-3"] != "":
            print("Extracting Ch2-3...")
            self.stats_Ch23 = self.extract(current_file_dict["Ch2-3"], threshold, width_enable, channel, chunksize, header)
            
        print("Extracting Peak...")
        self.stats_Peak = self.extract(current_file_dict["Peak Record"], threshold, width_enable, channel, 1000 , 2)

        print("Done.")

    def width_detect(self, data, threshold, width, above_tresh):
        """this function calculate the width specified at a given voltage and size"""
        if above_tresh:
            if threshold > data:
                return width + 1, True, False
            else:
                return 0, False, True
        else:
            if threshold > data:
                return 1, True, False
            else:
                return 0, False, False


    def extract(self, file, threshold=0, width_enable=True, width_channel=0, chunksize=1000, header=2):
        droplet_stats = []
        for chunk in pd.read_csv(file, chunksize=chunksize, header=header, iterator=True):
            max_holder = [0, 0, 0, 0]
            width_holder = 0
            width_max_holder = 0
            above_thresh = False
            for row in chunk.itertuples(index=False, name=None):
                for ch in range(4):
                    data = row[ch]
                    max_holder[ch] = max(max_holder[ch], data)
                    if ch == width_channel and width_enable:
                        width_holder, above_thresh, test_max = self.width_detect(data, threshold, width_holder, above_thresh)
                        if test_max:
                            width_max_holder = max(width_max_holder, width_holder)
            droplet_stats.append(Droplet(width_max_holder, max_holder))
        return droplet_stats


  
# os.chdir('C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/EXP200225-6')

# current_file_list = {'Ch1 ': '200225_171057 AFB AFB Ch1 Hit.csv', 'Ch2 ': '200225_171057 AFB AFB Ch2 Hit.csv', 'Ch3 ': '200225_171057 AFB AFB Ch3 Hit.csv', 'Ch1-2': '200225_171057 AFB AFB Ch1-2 Hit.csv', 'Ch1-3': '200225_171057 AFB AFB Ch1-3 Hit.csv', 'Ch2-3': '200225_171057 AFB AFB Ch2-3 Hit.csv', 'Locked': '', 'Param': '200225_171057 AFB Param.csv', 'Summary': '200225_171057 AFB Summary.csv', 'Peak Record': '200225_171057 AFB Peak Record.csv', 'Raw Time Log': '200225_171057 AFBRaw Time Log.csv', 'Time Log': '200225_171057 AFBRaw Time Log.csv', 'Root Folder': 'C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/EXP200225-6'}
# a = file_extracted_data(current_file_list, 2, True,0, 100, 0)
# a.stats_Ch2
