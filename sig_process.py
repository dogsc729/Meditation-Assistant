import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import time

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

def main():
    print("python main function")
    while 1:
        try:
            signal = np.load("./parse_data/data.npy")
        except:
            continue
        fs = 255

        print(signal)
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
        plt.figure()
        #plt.plot(t, alpha_filtered, label='Alpha', color='black')
        plt.plot(t, beta_filtered, label='Beta', color='purple')
        #plt.plot(t, delta_filtered, label='Delta', color='green')
        #plt.plot(t, theta_filtered, label='Theta', color='blue')
        plt.legend()
        plt.pause(0.5)
        plt.close()
        #plt.savefig('example_plot.png')


if __name__ == '__main__':
    main()
