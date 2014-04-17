# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionProcessor.py
# Provides various functions for querying a user question

from nltk import word_tokenize

class QuestionProcessor(object):
    def __init__(self, question):
        self.question = question

    def GetWordSet(self):
        return word_tokenize(self.question)

