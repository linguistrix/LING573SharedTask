# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionProcessor.py
# Provides various functions for querying a user question

from whoosh import qparser
import re

class QuestionProcessor(object):
    def __init__(self):
        pass

    def GetDocumentRetrievalQuery(self, question, schema):
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

        wordList = [x for x in question.GetWordList() if x not in wordsToRemove]

        og = qparser.OrGroup.factory(0.9)

        textParser = qparser.QueryParser("body", schema, group=og)
        targetParser = qparser.QueryParser("body", schema)
        headlineParser = qparser.QueryParser("headline", schema, group=og)

        target = re.sub("[^\\.A-Za-z0-9]+", " ", question.target)
        qtext = re.sub("[^\\.a-z0-9]+", " ", " ".join(wordList))

        return textParser.parse(qtext) & (targetParser.parse(target) | headlineParser.parse(target))

