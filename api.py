#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import requests
import re
import bs4


app = Flask(__name__)



@app.route('/login&<username>&<password>', methods=['GET', 'POST'])
def loginPage(username, password):
	a = manage(username, password)
	return str(a.grabProfile())



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

	def grabProfile(self, url='https://hackgt2017.devpost.com/participants?page=', name='.participant-name a'):
		information = []
		r = self.session.get(url)
		page = bs4.BeautifulSoup(r.text, "lxml")
		header = page.select("h3")
		participants = int(re.findall('\d+', str(header[0].getText()))[0])
		print participants
		if participants % 20 != 0:
			num = ((20 - (participants % 20)) + participants) / 20
		else:
			num = participants / 20
		for e in range(1, num):
			r = requests.get(url + str(e))
			page = bs4.BeautifulSoup(r.text, "lxml")
			for user in page.select(name):
				information.append(user)
		return information



		

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)