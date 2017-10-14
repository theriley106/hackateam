#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import requests
import re
import bs4
import threading


app = Flask(__name__)



@app.route('/login&<username>&<password>', methods=['GET', 'POST'])
def loginPage(username, password):
	a = manage(username, password)
	return jsonify(a.grabProfile())

@app.route('/hackathons/<hackathon>', methods=['GET', 'POST'])
def getHackathons(hackathon):
	return jsonify(grabHackathon(hackathon))

@app.route('/user/<userid>', methods=['GET', 'POST'])
def userData(userid):
	return jsonify(grabUser(userid))

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








def grabHackathon(hackathon='hackgt2017', name='.participant-name a'):
	url = 'https://{}.devpost.com/participants?page='.format(hackathon)
	s = requests.session()
	r = s.get(url)
	page = bs4.BeautifulSoup(r.text, "lxml")
	header = page.select("h3")
	participants = int(re.findall('\d+', str(header[0].getText()))[0])
	print participants
	if participants % 20 != 0:
		num = ((20 - (participants % 20)) + participants) / 20
	else:
		num = participants / 20
	users = []
	def scrape(session, url, element, headers={}):
		print url
		r = session.get(url, headers=headers)
		print str(r.history)
		page = bs4.BeautifulSoup(r.text, "lxml")
		for user in page.select(element):
			try:
				users.append(user)
			except:
				print("Error on User in {}".format(hackathon))
	s = requests.session()
	threads = [threading.Thread(target=scrape, args=(s, url + str(pages), name, {"Referer":"https://{}.devpost.com/participants?page=2".format(hackathon)},)) for pages in range(1, num)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return users

def grabUser(username):
	information = {}
	res = requests.get('https://devpost.com/{}'.format(username))
	totalsElem = '.totals'
	photo = '#portfolio-user-photo .image-replacement'
	location = '#portfolio-user-links li'
	uname = '#portfolio-user-name'
	skillsElem = '.cp-tag , #portfolio-user-info a'
	page = bs4.BeautifulSoup(res.text, 'lxml')
	skills = []
	for skill in page.select(skillsElem):
		a = skill.getText().strip()
		if len(a) > 1:
			skills.append(a)
	profilePic = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(page.select(photo)))[0]
	try:
		userLocation = page.select(location)[0].getText()
	except:
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
		res = requests.get('https://devpost.com/{}/challenges'.format(username))
		page = bs4.BeautifulSoup(res.text, 'lxml')
		for comp in page.select("a > .large-9"):

			eventTitle = comp.select(".title")[0].getText().strip()
			eventLocation = comp.select(".challenge-location")[0].getText().strip()
			Hackathons.append({"Event": eventTitle, "Location": eventLocation})
	return {"Hackathons": Hackathons, "Projects" : Projects, "Totals": totals, "Skills": list(set(skills)), "profilePic": profilePic, "userLocation": userLocation.strip(), "Name": name.strip()}

		

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)
	#username = raw_input('Username: ')
	#print grabUser(username)