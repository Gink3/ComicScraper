'''
	Taylor King
	telltaylor13@gmail.com
	
	Purpose: Grablinks from a index page of getcomics.info
	Outputs: A link.dat file that contatins a list of links to copy
	for jdownloader

	Has link duplication detection


	TODO:
		allow input of a search url and download results by page
		Add support for pages like https://getcomics.info/other-comics/sex-criminals-001-010-tpb-free-download/

	To run:
		source mods/bin/activate
		python3 comicScraper.py

	Files:
		rawlinks.dat
			Holds all newly scraped links
		cleanedlinks.dat
			new links that have not been previously scraped
		linklist.dat
			list of all links that have been scraped


'''
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os.path
import os

default_url = "https://getcomics.info/"
rawlinks = "rawlinks.dat"
linklist = "linklist.dat"
newlinks = "cleanedlinks.dat"
set_links = set()

#checks for linklist file, if not found creates
if not os.path.isfile(linklist):
	f=open(linklist,"w+")
	f.close()

#checks for rawlinks, removes old file
if os.path.isfile(rawlinks):
	os.remove(rawlinks)
	

#checks for cleanedlinks, removes old
if os.path.isfile(newlinks):
	os.remove(newlinks)
	


def index_page(url):
	#	Grabs index page
	#	Filters each link to a page
	#	to the appropriate function
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	post_info = soup.findAll('h1',{'class':'post-title'})
	for info in post_info:
		tags = info.findAll('a')
		for tag in tags:
			href_value = tag.get('href')
			if "week" in href_value:
				week_page(href_value)
			else:
				download(href_value)


def download(url):
	#	Figures out if a page
	#	is a red button or a
	#	collection page passes
	#	a soup to either red or collection
	#	functions
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	testtag = soup.find('a',{'title':'Download Now'})
	if testtag == None:
		tags = soup.findAll('a',{'rel':'noopener noreferrer'})
		for tag in tags:
			#print(tag)
			span = tag.find('span')
			if span != None and span.text == "Main Server":
				set_links.add(tag.get('href'))
		
		
	else:
		set_links.add(testtag.get('href'))



def week_page(url):
	#	New request
	#	New Soup
	#	Grab each link
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.findAll('a',{'rel':'noopener noreferrer'})
	for tag in tags:
		link = tag.get('href')
		download(link)





def write_links(linkset):
	with open(rawlinks,"a") as dataFile:
		for link in linkset:
			print(link)
			dataFile.write(link+'\n')
	


def clean_links(file_name):
	# compares raw links to see if contained in linklist file
	with open(newlinks,"w+") as nl:
		with open(rawlinks,'r') as rl:
			for raw in rl:
				with open(linklist,"a+") as links:
					found = False;
					for line in links:
						if line == raw:
							found = True
					if found:
						pass
					else:
						links.write(raw)
						nl.write(raw)


#iterates over the newest 16 pages of comics
for i in range(1,25):
	if i == 1:
		index_page("https://getcomics.info")
	
	else:
		#Sample url of the home page, 3
		#https://getcomics.info/page/3/
		index_page("https://getcomics.info/page/"+str(i)+"/")
		print("https://getcomics.info/page/"+str(i)+"/")
		write_links(set_links)
		clean_links(rawlinks)
		set_links.clear()

'''
download("https://getcomics.info/other-comics/teenage-mutant-ninja-turtles-1-70-extras-archie/")
write_links(set_links)
clean_links(rawlinks)
'''