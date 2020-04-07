#!/usr/bin/env python
# coding: utf-8

# In[3]:


import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import csv

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
def embed(input):
  return model(input)

# In[ ]:


def embed_useT(module):
    with tf.Graph().as_default():
        sentences = tf.placeholder(tf.string)
        embed = hub.Module(module)
        embeddings = embed(sentences)
        session = tf.train.MonitoredSession()
    return lambda x: session.run(embeddings, {sentences: x})
embed_fn = embed_useT('USE/')

# In[ ]:


def ApplyModel(csvPaperName, query):
    relevantSnippets = []
    file = csvPaperName.open(csvPaperName, rb)
    snippets = csv.reader(file, delimiter='<EOS>')
    query_embedding = embed([query])

    for snippet in snippets:
        snippet_embedding = embed([snippet])
        sim_matrix  = np.inner(snippet_embedding, query_embedding)
        if sim_matrix.max() > 0.3:
            releventSnippets.append(snippet)
        else:
          pass
    return relevantSnippets
