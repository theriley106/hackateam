#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
def login(username, password):
	r = requests.session()
	authenticity_token = re.findall('name="authenticity_token"\svalue="(\S+)"', str(r.get('https://secure.devpost.com/users/login').text))[0]
	data = {"utf8":"✓",
	'authenticity_token':authenticity_token,
	'user[email]':username,
	'user[password]': password,
	'return_to':'https://devpost.com/'}
	if str(r.post("https://secure.devpost.com/users/login", data=data).url) != 'https://devpost.com/':
		return False
	else:
		return True

