import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import matplotlib
from threading import Thread
import sys
import argparse
import subprocess


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def apply_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def apply_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

def processing():
    print("test")
    matplotlib.use('agg')
    while 1:
        try:
            signal = np.load("./parse_data/data.npy")
        except:
            print("error")
            continue
        fs = 255

        #print(signal)
        # Filter for Alpha wave (7.5 to 13 Hz)
        test = signal[0, :]
        alpha_filtered = apply_bandpass_filter(test, 7.5, 13, fs, order=8)

        # Filter for Beta wave (14 Hz and greater)
        beta_filtered = apply_highpass_filter(test, 14, fs, order=15)

        # Filter for Delta wave (3 Hz or below)
        delta_filtered = apply_lowpass_filter(test, 3, fs, order=10)

        # Filter for Theta wave (3.5 to 7.5 Hz)
        theta_filtered = apply_bandpass_filter(test, 3.5, 7.5, fs, order=6)

        t = [i for i in range(256)]
        #plt.figure()
        #plt.plot(t, alpha_filtered, label='Alpha', color='black')
        plt.plot(t, beta_filtered, label='Beta', color='purple')
        #plt.plot(t, delta_filtered, label='Delta', color='green')
        #plt.plot(t, theta_filtered, label='Theta', color='blue')
        plt.legend()
        plt.show()
        #plt.pause(0.5)
        #plt.close()
        #plt.savefig('example_plot.png')

def main():
    sys.path.append('./parse_data')
    from parse_data.parse import parse
    parser = argparse.ArgumentParser(description='Script to process a file at a custom location')
    parser.add_argument('file', metavar='FILE', type=str, help='Path to the file to process')
    args = parser.parse_args()
    target = args.file
    target_folder = f"../../../../OpenBCI_GUI/Recordings/OpenBCISession_{target}/"
    output = subprocess.check_output(f"ls -t {target_folder} | head -n 1", shell=True)
    file_name = output.decode("utf-8")
    target_file = target_folder + file_name[:-1] # remove the new line
    try:
        t1 = Thread(target = parse, args = (target_file,))
        t2 = Thread(target = processing)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    except FileNotFoundError:
        print("Parsing Failed!")
        return


if __name__ == '__main__':
    main()
