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


if (len(sys.argv) < 4):
    print("Usage: ./SystemEvaluator.py run_tag question_file result_file")
    sys.exit(1)

runTag = sys.argv[1]
questionsFilename = sys.argv[2]
resultFilename = sys.argv[3]

questions = GetAllQuestions(questionsFilename)

mainFacilitator = MainFacilitator()

output = ""
for question in questions:
    if question.type != "FACTOID":
        continue

    session = mainFacilitator.AnswerQuestion(question.text)
    if (len(session.answers) == 0):
        output += "{0} {1} NIL NIL\n".format(question.id, runTag)
    else:
        output += "{0} {1} {2} {3}\n".format(
            question.id,
            runTag,
            session.answers[0][1],
            session.answers[0][0])
   
resultFile = open(resultFilename, "w")
resultFile.write(output)
resultFile.close()



