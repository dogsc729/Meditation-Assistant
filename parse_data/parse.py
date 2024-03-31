import sys
import numpy as np

raw_file_name = "OpenBCI-RAW-2024-03-30_19-23-22.txt"
# array = np.empty(8, dtype=object)
# array.fill([])
channels = [[] for _ in range(8)]
try:
    with open(raw_file_name, 'r') as file:
        for line_idx, line in enumerate(file):
            if line_idx < 5:
                continue
            elements = line.strip().split(',')
            for elem_idx, elem in enumerate(elements[1:9]):
                channels[elem_idx].append(float(elem))
            np_channels = np.array(channels)
            # np_channels is a growing array of the 8 channels
            # add code here to process the signal after reading one line of data
            if (line_idx - 5) % 255 == 0 and not line_idx == 5:
                print(np_channels.shape, "")
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
