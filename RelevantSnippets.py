#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import spacy
import csv
import heapq

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

# In[ ]:


def returnRelevant(researchPaper, query, numSnippets = 15):
    # Make sure these are downloaded before using
    # model_list = ['en_trf_bertbaseuncased_lg','en_trf_robertabase_lg','en_trf_distilbertbaseuncased_lg']
    model_list = ['en_trf_bertbaseuncased_lg']
    relevantSnippets = []
    
    for model in model_list:
        researchPpr_NLP = spacy.load(model)
        with open(researchPaper, encoding='utf8') as researchPaperCSV:
            researchPaperReader = csv.reader(researchPaperCSV)
            score_max_heap = []
            queryObj = researchPpr_NLP(query)
            for snippet in researchPaperReader:
                if('<EOS>' not in snippet):
                    snippetStr = " "
                    snippetStr = ' '.join([str(elem) for elem in snippet])
                    snippetObj = researchPpr_NLP(snippetStr)
                    qs = QuerySnippet(query, snippet, queryObj.similarity(snippetObj))
                    if len(score_max_heap) < numSnippets or qs.similarity > score_max_heap[0].similarity:
                        if len(score_max_heap) == numSnippets: heapq.heappop(score_max_heap)
                        heapq.heappush(score_max_heap, qs)
            for qs in score_max_heap:
                relevantSnippets.append(qs.snippet)
    return relevantSnippets
