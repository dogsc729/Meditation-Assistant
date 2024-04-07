import numpy as np

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
                        # np_channels is a growing array of the 8 channels
                        # add code here to process the signal after reading one line of data
                        if (line_idx - 5) % 256 == 0 and not line_idx == 5:
                            #print(np_channels)
                            np.save("data.npy", np_channels)
                            #print(np_channels.shape, "")
        except FileNotFoundError:
            print(f"Error: File {file_name} not found.")
            raise FileNotFoundError
