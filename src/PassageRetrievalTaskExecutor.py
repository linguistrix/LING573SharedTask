# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# PassageRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from NewsDocument import *
import whoosh.highlight

MAX_CHAR_NUM = 250
fragmenter = whoosh.highlight.ContextFragmenter(maxchars=MAX_CHAR_NUM)
scorer = whoosh.highlight.BasicFragmentScorer()
formatter = whoosh.highlight.NullFormatter()

class PassageRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "PassageRetrievalTaskExecutor")

    def Execute(self, session):
        triples = [] #list of (score, fragment, docid) triples
        corpusPath = session.corpusPath
        q = session.query
        results = session.relevantDocuments

        for result in results:
            id = result['docno']

            doc = Document()
            doc.loadDocumentFromID(id, corpusPath)
            body = doc.body

            triples.extend( (scorer(f), f, id) for f in fragmenter.fragment_matches(body, q.all_tokens()) )
        triples.sort()
        triples.reverse()

        session.relevantPassages = [ (formatter(triple[1]), triple[2]) for triple in triples]
        triples = []
        self.LogTaskCompletion(session)
        return True


