# Section 3
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('data/Section 3 data.csv')

print(data.describe()) # displays mean, standard deviation, min, max
print(f"Data shape: {data.shape}") # see the data shape, it is 2d in our case: 4653(rows)x61(columns)
# print(data.isnull().sum())  # check for no data, we could possibly fill them later, but we can't drop them, since every row is 1 meter and column is 1 minute
# not used in our case, so I have decided to avoid printing it to not to display unnecessary information

# display simple plot to see at what depth the signal is high
plt.figure(figsize=(12, 6))
plt.plot(data)
plt.title("Simple 2D plot")
plt.xlabel('Depth (meters)')
plt.ylabel('Signal')
plt.show()

# # display heatmap
plt.figure(figsize=(12, 6))
plt.imshow(data.values, aspect='auto', cmap='cividis', interpolation='none')
plt.colorbar(label='Signal Heatmap')
plt.xlabel('Time (minutes)')
plt.ylabel('Depth (meters)')
plt.title('Distributed Acoustic Sensing (DAS) HeatMap')
plt.show()

# convert the DataFrame to a NumPy array to make it easier to slice
data_array = data.values

# function to find peaks
def find_peaks(signal, threshold=10):
    peaks = []
    for i in range(1, len(signal) - 1):  # avoid including edges
        if signal[i] > signal[i - 1] and signal[i] > signal[i + 1] and signal[i] > threshold:
            peaks.append(i)
    return peaks

# sum peak "heights" to find the most prominent rows
peak_info = {}
for depth_idx in range(data_array.shape[0]): # go thru each row
    signal = data_array[depth_idx, :]  # get signal at this depth
    peaks = find_peaks(signal, threshold=10)  # threshold for the sensitivity(can be changed)
    peak_prominence = sum(signal[peak] for peak in peaks)  # result sum
    peak_info[depth_idx] = peak_prominence

# sort depth in descending order to have most prominent ones at top
sorted_peaks = sorted(peak_info.items(), key=lambda x: x[1], reverse=True)

# get top 5(most prominent) rows
top_depths = [item[0] for item in sorted_peaks[:5]]

print(f"The top depths with possible anomalies: {top_depths}")

# plot simple chart to see them
plt.figure(figsize=(12, 6))
for depth in top_depths: # include our 'top_depth' array into the plot
    plt.plot(data_array[depth, :], label=f'Depth {depth}')
plt.title("Most Prominent Lines")
plt.xlabel("Time (minutes)")
plt.ylabel("Signal")
plt.show()