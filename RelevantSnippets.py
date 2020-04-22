#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import spacy
import csv
import heapq

# In[ ]:
from transformers import DistilBertTokenizer, DistilBertModel, DistilBertConfig
import torch


class QuerySnippet:

    def __init__(self, query, snippet, similarity):
        self.query = query
        self.snippet = snippet
        self.similarity = similarity

    
    def __gt__(self, other):
        return self.similarity > other.similarity

    def __lt__(self, other):
        return self.similarity < other.similarity

# In[ ]:

#def similarity(vec1, vec2):
#    import numpy
#    return numpy.dot(vec1, vec2) / (vec1 * vec2)

def similarity(x1, x2=None, eps=1e-8):
    x2 = x1 if x2 is None else x2
    w1 = x1.norm(p=2, dim=1, keepdim=True)
    w2 = w1 if x2 is x1 else x2.norm(p=2, dim=1, keepdim=True)
    return 1 - torch.mm(x1, x2.t()) / (w1 * w2.t()).clamp(min=eps)

def returnRelevant(researchPaper, query, numSnippets = 15):
    # Make sure these are downloaded before using
    config = DistilBertConfig.from_pretrained("distilbert-base-uncased")
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
    model = DistilBertModel.from_pretrained('distilbert-base-cased', config=config)
    relevantSnippets = []

    #from sentence_transformers import SentenceTransformer
    #model = SentenceTransformer('bert-base-nli-mean-tokens')
    #researchPpr_NLP = spacy.load(model)
    with open(researchPaper, encoding='utf8') as researchPaperCSV, torch.no_grad():
        researchPaperReader = csv.reader(researchPaperCSV)
        score_max_heap = []
        #queryArr = tokenizer.encode(query, add_special_tokens=True)
        #input_ids = torch.tensor(queryArr)
        #queryObj = model(input_ids)[0][0]
        input_ids = torch.tensor([tokenizer.encode(query, add_special_tokens=True)])
        print(input_ids)
        output_tuple = model(input_ids)
        last_hidden_states = output_tuple[0]
        queryObj = last_hidden_states.mean(1)
        #queryObj = model.encode(query)
        #queryObj = torch.tensor(queryObj)
        for snippet in researchPaperReader:
            if('<EOS>' not in snippet):
                snippetStr = " "
                snippetStr = ' '.join([str(elem) for elem in snippet])
                #snippetArr = tokenizer.encode(snippetStr, add_special_tokens=True)
                #input_ids = torch.tensor(snippetArr)
                #snippetObj = model(input_ids)[0][0]
                # Currently the snippet is just cut at 511 because if the snippet is too long distillbert breaks
                input_ids = torch.tensor([tokenizer.encode(snippetStr, add_special_tokens=True, max_length=2048)])
                output_tuple = model(input_ids)
                last_hidden_states = output_tuple[0]
                snippetObj = last_hidden_states.mean(1)
                #print(similarity(queryObj, snippetObj))
                #snippetObj = model.encode(snippetStr)
                #snippetObj = torch.tensor(snippetObj)
                #qs = QuerySnippet(query, snippet, queryObj.similarity(snippetObj))
                qs = QuerySnippet(query, snippet, similarity(queryObj, snippetObj))
                if len(score_max_heap) < numSnippets or qs.similarity > score_max_heap[0].similarity:
                    if len(score_max_heap) == numSnippets: heapq.heappop(score_max_heap)
                    heapq.heappush(score_max_heap, qs)
        for qs in score_max_heap:
            relevantSnippets.append(qs.snippet)
    return relevantSnippets
