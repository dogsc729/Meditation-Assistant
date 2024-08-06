import numpy as np
import time
'''
def parse(file_name):
    channels = np.zeros((8, 256))
    while 1:
        try:
            with open(file_name, 'r') as file:
                    for line_idx, line in enumerate(file):
                        if line_idx < 5:
                            continue
                        elements = line.strip().split(',')
                        for elem_idx, elem in enumerate(elements[1:9]):
                            try: 
                                channels[elem_idx][line_idx % 256] = float(elem)
                            except:
                                channels[elem_idx][line_idx % 256] = 0
                        np_channels = np.array(channels)
                        #np_channels = np.random.randn(8, 256)
                        # np_channels is a growing array of the 8 channels
                        # add code here to process the signal after reading one line of data
                        if (line_idx - 5) % 256 == 0 and not line_idx == 5:
                            #print(np_channels)
                            np.save("data.npy", np_channels)
                            #print(np_channels.shape, "")
        except FileNotFoundError:
            print(f"Error: File {file_name} not found.")
            raise FileNotFoundError
'''
def parse(file_name):
    # Initialize channels list
    channels = [[] for _ in range(8)]
    print(f"parsing {file_name}")
    while True:
        lines = read_last_256_lines(file_name)
        for line_idx, line in enumerate(lines):
            elements = line.strip().split(',')
            for elem_idx, elem in enumerate(elements[1:9]):
                try: 
                    channels[elem_idx].append(float(elem))
                except:
                    channels[elem_idx].append(0)
        
        # Trim each channel to 256 elements
        for i in range(8):
            channels[i] = channels[i][-256:]
        
        np_channels = np.array(channels)

        np.save("data.npy", np_channels)
        # Now np_channels contains the data from the last 256 lines, each channel having 256 elements
        
        # Process or use np_channels as needed
        
        time.sleep(1)  # Adjust the sleep duration as needed


def read_last_256_lines(filename):
    with open(filename, 'r') as file:
        file.seek(0, 2)  # Move the cursor to the end of the file
        size = file.tell()
        lines = []
        line_count = 0
        while size > 0 and line_count < 256:
            size -= 1
            file.seek(size)  # Move one byte backward
            char = file.read(1)
            if char == '\n':
                line_count += 1
            if line_count == 256:
                lines = file.readlines() + lines  # Read the last 256 lines
                break
        return lines
