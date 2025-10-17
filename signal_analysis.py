import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

#Load the CSV file
file_name = '/Users/pranavpanday/Downloads/100_ekg.csv'
df = pd.read_csv(file_name)


#Pick first two columns
x = df.iloc[:, 0]   # sample numbers
y = df.iloc[:, 1]   # ECG voltage (MLII)

#Bandpass filter function
def bandpass_filter(signal, fs=360, lowcut=0.5, highcut=40.0, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

# Apply filter
y_filtered = bandpass_filter(y)


plt.figure(figsize=(12, 4))
plt.plot(y_filtered[0:1000], color='blue')
plt.title('Filtered ECG Signal MIT-BIH:1 sample = 1/360 sec')
plt.xlabel('Sample number')
plt.ylabel('Amplitude (mV)')
plt.grid(True)
plt.show()
