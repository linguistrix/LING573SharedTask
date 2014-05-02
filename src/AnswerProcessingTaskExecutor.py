# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# AnswerProcessingTaskExecutor.py
# Comes up with an answer given the relevant passages and query 

from TaskExecutor import *


class AnswerProcessingTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "AnswerProcessingTaskExecutor")
    
    def Execute(self, session):
        session.answers = []
        for passage, docId in session.relevantPassages[:10]:
            passage = passage.replace("\n", " ")
            session.answers.append((passage, docId))
            session.logs.append("Answer: {0} | {1}".format(passage, docId))
        
        self.LogTaskCompletion(session)
        return True

