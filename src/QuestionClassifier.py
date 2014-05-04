# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# QuestionClassifier.py
# Provides routines to classify a question
import re

class QCat:
    DATETIME, YEAR, MONTH, DAY, DATE = range(1, 6)

def ClassifyQuestions(questions):
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
                question.category = QCat.DATETIME
            else:
                matchedDict = {"month": QCat.MONTH, "day": QCat.DAY, "date": QCat.DATE, "year": QCat.YEAR }
                matcher = re.match(regexDict['DAYMONTH'], searchText)
                if matcher is not None:
                    matched = matcher.group(3)
                    question.category = matchedDict[matched]

    return questions




