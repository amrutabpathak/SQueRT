#!/usr/bin/env python
# coding: utf-8

# In[1]:

import RelevantSnippets
import QuestionAnswering
import albert_QA
# import import_ipynb
import ProcessText
import glob
import os
print(dir(ProcessText))

# In[2]:


pdfdir = './Data/'
# txtdir = 'C:/Users/Evan/Documents/7180QueryTool/DataTxt/'
txtdir = "./DataTxt/"
#csvdir = "C:/Users/God/git/CS7800/7180QueryTool/DataCsv/"
csvdir = './DataCsv/'

# In[3]:


# Basic user interface; obtain query
query = "Which model is best for large batch optimization of bert?"
print("Query: %s", query)

# In[4]:


# Scrape papers to pdf folder
# %run -i arxiv_pdf_scraper "query" 1

# In[5]:


# Convert pdfs to text
# for pdfPaperName in glob.glob(pdfdir + "*.pdf"):
#     ProcessText.pdfToText(pdfPaperName, txtdir)

# In[6]:


# Convert text files to CSV snippets
if __name__ == "__main__":
    sentenceNum = 3
    for txtPaperName in glob.glob(txtdir + "*.txt"):
        ProcessText.snippetToCsv(txtPaperName, sentenceNum, csvdir)
    for csvPaperName in glob.glob(csvdir + "*.csv"):
        relevantSnippets = RelevantSnippets.returnRelevant(csvPaperName, query)
        print(relevantSnippets + "\n\n")
        # From snippets for each paper, return answer
        predictions = albert_QA.question_answering_albert(query, relevantSnippets)
        print(predictions)

# In[7]:


# Obtain best snippets for the query



# In[ ]:



