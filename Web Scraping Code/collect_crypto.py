import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import os
import requests

rvn = "https://2miners.com/rvn-network-difficulty"
ergo = "https://2miners.com/erg-network-difficulty"
xmr = "https://2miners.com/xmr-network-difficulty"

weblist = [rvn, ergo, xmr]

def scrape_difficulty(weblist):
    for web in weblist:
        # Make a GET request to the website
        response = requests.get(web)
        # Click "All-time"
        response = requests.get(web + "?time=all")
        # Get the network request URL
        coin_name = web[web.rfind("/") + 1:web.rfind("-")]
        if coin_name == "rvn-network":
            request_url = "https://hr.2miners.com/api/v1/hashrate/1d/rvn"
        elif coin_name == "erg-network":
            request_url = "https://hr.2miners.com/api/v1/hashrate/1d/erg"
        elif coin_name == "xmr-network":
            request_url = "https://hr.2miners.com/api/v1/hashrate/1d/xmr"
        else:
            raise ValueError("Unsupported coin name: " + coin_name)
        print("request_url: " + request_url)
        # Make a GET request to the network request URL
        response = requests.get(request_url)
        # Get the response body
        response_text = response.text
        # Save the response as a text file
        filename = web[web.rfind("/") + 1:web.rfind("-")]
        with open(f"network_txt/{filename}.txt", "w") as f:
            f.write(response_text)






import re
import shutil

# extract the difficulty data from the text files
def extract_difficulty():
    # Create a dictionary to hold difficulty data for each crypto
    difficulties = {"rvn": [], "ergo": [], "xmr": []}

    # Clear out the network_csv folder
    shutil.rmtree("network_csv")
    os.mkdir("network_csv")

    # For each text file in network_txt
    for textfile in os.listdir("network_txt"):
        with open("network_txt/" + textfile, "r") as f:
            data = f.read()

        # Extract the difficulty and timestamp values for the corresponding crypto
        if "rvn" in textfile or "erg" in textfile or "xmr" in textfile:
            diff_values = re.findall(r'"difficulty":\s*(\d+)', data)
            time_values = re.findall(r'"timestamp":\s*(\d+)', data)
            datetime_values = [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tv))) for tv in time_values]

            # Add the difficulty and timestamp values to the dictionary
            if "rvn" in textfile:
                difficulties["rvn"] += list(zip(datetime_values, diff_values))
            elif "erg" in textfile:
                difficulties["ergo"] += list(zip(datetime_values, diff_values))
            elif "xmr" in textfile:
                difficulties["xmr"] += list(zip(datetime_values, diff_values))

    # save the difficulties to separate csv files for each crypto
    for c in difficulties:
        with open(f"network_csv/{c}_difficulties.csv", "w", newline="") as f:
            writer = csv.writer(f)

            # Write a header row with the column names
            writer.writerow(["datetime", "difficulty"])

            # Write the difficulty and timestamp data to the corresponding columns
            for row in difficulties[c]:
                writer.writerow(row)

scrape_difficulty(weblist)
extract_difficulty()
