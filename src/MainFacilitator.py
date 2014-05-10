# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# MainFacilitator.py
# The entry point of the MIM QA system.
# Initializes all components and facilitates the QA operations

from nltk import word_tokenize
from TaskExecutor import *
from DocumentRetrievalTaskExecutor import *
from PassageRetrievalTaskExecutor import *
from AnswerProcessingTaskExecutor import *

class Question(object):
    def __init__(self, id, type, text, target):
        self.id = id
        self.type = type
        self.text = text
        self.target = target

    def __str__(self):
        return " | ".join([self.id, self.type, self.text, self.target])

    def GetWordList(self):
        return word_tokenize(self.text)

class MainFacilitator(object):
    def __init__(self):
        self.setMode(None)
        self.InitializeTaskExecutors()

    def setMode(self, mode):
        self.mode = mode

    def InitializeTaskExecutors(self):
        self.taskExecutors = []
        self.taskExecutors.append(DocumentRetrievalTaskExecutor())
        self.taskExecutors.append(PassageRetrievalTaskExecutor())
        self.taskExecutors.append(AnswerProcessingTaskExecutor())

    def AnswerQuestion(self, question):
        session = Session(question, self.mode)
        
        for taskExecutor in self.taskExecutors:
            if (False == taskExecutor.Execute(session)):
                print("Execution failed at {0}".format(taskExecutor.taskName))
                break

        print(session.GetLogs())
        print("")
        
        return session
