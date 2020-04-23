#!/usr/bin/env python
# coding: utf-8

# In[1]:

import RelevantSnippets
import albert_QA
import arxiv_pdf_scraper
import ProcessText
import glob
import os
import db_operations
import socket
import download_models
import re
import time

def main(query, keyword):
    # download_models.getModels()
    pdfdir = os.path.join(os.getcwd(), "Data/")
    txtdir = os.path.join(os.getcwd(), "DataTxt/")
    csvdir = os.path.join(os.getcwd(), "DataCsv/")
    snippetSize = 3
    outputJson = '{ "keyword": ' + '"' + keyword + '" ,' + '"query": ' + '"' + query + '" ,' + '"results": ['

    # Ensure directories are clear
    for root, dirs, files in os.walk(pdfdir):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(txtdir):
        for file in files:
            os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(csvdir):
        for file in files:
            os.remove(os.path.join(root, file))
    start_time = time.time()
    # Create Table
    db_operations.createTable()

    # Scrape papers to pdf folder
    arxiv_pdf_scraper.scrape(keyword, 1)
    time_to_scraping = time.time()
    time_scraping = time.time() - start_time
    # Convert pdfs to text, then to csv snippets
    for root, dirs, files in os.walk(pdfdir):
        for pdfPaperName in files:
            ProcessText.pdfToText(os.path.join(pdfdir, pdfPaperName), txtdir)
    time_to_pdf_to_text = time.time()
    time_pdf_to_text = time.time() - time_to_scraping
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, snippetSize, csvdir)
    time_to_snipptizing_csv = time.time()
    time_snipptizing_csv = time.time() - time_to_pdf_to_text
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
   
        relevantSnippetsFormated = []
        for snippet in relevantSnippets:
            relevantSnippetsFormated.append(snippet[0])
        time_to_stage1 = time.time()
        time_stage1_distillbert = (time.time() - time_to_snipptizing_csv)
        # From snippets for each paper, return answer
        # relevantSnippetsFormated must be list of strings and query must be passed as a list for whatever reason
        predictions, snippet = albert_QA.question_answering_albert(relevantSnippetsFormated, [query])
        time_stage2_albert = time.time() - time_to_stage1
        paper_identifier = getUrl(csvPaperName)
        total_time = time.time() - start_time
        print('''
Scraping PDFs: %1.3f seconds
PDFs to text: %1.3f seconds
Snippitizing and putting snippetis in CSV: %1.3f seconds
Stage 1 Distillbert: %2.3f seconds
Stage 2 Albert: %2.3f seconds
Total Time: %4.3f seconds\n''' % (time_scraping, time_pdf_to_text, time_snipptizing_csv, time_stage1_distillbert, time_stage2_albert, total_time))
        if paper_identifier is None:
            paper_identifier = ''
        outputJson += '{' + \
                      '"predictions": ' + '"' + predictions + '" ,' + \
                      '"snippet": ' + '"' + snippet + '" ,' + \
                      '"paper_identifier": ' + '"' + paper_identifier + '" },'
    outputJson += '] }'
    # removing the last comma
    lastCommaIndex = outputJson.rfind(",")
    resultJson = outputJson[:lastCommaIndex] + "" + outputJson[lastCommaIndex + 1:]
    print(resultJson)
    

    # paper_identifier and snippet need to be returned from above methods
    return resultJson


def save_feedback(topic, query, feedback):
    db_operations.updateRecords(topic, query, feedback)
    print('Feedback saved!')


def getUrl(csvPaperName):
    # This needs to actually return a url currently it returns a path to the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    # url = 'https://arxiv.org/pdf/' + str(s.getsockname()[1]) + '/Data/'
    url = 'https://arxiv.org/pdf/'
    fileName = csvPaperName.rsplit('_', 1)[0] +'.pdf'
    pathList = re.split(r'[\\/]', fileName)
    url +=pathList[-1]
    print(url)
    return url

# Run from here so as to properly employ multithreading
if __name__ == "__main__":
    main("What model is used in the paper?", "Machine learning")