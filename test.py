import requests
import re
import bs4
import threading


def grabHackathons():
	res = requests.get('https://devpost.com/hackathons?page=1000')
	page = bs4.BeautifulSoup(res.text)
	num = int(page.select(".pagination a")[-1].getText().strip())
	elementToScrape = "Type the element here"
	def scrape(session, url, element):
		r = session.get(url)
		page = bs4.BeautifulSoup(r.text, "lxml")
		for val in page.select(element):
			try:
				users.append(val)
			except:
				print("Error on Val")
	s = requests.session()
	threads = [threading.Thread(target=scrape, args=(s, 'https://devpost.com/hackathons?page=' + str(pages), elementToScrape)) for pages in range(1, num)]
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return users