# this is the file that contains all the analysis functions
# all functions that perform computation or analytical purpose should be made here
import pandas as pd
import time

class Droplet:
    """this class holds all the statistic info for each droplet, this DOES NOT hold raw data"""
    def __init__(self, width, peaks):
        self.width = width
        self.peak_voltage = peaks


def width_detect(data, threshold, width, above_tresh):
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


def extract(file, threshold=0, width_enable=False, width_channel=0, chunksize=1000, header=2):
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
                    width_holder, above_thresh, test_max = width_detect(data, threshold, width_holder, above_thresh)
                    if test_max:
                        width_max_holder = max(width_max_holder, width_holder)
        droplet_stats.append(Droplet(width_max_holder, max_holder))
    return droplet_stats


if __name__ == "__main__":
    stats = []
    start = time.time()
    stats = extract(r"D:\Users\QIwei Fu\Downloads\EXP200601-2\EXP200601-2/200601_140723 AFB Peak Record.csv", 1, True, 0)
    print(stats[1].peak_voltage)
    print(time.time() - start)
