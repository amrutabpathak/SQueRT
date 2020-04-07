#!/usr/bin/env python
# coding: utf-8

# Models Installation:
# Please note to restart your runtime for these to take effect

# In[1]:


!python -m spacy download en
!pip install spacy-transformers[cuda100]==0.5.1
!python -m spacy download en_trf_bertbaseuncased_lg
!python -m spacy download en_trf_robertabase_lg
!python -m spacy download en_trf_distilbertbaseuncased_lg


# One time step

# In[1]:


#One time step
!mkdir /content/googleUSE
!curl -L "https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed" | tar -zxvC /content/googleUSE


# In[ ]:


class QuerySnippet:

    def __init__(self, query, snippet, similarity):
        self.query = query
        self.snippet = snippet
        self.similarity = similarity

    
    def __gt__(self, other):
        return self.similarity > other.similarity

    def __lt__(self, other):
        return self.similarity < other.similarity


# In[14]:


import tensorflow_hub as hub
import csv 
import numpy as np
import heapq
import tensorflow

modelHeapDict2 = {}
model = 'Google_USE'

def googleUSEEmbedding(modelName):
    with tensorflow.Graph().as_default():
        researchStr = tensorflow.placeholder(tensorflow.string)
        hubModuleFn = hub.Module(modelName)
        reserachEmbedRes = hubModuleFn(researchStr)
        s = tensorflow.train.MonitoredSession()
    return lambda x: s.run(reserachEmbedRes, {researchStr: x})
researchEmbedding = googleUSEEmbedding('/content/googleUSE/')

def similarSentencesWIthGoogleUSE(researchPaper, queriesList, highestScoredNSnippets):
  print('Inside')
  with open(researchPaper) as researchPaperCSV:
    researchPaperReader = csv.reader(researchPaperCSV)
    print(researchPaperReader)
    score_max_heap = [] 
    for query in queriesList:
      #print(query)
      embeddedQuery = researchEmbedding([query])
      #print(embeddedQuery)
      for snippet in researchPaperReader:
          if('<EOS>' not in snippet):
            snippetStr = " "
            snippetStr = ' '.join([str(elem) for elem in snippet])
            #print('snippetStr:', snippetStr)
            embeddedSnippet = researchEmbedding([snippetStr])
            #print(embeddedSnippet)
            qs = QuerySnippet(query, snippet,  np.inner(embeddedQuery, embeddedSnippet))
            print(qs.query)
            print(qs.snippet)
            print(qs.similarity)
            if len(score_max_heap) < highestScoredNSnippets or qs.similarity > score_max_heap[0].similarity:
              if len(score_max_heap) == highestScoredNSnippets: heapq.heappop(score_max_heap)
              heapq.heappush( score_max_heap, qs )
      modelHeapDict2[model] =  score_max_heap       
  return  modelHeapDict2  

#similarSentencesWIthGoogleUSE('/content/large_batch_optimization_for_deep_learning_training_bert_in_76_minutes_1.csv',["Which is the best model"],10)



# In[15]:


'''for h in modelHeapDict2:
  print(h)
  print(modelHeapDict2[h])
  while modelHeapDict2[h]:
    qs = heapq.heappop(modelHeapDict2[h])
    print(qs.snippet)
    print(qs.similarity)  
'''

# Pass the snippet csv file, query list and number of results desired.
# 

# In[16]:


useHeapDict=similarSentencesWIthGoogleUSE('/content/graph_inference_learning_for_semi_supervised_classification_3.csv',["Which is the best model"],10)


# In[17]:


'''modelResultFile = open("/content/Model.txt", "a")

for model in useHeapDict:
  modelResultFile.write(model)
  modelResultFile.write("\n")
  modelHeap = useHeapDict[model]
  while modelHeap: 
    qs = heapq.heappop(modelHeap)
    modelResultFile.write(qs.query)
    modelResultFile.write("\n")
    modelResultFile.write(' '.join([str(elem) for elem in qs.snippet]))
    modelResultFile.write("\n")
    modelResultFile.write(str(qs.similarity))
    modelResultFile.write("\n")
    

modelResultFile.close()
'''

