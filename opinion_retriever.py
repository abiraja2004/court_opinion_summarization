import sys
from bs4 import BeautifulSoup
import urllib2
import requests
import time
import re
import os

count = 0
with open("case_urls.txt", "r") as f:
    for url in f:
        url_split = url.split('/')
        volume = url_split[6]
        docket = url_split[7]

        if count % 100 == 0:
            print("Completed {} cases. Processing case: {}/{}".format(count, volume, docket))
        count+=1

        summary_url = url[:-1]
        opinion_url = summary_url + "opinion.html"
        summary_data = requests.get(summary_url).text
        opinion_data = requests.get(opinion_url).text
        summary_soup = BeautifulSoup(summary_data, "html5lib")
        opinion_soup = BeautifulSoup(opinion_data, "html5lib")

        summaries = summary_soup.find_all('div', {'class': 'text-diminished'})
        opinions = opinion_soup.find_all('div', {'id': 'opinion'})

        if len(summaries) > 0:
            summary_path = "summaries/{}/{}.txt".format(volume, docket)
            if not os.path.exists(os.path.dirname(summary_path)):
                try:
                    os.makedirs(os.path.dirname(summary_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(summary_path, "w+") as summary_file:
                for s in summaries:
                    summary_file.write(s.getText().strip().encode('utf8') + "\n")
        if len(opinions) > 0:
            opinion_path = "opinions/{}/{}.txt".format(volume, docket)
            if not os.path.exists(os.path.dirname(opinion_path)):
                try:
                    os.makedirs(os.path.dirname(opinion_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(opinion_path, "w+") as opinion_file:
                for o in opinions:
                    opinion_file.write(o.getText().strip().encode('utf8') + "\n")


