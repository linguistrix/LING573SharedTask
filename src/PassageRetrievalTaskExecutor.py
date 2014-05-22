# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# PassageRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from NewsDocument import *
import re
import whoosh.analysis
import whoosh.highlight

MAX_CHAR_NUM = 500

class PassageRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "PassageRetrievalTaskExecutor")
        self.fragmenter = whoosh.highlight.SentenceFragmenter(maxchars=MAX_CHAR_NUM)
        self.scorer = whoosh.highlight.BasicFragmentScorer()
        self.formatter = whoosh.highlight.NullFormatter()
        self.analyzer = whoosh.analysis.SimpleAnalyzer()

    def Execute(self, session):
        triples = [] #list of (score, fragment, docid) triples
        corpusPath = session.corpusPath
        q = session.query
        results = session.relevantDocuments

        qwords = frozenset(term[1] for term in q.all_terms())
        session.logs.append("Passage retrieval qwords: {0}".format(",".join(qwords)))

        for result in results:
            id = result[0]

            doc = Document()
            doc.loadDocumentFromID(id, corpusPath)
            body = doc.body

            tokens = self.analyzer(body, positions=True, chars=True, removestops=False)
            tokens = whoosh.highlight.set_matched_filter(tokens, qwords)

            triples.extend(
                (self.scorer(f),
                 removeNewline(self.formatter.format_fragment(f)),
                 id)
                    for f in self.fragmenter.fragment_tokens(body, tokens) )
        
        triples.sort(reverse=True)

        relevantPassages = []
        for triple in triples:
            score = triple[0]
            relevantPassage = triple[1] 
            id = triple[2]
            relevantPassages.append((relevantPassage, id))
            session.logs.append("Relevant passage: {0} | score: {1}".format(relevantPassage, score)) 
       
        session.relevantPassages = relevantPassages
        
        self.LogTaskCompletion(session)
        return True

def removeNewline(s):
  return re.sub(r'\s+', ' ', s.strip())
