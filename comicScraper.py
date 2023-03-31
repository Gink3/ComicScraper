#!/usr/bin/python3

'''
	Taylor King
	telltaylor13@gmail.com
	
	Purpose: Grablinks from a index page of getcomics.info
	Outputs: A link.dat file that contatins a list of links to copy
	for jdownloader




	TODO:
		allow input of a search url and get_link results by page
		Add support for pages like https://getcomics.info/other-comics/sex-criminals-001-010-tpb-free-get_link/

	To run:
		source mods/bin/activate
		python3 comicScraper.py




'''
import requests
import urllib.request
import urllib.parse
import time
from bs4 import BeautifulSoup
import os.path
import os
import sys
import argparse

rawlinks = "links.txt"
set_links = set()
query = ""
debug = 0

parser = argparse.ArgumentParser (
        prog = 'ComicScraper' )

parser.add_argument( '-q', '--query' )
parser.add_argument( '-s', '--start-page', type=int, default=1 )
parser.add_argument( '-n', '--num-pages', type=int, default=1 )
parser.add_argument( '-w', '--write-links', action='store_true' )
parser.add_argument( '-a', '--append-links', action='store_true' )
parser.add_argument( '-o', '--output' )
parser.add_argument( '-d', '--debug', action='store_true' )

args = parser.parse_args()

if args.query:
	query = "/?s=" + urllib.parse.quote_plus(args.query)
	
if args.output:
	rawlinks = args.output

if args.debug:
	debug = 1


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
			if debug: print(href_value)
			if "week" in href_value:
				week_page(href_value)
			else:
				get_link(href_value)


def get_link(url):
	#	Figures out if a page
	#	is a red button or a
	#	collection page passes
	#	a soup to either red or collection
	#	functions
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	titlesoup = soup
	testtag = soup.find('a',{'title':'Download Now'})
	if testtag == None:
		tags = soup.findAll('a',{'rel':'noopener noreferrer'})
		for tag in tags:
			if debug: print(tag)
			span = tag.find('span')
			if debug: print(type(span))
			if span != None:
				if span.text == "Main Server":
					link = tag.get('href')
					title = titlesoup.find('section',{'class':'post-contents'}).h2
					titletext = title.text
					titletext = titletext.replace("The Story – ", "")
					statustext = titletext
					titletext = titletext.replace(" ","_")
					set_links.add(link + " " + titletext)
					print(statustext)
	else:
		link = testtag.get('href')
		title = titlesoup.find('section',{'class':'post-contents'}).h2
		titletext = title.text
		titletext = titletext.replace("The Story – ","")
		statustext = titletext
		titletext = titletext.replace(" ","_")
		set_links.add(link + " " + titletext)
		print(statustext)
		

def week_page(url):
	print("Week Page")
	#	New request
	#	New Soup
	#	Grab each link
	response = requests.get(url)
	data = response.text
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.findAll('a',{'rel':'noopener noreferrer'})
	for tag in tags:
		link = tag.get('href')
		if link != None:
			get_link(link)
		else:
			pass


def write_links(linkset):
	if args.write_links or args.append_links:
		print("Writing links")
		with open(rawlinks,"a+") as dataFile:
			for link in linkset:
				dataFile.write(link+'\n')
	
				
if args.write_links and not args.append_links: 
	open( rawlinks, "w" )

for i in range(args.start_page,args.start_page + args.num_pages):
	if i == 1:
		url = "https://getcomics.info"+query
		if debug: print(url)
		index_page(url)
	else:
		url = "https://getcomics.info/page/"+str(i)+query
		if debug: print(url)
		index_page(url)	
	write_links(set_links)
	set_links.clear()
