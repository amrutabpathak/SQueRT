#!/usr/bin/env python
# coding: utf-8

# In[1]:

import RelevantSnippets
import albert_QA
# import import_ipynb
import ProcessText
import glob
import os
import db_operations


def main(query, topic):
    print(dir(ProcessText))
    pdfdir = './Data/'
    # txtdir = 'C:/Users/Evan/Documents/7180QueryTool/DataTxt/'
    txtdir = "./DataTxt/"
    #csvdir = "C:/Users/God/git/CS7800/7180QueryTool/DataCsv/"
    csvdir = './DataCsv/'
    # Basic user interface; obtain query
    # query = "Which model is best for large batch optimization of bert?"
    # print("Query: %s", query)
    #Create Table
    db_operations.createTable()

    # Convert text files to CSV snippets

    # Scrape papers to pdf folder
    # This no longer works without ipynb. There should probably be another way to run it.
    # %run -i arxiv_pdf_scraper "query" 1
    # Convert pdfs to text
    for pdfPaperName in glob.glob(pdfdir + "*.pdf"):
        ProcessText.pdfToText(pdfPaperName, txtdir)
        sentenceNum = 3
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, sentenceNum, csvdir)
    outputJson = '{ "topic": ' + '"' + topic + '" ,' + '"query": ' + '"' + query + '" ,' + '"results": ['
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
        print(relevantSnippets + "\n\n")
        # From snippets for each paper, return answer
        predictions, snippet = albert_QA.question_answering_albert(query, relevantSnippets)
        paper_identifier = getUrl(csvPaperName)
        outputJson += '{' + \
                      '"predictions": ' + '"' + predictions + '" ,' + \
                      '"snippet": ' + '"' + snippet + '" ,' + \
                      '"paper_identifier": ' + '"' + paper_identifier + '" },'
        print(predictions)
        print(snippet)
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
    url = 'http://localhost:8080/Data/'
    fileName = csvPaperName.rsplit('_', 1)[0] +'.pdf'
    url +=fileName
    return url

if __name__ == "__main__":
    main(query, topic)