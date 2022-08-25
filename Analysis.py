# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here
import pandas as pd
import time
import numpy as np
import os
import csv
import math
import concurrent.futures
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Droplet:
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __init__(self, width, peaks):
        self.width = width
        self.peak_voltage = peaks


def extracted_data_loader(parent, progress_index, file_name):
    """function used to load extracted data"""
    print("start extracted data loading")
    start = time.time()
    peak = [[], [], [], []]
    width = [[], [], [], []]
    peak_counts = [[], [], [], []]
    fret_ratio = []
    time_data = []
    chunk_size = 0


    # progress span indcate how much of the progress this process is
    progress_span = progress_index[1] - progress_index[0]
    progress_start = progress_index[0]

    """loading the data, return empty array is file does not exist"""
    try:
        extracted_data = pd.read_csv(file_name, header=None)
        length = len(extracted_data.index)
        print("reading: " + str(file_name))
    except:
        print("file did not exist")
        return peak, width, peak_counts, time_data, fret_ratio

    counter = 0
    start_count = False
    """while loop to figure out chunksize"""
    while chunk_size == 0 and counter < length:
        if extracted_data.iloc[counter, 0] == -16 and extracted_data.iloc[counter, 1] == -16:
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
    curent_droplet = 0
    current_percent = 0
    for i in range(0, length, chunk_size):
        """load each chunk and process """
        curent_droplet += 1
        droplet_size = extracted_data.iloc[i, 4]
        time_stamp = extracted_data.iloc[i, 3]
        fret_ratio_data = extracted_data.iloc[i, 2]
        if math.isnan(fret_ratio_data) or math.isinf(fret_ratio_data):
            fret_ratio_data = 0
        if time_stamp < 0:
            #this is just a test case
            time_stamp = curent_droplet // 6000 + 1
        for j in range(i, i+chunk_size):
            channel = (j-(curent_droplet-1)*chunk_size) // 3
            mode = (j-curent_droplet) % 3
            if mode == 0:
                """first line of the chunk, extract number of peaks and vertical value"""
                peak_counts[channel].append(extracted_data[0][j])
                peak[channel].append(extracted_data[1][j])
                width[channel].append(droplet_size)
        time_data.append(time_stamp)
        fret_ratio.append(fret_ratio_data)
        if total_channels < 4:
            """handle AFA data, missing fourth channel"""
            peak[3].append(0)
            peak_counts[3].append(0)
            width[3].append(0)
        percentage = curent_droplet * progress_span / total_droplets // 1 + progress_start
        if current_percent != percentage:
            current_percent = percentage
            parent.progress.emit([current_percent, "Extracting " + str(file_name)])
    print("Extracted data loading time: " + str(start-time.time()))

    return peak, width, peak_counts, time_data, fret_ratio


def extract(file, threshold,
            width_enable=True, peak_enable = False, width_channel=0, user_set_chunk_size=200, header=0,
            channel_name = "N/A", channel_count = "1", peak_threshold=1, peak_min=0, peak_max=1000):

    # select channel and threshold
    peak = [[],[],[],[],[]]
    width =[[],[],[],[],[]]
    peak_counts = [[],[],[],[],[]]
    current_row_number = 0
    row_chunk = 0
    peak_row_count = 0
    row_count = 0
    for Ch in pd.read_csv(file, chunksize=20000000, header=header):
        start = time.time()
        Ch.columns =[0,1,2,3,4]
        row_count += len(Ch)
        progress_percentage = round(((row_count+1)/(float(channel_count)*user_set_chunk_size))*100,2)
        print(channel_name,progress_percentage,"%")

        current_row_number = row_chunk + user_set_chunk_size
        for channel in range(5):
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

    for col in range(5):
        peak[col] = [0 if math.isnan(x) else x for x in peak[col]]

    return (peak, width, peak_counts)


