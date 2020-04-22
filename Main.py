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



def main(query, keyword):
    # download_models.getModels()
    pdfdir = os.path.join(os.getcwd(), "Data/")
    txtdir = os.path.join(os.getcwd(), "DataTxt/")
    csvdir = os.path.join(os.getcwd(), "DataCsv/")
    snippetSize = 3
    outputJson = '{ "keyword": ' + '"' + keyword + '" ,' + '"query": ' + '"' + query + '" ,' + '"results": ['

    #Create Table
    db_operations.createTable()

    # Scrape papers to pdf folder
    arxiv_pdf_scraper.scrape(keyword, 1)
    # Convert pdfs to text, then to csv snippets
    for roots, dirs, files in os.walk(pdfdir):
        for pdfPaperName in files:
            ProcessText.pdfToText(os.path.join(pdfdir, pdfPaperName), txtdir)
            os.remove(os.path.join(pdfdir, pdfPaperName))
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, snippetSize, csvdir)
        os.remove(txtPaperName)
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
        print(relevantSnippets)
        print("\n\n")
        # From snippets for each paper, return answer
        predictions, snippet = albert_QA.question_answering_albert(query, relevantSnippets)
        paper_identifier = getUrl(csvPaperName)
        outputJson += '{' + \
                      '"predictions": ' + '"' + predictions + '" ,' + \
                      '"snippet": ' + '"' + snippet + '" ,' + \
                      '"paper_identifier": ' + '"' + paper_identifier + '" },'
        print(predictions)
        print(snippet)
        os.remove(csvPaperName)
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    url = 'http://localhost:'+str(s.getsockname()[1])+'/Data/'
    fileName = csvPaperName.rsplit('_', 1)[0] +'.pdf'
    url +=fileName
    print(url)



#pdfdir = os.path.join(os.getcwd(), "Data")
#print(pdfdir)
#for pdfPaperName in glob.glob(pdfdir):
#    print("Hello there!")

if __name__ == "__main__":
    main("What model is best for large batch training for bert", "Machine learning")