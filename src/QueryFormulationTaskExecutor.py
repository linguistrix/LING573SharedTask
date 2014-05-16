# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QueryFormulationTaskExecutor.py
# Formulates a query from the question 

from TaskExecutor import *
from whoosh import qparser
from WebSnippetRetrieval import *
from sets import Set
import re

class QueryFormulationTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "QueryFormulationTaskExecutor")
        self.webSnippetRetrieval = WebSnippetRetrieval()

    def Execute(self, session):
        
        wordsToRemove = set([
            "who",
            "what",
            "why",
            "where",
            "when",
            "which",
            "how",
            "that",
            "do",
            "did",
            "does",
            "?"])

        wordList = [x.lower() for x in session.question.GetWordList() if x not in wordsToRemove]
        
        # Add words from top bigrams to the word list
        session.topBigramsFromWeb = self.webSnippetRetrieval.GetTopSortedBigramsFromWeb(
            session.question,
            10)

        wordListFromWeb = Set()
        for eachBigram in session.topBigramsFromWeb:
            words = eachBigram.lower().split("_")
            wordListFromWeb.update(words)

        wordList.extend(wordListFromWeb)

        og = qparser.OrGroup.factory(0.9)

        textParser = qparser.QueryParser("body", session.index.schema, group=og)
        targetParser = qparser.QueryParser("body", session.index.schema)
        headlineParser = qparser.QueryParser("headline", session.index.schema, group=og)

        target = re.sub("[^\\.A-Za-z0-9]+", " ", session.question.target)
        qtext = re.sub("[^\\.a-z0-9]+", " ", " ".join(wordList))

        session.query = textParser.parse(qtext) & (targetParser.parse(target) | headlineParser.parse(target))
        
        self.LogTaskCompletion(session)
        return True

