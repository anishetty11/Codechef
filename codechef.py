import argparse
from bs4 import BeautifulSoup
import requests
import re
import logging
import os
import subprocess

logger=logging.getLogger()
logging.basicConfig(level='DEBUG')



def scrap(link,dir):

	'''
	To Extract the detials of the problems,and store it in a file
	'''
	
	# create BeautifullSoup object of the given link
	print("\n\n\n")
	print (link)
	r=requests.get(link)
	if not r:
		print("data not got")
		return
	soup=BeautifulSoup(r.content,'html.parser')

	# select the division of the html code which contains the problem 
	# statement 	

	divTag = soup.find_all("div", {"class": "content"})
	
	# the html code corresponding to the problem statement will be 
	# present in divTag[1]. Removing all the tags, and extracting the 
	# raw text

	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', divTag[1].decode())
	#print(cleantext)

	# extracting the problem name from the given link
	# e.g: www.codechef.com/LTIME51/problems/MATPAN => MATPAN
	filename=re.match('.*/(.*)',link).group(1)

	# write the extracted data into a file corresponding to the 
	# problem
	with open('%s/%s.py'%(dir,filename.lower()),'w') as fp:
		fp.write("'''\n%s\n'''"%cleantext)

	return '%s/%s.py'%(dir,filename.lower())




	



	



def main():

	'''
	 Download the contest page of the given contents code

	 '''


	parser=argparse.ArgumentParser()
	parser.add_argument("CONTESTCODE")
	args=parser.parse_args()
	page_address='https://www.codechef.com/%s'%(args.CONTESTCODE)
	print(page_address)


	# get the contents of the web page and save it in r
	r=requests.get(page_address)
	
	# create a beautiful soup object

	soup=BeautifulSoup(r.content,'html.parser')

	probs=[]
	# get all the links from the soup object
	for link in soup.find_all('a', href=True):

		# check if the links belong to a particular problem, 
		# links belonging to problems will have the following
		# pattern : www.codechef.com/<contest_name>/problems/<problem_name>
		#logger.debug(link)
		matchObj=re.search(r'%s/problems/.*'%args.CONTESTCODE,link['href'],re.I)

		# if link belongs to a problem, append it to probs[]
		if matchObj:
			probs.append('https://www.codechef.com/%s'%matchObj.group())

	logger.debug(probs)

	if len(probs)<1:
		print("Could not fetch the web page, check your network connection")
		return

	# create a new folder to store all the problems, 
	# you can change the path where the new folder will be created
	try:
		os.mkdir("%s"%args.CONTESTCODE)
	except FileExistsError as e:
		print (e)
		pass

	# call the scrap() function for each link(problem) 
	# scrap() function creates a file for each problem 
	# and returns the filename, the filenames are stored 
	# in a list called problems	
	problems=[]
	for i in probs:
		problems.append(scrap(i,args.CONTESTCODE))

	#print(problems)
	

	# open the created files using the given text editor
	text_editor=input("\n\n\nEnter you favourite text editor \n\
		e.q: if your fav text editor is Sublime-text: Enter subl\n")

	try:
		for i in problems:
			os.system('%s ~/Desktop/Python/%s'%(text_editor,i))
	except:
		pass

	print("Files have been created in the %s directory"%args.CONTESTCODE)




main()