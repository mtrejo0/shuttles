import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import json

def get_stops_data(id):

    url = 'https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route={}'.format(id)

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
    return data

