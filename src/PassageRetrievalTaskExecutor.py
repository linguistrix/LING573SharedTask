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
        '''
        frags = []
        corpusPath = session.corpusPath
        qobj = session.queryObject

        for result in results:
            doc = Document()
            doc.loadDocumentFromID(result['docno'], corpusPath)
            body = doc.body
            frags.extend(fragmenter.fragment_matches(body, qobj.all_tokens()))
        frags.sort(key=scorer).reverse()

        session.relevantPassages = [formatter(frag) for frag in frags]
        frags = []
        '''
        self.LogTaskCompletion(session)
        return True


