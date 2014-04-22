# SystemEvaluator.py
# Reads in the questions set and generates a result file

import sys
from bs4 import BeautifulSoup
from MainFacilitator import *

class Question(object):
    def __init__(self, id, type, text):
        self.id = id 
        self.type = type 
        self.text = text 

    def __str__(self):
        return " | ".join([self.id, self.type, self.text])

def GetAllQuestions(questionsFilename):
    questionsFile = open(questionsFilename, "r")
    questionsContent = questionsFile.read()
    questionsFile.close()

    soup = BeautifulSoup(questionsContent)

    questions = []
    for question in soup.find_all('q'):
        question = Question(
            question.get('id').strip(),
            question.get('type').strip(),
            question.string.strip())

        questions.append(question)

    return questions


if (len(sys.argv) < 3):
    print("Usage: ./SystemEvaluator.py question_file result_file")

questionsFilename = sys.argv[1]
resultFilename = sys.argv[2]
runTag = "foo"

questions = GetAllQuestions(questionsFilename)

mainFacilitator = MainFacilitator()

output = ""
for question in questions:
    if question.type != "FACTOID":
        continue

    session = mainFacilitator.AnswerQuestion(question.text)
    if (len(session.relevantDocuments) == 0000):
        output += "{0} {1} NIL\n".format(question.id, runTag)
    else:
        output += "{0} {1} {2} {3}\n".format(
            question.id,
            runTag,
            session.relevantDocuments[0][0],
            session.answers[0])
   
resultFile = open(resultFilename, "w")
resultFile.write(output)
resultFile.close()



