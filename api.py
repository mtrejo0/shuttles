import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import json

def get_stops_data(route, stop):

    try:
        url = 'https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route={}'.format(route)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        m = re.findall('\n.*mins', soup.get_text())

        now = datetime.datetime.now()

        data = []
        for g in m:
            
            s = g.split("Arriving in")

            if len(s) < 2: continue
            name = s[0].strip()
            times = s[1].strip()

            if len(times.split(",")) < 1 : continue
            if len(times.split(",")[0].split(" ")) < 1 : continue
            
            mins_away = int(times.split(",")[0].split(" ")[0])

            time_change = datetime.timedelta(minutes=mins_away)

            arrival_time = now + time_change

            arrival_time = arrival_time.strftime("%H:%M:%S")

            data.append({
                "name": name, 
                "times": times, 
                "mins_away": mins_away, 
                "arrival_time": arrival_time})

            if name == stop:
                
                return stop + ": " + str(times)
        
        return stop + ": Not Available" 
        
    except Exception as e:

        return stop + ": Not Available"


def get_m2_stop(stop):

    try:

        url = 'https://harvard.transloc.com/t/routes/4015412'

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        m = re.findall('\n.*mins', soup.get_text())


        soup = str(soup)

        soup = soup[soup.index(stop):]

        soup = soup[:400]

        soup = soup[:soup.index("<abbr title=\"minutes\">")]


        t = "<span class=\"time_1\">"
        times = soup[soup.index(t) + len(t):].split("&amp;")

        times = ", ".join([each.strip().replace("&lt;", "<") for each in times]) + " mins"

        return stop + " " + times

    except Exception as e:
        print(e)
        return stop + ": Not Available"