def extract_parallel(file, threshold,
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





def file_extracted_data_Qing(parent, current_file_dict, threshold, peak_threshold, width_min=0, width_max=1000, width_enable=True,
                 peak_enable=False, channel=0, chunksize=1000, header=2, ch1_count="1", ch2_count="1", ch3_count="1",
                 ch12_count="1", ch13_count="1", ch23_count="1", Droplet_Record_count="1", locked_out_count="1",
                 total_count="1", rethreshold=False):
        analog_file = {}
        peak_file_chunksize = 1000
        threshold = threshold

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
        if locked_out_count == '0':
            locked_out_count = '1'
        if total_count == '0':
            total_count = '1'

        # Processing progress bar
        total_files = 0
        if current_file_dict["Ch1 "] != "":
            total_files += 1
        if current_file_dict["Ch2 "] != "":
            total_files += 1
        if current_file_dict["Ch3 "] != "":
            total_files += 1
        if current_file_dict["Ch1-2"] != "":
            total_files += 1
        if current_file_dict["Ch1-3"] != "":
            total_files += 1
        if current_file_dict["Ch2-3"] != "":
            total_files += 1
        if current_file_dict["Droplets Extracted Data"] != "" and not rethreshold:
            total_files += 1
        elif current_file_dict["Droplet Record"] != "":
            total_files += 1
        if current_file_dict["Locked Out Extracted Data"] != "":
            total_files += 1
        elif current_file_dict["Locked Out Peaks"] != "":
            total_files += 1
        if current_file_dict["Sorted Extracted Data"] != "":
            total_files += 1
        else:
            total_files += 1
        progress_index_list = []
        for i in range(total_files):
            start = 100*i//total_files
            end = 100*(i+1)//total_files
            progress_index_list.append([start, end])

        if current_file_dict["Ch1 "] != "":
            print("Extracting Ch1...")
            progress_index = progress_index_list.pop(0)
            list1, width1, num_peaks1 = extract_parallel2(parent, progress_index, current_file_dict["Ch1 "], threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1', ch1_count, peak_threshold, width_min, width_max)
            time1 = [0 for i in range(len(list1[0]))]
            ratio1= []
            analog_file[current_file_dict["Ch1 "]] = [list1, width1, num_peaks1, time1, ratio1]

        if current_file_dict["Ch2 "] != "":
            print("Extracting Ch2...")
            progress_index = progress_index_list.pop(0)
            list2, width2, num_peaks2 = extract_parallel2(parent, progress_index, current_file_dict["Ch2 "], threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch2', ch2_count, peak_threshold, width_min, width_max)
            time2 = [0 for i in range(len(list2[0]))]
            ratio2 = []
            analog_file[current_file_dict["Ch2 "]] = [list2, width2, num_peaks2, time2, ratio2]

        if current_file_dict["Ch3 "] != "":
            print("Extracting Ch3...")
            progress_index = progress_index_list.pop(0)
            list3, width3, num_peaks3 = extract_parallel2(parent, progress_index, current_file_dict["Ch3 "], threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch3', ch3_count, peak_threshold, width_min, width_max)
            time3 = [0 for i in range(len(list3[0]))]
            raiot3 = []
            analog_file[current_file_dict["Ch3 "]] = [list3, width3, num_peaks3, time3, raiot3]

        if current_file_dict["Ch1-2"] != "":
            print("Extracting Ch1-2...")
            progress_index = progress_index_list.pop(0)
            list12, width12, num_peaks12 = extract_parallel2(parent, progress_index, current_file_dict["Ch1-2"], threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1_2', ch12_count, peak_threshold, width_min, width_max)
            time12 = [0 for i in range(len(list12[0]))]
            ratio12 = []
            analog_file[current_file_dict["Ch1-2"]] = [list12, width12, num_peaks12, time12, ratio12]

        if current_file_dict["Ch1-3"] != "":
            print("Extracting Ch1-3...")
            progress_index = progress_index_list.pop(0)
            list13, width13, num_peaks13 = extract_parallel2(parent, progress_index, current_file_dict["Ch1-3"], threshold, width_enable, peak_enable, channel, chunksize, header, 'Ch1_3', ch13_count, peak_threshold, width_min, width_max)
            time13 = [0 for i in range(len(list13[0]))]
            ratio13 = []
            analog_file[current_file_dict["Ch1-3"]] = [list13, width13, num_peaks13, time13, ratio13]

        if current_file_dict["Ch2-3"] != "":
            print("Extracting Ch2-3...")
            progress_index = progress_index_list.pop(0)
            list23, width23, num_peaks23 = extract_parallel2(parent, progress_index, current_file_dict["Ch2-3"], threshold, width_enable,
                                                                  peak_enable, channel, chunksize, header,
                                                                  'Ch2_3', ch23_count, peak_threshold, width_min, width_max)
            time23 = [0 for i in range(len(list23[0]))]
            ratio23 = []
            analog_file[current_file_dict["Ch2-3"]] = [list23, width23, num_peaks23, time23, ratio23]

        if current_file_dict["Droplets Extracted Data"] != "" and not rethreshold:
            print("Importing Extracted Droplet Record...")
            progress_index = progress_index_list.pop(0)
            listDR, widthDR, num_peaksDR, timeDR, ratioDR = extracted_data_loader(parent, progress_index, current_file_dict["Droplets Extracted Data"])

            analog_file[current_file_dict["Droplet Record"]] = [listDR, widthDR, num_peaksDR, timeDR, ratioDR]
        elif current_file_dict["Droplet Record"] != "":
            print("Extracting Droplet Record...")
            progress_index = progress_index_list.pop(0)
            listDR, widthDR, num_peaksDR = extract_parallel2(parent, progress_index, current_file_dict["Droplet Record"], threshold, width_enable, peak_enable, channel, chunksize, header, 'Droplet Record', Droplet_Record_count, peak_threshold, width_min, width_max)
            timeDR = [0 for i in range(len(listDR[0]))]
            ratioDR = []
            analog_file[current_file_dict["Droplet Record"]] = [listDR, widthDR, num_peaksDR, timeDR, ratioDR]

        if current_file_dict["Locked Out Extracted Data"] != "":
            print("Extracting locked out peaks extracted data")
            progress_index = progress_index_list.pop(0)
            list_locked, width_locked, num_peaks_locked, time_locked, ratio_locked = extracted_data_loader(parent, progress_index, current_file_dict["Locked Out Extracted Data"])
            analog_file[current_file_dict["Locked Out Peaks"]] = [list_locked, width_locked, num_peaks_locked, time_locked, ratio_locked]

        elif current_file_dict["Locked Out Peaks"] != "":
            print("Extracting locked out peaks")
            progress_index = progress_index_list.pop(0)
            list_locked, width_locked, num_peaks_locked = extract_parallel2(parent, progress_index, current_file_dict["Locked Out Peaks"], threshold, width_enable,
                                                                  peak_enable, channel, chunksize, header,
                                                                  'Locked Out Peaks', locked_out_count, peak_threshold, width_min, width_max)
            time_locked = [0 for i in range(len(list_locked[0]))]
            ratio_locked = []
            analog_file[current_file_dict["Locked Out Peaks"]] = [list_locked, width_locked, num_peaks_locked, time_locked, ratio_locked]

        if current_file_dict["Sorted Extracted Data"] != "":
            print("Extracting peaks extracted data")
            progress_index = progress_index_list.pop(0)
            Peaklist, Peakwidth, NumPeaks, TimePeaks, ratio_peaks = extracted_data_loader(parent, progress_index, current_file_dict["Sorted Extracted Data"])
            analog_file[current_file_dict["Peak Record"]] = [Peaklist, Peakwidth, NumPeaks, TimePeaks, ratio_peaks]

        else:
            print("Extracting Peak... Parallel")
            start = time.time()
            progress_index = progress_index_list.pop(0)
            Peaklist, Peakwidth, NumPeaks = extract_parallel2(parent, progress_index, current_file_dict["Peak Record"], threshold, width_enable,
                                                         peak_enable, channel, 200, 2, 'Peak Record', total_count,
                                                         peak_threshold, width_min, width_max)
            TimePeaks = [1 for i in range(len(Peaklist[0]))]
            ratio_peaks = []
            analog_file[current_file_dict['Peak Record']] = [Peaklist, Peakwidth, NumPeaks, TimePeaks, ratio_peaks]
            end = time.time()
            print("parallel extrack time: ", str(start-end))
        """
        print("Extracting Peak...")
        start = time.time()
        Peaklist, Peakwidth, NumPeaks = extract(current_file_dict["Peak Record"], threshold, width_enable, peak_enable, channel, 1000 , 2, 'Peak Record', total_count, peak_threshold, width_min, width_max)
        analog_file[current_file_dict['Peak Record']] = [Peaklist, Peakwidth, NumPeaks]
        end = time.time()
        print("normal extrack time", str(start-end))
        """
        parent.progress.emit([100, "Extraction complete!"])
        return analog_file


def extract_parallel2(parent, progress_index, file, threshold,
                      width_enable=True, peak_enable=False, width_channel=0, user_set_chunk_size=100, header=0,
                      channel_name="N/A", channel_count="1", peak_threshold=1, peak_min=0, peak_max=1000):

    print("user_set_chunk_size",user_set_chunk_size)
    # select channel and threshold
    peak = [[], [], [], []]
    width = [[], [], [], []]
    peak_counts = [[], [], [], []]
    progress_counter = 0
    current_row_number = 0
    row_chunk = 0
    peak_row_count = 0
    row_count = 0
    file_size = os.path.getsize(file)
    estimated_chunks = file_size // 500000000
    if estimated_chunks == 0:
        estimated_chunks = 1
    print(file_size)
    parent.progress.emit([progress_index[0], "Extracting" + str(file)])
    csv_file = pd.read_csv(file, chunksize=20000000, header=header)
    total_portions = 0
    for Ch in csv_file:
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
        parent.progress.emit([progress_index[0] + (progress_index[1]-progress_index[0])//estimated_chunks, "Extracting " + str(file)])
        print("Parallel execution time", str(time.time()-start))

    """
    for col in range(4):
        peak[col] = [0 if math.isnan(x) else x for x in peak[col]]
    """
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



