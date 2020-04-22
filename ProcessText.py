#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import glob
import sys
import re

# pip install pdfminer.six
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

# In[7]:


# Negative Look behind for WC.WCAnyCharacter Capitallower. Capital. Positive Look behind for . ? !
# Making sure that following is a capital or a number.
split_sentences = re.compile(r'(?<!\w\.\w.)(?<!\s[A-Z][a-z]\.)(?<!\s[A-Z]\.)(?<!\s[a-z]\.)(?<=\.|\?|\!)\s(?=[A-Z0-9]|\s|\“[A-Z0-9])')
#Replace words now removes citations in () but only them.
remove_intext_citations = r'\([\w-]+\s[\w&]+\s[\w,\.]+\s[0-9]+\)'
replace_words = [r'conv\.', r'\sal\.', r'\spp\.', r'\sFig\.', r'\s\.\s', r'\sEqn.', 'ﬁ', r'\(Nos.', remove_intext_citations]
replace_to_word = [' conv', ' al', ' pp', ' Fig', '', ' Eqn', 'fi', '(Nos', '']
remove_references = r'REFERENCES\n|Works Cited\n|References\n'

#     f = open(file, encoding='utf8', errors='ignore')
#     file_content = f.read()

# In[8]:


def pdfToText(research_paper_name, txtdir):
    #Create directory for the text files
    if (not os.path.exists(txtdir)):
        os.mkdir(txtdir)
    
    fp = open(research_paper_name, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    #codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()
    research_paper_txt_name = research_paper_name.replace("pdf","txt")
    research_paper_txt_name = research_paper_txt_name.replace("Data","Datatxt")
    output_file = open(research_paper_txt_name, "wb")
    output_file.write(data.encode("utf8"))
    fp.close()

# In[9]:


def snippetToCsv(researchFile, sentenceNum, csvdir):
  try:
    #Calling Spacy function to return a list
    #sentenceList = spacyFunction(researchFile,sentenceNum)
    #Test List
    snippets = snippetProducerSplit(researchFile, sentenceNum)

    #Splitting file name and path
    filePath, fileName = os.path.split(researchFile)

    #Creating a separate folder for all the csv files if it does not exist
    snippetDataDirPath = "C:/Users/God/git/CS7800/7180QueryTool/DataCsv"

    # Creating a folder for all the csv files if it does not exist
    if( not os.path.exists(csvdir)):
      os.mkdir(csvdir)

    #create a file name : Eg BestModel_3.csv
    fileName = fileName.replace(".txt","")
    fileName = fileName +"_"+ str(sentenceNum) + ".csv"
    # print(fileName)

    #Complete path
    fileName = csvdir +"/"+fileName

    #Checking if the files already exist in snippet_data
    if(glob.glob(fileName)):
      print("File already exists.")
      return

    #If not, we create and write in the files
    with open(fileName,"w+", encoding='utf-8' ) as file: 
      for sentence in snippets:
          # print(str(sentence.encode(sys.stdout.encoding, errors='replace')))
          # file.write(str(sentence.encode(sys.stdout.encoding, errors='replace')))
          file.write(sentence)
          file.write("\n")
          file.write("<EOS>")
          file.write("\n")
    file.close()
    
  except Exception as e:
    print ("Unexpected error occurred : Details are ", sys.exc_info()[0], sys.exc_info()[1])


# In[10]:


def snippetProducerSplit(file, lengthSnippets):
    f = open(file, encoding='utf8', errors='ignore')
    file_content = f.read()
    # Replaces certain words that likely end with a period with words without aperiod
    for i in range(len(replace_words)):
      file_content = re.sub(replace_words[i], replace_to_word[i], file_content)
    # Split at sentences which means its in regex \w\.\s[A-Z0-9]|\s
    # So its splits at word character a period or ! or ? followed by a space then A-Z capital or 0-9 or a space
    sentences = re.split(split_sentences, file_content)
    snippets = [] # Snippet Array
    # Takes each setence the spacy displays and for the lenght of snippet paramter
    # which should be the number of sentences returns a snippet of that number of sentences
    for i in range(0, len(sentences), lengthSnippets):
        snippet = ""
        for j in range(lengthSnippets):
            if i+j >= len(sentences):
                continue
            snippet = snippet + sentences[i+j]
        if re.search(remove_references, snippet) is not None:
            return snippets
        snippet = re.sub(r'\n', ' ', snippet)
        print(snippet)
        snippets.append(snippet)
    return snippets

# In[ ]:




# In[ ]:



