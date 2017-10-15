#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import requests
from selenium import webdriver
import re
import gpxpy.geo
import bs4
import csv
from itertools import product
import time
import glob
import os
import json
import threading
from sklearn import tree
from geopy.geocoders import Nominatim
geolocator = Nominatim()

app = Flask(__name__)

with open('static/Final.csv') as csvfile:
		rows = csv.reader(csvfile)
		res = list(rows)

features = []
labels = []
for e in res:
	features.append([e[2]])
	labels.append(e[3])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)
DATASET = "static/val.csv"

@app.route('/calc/', methods=['POST'])
def Add():
	items = request.form.items()
	member1 = items[0][1]
	member2 = items[1][1]
	if '1' in str(determineTeamQuality(member1, member2)):
		return render_template("cc.html", member = grabUser(member1), memberz = grabUser(member2), memb = member1, membb = member2, f = "Good Match :)")
	else:
		return render_template("cc.html", member = grabUser(member1), memberz = grabUser(member2), memb = member1, membb = member2, f = "Not a Good Match :(")
	#print items['tctc'], items['pass']
	#a = account(items['tctc'], items['pass'])
	#return str(a.loggedIn())

@app.route('/login&<username>&<password>', methods=['GET', 'POST'])
def loginPage(username, password):
	a = manage(username, password)
	return jsonify(a.grabProfile())

@app.route('/hackathons/<hackathon>', methods=['GET', 'POST'])
def getHackathons(hackathon):
	return jsonify(grabHackathon(hackathon))

@app.route('/calc/<hackathon>', methods=['GET', 'POST'])
def calcRel(hackathon):
	info = []
	for e in genUserFromCsv():
		info.append({"Name": str(e)})
	return render_template("selection.html", participants=info)

@app.route('/user/<userid>', methods=['GET', 'POST'])
def userData(userid):
	return jsonify(grabUser(userid))

@app.route('/hackathons', methods=['GET', 'POST'])
def returnHackathons(database="static/Hackathons.csv"):
	a = []
	with open(database) as csvfile:
		rows = csv.reader(csvfile)
		res = list(rows)
	for lines in res:
		try:
			information = {}
			information["Location"] = lines[1]
			information["Pic"] = lines[2]
			information["Title"] = lines[0]
			longLat = lines[3]
			Long = longLat.partition(',')[0].strip()
			Lat = longLat.partition(',')[2].strip()
			information["Long"] = Long
			information["Lat"] = Lat
			a.append(information)
		except Exception as exp:
			pass
	return render_template("hackmap.html", hackathons=a)


@app.route('/map/<hackathon>', methods=['GET', 'POST'])
def genMap(hackathon):
	participants = []
	for file in glob.glob("static/*.json"):
		try:
			f = json.loads(str(open(file).read()))
			if f['Long'] != None:
				participants.append(f)
		except Exception as exp:
			print exp
	return render_template('map.html', participants=participants)

def genUserFromCsv():
	a = []
	with open(DATASET) as csvfile:
		rows = csv.reader(csvfile)
		res = list(rows)
	for e in res:
		a.append(e[0])
	return a

def diffBetween(user1, user2):
	total = 0
	try:
		userData1 = json.loads(open("static/{}.json".format(user1)).read())
	except:
		return None
		userData1 = grabUser(user1)
		'''file = open("static/{}.json".format(user1),"w")
		if len(str(userData1)) > 20:
			file.write(str(userData1))
		file.close()'''
			
	try:
		userData2 = json.loads(open("static/{}.json".format(user1)).read())
	except:
		try:
			return None
			userData2 = grabUser(user2)
			'''file = open("static/{}.json".format(user1),"w")
			if len(str(userData1)) > 20:
				file.write(str(userData1))
			file.close()'''
			
		except Exception as exp:
			print exp
	try:
		dist = gpxpy.geo.haversine_distance(float(userData1["Lat"]), float(userData1["Long"]), float(userData1["Lat"]), float(userData2["Long"])) * .0001
		total = total + dist
	except:
		total = total - 10
	if abs(float(userData1["Totals"]["Projects"]) - float(userData2["Totals"]["Projects"])) < 3:
		total = total + 100
	if abs(float(userData1["Totals"]["Hackathons"]) - float(userData2["Totals"]["Hackathons"])) < 2:
		total = total + 100
	if abs(float(userData1["Totals"]["Hackathons"]) - float(userData2["Totals"]["Hackathons"])) == 1:
		total = total + 100
	if abs(float(userData1["Totals"]["Hackathons"]) - float(userData2["Totals"]["Hackathons"])) > 20:
		total = total - 40
	if len(list(set(userData1["Skills"]).intersection(userData2["Skills"]))) > 10:
		total = total + 100
	if len(list(set(userData1["Skills"]).intersection(userData2["Skills"]))) > 5:
		total = total + 50
	return [user1, user2, total]


	



class manage(object):
	def __init__(self, username, password):
		self.status = self.login(username, password)


	def login(self, username, password):
		self.session = requests.session()
		r = self.session
		authenticity_token = re.findall('name="authenticity_token"\svalue="(\S+)"', str(r.get('https://secure.devpost.com/users/login').text))[0]
		data = {"utf8":"✓",
		'authenticity_token':authenticity_token,
		'user[email]':username,
		'user[password]': password,
		'return_to':'https://devpost.com/'}
		a = str(r.post("https://secure.devpost.com/users/login", data=data).url)
		if a != 'https://devpost.com/':
			status = False
		else:
			status = True
		return {"Status": status}

def quantifyJson(dic):
	total = 0
	total = total + len(dic["Skills"]) / 2
	if dic["Totals"]["Following"] > 5:
		total = total + 1
	if dic["Totals"]["Hackathons"] >= 2:
		total = total + 2
	if dic["Totals"]["Likes"] > 10:
		total = total + 2
	if dic["Totals"]["Projects"] > 10:
		total = total + 4
	if dic["Totals"]["Projects"] > 20:
		total = total + 5
	return total

def grabHackathon(hackathon='hackgt2017', name='.participant-name a'):
	url = 'https://{}.devpost.com/participants?page='.format(hackathon)
	s = requests.session()
	r = s.get(url)
	page = bs4.BeautifulSoup(r.text, "lxml")
	header = page.select("h3")
	participants = int(re.findall('\d+', str(header[0].getText()))[0])
	if participants % 20 != 0:
		num = ((20 - (participants % 20)) + participants) / 20
	else:
		num = participants / 20
	users = []
	driver = webdriver.PhantomJS()
	driver.get('https://{}.devpost.com/participants'.format(hackathon))
	for i in range(num):
		driver.get('javascript: window.scroll(0, document.documentElement.offsetHeight);')
		time.sleep(1)
	driver.save_screenshot('screen.png')
	return users

def genAllPossible(members, amt=4):
	return [a+b+c+d for a,b,c,d in product(members, repeat=amt)]

def grabUser(username):
	information = {}
	devpostUrl = 'https://devpost.com/{}'.format(username)
	res = requests.get(devpostUrl, headers = {'User-agent': 'your bot 0.1'})
	totalsElem = '.totals'
	photo = '#portfolio-user-photo'
	location = '#portfolio-user-links li'
	uname = '#portfolio-user-name'
	skillsElem = '.cp-tag , #portfolio-user-info a'
	page = bs4.BeautifulSoup(res.text, 'lxml')
	skills = []
	for skill in page.select(skillsElem):
		a = skill.getText().strip()
		if len(a) > 1:
			skills.append(a)
	try:
		ef = page.select(photo)
		profilePic = str(ef).partition('image-replacement" src="')[2].partition('"/')[0]
		if 'http' not in str(profilePic):
			profilePic = "http:" + profilePic
	except Exception as exp:
		profilePic = None
	try:
		userLocation = page.select(location)[0].getText().strip()
	except:
		userLocation = None
	if str(userLocation) == "Website":
		userLocation = None
	name = page.select(uname)[0].getText().partition('(')[0]
	totals = {}
	totals["Projects"] = page.select(totalsElem)[0].getText()
	totals["Hackathons"] = page.select(totalsElem)[1].getText()
	totals["Followers"] = page.select(totalsElem)[2].getText()
	totals["Following"] = page.select(totalsElem)[3].getText()
	totals["Likes"] = page.select(totalsElem)[4].getText()
	Projects = []
	if int(totals["Projects"]) != 0:
		for e in page.select('.visible'):
			photoUrl = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(e))[0]
			a = e.select("h5")[0].getText().strip()
			if len(a) > 2:
				projectAddress = "https://devpost.com/software/{}".format(a.lower())
				Projects.append({"URL": projectAddress, "Graphic": photoUrl})
	Hackathons = []
	if int(totals["Hackathons"]) != 0:
		res = requests.get('https://devpost.com/{}/challenges'.format(username), headers = {'User-agent': 'your bot 0.1'})
		page = bs4.BeautifulSoup(res.text, 'lxml')
		for comp in page.select("a > .large-9"):

			eventTitle = comp.select(".title")[0].getText().strip()
			eventLocation = comp.select(".challenge-location")[0].getText().strip()
			eventLongLat = None
			if str(eventLocation) != "Online":
				eventLongLat = genLongLat(eventLocation)
			Hackathons.append({"Event": eventTitle, "Location": eventLocation, "EventLongLat": eventLongLat})
	longLat = None
	if userLocation != None:
		try:
			longLat = genLongLat(userLocation)
		except Exception as exp:
			print exp
			longLat = None
	if longLat != None:
		Long = longLat.partition(',')[0].strip()
		Lat = longLat.partition(',')[2].strip()
	else:
		Long = None
		Lat = None
	a = {"devpostUrl": devpostUrl, "Lat": Lat, "Long": Long, "LongLat": longLat, "Hackathons": Hackathons, "Projects" : Projects, "Totals": totals, "Skills": list(set(skills)), "profilePic": profilePic, "userLocation": userLocation, "Name": name.strip()}
	return json.dumps(a)
def genLongLat(location):
	return str(geolocator.geocode(location)[1]).strip('(').strip(')')

def determineTeamQuality(member1, member2):
	a = diffBetween(member1, member2)
	return clf.predict([a[2]])


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)
	#print determineTeamQuality('hlin3565', 'NicholasGreenwald')
	#print len(genAllPossible(genUserFromCsv()))
	#username = raw_input('Username: ')
	#print grabUser(username)
	#print grabHackathon()