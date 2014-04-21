# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# MainFacilitator.py
# The entry point of the MIM QA system.
# Initializes all components and facilitates the QA operations

from TaskExecutor import *
from DocumentRetrievalTaskExecutor import *
from PassageRetrievalTaskExecutor import *
from AnswerProcessingTaskExecutor import *


class MainFacilitator(object):
    def __init__(self):
        self.taskExecutors = None 
        self.InitializeTaskExecutors()

    def InitializeTaskExecutors(self):
        self.taskExecutors = []
        self.taskExecutors.append(DocumentRetrievalTaskExecutor())
        self.taskExecutors.append(PassageRetrievalTaskExecutor())
        self.taskExecutors.append(AnswerProcessingTaskExecutor())

    def AnswerQuestion(self, question):
        session = Session(question)
        
        for taskExecutor in self.taskExecutors:
            if (False == taskExecutor.Execute(session)):
                print("Execution failed at {0}".format(taskExecutor.taskName))
                break

        print(session.GetLogs())
        
        return session.answers




