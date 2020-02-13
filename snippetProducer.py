import spacy

def snippetProducer(file, lengthSnippets):
    ''' Spacy is not working correctly with a large amount of symbols it tends
    to seperate a large amount of symbols into different sentences'''
    nlp = spacy.load("en_core_web_sm") # Loading Spacy Model for English
    doc = nlp(file) # Applying spacy to raw text
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
