from bs4 import BeautifulSoup
import urllib
from urllib import request
import os
import time

destination = 'webscraping/'
prefix = 'https://arxiv.org/pdf/'
starting_url = 'https://arxiv.org/search/?searchtype=all&query=deep+learning&abstracts=show&size=200'

htmltext = urllib.request.urlopen(starting_url).read()
#print(htmltext)
soup = BeautifulSoup(htmltext, "html.parser")
urls = []
export_urls = []
count = 0

# Extract urls for all pdfs linked to on starting page
for link in soup.findAll('a', href=True):
    _FULLURL = link.get('href')
    if _FULLURL.startswith(prefix):
        urls.append(_FULLURL)
        count += 1

# Convert url list to the arxiv export form
for addy in urls:
	addy = addy.replace('https://', '')
	addy = 'export.' + addy
	addy = 'https://' + addy
	export_urls.append(addy)

#print(export_urls)
#print(len(export_urls))	

export_urls_trunc = export_urls[:3]

for doc in export_urls_trunc:
	print('Downloading %s' % doc)
	destination_file_name = os.path.join(destination, doc[-10:])	# keep unique identifier for file name
	destination_file_name = destination_file_name + '.pdf'
	print(destination_file_name)
	request.urlretrieve(doc, destination_file_name)
	time.sleep(1)	# be polite