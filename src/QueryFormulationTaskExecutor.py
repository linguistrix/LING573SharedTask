# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QueryFormulationTaskExecutor.py
# Formulates a query from the question 

from TaskExecutor import *
from whoosh import qparser
from WebSnippetRetrieval import *
from verb import *
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

        wordList = [x.lower() for x in session.question.GetWordList()]

        # Morphological expansion
        if "did" in wordList:
            for word in set(wordList):
                if verb_infinitive(word) == word:
                    wordList.append(verb_past(word))
        if "does" in wordList:
            for word in set(wordList):
                if verb_infinitive(word) == word:
                    wordList.append(verb_present(word, person=3))

        # Add words from top bigrams to the word list
        session.topBigramsFromWeb = self.webSnippetRetrieval.GetTopSortedBigramsFromWeb(
            session,
            10)

        session.logs.append("Top bigrams from web: " + ", ".join(session.topBigramsFromWeb))

        wordListFromWeb = set()
        for eachBigram in session.topBigramsFromWeb:
            words = eachBigram.lower().split("_")
            wordListFromWeb.update(words)

        wordList.extend(wordListFromWeb)

        schema = session.index.schema
        og = qparser.OrGroup.factory(0.9)

        textParser = qparser.QueryParser("body", schema, group=og)
        targetParser = qparser.QueryParser("body", schema)
        headlineParser = qparser.QueryParser("headline", schema, group=og)

        target = re.sub("[^\\.A-Za-z0-9]+", " ", session.question.target)
        qtext = re.sub("[^\\.a-z0-9]+", " ", " ".join(x for x in wordList if x not in wordsToRemove))

        session.query = textParser.parse(qtext) & (targetParser.parse(target) | headlineParser.parse(target))
        
        self.LogTaskCompletion(session)
        return True

