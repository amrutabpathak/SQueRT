'''
To do:
- Fix returning an extra file when input num isn't a multiple of 200
- Exception handling if a PDF is taking too long to download
'''
import sys
from bs4 import BeautifulSoup
import urllib
from urllib import request
import os
import time


def scrape(num_pdfs):
    url_prefix = 'https://arxiv.org/search/?searchtype=all&query=deep+learning&abstracts=show&size=200&order=-announced_date_first&start='
    start_file_idx = 0
    urls = []
    export_urls = []
    num_retrieved = 0

    #while start_file_idx + 200 <= num_pdfs:
    while num_retrieved < num_pdfs:
        url_to_scrape = url_prefix + str(start_file_idx)
        htmltext = urllib.request.urlopen(url_to_scrape).read()
        soup = BeautifulSoup(htmltext, "html.parser")

        # Extract urls for all pdfs linked to on page
        for link in soup.findAll('a', href=True):
            if len(urls) > num_pdfs:
                break
            _FULLURL = link.get('href')
            if _FULLURL.startswith('https://arxiv.org/pdf/'):
                #while len(urls) < num_pdfs:
                num_retrieved += 1
                urls.append(_FULLURL)
                #num_retrieved += 1

        if num_pdfs % 200 == 0:    # if num_pdfs is a multiple of 200
            start_file_idx += 200   # increment start index in url by 200 to get next page of results

    print("num_retrieved: ", num_retrieved)
    # Convert url list to the arxiv export form
    for addy in urls:
        addy = addy[:8] + 'export.' + addy[8:]
        export_urls.append(addy) 

    print(export_urls)
    print(len(export_urls)) 
    #print(export_urls[497])

    #export_urls_trunc = export_urls[:3]

    for doc in export_urls:
        print('Downloading %s' % doc)
        destination_file_name = os.path.join('webscraping/', doc[-10:]) + '.pdf'   # keep unique identifier for file name
        request.urlretrieve(doc, destination_file_name)
        time.sleep(1)   # be polite      


def main():
    '''
     Input: python filename <num_pdfs>
     Then: sys.argv = [filename, <seed>]
     Example to invoke:
        python arxiv_pdf_scraper.py 1000
    '''
    num_files = int(sys.argv[1])
    scrape(num_files)


if __name__ == '__main__':
    main()