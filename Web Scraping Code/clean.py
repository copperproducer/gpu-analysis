import os
import pandas as pd
import matplotlib.pyplot as plt

allGpus = []
names = []
#for every file in gpus_raw, add the data to allGpus
for file in os.listdir("gpus_raw"):
    with open("gpus_raw/" + file, "r") as f:
        allGpus.append(f.read())
        names.append(file)


    print("Added " + file + " to allGpus")

#remove "New" prices from the data
for gpu in allGpus:
    #remove everything before and including the first "Used"
    gpu = gpu[gpu.find("Used"):]
    #if gpu has "New" in it, print it
    if "New" in gpu:
        print('ATTENTION CHECK THAT NEW PRICES ARE NOT INCLUDED IN THE DATA')



import re
gpuPrices = []
for gpu in allGpus:
    # use regex to extract y-values
    y_values = re.findall(r"y: (\d+)", gpu)

    #print(y_values)
    gpuPrices.append(y_values)


# # assume gpuPrices is a list of lists, where each inner list contains the price history of a GPU
# smoothed_prices = []
# displaycounter = 0
# for history in gpuPrices:
#     series = pd.Series(history)
#     smoothed_series = series.rolling(window=3).mean()  # rolling mean with a window size of 7
#     smoothed_prices.append(smoothed_series.tolist())
#
#     plt.plot(smoothed_series)
#     plt.ylim(ymin=0)  # set the minimum value of the y-axis to 0
#     plt.title(f"Price history of {names[displaycounter]}")
#     plt.show()
#     displaycounter += 1
#
#

#save the price history data to a csv file
#save each index of gpuPrices as its own column
import csv
with open("gpu-prices.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(gpuPrices)


