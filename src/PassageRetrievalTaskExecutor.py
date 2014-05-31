# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# PassageRetrievalTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from NewsDocument import *
from sets import Set
from nltk import word_tokenize
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
        
        
        relevantPassages = [] 
        for triple in triples:
            bigramMatchesWithQuestion = self.GetBigramMatches(session.question.text, triple.text)
            bigramMatchesWithTargetText = self.GetBigramMatches(session.question.target, triple.text)
            webBigramMatches = self.GetMatchesWithBigramsFromWeb(triple.text, session.topBigramsFromWeb)

            bigramMatches = bigramMatchesWithQuestion + bigramMatchesWithTargetText + webBigramMatches
            
            relevantPassages.append(
                    (triple.score,
                    bigramMatches,
                    triple.text,
                    triple.docId))

        relevantPassages.sort(reverse=True)

        session.relevantPassages = relevantPassages

        #for score, bigramMatches, passage, docId in session.relevantPassages: 
            #session.logs.append("Relevant passage: {0} | score: {1} | bigram macthes: {2}".format(passage, score, bigramMatches)) 

        self.LogTaskCompletion(session)
        
        return True
    
    def GetBigrams(self, text):
        bigrams = Set()
        tokens = word_tokenize(text.lower())
        for i in range(0, len(tokens) - 1):
            bigram = "_".join(tokens[i:i+2])
            bigrams.add(bigram) 
        
        return bigrams

    def GetBigramMatches(self, text1, text2):
        bigrams1 = self.GetBigrams(text1)
        bigrams2 = self.GetBigrams(text2)

        return len(bigrams1.intersection(bigrams2))

    def GetMatchesWithBigramsFromWeb(self, text, bigramsFromWeb):
        bigramsFromWeb = Set(bigramsFromWeb)

        bigrams = self.GetBigrams(text)
        
        return len(bigrams.intersection(bigramsFromWeb))

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
