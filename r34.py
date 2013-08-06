#r34 pahael image ripper

#written by nokocode
#	Updated by SudoAge

#######
#If you like it, consider donating, Bitcoin: 1N67GRbwJz93k5DBJn6ETR3z1tPcw9BCnU
#Don't like it or found bugs? Drop a email too either anon@nokocode.tk or SudoAge@gmail.com
#######

#licensed under gpl 1.0
#Enjoy it anons.

import os
import urllib2
import urllib
from xml.dom import minidom
import urlparse
from urllib2 import urlopen, URLError, HTTPError

#set max number of pages
maxNumberOfPages = int(raw_input('how many pages max do you want?: '))
#pahael directory default name
pahealUrlPreAdd = 'http://rule34.paheal.net/post/list/'
directoryName = []
#get directory name
i = 0
directoryName.append(raw_input('What would you like rule 34 of?: '))

userDone = 1

while userDone != 0:
	isDoneInput = raw_input('any addl params? (leave blank to stop): ') 
	if isDoneInput:
		i+= 1
		directoryName.append(isDoneInput)
	if not isDoneInput:
		userDone = 0
		
#function that turns input into paheal readable text. 
def QueryParser(dirName):
	inputNameLength = len(dirName)
	i = inputNameLength - 1
	j = 0
	while j <= i:
		dirNameWords = dirName[j].split(' ')
		dirNameWordCount = len(dirNameWords)
		
		dirNameWordCount = dirNameWordCount - 1
		dirUnderscoreName = dirNameWords[0]
		k = 1
		while k <= dirNameWordCount:
			dirUnderscoreName += '_'
			dirUnderscoreName += dirNameWords[k]
			k += 1
		dirName[j] = dirUnderscoreName
		j += 1
	print dirName	
#calls function above
QueryParser(directoryName)


#adds spaces to new directory name with %20 for easier url parsing
stringCombinator = '%20'
newDirectoryName = stringCombinator.join( directoryName )
print newDirectoryName

#if directory doesn't exist, create it. 
if not os.path.exists(newDirectoryName):
	os.makedirs(newDirectoryName)

os.chdir(newDirectoryName)
	
pahealUrl = pahealUrlPreAdd + newDirectoryName + '/1'


print pahealUrl

def pageDownloader(pahealUrl):
	#get all a tags from web page
	aUrlList = []
	
	response = urllib2.urlopen(pahealUrl)
	html = response.read()
	
	filesThisMissed = 0
	aTagList = []
	html = html.split()
	
	for x in html:
		if not 'href' in x:
			continue
		elif 'Image' in x:
			aTagList.append(x)
		
	for link in aTagList:
		#once a tag contains image only text, split to get link. 
		linkString = str(link)
		urlNoHtmlTag = linkString.split('"')
		aUrlList.append(urlNoHtmlTag[1])
		
	#print aUrlList
	urlListLength = len(aUrlList)

	#attempt to write to directory...
	def dlfile(url):
		#open url
		try:
			f = urlopen(url)
			print "downloading " + url

			#open our local file for writing
			with open(os.path.basename(url), "wb") as local_file:
				local_file.write(f.read())
			
		#handle errors
		except HTTPError, e:
			print "HTTP Error:", e.code, url
		except URLError, e:
			print "URL Error:", e.reason, url
			
		
	urlListLength -= 1 
	i=0
	while urlListLength >=0:
		url = aUrlList[i]
		i += 1
		urlListLength -=1
		dlfile(url)
		print i
		print "of"
		print len(aUrlList)
		

pageIterator = 1
while pageIterator <= maxNumberOfPages:
	pahealUrl = pahealUrlPreAdd + newDirectoryName + '/' + str(pageIterator)
	pageDownloader(pahealUrl)
	pageIterator +=1
	
