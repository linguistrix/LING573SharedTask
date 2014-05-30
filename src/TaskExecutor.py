# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# TaskExecutor.py

import whoosh.index
import os, sys

class TaskExecutor(object):
    def __init__(self, taskName):
        self.taskName = taskName

    def Execute(self, session):
        return True
   
    def LogTaskCompletion(self, session):
        session.logs.append("Executed {0} task successfully.".format(self.taskName)) 


class Session(object):
    def __init__(self, question, mode, datasettype):

        self.dataSetType = datasettype

        if self.dataSetType == 'devtest':
            self.corpusPath = "/corpora/LDC/LDC02T31"
            self.indexPath = "/home2/abothale/ling573/LING573SharedTask/src/devtestindex"
            self.cachedSnippetsPath = os.path.join(sys.path[0], "../CachedWebContent/DevTestSnippets")
        elif self.dataSetType == 'evaltest':
            self.corpusPath = "/corpora/LDC/LDC08T25/"
            self.indexPath = "/home2/abothale/ling573/LING573SharedTask/src/evaltestindex"
            self.cachedSnippetsPath = os.path.join(sys.path[0], "../CachedWebContent/EvalTestSnippets")

        self.index = whoosh.index.open_dir(self.indexPath)

        self.question = question
        self.mode = mode

        self.query = None 
        self.topBigramsFromWeb = None 
        self.relevantDocuments = None
        self.relevantPassages = None
        self.answers = None
        self.maxNumberOfReturnedDocuments = 20
        self.logs = []
        self.logs.append("Question: {0}".format(question))

    def GetLogs(self):
        return "\n".join(self.logs) 
