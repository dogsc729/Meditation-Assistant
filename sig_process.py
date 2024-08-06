import numpy as np
from scipy.signal import butter, filtfilt, freqz
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
    print("signal processing start")
    try:
        data = np.load("data.npy")
        np.save("backup.npy", data)
    except:
        data = np.load("backup.npy")

    fs = 256
    #print(signal.size())
    # Filter for Alpha wave (7.5 to 13 Hz)
    num_channels = 8
    frequency_responses = []
    for i in range(num_channels):
        #normalized_signal = (data[i, :] - np.std(data[i, :])) / np.mean(data[i, :])
        #noise_filtered = apply_lowpass_filter(normalized_signal, 40, fs, order=15)
        noise_filtered = apply_lowpass_filter(data[i, :],  40, fs, order=15)
        low_beta_filtered = apply_bandpass_filter(noise_filtered, 12, 15, fs, order=6)
        mid_beta_filtered = apply_bandpass_filter(noise_filtered, 15, 20, fs, order=6)
        high_beta_filtered = apply_bandpass_filter(noise_filtered, 20, 40, fs, order=6)
        frequencies, response = freqz(mid_beta_filtered, fs=fs)
        #print("max freq", np.max(frequencies))
        frequency_responses.append((frequencies, np.abs(response)))
    return frequency_responses
    alpha_filtered = apply_bandpass_filter(test, 7.5, 13, fs, order=8)

    # Filter for Beta wave (14 Hz and greater)
    beta_filtered = apply_highpass_filter(test, 14, fs, order=15)

    # Filter for Delta wave (3 Hz or below)
    delta_filtered = apply_lowpass_filter(test, 3, fs, order=10)

    # Filter for Theta wave (3.5 to 7.5 Hz)
    theta_filtered = apply_bandpass_filter(test, 3.5, 7.5, fs, order=6)

    frequencies, response = signal.freqz(beta_filtered, fs=fs)
    #plt.figure()
    #plt.plot(t, alpha_filtered, label='Alpha', color='black')
    #plt.plot(t, beta_filtered, label='Beta', color='purple')
    #plt.plot(t, delta_filtered, label='Delta', color='green')
    #plt.plot(t, theta_filtered, label='Theta', color='blue')
    #plt.legend()
    #plt.show()
    #plt.pause(0.5)
    #plt.close()
    #plt.savefig('example_plot.png')
    return frequencies, np.abs(response)
