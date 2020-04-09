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

print(dir(ProcessText))
pdfdir = './Data/'
# txtdir = 'C:/Users/Evan/Documents/7180QueryTool/DataTxt/'
txtdir = "./DataTxt/"
#csvdir = "C:/Users/God/git/CS7800/7180QueryTool/DataCsv/"
csvdir = './DataCsv/'
# Basic user interface; obtain query
# query = "Which model is best for large batch optimization of bert?"
# print("Query: %s", query)


# Convert text files to CSV snippets
if __name__ == "__main__":
    # Scrape papers to pdf folder
# This no longer works without ipynb. There should probably be another way to run it.
# %run -i arxiv_pdf_scraper "query" 1
# Convert pdfs to text
    for pdfPaperName in glob.glob(pdfdir + "*.pdf"):
        ProcessText.pdfToText(pdfPaperName, txtdir)
        sentenceNum = 3
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, sentenceNum, csvdir)
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
        print(relevantSnippets + "\n\n")
        # From snippets for each paper, return answer
        predictions = albert_QA.question_answering_albert(query, relevantSnippets)
        print(predictions)

def saveFeedback(topic, query, feedback):
    db_operations.updateRecords(topic, query, feedback)
    print('Feedback saved!')





