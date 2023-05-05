import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#go to https://howmuch.one/gpus
driver = webdriver.Chrome()
driver.get("https://howmuch.one/gpus")



#for each link that has the word "Average" in it, go to the link and copy the code from howmuch.one>product/average{gpu}>price-history.js and paste the code in a new file called raw-price-history-{gpu}
#example: https://howmuch.one/product/average-geforce-gtx-1070 has the code for https://howmuch.one/product/price-history.js

time.sleep(2)
links = driver.find_elements(By.PARTIAL_LINK_TEXT, "Average")
print(links)


# make a list of all the links that have the word "Average" in it
link_list = []
for link in links:
    link_list.append(link.get_attribute("href"))
print(link_list)
gpuName = []
for gpu in link_list:
    if "gddr" in gpu:
        #if the gpu name has gddr in it, remove everything after and including the last dash
        gpu = gpu[:gpu.rfind("-") - 1]
    # Cut the link to just the gpu name. Remove everything before and including the first dash and everything after and including the last dash
    gpu = gpu[gpu.find("-") + 1:]
    gpu = gpu[:gpu.rfind("gb-")-3]
    if gpu[-1] == "-":
        #remove the last dash
        gpu = gpu[:-1]

    print(gpu)
    gpuName.append(gpu)
#save the gpu names as a csv file
import csv
with open("gpu-names.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(gpuName)

gpuMem = []
for gpu in link_list:
    #if the gpu name has gddr in it, remove everything after and including the last dash
    if "gddr" in gpu:
        gpu = gpu[:gpu.rfind("-") - 1]

    # remove everything except the last number in the link
    gpu = gpu[gpu.rfind("-") + 1:]

    gpu = gpu[:gpu.rfind("gb")]

    print(gpu)
    gpuMem.append(gpu)
#save the gpu memory as a csv file
with open("gpu-memory.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(gpuMem)

import re
import os

def get_gpu_prices(link_list):
    gpuPriceHistoryRaw = []
    for link in link_list:
        driver.get(link)
        time.sleep(1)
        # click on the "price history" button
        driver.find_element(By.LINK_TEXT, "Price history").click()
        time.sleep(1)

        # Locate the script tag containing the data
        script_tag = driver.find_element(By.XPATH, '//script[contains(., "var datasets")]')

        # extract the text from the tag
        script_text = script_tag.get_attribute('innerHTML')
        print(script_text)
        gpuPriceHistoryRaw.append(script_text)

    nameMemory = []
    # save the raw price history data to a text file
    for i in range(len(gpuName)):
        # if the gpu name has already been added to the list, add the memory to the name
        if gpuName[i] in nameMemory:
            gpuName[i] = gpuName[i] + "-" + gpuMem[i]
        nameMemory.append(gpuName[i])
        with open(os.path.join("gpus_raw", "raw-price-history-" + gpuName[i] + ".txt"), "w") as f:
            f.write(gpuPriceHistoryRaw[i])

get_gpu_prices(link_list)

