# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionProcessor.py
# Provides various functions for querying a user question

from nltk import word_tokenize
from sets import Set

class QuestionProcessor(object):
    def __init__(self, question):
        self.question = question

    def GetWordList(self):
        return map(lambda x: x.lower(), word_tokenize(self.question))

    def GetDocumentRetrievalQuery(self):
        wordsToRemove = Set([
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
       
        wordList = self.GetWordList()

        for i in reversed(range(0, len(wordList))):
            if (wordList[i] in wordsToRemove):
                wordList.pop(i)

        return " ".join(wordList)

