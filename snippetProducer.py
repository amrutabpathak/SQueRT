import spacy
import glob
import os
import sys
import re
find_words = re.compile(r'(\w+\.?)')

def remove_symbols(file_content):
  file_input = file_content
  processed_output = re.sub(r'[^\w\s\-\?\.\!\,]', '', file_input)

  return processed_output

def remove_symbols_small_words(file_content):
  file_input = file_content
  first_process_list = re.findall(r'(\w|\.|\,|\?|\!|\-|\s)*', file_input)
  return first_process_list

def only_words(file_content):
  file_input = file_content
  first_process_list = re.findall(find_words, file_input)
  processed_file = ''
  nlp = spacy.load("en_core_web_sm")
  word_set = set(nlp.vocab)
  print(word_set)
  for possible_word in first_process_list:
    word_without_punc = re.findall(r'\w+', possible_word)
    word_with_punc = re.findall(r'\w+\.', possible_word)
    for a_word_without_punc in word_without_punc:
      nlp_word = nlp(a_word_without_punc)
      if nlp_word.text in nlp.vocab:
        # print(a_word_without_punc)
        if len(word_with_punc) <= 0:
          processed_file = processed_file + " " +  possible_word
        elif len(word_with_punc[0]) > 3:
          processed_file = processed_file + " " +  possible_word
  return processed_file
    

def snippetProducer(file, lengthSnippets):
    ''' Spacy is not working correctly with a large amount of symbols it tends
    to seperate a large amount of symbols into different sentences'''
    f = open(file, encoding='utf8', errors='ignore')
    file_content = f.read()
    processed_output = only_words(file_content)
    nlp = spacy.load("en_core_web_sm") # Loading Spacy Model for English
    doc = nlp(processed_output) # Applying spacy to raw text
    sentences = [sent.string.strip() for sent in doc.sents] # Changing document into sentences
    snippets = [] # Snippet Array
    # Takes each setence the spacy displays and for the lenght of snippet paramter
    # which should be the number of sentences returns a snippet of that number of sentences
    for i in range(0, len(sentences), lengthSnippets):
        snippet = ""
        for j in range(lengthSnippets):
            if i+j >= len(sentences):
                continue
            snippet = snippet + sentences[i+j] 
        snippets.append(snippet)
    return snippets

def snippetToCsv(researchFile, sentenceNum, csvdir):
  try:
    #Calling Spacy function to return a list
    #sentenceList = spacyFunction(researchFile,sentenceNum)
    #Test List
    snippets = snippetProducer(researchFile, sentenceNum)

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
    with open(fileName,"w+") as file: 
      for sentence in snippets:
          # print(str(sentence.encode(sys.stdout.encoding, errors='replace')))
          file.write(str(sentence.encode(sys.stdout.encoding, errors='replace')))
          file.write("\n")
          file.write("<EOS>")
          file.write("\n")
    
  except Exception as e:
    print ("Unexpected error occurred : Details are ", sys.exc_info()[0], sys.exc_info()[1])

def main():
    csvDir = "C:/Users/God/git/CS7800/7180QueryTool/DataCsv"
    dir = 'dataTxt/*.txt'
    for research_paper in glob.glob(dir):
      snippetToCsv(research_paper, 1,csvDir)
      # f = open(research_paper, encoding='utf8', errors='ignore')
      # file_content = f.read()
      # # print(remove_symbols_small_words(file_content))
      # print(only_words(file_content))
      return
main()