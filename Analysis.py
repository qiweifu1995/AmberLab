# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here
import pandas as pd
import time
import numpy as np
import os
import csv
import math
import concurrent.futures


class Droplet:
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __init__(self, width, peaks):
        self.width = width
        self.peak_voltage = peaks



class file_extracted_data_Qing:
    def __init__(self, current_file_dict, threshold, peak_threshold, width_min=0, width_max=1000, width_enable=True, peak_enable = False, channel=0, chunksize=1000, header=2, ch1_count="1", ch2_count="1", ch3_count="1", ch12_count="1", ch13_count="1", ch23_count="1", Droplet_Record_count="1", total_count="1"):
        self.analog_file = {}
        peak_file_chunksize = 1000
        self.threshold = threshold
        
        # prevent /0 error
        if chunksize == 0:
            chunksize = 1000

        if ch1_count == '0':
            ch1_count = '1'
        if ch2_count == '0':
            ch2_count = '1'
        if ch3_count == '0':
            ch3_count = '1'
        if ch12_count == '0':
            ch12_count = '1'
        if ch13_count == '0':
            ch13_count = '1'
        if ch23_count == '0':
            ch23_count = '1'
        if Droplet_Record_count == '0':
            Droplet_Record_count = '1'
        if total_count == '0':
            total_count = '1'
    
    
        
        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            list1, width1, num_peaks1 = self.extract_parallel2(current_file_dict["Ch1 "], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1', ch1_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch1 "]] = [list1, width1, num_peaks1]

        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            list2, width2, num_peaks2 = self.extract_parallel2(current_file_dict["Ch2 "], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch2', ch2_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch2 "]] = [list2, width2, num_peaks2]

        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            list3, width3, num_peaks3 = self.extract_parallel2(current_file_dict["Ch3 "], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch3', ch3_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch3 "]] = [list3, width3, num_peaks3]

        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            list12, width12, num_peaks12 = self.extract_parallel2(current_file_dict["Ch1-2"], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1_2', ch12_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch1-2"]] = [list12, width12]

        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            list13, width13, num_peaks13 = self.extract_parallel2(current_file_dict["Ch1-3"], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1_3', ch13_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch1-3"]] = [list13, width13, num_peaks13]

        if current_file_dict["Ch2-3"] != "":
            print("Extracting Ch2-3...")
            list23, width23, num_peaks23 = self.extract_parallel2(current_file_dict["Ch2-3"], self.threshold, width_enable, 
                                                                  peak_enable, channel, chunksize, header, 
                                                                  'Ch2_3', ch23_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Ch2-3"]] = [list23, width23, num_peaks23]

        if current_file_dict["Droplets Extracted Data"] != "":
            print("Importing Extracted Droplet Record...")
            listDR, widthDR, num_peaksDR = self.extracted_data_loader(current_file_dict["Droplets Extracted Data"])

            self.analog_file[current_file_dict["Droplet Record"]] = [listDR, widthDR, num_peaksDR]
        elif current_file_dict["Droplet Record"] != "":
            print("Extracting Droplet Record...")
            listDR, widthDR, num_peaksDR = self.extract_parallel2(current_file_dict["Droplet Record"], self.threshold, width_enable, peak_enable, channel, chunksize, header, 'Droplet Record', Droplet_Record_count, peak_threshold, width_min, width_max)

            self.analog_file[current_file_dict["Droplet Record"]] = [listDR, widthDR, num_peaksDR]
            
        print("Extracting Peak... Parallel")
        start = time.time()
        Peaklist, Peakwidth, NumPeaks = self.extract_parallel2(current_file_dict["Peak Record"], self.threshold, width_enable,
                                                     peak_enable, channel, 1000, 2, 'Peak Record', total_count,
                                                     peak_threshold, width_min, width_max)
        self.analog_file[current_file_dict['Peak Record']] = [Peaklist, Peakwidth, NumPeaks]
        end = time.time()
        print("parallel extrack time: ", str(start-end))
        """
        print("Extracting Peak...")
        start = time.time()
        Peaklist, Peakwidth, NumPeaks = self.extract(current_file_dict["Peak Record"], self.threshold, width_enable, peak_enable, channel, 1000 , 2, 'Peak Record', total_count, peak_threshold, width_min, width_max)
        self.analog_file[current_file_dict['Peak Record']] = [Peaklist, Peakwidth, NumPeaks]
        end = time.time()
        print("normal extrack time", str(start-end))
        """
        for i in range(4):
            print("ch", i, " Peaklist len: ", len(Peaklist[i]))
            print("ch", i, "Peakwidth len: ", len(Peakwidth[i]))
            print("ch", i, "NumPeak len: ", len(NumPeaks[i]))
        print("Done")

    def extract(self, file, threshold,
                width_enable=True, peak_enable = False, width_channel=0, user_set_chunk_size=200, header=0,
                channel_name = "N/A", channel_count = "1", peak_threshold=1, peak_min=0, peak_max=1000):

        # select channel and threshold
        peak = [[],[],[],[]]
        width =[[],[],[],[]]
        peak_counts = [[],[],[],[]]
        current_row_number = 0
        row_chunk = 0
        peak_row_count = 0
        row_count = 0
        for Ch in pd.read_csv(file, chunksize=20000000, header=header):
            start = time.time()
            Ch.columns =[0,1,2,3]
            row_count += len(Ch)
            progress_percentage = round(((row_count+1)/(float(channel_count)*user_set_chunk_size))*100,2)
            print(channel_name,progress_percentage,"%")

            current_row_number = row_chunk + user_set_chunk_size
            for channel in range(4):
                loop_tracker = 0
                if peak_enable:
                    for row in range(0,len(Ch),user_set_chunk_size):
                        peak[channel].append((round(Ch.iloc[row:(row+user_set_chunk_size),channel].max(),3)))

                if width_enable:
                    sign = Ch[channel] - threshold[channel]
                    sign[sign > 0] = 1
                    sign[sign < 0] = -1

                    diff1 = sign.diff(periods=1).fillna(0)
                    df1 = sign.loc[diff1[diff1 != 0].index]
                    index_list = df1.index
                    row_chunk = current_row_number
                    current_width = 0
                    for i in range(1,len(index_list)):
                            # 0~99
                        if df1.index[i] > row_chunk:
                            width[channel].append(current_width)
                            current_width = 0
                            for number_of_skip_chunck in range((df1.index[i]-row_chunk)//user_set_chunk_size):
                                width[channel].append(current_width)
                                row_chunk += user_set_chunk_size
                            row_chunk += user_set_chunk_size
                            continue
                        if df1[index_list[i-1]] >= 0:
                            if df1[index_list[i]] <= 0:
                                current_width = max(index_list[i] - index_list[i-1],current_width)

                    width[channel].append(current_width)

                    for number_of_skip_chunck_after in range(round(len(Ch)/user_set_chunk_size) -
                                                             (len(width[channel]) -
                                                              round((current_row_number-user_set_chunk_size)/user_set_chunk_size))):
                        row_chunk += user_set_chunk_size
                        width[channel].append(0)

                    """Code for peak extraction starts here"""

                    peaks_signs = Ch[channel] - peak_threshold[channel]
                    peaks_signs[peaks_signs > 0] = 1
                    peaks_signs[peaks_signs < 0] = -1
                    edges = peaks_signs.diff(periods=1).fillna(0)
                    edges_index = peaks_signs.loc[edges[edges != 0].index]
                    edges_index_list = edges_index.index
                    peak_row_count = current_row_number-user_set_chunk_size
                    number_of_peaks = 0
                    for i in range(1,len(edges_index_list)): #check for each direction changing index
                        """this case deal with when current edge is in next droplet, return peaks count"""
                        while edges_index.index[i] >= peak_row_count + user_set_chunk_size:
                            peak_counts[channel].append(number_of_peaks)
                            number_of_peaks = 0
                            peak_row_count += user_set_chunk_size
                            loop_tracker += user_set_chunk_size
                            """this case deal with when direction change is with the next dorplet"""
                        if edges_index[edges_index_list[i-1]] >= 0 and edges_index_list[i-1] >= peak_row_count:
                            if edges_index[edges_index_list[i]] <= 0:
                                peak_width = edges_index_list[i] - edges_index_list[i-1]
                                if peak_min[channel] <= peak_width <= peak_max[channel]:
                                    number_of_peaks += 1
                    for skipped_end in range(loop_tracker, len(Ch), user_set_chunk_size):
                        peak_row_count += user_set_chunk_size
                        peak_counts[channel].append(number_of_peaks)
            end = time.time() - start
            print("single core execution time: ", str(end))

#             if row_count>=1500000 :
#                 print('len(peak[0])',len(peak[0]),len(peak[1]),len(peak[2]),len(peak[3]))
#                 print('len(width[0])',len(width[0]),len(width[1]),len(width[2]),len(width[3]))
#                 break

        for col in range(4):
            peak[col] = [0 if math.isnan(x) else x for x in peak[col]]

        return (peak, width, peak_counts)


    def extract_parallel(self, file, threshold,
                width_enable=True, peak_enable = False, width_channel=0, user_set_chunk_size=100, header=0,
                channel_name = "N/A", channel_count = "1", peak_threshold=1, peak_min=0, peak_max=1000):

        # select channel and threshold
        peak = [[],[],[],[]]
        width =[[],[],[],[]]
        peak_counts = [[],[],[],[]]
        current_row_number = 0
        row_chunk = 0
        peak_row_count = 0
        row_count = 0
        for Ch in pd.read_csv(file, chunksize=2000000, header=header):
            Ch.columns =[0,1,2,3]
            row_count += len(Ch)
            progress_percentage = round(((row_count+1)/(float(channel_count)*user_set_chunk_size))*100,2)
            print(channel_name,progress_percentage,"%")

            current_row_number = row_chunk + user_set_chunk_size
            start = time.time()
            with concurrent.futures.ProcessPoolExecutor() as executor:
                timer_start = time.time()
                peak_result = [executor.submit(peak_finder, channel, Ch, user_set_chunk_size) for channel in range(4)]
                width_result = [executor.submit(width_finder,channel, Ch, threshold,
                                                                                       current_row_number,
                                                                                       user_set_chunk_size) for channel in range(4)]
                num_result = [executor.submit(peak_num_finder, channel, Ch, peak_threshold, peak_row_count, user_set_chunk_size, 0, peak_min, peak_max) for channel in range(4)]
                timer_end = time.time() - timer_start
                print("allocation timer: ",str(timer_end))
                for result in concurrent.futures.as_completed(peak_result):
                    holder = result.result()
                    peak[holder[1]].append(holder[0])
                for result in concurrent.futures.as_completed(width_result):
                    holder = result.result()
                    width[holder[1]].append(holder[0])
                for result in concurrent.futures.as_completed(num_result):
                    holder = result.result()
                    peak_counts[holder[1]].append(holder[0])

#             if row_count>=1500000 :
#                 print('len(peak[0])',len(peak[0]),len(peak[1]),len(peak[2]),len(peak[3]))
#                 print('len(width[0])',len(width[0]),len(width[1]),len(width[2]),len(width[3]))
#                 break
            end = time.time() - start
            print("executor timer raw: ", str(time.time()))
            print("executor timer: ", str(end))

        for col in range(4):
            peak[col] = [0 if math.isnan(x) else x for x in peak[col]]

        return (peak, width, peak_counts)

    def extract_parallel2(self, file, threshold,
                width_enable=True, peak_enable=False, width_channel=0, user_set_chunk_size=100, header=0,
                channel_name="N/A", channel_count="1", peak_threshold=1, peak_min=0, peak_max=1000):

        print("user_set_chunk_size",user_set_chunk_size)
        # select channel and threshold
        peak = [[], [], [], []]
        width = [[], [], [], []]
        peak_counts = [[], [], [], []]
        current_row_number = 0
        row_chunk = 0
        peak_row_count = 0
        row_count = 0
        for Ch in pd.read_csv(file, chunksize=20000000, header=header):
            start = time.time()
            Ch.columns = [0, 1, 2, 3]
            row_count += len(Ch)
            
#             progress_percentage = round(((row_count + 1) / (float(channel_count) * user_set_chunk_size)) * 100, 2)
#             print(channel_name, progress_percentage, "%")

            current_row_number = row_chunk + user_set_chunk_size
            with concurrent.futures.ProcessPoolExecutor() as executor:
                extracted_data = [executor.submit(data_extractor, Ch[channel], threshold[channel], peak_threshold[channel], current_row_number, user_set_chunk_size, peak_max[channel], peak_min[channel], channel) for channel in range(4)]
                for f in concurrent.futures.as_completed(extracted_data):
                    holder = f.result()
                    for x in holder[1]:
                        peak[holder[0]].append(x)
                    for x in holder[2]:
                        width[holder[0]].append(x)
                    for x in holder[3]:
                        peak_counts[holder[0]].append(x)
                    row_chunk = holder[4]
            print("Parallel execution time", str(time.time()-start))

        """
        for col in range(4):
            peak[col] = [0 if math.isnan(x) else x for x in peak[col]]
        """
        return peak, width, peak_counts

    def extracted_data_loader(self, file_name):
        """function used to load extracted data"""
        print("start extracted data loading")
        peak = [[], [], [], []]
        width = [[], [], [], []]
        peak_counts = [[], [], [], []]
        chunk_size = 0

        """loading the data, return empty array is file does not exist"""
        try:
            extracted_data = pd.read_csv(file_name, header=None)
            length = len(extracted_data.index)
            print("reading: " + str(file_name))
        except:
            print("file did not exist")
            return peak, width, peak_counts

        counter = 0
        start_count = False
        """while loop to figure out chunksize"""
        while chunk_size == 0 and counter < length:
            if extracted_data.iloc[counter, 0] == 16 and extracted_data.iloc[counter, 3] == 16:
                """rows with 16,16,16,16 is divider"""
                if start_count:
                    chunk_size = counter
                    break
                else:
                    start_count = True
                    counter += 1
            else:
                counter += 1

        total_droplets = length/chunk_size
        print("Total number of droplet extracted: " + str(total_droplets))
        total_channels = (chunk_size-1)//3
        for i in range(0, length, chunk_size):
            """load each chunk and process """
            current_chunk = extracted_data.iloc[i:i+chunk_size]
            droplet_size = current_chunk.iloc[0, 4]
            for j in range(1, chunk_size):
                channel = (j-1) // 3
                mode = (j-1) % 3
                if mode == 0:
                    """first line of the chunk, extract number of peaks and vertical value"""
                    peak_counts[channel].append(current_chunk.iloc[j, 0])
                    peak[channel].append(current_chunk.iloc[j, 1])
                    width[channel].append(droplet_size)
            if total_channels < 4:
                """handle AFA data, missing fourth channel"""
                peak[3].append(0)
                peak_counts[3].append(0)
                width[3].append(0)

        return peak, width, peak_counts






def peak_finder(channel, Ch, user_set_chunk_size):
    print("Peak Finder Start: ", str(time.time()))
    start = time.time()
    peak = []
    for row in range(0, len(Ch), user_set_chunk_size):
        peak.append(round(Ch.iloc[row:(row + user_set_chunk_size), channel].max(),3))
    end = time.time()-start
    print("peak finder done, time: ", str(end))
    return peak, channel

def width_finder(channel, Ch, threshold, current_row_number, user_set_chunk_size):
    print("Width Finder Start: ", str(time.time()))
    start = time.time()
    sign = Ch[channel] - threshold[channel]
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    width = []
    diff1 = sign.diff(periods=1).fillna(0)
    df1 = sign.loc[diff1[diff1 != 0].index]
    index_list = df1.index
    row_chunk = current_row_number
    current_width = 0
    for i in range(1, len(index_list)):
        # 0~99
        if df1.index[i] > row_chunk:
            width.append(current_width)
            current_width = 0
            for number_of_skip_chunck in range((df1.index[i] - row_chunk) // user_set_chunk_size):
                width.append(current_width)
                row_chunk += user_set_chunk_size
            row_chunk += user_set_chunk_size
            continue
        if df1[index_list[i - 1]] >= 0:
            if df1[index_list[i]] <= 0:
                current_width = max(index_list[i] - index_list[i - 1], current_width)

    width.append(current_width)

    for number_of_skip_chunck_after in range(round(len(Ch) / user_set_chunk_size) -
                                             (len(width) -
                                              round((current_row_number - user_set_chunk_size) / user_set_chunk_size))):
        row_chunk += user_set_chunk_size
        width.append(0)
    end = time.time() - start
    print("width finder done, time: ", str(end))

    return width, channel


def peak_num_finder(channel, Ch, peak_threshold, peak_row_count, user_set_chunk_size, loop_tracker,
                    peak_min, peak_max):
    print("Peak Num Start: ", str(time.time()))
    start = time.time()
    peak_counts = []
    peaks_signs = Ch[channel] - peak_threshold[channel]
    peaks_signs[peaks_signs > 0] = 1
    peaks_signs[peaks_signs < 0] = -1
    edges = peaks_signs.diff(periods=1).fillna(0)
    edges_index = peaks_signs.loc[edges[edges != 0].index]
    edges_index_list = edges_index.index
    number_of_peaks = 0
    for i in range(1, len(edges_index_list)):  # check for each direction changing index
        """this case deal with when current edge is in next droplet, return peaks count"""
        if edges_index.index[i] >= peak_row_count + user_set_chunk_size:
            peak_counts.append(number_of_peaks)
            number_of_peaks = 0
            peak_row_count += user_set_chunk_size
            loop_tracker += user_set_chunk_size
            """this case deal with when direction change is with the next dorplet"""
        elif edges_index[edges_index_list[i - 1]] >= 0 and edges_index_list[i - 1] >= peak_row_count:
            if edges_index[edges_index_list[i]] <= 0:
                peak_width = edges_index_list[i] - edges_index_list[i - 1]
                if peak_min[channel] <= peak_width <= peak_max[channel]:
                    number_of_peaks += 1
    for skipped_end in range(loop_tracker, len(Ch), user_set_chunk_size):
        peak_row_count += user_set_chunk_size
        peak_counts.append(0)
    end = time.time() - start
    print("peak num finder done, time: ", str(end))
    return peak_counts, channel


def data_extractor(Ch, threshold, peak_threshold, current_row_number, user_set_chunk_size, peak_max, peak_min, channel):
    loop_tracker = 0
    peak = []
    width = []
    peak_counts = []
    for row in range(0, len(Ch), user_set_chunk_size):
        peak.append(round(Ch.iloc[row:(row + user_set_chunk_size)].max(), 3))

    sign = Ch - threshold
    sign[sign > 0] = 1
    sign[sign < 0] = -1
    diff1 = sign.diff(periods=1).fillna(0)
    df1 = sign.loc[diff1[diff1 != 0].index]
    index_list = df1.index
    row_chunk = current_row_number
    current_width = 0

    for i in range(1, len(index_list)):
        # 0~99
        while df1.index[i] >= row_chunk:
            width.append(current_width)
            current_width = 0
            row_chunk += user_set_chunk_size
            loop_tracker += user_set_chunk_size
        if df1[index_list[i - 1]] >= 0 >= df1[index_list[i]] and 0 < index_list[i] - index_list[i - 1] < user_set_chunk_size:
            current_width = max(index_list[i] - index_list[i - 1], current_width)

    for number_of_skip_chunck_after in range(loop_tracker, len(Ch), user_set_chunk_size):
        width.append(0)

        """Code for peak extraction starts here"""
    loop_tracker = 0
    peaks_signs = Ch - peak_threshold
    peaks_signs[peaks_signs > 0] = 1
    peaks_signs[peaks_signs < 0] = -1
    edges = peaks_signs.diff(periods=1).fillna(0)
    edges_index = peaks_signs.loc[edges[edges != 0].index]
    edges_index_list = edges_index.index
    peak_row_count = current_row_number - user_set_chunk_size
    number_of_peaks = 0
    for i in range(1, len(edges_index_list)):  # check for each direction changing index
        """this case deal with when current edge is in next droplet, return peaks count"""
        while edges_index.index[i] >= peak_row_count + user_set_chunk_size:
            peak_counts.append(number_of_peaks)
            number_of_peaks = 0
            peak_row_count += user_set_chunk_size
            loop_tracker += user_set_chunk_size
            """this case deal with when direction change is with the next dorplet"""
        if edges_index[edges_index_list[i - 1]] >= 0 and edges_index_list[i - 1] >= peak_row_count:
            if edges_index[edges_index_list[i]] <= 0:
                peak_width = edges_index_list[i] - edges_index_list[i - 1]
                if peak_min <= peak_width <= peak_max:
                    number_of_peaks += 1
    for skipped_end in range(loop_tracker, len(Ch), user_set_chunk_size):
        peak_row_count += user_set_chunk_size
        peak_counts.append(0)
    return channel, peak, width, peak_counts, peak_row_count




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


