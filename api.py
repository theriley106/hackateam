#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response
import login
import requests
import re


app = Flask(__name__)



@app.route('/login&<username>&<password>')
def fileDownloading(username, password):
	a = manage(username, password)
	return str(a.status)



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

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8888)