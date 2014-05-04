# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# AnswerProcessingTaskExecutor.py
# Comes up with an answer given the relevant passages and query 

from TaskExecutor import *
from QuestionClassifier import QCat

class AnswerProcessingTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "AnswerProcessingTaskExecutor")
    
    def Execute(self, session):
        session.answers = []
        # Just trying out if putting an answer containing date / time for a WHEN query is sensible
        # and improves scoring. Crudely done. This is heavily hardcoded.

        monthRegex = r'(\d{1-2}(th|st|rd|nd)?)? january|february|march|april|may|june|july|august|september|october|november|december *\d{1-2}?'
        daySet = set(['sunday','monday','tuesday','wednesday','thursday','friday','saturday'])

        goodAnswers = []
        badAnswers = []

        for passage, docId in session.relevantPassages[:20]:
            passage = passage.replace("\n", " ")

            if session.question.category in [QCat.DATETIME, QCat.DATE, QCat.DAY, QCat.MONTH, QCat.YEAR]:
                if re.match(monthRegex, session.question.text.lower()) or len(daySet.intersection(session.question.text.lower().split())) > 0:
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

