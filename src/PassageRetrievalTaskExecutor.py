# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# PassageRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from NewsDocument import *
import re
import whoosh.analysis
import whoosh.highlight

class PassageRetrievalTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "PassageRetrievalTaskExecutor")
        self.fragmenter = whoosh.highlight.SentenceFragmenter(maxchars=500)
        self.scorer = whoosh.highlight.BasicFragmentScorer()
        self.formatter = whoosh.highlight.NullFormatter()
        self.analyzer = whoosh.analysis.SimpleAnalyzer()

    def Execute(self, session):
        triples = set()
        corpusPath = session.corpusPath
        q = session.query
        results = session.relevantDocuments

        qwords = frozenset(term[1] for term in q.all_terms())
        session.logs.append("Passage retrieval qwords: {0}".format(",".join(qwords)))

        for result in results:
            id = result[0]

            doc = Document()
            doc.loadDocumentFromID(id, corpusPath, session.dataSetType)

            body = doc.body

            tokens = self.analyzer(body, positions=True, chars=True, removestops=False)
            tokens = whoosh.highlight.set_matched_filter(tokens, qwords)

            triples.update(
                PassageTriple(self.scorer(f), removeNewline(self.formatter.format_fragment(f)), id)
                for f in self.fragmenter.fragment_tokens(body, tokens) )
        
        #triples.sort(reverse=True)

        relevantPassages = [(triple.score, triple.text, triple.docId) for triple in triples]
        relevantPassages.sort(reverse=True)

        session.relevantPassages = relevantPassages

        for score, passage, docId in relevantPassages: 
            session.logs.append("Relevant passage: {0} | score: {1}".format(passage, score)) 
        self.LogTaskCompletion(session)
        return True

class PassageTriple(object):
    def __init__(self, score, text, docId):
        self.score = score
        self.text = text
        self.docId = docId

    def __eq__(self, other):
        return self.text[:250].lower() == other.text[:250].lower()

    def __hash__(self):
        return hash(self.text[:250].lower())

def removeNewline(s):
  return re.sub(r"\s+", " ", s.strip())