# Other Models
# 

# In[ ]:




# In[ ]:




# In[ ]:


import spacy
import csv
import heapq

# In[19]:



def compareDifferentLanguageModels(researchPaper,queriesList,highestScoredNSnippets = 10):
  spacy_model_list = ['en_trf_bertbaseuncased_lg','en_trf_robertabase_lg','en_trf_distilbertbaseuncased_lg']
  #queriesList= ["Which model is the best"]
  modelHeapDict = {}
  #model_bert = 'en_trf_bertbaseuncased_lg'
  
  
  #with open(researchPaper) as researchPaperCSV:
  #researchPaperReader = csv.reader(researchPaperCSV)
  #print(researchPaperCSV)
  #For every model , iterate
  for model in spacy_model_list:
    researchPpr_NLP = spacy.load(model)

    with open(researchPaper) as researchPaperCSV:
      researchPaperReader = csv.reader(researchPaperCSV)
      score_max_heap = [] 
      for query in queriesList:
        queryObj = researchPpr_NLP(query)
        print(queryObj)
        for snippet in researchPaperReader:
            #print(snippet)
            #EOS tag ignore
            if('<EOS>' not in snippet):
              #print(snippet)
              #snippet = 'In Advances in neural information processing systems pp 693–701 2011.'
              snippetStr = " "
              snippetStr = ' '.join([str(elem) for elem in snippet])
              #print(snippetStr)
              snippetObj = researchPpr_NLP(snippetStr)
              #print(snippetObj)
              qs = QuerySnippet(query, snippet,  queryObj.similarity(snippetObj))
              print(model)
              #print(qs.query)
              print(qs.snippet)
              print(qs.similarity)
              #heap logic
              if len(score_max_heap) < highestScoredNSnippets or qs.similarity > score_max_heap[0].similarity:
                if len(score_max_heap) == highestScoredNSnippets: heapq.heappop(score_max_heap)
                heapq.heappush( score_max_heap, qs )
    modelHeapDict[model] =  score_max_heap
    print(model)
    print(len(score_max_heap))            
  return  modelHeapDict         
'''
modelHeapDict=compareDifferentLanguageModels('/content/large_batch_optimization_for_deep_learning_training_bert_in_76_minutes_1.csv')
print(modelHeapDict)
for h in modelHeapDict:
  print(h)
  print(modelHeapDict[h])
  while modelHeapDict[h]:
    qs = heapq.heappop(modelHeapDict[h])
    print(qs.snippet)
    print(qs.similarity)
'''
  




# Pass The file and  Snippet arraylist below

# In[20]:


modelHeapDict=compareDifferentLanguageModels('/content/graph_inference_learning_for_semi_supervised_classification_3.csv',["Which is the best model"])


# Pass the filename with path to save the results 

# In[21]:



modelResultFile = open("/content/ModelComparison.tsv", "a")

for model in modelHeapDict:
  modelResultFile.write(model)
  modelResultFile.write("\n")
  modelHeap = modelHeapDict[model]
  while modelHeap:
    qs = heapq.heappop(modelHeap)
    modelResultFile.write(model)
    modelResultFile.write("\t")
    modelResultFile.write(qs.query)
    modelResultFile.write("\t")
    modelResultFile.write(' '.join([str(elem) for elem in qs.snippet]))
    modelResultFile.write("\t")
    modelResultFile.write(str(qs.similarity))
    print(qs.similarity)
    modelResultFile.write("\n")

for model in useHeapDict:
  modelResultFile.write(model)
  modelResultFile.write("\n")
  modelHeap = useHeapDict[model]
  while modelHeap: 
    qs = heapq.heappop(modelHeap)
    modelResultFile.write(model)
    modelResultFile.write("\t")
    modelResultFile.write(qs.query)
    modelResultFile.write("\t")
    modelResultFile.write(' '.join([str(elem) for elem in qs.snippet]))
    modelResultFile.write("\t")
    modelResultFile.write(str(qs.similarity))
    modelResultFile.write("\n")
    

modelResultFile.close()
