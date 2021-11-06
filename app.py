from flask import Flask, jsonify
app = Flask(__name__)

import requests
import re
from bs4 import BeautifulSoup
import time
import datetime
import json


def get_times(route_name, url):
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

    html = "<h1><a target=\"_blank\" href=\""+ url + "\">" + route_name +"</a></h1>"
    html += "<ul>"
    for each in data:
        html += "<li>" + each['name'] + "</li>"
        html += "<ul>"
        html += "<li>" + each["times"] + "</li>"
        html += "<li>Arrival Time:" + each["arrival_time"] + "</li>"
        if each["mins_away"] in list(range(8,10)):
            html += "LEAVE FOR STOP NOW!"
        html += "</ul>"
    html += "</ul>"
    if len(data) == 0 :
        html += "Its offline :("

    return html


def get_data(url):
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

url_daytime = 'https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route=boston'

url_beast = 'https://mobi.mit.edu/default/transit/route?feed=nextbus&direction=loop&agency=mit&route=saferidebostone'


@app.route('/')
def index():
    
    html = ""
    html += get_times("Boston Daytime Shuttle", url_daytime)
    html += get_times("Saferide Boston East", url_beast)
    
    return html

@app.route('/route_info')
def route_info():
        
    response = {
        "daytime": get_data(url_daytime),
        "beast": get_data(url_beast)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000)