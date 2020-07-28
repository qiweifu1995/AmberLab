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

