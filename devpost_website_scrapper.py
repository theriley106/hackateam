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
        #print (events)
        #print ("---------------")

def request_stuff(events, page, i):
    devpost_url = "https://devpost.com/hackathons?page=" + str(page)
    devpost_html = requests.get(devpost_url)
    soup = BeautifulSoup(devpost_html.content, "lxml")
    event_titles = soup.select(".title")
    #event_locations = soup.select(".challenge-location")
    event_descriptions = soup.select(".challenge-description")
    '''event_prizes_dates = soup.select(".value")
    event_prizes = [None] * (len(event_prizes_dates)/2)
    event_dates = [None] * (len(event_prizes_dates)/2)'''
    #event_prizes = soup.select(".prizes .value")
    #print (len(event_prizes))
    event_dates = soup.select(".date-range")

    #If prize is non-monetory
    #if len(event_prizes) < len(event_titles):
#        event_prizes = soup.select(".prizes")
#    print (event_prizes)
    #If date abnormal
    if len(event_dates) < len(event_titles):
        event_dates = soup.select(".submission-time .value")

    '''j = 0
    k = 0
    for index in range(0, len(event_prizes_dates)):
        if index % 2 == 0:
            event_prizes[k] = event_prizes_dates[index].getText().strip()
            k+=1
        else:
            event_dates[j] = event_prizes_dates[index].getText().strip()
            j+=1'''

    #i = 0
    for index in range(0, len(event_titles)):
        event = {}
        event["name"] = event_titles[index].getText().strip()
        #event["location"] = event_locations[index].getText().strip()
        event["description"] = event_descriptions[index].getText().strip()
        #event["prizes"] = event_prizes[index]
        #event["dates"] = event_dates[index]
#        event["prizes"] = event_prizes[index].getText().strip()
        event["dates"] = event_dates[index].getText().strip()
        events[i] = event
        i += 1
    return i


@app.route('/')
def index():
    events = {}
    grabHackathons(events)
    #request_stuff(events)
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True, port=50981
    )
