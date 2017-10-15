import sys
reload(sys)
sys.setdefaultencoding('UTF8')

import bs4
import random
import requests
import csv
import json
import re
import api
import time
import threading
from itertools import combinations
'''from geopy.geocoders import Nominatim
geolocator = Nominatim()
def genLongLat(location):
	return str(geolocator.geocode(location)[1]).strip('(').strip(')')	
res = requests.get('https://mlh.io/seasons/na-2017/events')
page = bs4.BeautifulSoup(res.text)
boxes = page.select('.inner')
hackathons = []
for box in boxes:
	try:
		name = box.select("h3")[0].getText()
		city = box.select("span")[0].getText()
		state = box.select("span")[1].getText()
		date = box.select("p")[0].getText()
		pic = str(box.select('.image-wrap img')).partition('src="')[2].partition('"')[0]
		LatLong = genLongLat("{}, {}".format(city, state))
		hackathons.append([name, "{}, {}".format(city, state), pic, LatLong, date])
	except Exception as exp:
		print exp

with open("output.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(hackathons)'''
'''r = []
page = bs4.BeautifulSoup(open('x.html'))
e = page.select(".participant-portfolio a")
for a in e:
	r.append([str(a).partition('https://devpost.com/')[2].partition('">')[0]])
with open("output.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(r)'''

'''with open('file.csv', 'rb') as f:
	reader = csv.reader(f)
	your_list = list(reader)'''


'''with open('static/GATech.csv', 'rb') as f:
	reader = csv.reader(f)
	your_list = list(reader)
def doIt():
	a = []
	def getit(username):
		time.sleep(random.randint(1,30))
		try:
			e = api.grabUser(username)
			file = open("static/{}.json".format(username),"w")
			if len(str(e)) > 20:
				file.write(str(e))
			file.close()
		except Exception as exp:
			print exp
	threads = [threading.Thread(target=getit, args=username,) for username in your_list]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
r = []
for username in your_list:
	username = username[0]
	try:
		g = json.loads(str(open('static/{}.json'.format(username)).read()))
		g = api.quantifyJson(g)
		r.append([username, g])
	except Exception as exp:
		print exp
		pass
random.shuffle(r)
with open("output.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(r)'''


page = bs4.BeautifulSoup(open("k.html"), 'lxml')
goodPairs = []
for e in page.select("footer"):
	usernames = []
	for f in re.findall('data-url="\s*(.*?)\s*"', str(e)):
		usernames.append(f.replace('https://devpost.com/', ''))
	for pair in combinations(usernames, 2):
		goodPairs.append(list(pair))
final = []
for e in goodPairs:
	if len(e) > 1:
		try:
			afe = api.diffBetween(e[0], e[1])
			if afe != None:
				final.append(afe)
				print afe
		except Exception as exp:
			print exp



with open("Final.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(final)