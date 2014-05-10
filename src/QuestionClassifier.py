# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionClassifier.py
# Provides routines to classify a question
from QuestionFeatureFactory import QuestionFeatureFactory
import pickle, re, os, sys


def ClassifyQuestions(questions):

    factory = QuestionFeatureFactory()
    with open(os.path.join(sys.path[0], "QuestionClassifier.svm"), "rb") as classiFile:
        classifier = pickle.load(classiFile)
        for question in questions:
            features = factory.GetAllFeatures(question)
            question.type = classifier.classify(features)
            


    """
    # Takes in a list of type Question and returns the list with the Question.category field populated.
    regexDict = {}
    regexDict['DAYMONTH'] = r"(in|on|at) (what|which) (date|day|month|year)"

    for question in questions:
        searchText = question.text.lower()
        splitText = searchText.lower().split()
        if len(splitText) <= 3:
            continue
        else:
            whenFlag = False
            if "when" in splitText[:2]:
                question.category = "DATETIME"
            else:
                matchedDict = {"month": "MONTH", "day": "DAY", "date": "DATE", "year": "YEAR" }
                matcher = re.match(regexDict['DAYMONTH'], searchText)
                if matcher is not None:
                    matched = matcher.group(3)
                    question.category = matchedDict[matched]
    """
    return questions
