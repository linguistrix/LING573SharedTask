# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# TaskExecutor.py

from QuestionProcessor import *
import whoosh.index

class TaskExecutor(object):
    def __init__(self, taskName):
        self.taskName = taskName

    def Execute(self, session):
        return True
   
    def LogTaskCompletion(self, session):
        session.logs.append("Executed {0} task successfully.".format(self.taskName)) 


class Session(object):
    def __init__(self,  question):
        
        self.corpusPath = "/corpora/LDC/LDC02T31"
        self.indexPath = "/home2/abothale/ling573/LING573SharedTask/src/index"
        self.index = whoosh.index.open_dir(self.indexPath)

        self.question = question
        self.query = QuestionProcessor(self.index).GetDocumentRetrievalQuery(question, self.index.schema)

        self.relevantDocuments = None
        self.relevantPassages = None
        self.answers = None
        self.maxNumberOfReturnedDocuments = 20
        self.logs = []
        self.logs.append("Question: {0}".format(question.text))


    def GetLogs(self):
        return "\n".join(self.logs) 
