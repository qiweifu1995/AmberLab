import os, csv


class Wells:
    """This class is used to store signal and attribute of individual wells"""
    number_of_plates = 0
    number_of_strips = 0

    def __init__(self, rootfolder, indexed_files, chunk_size, well_mode):
        """initialize speicifed numbers of channels, assign data and if well is filled"""

        self.current_well = 1
        self.current_strip = 1
        self.current_plate = 1
        self.strip_data = []
        self.plate_data = []

        os.chdir(rootfolder)

        for n in range(len(indexed_files)):

            # loading the indexing
            if os.path.exists(indexed_files[n][0]) and indexed_files[n][0].rfind('Mapping') > 1:
                with open(indexed_files[n][0]) as mapping_files:
                    mapping_reader = csv.reader(mapping_files, delimiter=',')
                    well_index = []
                    peak_holder = []
                    new_file = True
                    for lines, index in enumerate(mapping_reader):
                        if 2 < lines and int(float(index[0])) <= well_mode:
                            well_index.append([int(float(index[0])), int(float(index[1]))])
                    #print(well_index)
                    if len(well_index):
                        # iterating each mapping files, loading peak into a buffer first
                        if os.path.exists(indexed_files[n][1]) and indexed_files[n][1].rfind('Peak') > 1:
                            #print(indexed_files[n][0])
                            #print(indexed_files[n][1])
                            with open(indexed_files[n][1]) as peak_files:
                                peak_reader = csv.reader(peak_files, delimiter=',')
                                for i in range(3):  # skipping the header
                                    next(peak_reader)
                                for data in peak_reader:
                                    peak_holder.append(data)
                    while len(well_index):
                        for well_x in range(self.current_well-1, well_mode):
                            if len(well_index) == 0:
                                break
                            elif well_index[0][0] == self.current_well:
                                # if well index match plate index append the peak profile
                                if len(self.strip_data) == 8:
                                    #print('strip append1')
                                    self.plate_data.append(self.strip_data[:])
                                    self.strip_data.clear()
                                    self.number_of_strips += 1
                                self.strip_data.append(peak_holder[(well_index[0][1]-1)*chunk_size:
                                                                   well_index[0][1]*chunk_size])
                                well_index.pop(0)
                                self.current_well += 1
                                new_file = False
                            elif well_index[0][0] > self.current_well:
                                # if well index smaller than what is looked for, well missing, append empty
                                if len(self.strip_data) == 8:
                                    self.plate_data.append(self.strip_data[:])
                                    self.strip_data.clear()
                                    self.number_of_strips += 1
                                    #print("strip append2")
                                self.strip_data.append([])
                                self.current_well += 1
                                new_file = False
                            else:
                                if new_file:
                                    self.strip_data.append([])
                                    self.current_well += 1
                                    if len(self.strip_data) == 8:
                                        #print('strip append3')
                                        self.plate_data.append(self.strip_data[:])
                                        self.strip_data.clear()
                                        self.number_of_strips += 1
                                else:
                                    well_index.pop(0)
                            if self.current_well > well_mode:
                                self.current_well = 1
        if len(self.strip_data):
            self.plate_data.append(self.strip_data[:])
            self.number_of_strips += 1
            #print('strip append4')
        #print("finished")
        #print(len(self.plate_data))



def index_files(rootfolder):
    """return the linked dispense map and peak profile files"""
    output = []
    list_of_files = os.scandir(rootfolder)
    file_location = 0
    with list_of_files as files:
        for file in files:
            if os.path.exists(file.path) and file.path.rfind('Mapping') > 1:
                with open(file.path) as mapping_files:
                    mapping_reader = csv.reader(mapping_files, delimiter=',')
                    mapping_holder = []
                    for lines in mapping_reader:
                        mapping_holder.append(lines)
                    for i in range(len(mapping_holder[1])):
                        if mapping_holder[1][i] == '':
                            file_location = i-1
                            break
                        elif i == len(mapping_holder[1])-1:
                            file_location = i
                    output.append([file.name, mapping_holder[1][file_location]])
    return output
