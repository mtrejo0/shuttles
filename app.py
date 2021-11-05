from flask import Flask, jsonify
app = Flask(__name__)

import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import json

url = 'https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route=boston&_tab=stops'

@app.route('/')
def index():
    
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

        mins_away = int(times.split(",")[0])

        time_change = datetime.timedelta(minutes=mins_away)

        arrival_time = now + time_change

        arrival_time = arrival_time.strftime("%H:%M:%S")

        data.append({
            "name": name, 
            "times": times, 
            "mins_away": mins_away, 
            "arrival_time": arrival_time})

    current_time = now.strftime("%H:%M:%S")
    
    html = "<h1><a href=\"https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route=boston&_tab=stops\">Boston Daytime Shuttle</a></h1>"
    html += "<ul>"
    print(data)
    for each in data:
        html += "<li>" + each['name'] + "</li>"
        html += "<ul>"
        html += "<li>" + each["times"] + "</li>"
        html += "<li>Arrival Time:" + each["arrival_time"] + "</li>"
        if each["mins_away"] in list(range(8,10)):
            html += "LEAVE FOR STOP NOW!"
        html += "</ul>"
    html += "</ul>"

    return html

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)