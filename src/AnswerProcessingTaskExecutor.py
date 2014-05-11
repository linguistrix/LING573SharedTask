# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# AnswerProcessingTaskExecutor.py
# Comes up with an answer given the relevant passages and query 

from TaskExecutor import *
import pickle, os, sys

class AnswerProcessingTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "AnswerProcessingTaskExecutor")
    
    def Execute(self, session):

        session.answers = []
        # Just trying out if putting an answer containing date / time for a WHEN query is sensible
        # and improves scoring. Crudely done. This is heavily hardcoded.

        monthRegex = r'(january|february|march|april|may|june|july|august|september|october|november|december)'
        yearRegex = r'\d{4}'
        daySet = set(['sunday','monday','tuesday','wednesday','thursday','friday','saturday'])

        goodAnswers = []
        badAnswers = []

        answerType = session.answerType

        for passage, docId in session.relevantPassages[:20]:
            passage = passage.replace("\n", " ")


            if answerType == "NUM:date":
            #if session.question.category in ["DATETIME", "DATE", "DAY", "MONTH", "YEAR"]:
                print ("When Question Found:" + session.question.text)
                if re.match(monthRegex, session.question.text.lower()) or len(daySet.intersection(session.question.text.lower().split())) > 0 or re.match(yearRegex, session.question.text.lower()):
                    goodAnswers.append((passage, docId))
                else:
                    badAnswers.append((passage, docId))
            else:
                goodAnswers.append((passage, docId))

        session.answers = goodAnswers + badAnswers
        for (passage, docId) in session.answers:
            session.logs.append("Answer: {0} | {1}".format(passage, docId))
        
        self.LogTaskCompletion(session)
        return True

