# SQueRT: The Scientific Query Research Tool

SQueRT is a web application that assists researchers by leveraging artificial intelligence to query the latest academic literature. It utilizes the state-of-the-art natural language processing deep learning models ALBERT and DistilBERT to search the academic literature database arXiv for articles  relevant to the user's query. SQueRT can greatly reduce the time and effort necessary find reported answers to research questions.

**Who is our user?**\
Our user is most likely to be a(n):
* academic
* student
* scientist
* scientific reporter or technical writer

In other words, our user is someone who reads scientific papers with the goal of finding and extracting information.

**What does our user want?**\
Our user is seeking answers to specific queries that can be found in scientific journal articles. Desired information might be general or specific in nature. It might include experimental data, conclusions, methodology, or domain knowledge. They might be seeking information that can be found in a single article and ultimately (as a stretch goal) information from multiple articles in a particular domain.

Given a user query and the keyword, our tool will return the relevant answer, the text snippet that contains the answer, and the link to the research paper from which the answer is extracted.


  Some examples of queries and responses are shown below, with actual text snippets from deep learning-related scientific journal articles returned by our model.

Examples:\
_Which model is proposed in the paper?_\
Answer: proposed GIL \
URL: https://arxiv.org/pdf/2001.06137.pdf \
Snippet : [Comprehensive evaluations on three citation network datasets (including Cora  Citeseer  and Pubmed) and one knowledge graph data (i.e.  NELL) demonstrate the superiority of our proposed GIL in contrast with other state-of-the-art methods on the semi-supervised classification task.]

_Which model proved to be extremely effective?_\
Answer: GIL /w learning on Vtr \
URL: https://arxiv.org/pdf/2001.06137.pdf \
Snippet : [When using structure relations  “GIL /w learning on Vtr" obtains an improvement of 1.9% (over “GCN /w learning on Vtr”)  which can be attributed to the building connection between nodes.]

_Which is the best model?_\
Answer: proposed GIL \
URL: https://arxiv.org/pdf/2001.06137.pdf \
Snippet : [Furthermore  we report the classification results of our proposed GIL by using mean and max-pooling mechanisms  respectively.GIL with mean pooling (i.e.  “GIL /w 2 conv layers + mean pooling") can get a better result than the GIL method with max-pooling (i.e.  “GIL /w 2 conv layers + max-pooling")  e.g.  86.2% vs 85.2% on the Cora graph dataset.]

_What are the graph construction techniques discussed?_\
Answer: static and dynamic graph construction \
URL: https://arxiv.org/pdf/1908.04942.pdf \
Snippet : [Although there are early attempts on constructing a graph from a sentence (Xu et al  2018b)  there is no clear an- swer as to the best way of representing text as a graph.We explore both static and dynamic graph construction approaches  and systematically investigate the performance differences between these two methods in the experimental section. Syntax-based static graph construction: We construct a directed and unweighted passage graph based on dependency parsing.]

_What is the difference between BiGNN and GraphSage?_\
Answer: fuse the intermediate node embeddings from both incoming and outgoing edges in every iteration during the training  whereas their model simply trains the node embeddings of each direction independently and concatenates them in the final step \
URL: https://arxiv.org/pdf/1908.04942.pdf \
Snippet : [However  one of key difference between our BiGGNN and their bidi- rectional GraphSAGE is that we fuse the intermediate node embeddings from both incoming and outgoing edges in every iteration during the training  whereas their model simply trains the node embeddings of each direction independently and concatenates them in the final step. In BiGGNN  node embeddings are initialized to the passage embeddings X returned by DAN.The same set of network parameters are shared at every hop of computation.
]

_What is common between SQIL and GAIL?_\
Answer: use deep Q-learning for RL \
URL: https://arxiv.org/pdf/1905.11108.pdf \
[SQIL outperforms GAIL in both conditions.Since SQIL and GAIL both use deep Q-learning for RL in this experiment  the gap between them may be attributed to the difference in the reward functions they use to train the agent.SQIL benefits from providing a constant reward that does not require fitting a discriminator  while GAIL struggles to train a discriminator to provide learned rewards directly from images.
]

Some examples of queries could be - 
_Which model is the best to use for this task?_\
_What is the name of the model to use?_ \
_What type of model should I use to do this?

**How do we know that our user is getting what they want?**\
We have included a feedback mechanism that asks the user to rank the relevancy of the result we provide. We would then have to track these relevancy reports and adjust our methods such that they provide more relevant results.

**How do we know that what we are doing is useful?**\
We will curate a test set of annotated data with expected output/results. We will use the test set as a metric to assess performance of our query tool. 

**What are our goals for these metrics? How will we use them to refine development?**\
Good ROUGE and/or BLEU scores. Note: define 'good'! How does our baseline do? How much of an improvement do we want over the baseline?

## Architecture
SQueRT is a Flask application with SQLite database support that runs in two primary stages. In the first stage, a web scraper is employed to scrape PDFs from arXiv.org based on the user's input. The text from the PDFs is processed and DistilBERT used to locate relevant text snippets. In the second stage, ALBERT is employed to rank candidate snippets according to their relevance to the user's query. Results are displayed on the web page, including a link to the PDF that contains the answer returned by SQueRT. The script Main.py acts as the Controller for the program. For a comprehensive list of packages used, see requirements.txt.

## User Manual
_Before attempting to run SQueRT, ensure that you have all the required packages installed. These are enumerated in requirements.txt._

The entry point to SQueRT is the script app.py.

**To run:**

Open a terminal window and navigate to the directory where SQueRT is located. On the command line, type ```python app.py```. The message ```Running on http://127.0.0.1:8080``` will appear shortly in Terminal. When it does, copy and paste the link http://127.0.0.1:8080 in a web browser.

> **Note**: Port 8080 must not be in use. If it is, you can either kill the running process and then try running app.py again or you can alter the port in the app.py script.
	
