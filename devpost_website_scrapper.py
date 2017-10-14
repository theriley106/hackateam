#!flask/bin/python
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests, time
import urllib
import datetime
import threading

app = Flask(__name__)


def grabHackathons(events):
    devpost_html = requests.get('https://devpost.com/hackathons?page=1000')
    soup = BeautifulSoup(devpost_html.content, "lxml")
    num = int(soup.select(".pagination a")[-1].getText().strip())
    i = 0
    for pages in range(1, num+1):
        i = request_stuff(events, pages, i)

def request_stuff(events, page, i):
    devpost_url = "https://devpost.com/hackathons?page=" + str(page)
    devpost_html = requests.get(devpost_url)
    soup = BeautifulSoup(devpost_html.content, "lxml")
    event_titles = soup.select(".title")
    event_descriptions = soup.select(".challenge-description")
    event_dates = soup.select(".date-range")

    #If date abnormal
    if len(event_dates) < len(event_titles):
        event_dates = soup.select(".submission-time .value")

    for index in range(0, len(event_titles)):
        event = {}
        event["name"] = event_titles[index].getText().strip()
        event["description"] = event_descriptions[index].getText().strip()
        event["dates"] = event_dates[index].getText().strip()
        events[i] = event
        i += 1
    return i


@app.route('/')
def index():
    events = {}
    grabHackathons(events)
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=50981
    )
