#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import spacy
import csv
import heapq

# In[ ]:
from transformers import DistilBertTokenizer, DistilBertModel
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


def returnRelevant(researchPaper, query, numSnippets = 15):
    # Make sure these are downloaded before using
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
    model = DistilBertModel.from_pretrained('distilbert-base-cased')
    relevantSnippets = []

    #researchPpr_NLP = spacy.load(model)
    with open(researchPaper, encoding='utf8') as researchPaperCSV:
        researchPaperReader = csv.reader(researchPaperCSV)
        score_max_heap = []
        input_ids = torch.tensor(tokenizer.encode(query, add_special_tokens=True, pad_to_max_length=True)).unsqueeze(0)
        queryObj = model(input_ids)[0].squeeze()
        #queryObj = model(query)
        for snippet in researchPaperReader:
            if('<EOS>' not in snippet):
                snippetStr = " "
                snippetStr = ' '.join([str(elem) for elem in snippet])
                input_ids = torch.tensor(tokenizer.encode(snippetStr, add_special_tokens=True, pad_to_max_length=True)).unsqueeze(0)
                snippetObj = model(input_ids)[0].squeeze()
                #snippetObj = model(snippetStr)
                #qs = QuerySnippet(query, snippet, queryObj.similarity(snippetObj))
                qs = QuerySnippet(query, snippet, torch.cosine_similarity(queryObj, snippetObj))
                if len(score_max_heap) < numSnippets or qs.similarity > score_max_heap[0].similarity:
                    if len(score_max_heap) == numSnippets: heapq.heappop(score_max_heap)
                    heapq.heappush(score_max_heap, qs)
        for qs in score_max_heap:
            relevantSnippets.append(qs.snippet)
    return relevantSnippets
