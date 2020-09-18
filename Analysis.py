# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here
import pandas as pd
import time
import numpy as np
import os
import math

class Droplet:
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __init__(self, width, peaks):
        self.width = width
        self.peak_voltage = peaks



class file_extracted_data_Qing:
    def __init__(self, current_file_dict, threshold=0, width_enable=True, channel=0, chunksize=1000, header=2):
        self.analog_file = {} 
        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            list1, width1 = self.extract(current_file_dict["Ch1 "], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch1 "]] = [list1, width1]
            
        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            list2, width2 = self.extract(current_file_dict["Ch2 "], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch2 "]] = [list2, width2]
        
        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            list3, width3 = self.extract(current_file_dict["Ch3 "], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch3 "]] = [list3, width3]  
        
        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            list12, width12 = self.extract(current_file_dict["Ch1-2"], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch1-2"]] = [list12, width12]        
        
        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            list13, width13  = self.extract(current_file_dict["Ch1-3"], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch1-3"]] = [list13, width13]      
        
        if current_file_dict["Ch2-3"] != "":
            print("Extracting Ch2-3...")
            list23, width23 = self.extract(current_file_dict["Ch2-3"], threshold, width_enable, channel, 200, header)
            self.analog_file[current_file_dict["Ch2-3"]] = [list23, width23] 
            
        print("Extracting Peak...")
        Peaklist, Peakwidth = self.extract(current_file_dict["Peak Record"], threshold, width_enable, channel, 1000 , 2)
        self.analog_file[current_file_dict['Peak Record']] = [Peaklist, Peakwidth]  
            
        print("Done")
            
    def extract(self, file, threshold=2, width_enable=True, width_channel=0, user_set_chunk_size=100, header=0):

        # select channel and threshold
        peak = [[],[],[],[]]
        width =[]
        count = 0
        
        for Ch in pd.read_csv(file, chunksize=500000, header=header):
            count += 1
            print(count)
            Ch.columns =[0,1,2,3] 

            for channel in range(4):
                for row in range(0,len(Ch),user_set_chunk_size):
                    peak[channel].append((round(Ch.iloc[row:(row+user_set_chunk_size),channel].max(),3)))

                if channel == width_channel and width_enable:
                    sign = Ch - threshold
                    sign[sign > 0] = 1
                    sign[sign < 0] = -1

                    diff1 = sign[channel].diff(periods=1).fillna(0)
                    df1 = sign[channel].loc[diff1[diff1 != 0].index]
                    index_list = df1.index
        #             print(df1.index)


                    row_chunk = user_set_chunk_size
                    current_width = 0
                    for i in range(len(index_list)):
                            # 0~99
                        if df1.index[i] > row_chunk:
        #                     print(df1.index[i],current_width)
        #                     print((df1.index[i]-row_chunk)//user_set_chunk_size)
                            width.append(current_width)
                            current_width = 0
                            for number_of_skip_chunck in range((df1.index[i]-row_chunk)//user_set_chunk_size):
                                row_chunk += user_set_chunk_size
                            row_chunk += user_set_chunk_size
                        if df1[index_list[i-1]] >= 0:
                            if df1[index_list[i]] <= 0:
                                current_width = max(index_list[i] - index_list[i-1],current_width)
        #                         print(df1.index[i],current_width)
                    width.append(current_width)
        #     break 
        for col in range(4):
            peak[col] = [0 if math.isnan(x) else x for x in peak[col]]

                
                    
        return (peak, width)

    
    
class file_extracted_data:
    def __init__(self, current_file_dict, threshold=0, width_enable=True, channel=0, chunksize=1000, header=0):
        self.analog_file = {} 
        
        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            self.analog_file[current_file_dict["Ch1 "]] =  self.extract(current_file_dict["Ch1 "], threshold, width_enable, channel, chunksize, header)
            
        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            self.analog_file[current_file_dict["Ch2 "]]  = self.extract(current_file_dict["Ch2 "], threshold, width_enable, channel, chunksize, header)
            
        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            self.analog_file[current_file_dict["Ch3 "]] = self.extract(current_file_dict["Ch3 "], threshold, width_enable, channel, chunksize, header)
            
        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            self.analog_file[current_file_dict["Ch1-2"]] = self.extract(current_file_dict["Ch1-2"], threshold, width_enable, channel, chunksize, header)

            
        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            self.analog_file[current_file_dict["Ch1-3"]] = self.extract(current_file_dict["Ch1-3"], threshold, width_enable, channel, chunksize, header)
            
        if current_file_dict["Ch2-3"] != "":
            print("Extracting Ch2-3...")
            self.analog_file[current_file_dict["Ch2-3"]] = self.extract(current_file_dict["Ch2-3"], threshold, width_enable, channel, chunksize, header)
            
            
        print("Extracting Peak...")
        self.analog_file[current_file_dict['Peak Record']] = self.extract(current_file_dict["Peak Record"], threshold, width_enable, channel, 1000 , 2)


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

  
  

# time1 = time.time()
# # os.chdir('C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/EXP200225-6')
# os.chdir('C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/Test_file_1')

# current_file_list = {'Ch1 ': '', 
#                      'Ch2 ': '', 
#                      'Ch3 ': '', 
#                      'Ch1-2': '', 
#                      'Ch1-3':'' , 
#                      'Ch2-3': '', 
#                      'Locked': '',
#                      'Param': '200225_171057 AFB Param.csv', 
#                      'Summary': '200225_171057 AFB Summary.csv', 
#                      'Peak Record': '200225_171057 AFA Peak Record.csv', 
#                      'Raw Time Log': '200225_171057 AFBRaw Time Log.csv', 
#                      'Time Log': '200225_171057 AFBRaw Time Log.csv', 
#                      'Root Folder': 'C:/Users/qingy/Desktop/Jupiter/Internship_Amberstone/AmberLab/EXP200225-6'}
# ### Qing's 
# a = file_extracted_data_Qing(current_file_list, 2, True,0, 100, 0)
# # print(a.analog_file['200225_171057 AFA Peak Record.csv'][0])


# ### Qiwei's 
# # a = file_extracted_data(current_file_list, 2, True,0, 100, 0)
# # print(a.analog_file['200225_171057 AFB AFB Ch1 Hit.csv'][1].width)
# # print(a.analog_file['200225_171057 AFA Peak Record.csv'][1].peak_voltage)



# print(time.time()-time1)
