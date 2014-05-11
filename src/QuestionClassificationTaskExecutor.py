# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionClassificationTaskExecutor.py
# Performs document retrieval given a query session

from TaskExecutor import *
from QuestionFeatureFactory import QuestionFeatureFactory
import pickle, re, os, sys



class QuestionClassificationTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "QuestionClassificationTaskExecutor")
        
        self.questionFeatureFactory = QuestionFeatureFactory()
        
        with open(os.path.join(sys.path[0], "QuestionClassifier.svm"), "rb") as classiFile:
            self.classifier = pickle.load(classiFile)

    def Execute(self, session):
        if session.question == None:
            session.logs.append("[ERROR]: Session has no question")
            return False
        
        self.questionFeatureFactory.SetMode(session.mode) 
        features = self.questionFeatureFactory.GetAllFeatures(session.question)
        session.question.answerType = self.classifier.classify(features)
       
        self.LogTaskCompletion(session)
        return True

            

