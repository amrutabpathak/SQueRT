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


def scrape(keyword, num_pdfs):
    num_results_displayed = 25
    urlQuery = parse.quote_plus(keyword)
    url_prefix = 'https://arxiv.org/search/?searchtype=all&query='+urlQuery+'&abstracts=show&size='+str(num_results_displayed)+'&order=-announced_date_first&start='
    start_file_idx = 0
    urls = []
    export_urls = []
    num_retrieved = 0

    while num_retrieved < num_pdfs:
        url_to_scrape = url_prefix + str(start_file_idx)
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

        # Handle case when no search results found
        if num_retrieved == 0:
            print("No search results found. Please try a different search.")
            raise Exception

        if num_pdfs % num_results_displayed == 0:    # if num_pdfs is a multiple of num displayed results
            start_file_idx += num_results_displayed   # increment start index in url to get next page of results

    # Convert url list to the arxiv export form
    for addy in urls:
        addy = addy[:8] + 'export.' + addy[8:]
        export_urls.append(addy)

    # Create webscraping folder if it doesn't already exist
    check_folder = os.path.isdir('Data')
    if not check_folder:
        os.makedirs('Data')
        print("created folder: ", 'Data')

    for doc in export_urls:
        print('Downloading %s' % doc)
        destination_file_name = os.path.join('Data/', doc[-10:]) + '.pdf'   # keep unique identifier for file name
        request.urlretrieve(doc, destination_file_name)
        time.sleep(1)   # be polite


def main():
    '''
     Input: python filename <keyword> <num_pdfs>
     Then: sys.argv = [filename, <seed>]
     Example to invoke:
        python arxiv_pdf_scraper.py "cifar" 100
    '''
    keyword = sys.argv[1]
    num_files = int(sys.argv[2])
    if len(sys.argv) == 3:
        scrape(keyword, num_files)
    else:
        print("Invalid arguments")


if __name__ == '__main__':
    main()
