'''
To do:
- Exception handling if a PDF is taking too long to download
'''
import sys
from bs4 import BeautifulSoup
import urllib
from urllib import request
import os
import time
import re
from urllib import parse


def scrape(query, num_pdfs, topic = 'All'):
    if(topic != 'All'):
        query += ' ' + topic
    query = re.sub(' +', ' ', query)
    print(query)
    urlQuery = parse.quote_plus(query)
    print(urlQuery)
    url_prefix = 'https://arxiv.org/search/?searchtype=all&query='+urlQuery+'&abstracts=show&size=200&order=-announced_date_first&start='
    start_file_idx = 0
    urls = []
    export_urls = []
    num_retrieved = 0

    while num_retrieved < num_pdfs:
        url_to_scrape = url_prefix + str(start_file_idx)
        print(url_to_scrape)
        htmltext = urllib.request.urlopen(url_to_scrape).read()
        soup = BeautifulSoup(htmltext, "html.parser")

        # Extract urls for all pdfs linked to on page
        for link in soup.findAll('a', href=True):
            if len(urls) >= num_pdfs:
                break
            _FULLURL = link.get('href')
            if _FULLURL.startswith('https://arxiv.org/pdf/'):
                num_retrieved += 1
                urls.append(_FULLURL)

        if num_pdfs % 200 == 0:    # if num_pdfs is a multiple of 200
            start_file_idx += 200   # increment start index in url by 200 to get next page of results

    print("num_retrieved: ", num_retrieved)

    # Convert url list to the arxiv export form
    for addy in urls:
        addy = addy[:8] + 'export.' + addy[8:]
        export_urls.append(addy) 

    #print(export_urls)
    #export_urls_trunc = export_urls[:3]

    for doc in export_urls:
        print('Downloading %s' % doc)
        destination_file_name = os.path.join('webscraping/', doc[-10:]) + '.pdf'   # keep unique identifier for file name
        request.urlretrieve(doc, destination_file_name)
        time.sleep(1)   # be polite      


def main():
    '''
     Input: python filename <Query> <num_pdfs> <topic - optional>
     Then: sys.argv = [filename, <seed>]
     Example to invoke:
        python arxiv_pdf_scraper.py "What is the best accuracy achieved for mnist" 1000
        OR
        python arxiv_pdf_scraper.py "What is the best accuracy achieved for mnist" 1000 "Deep Learning"

    '''
    query = sys.argv[1]
    num_files = int(sys.argv[2])
    if len(sys.argv) == 3:
        scrape(query, num_files)
    elif len(sys.argv) == 4:
        topic = sys.argv[3]
        scrape(query, num_files, topic)
    else:
        print("Invalid arguments")


if __name__ == '__main__':
    main()