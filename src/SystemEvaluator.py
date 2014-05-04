# SystemEvaluator.py
# Reads in the questions set and generates a result file

import sys
from bs4 import BeautifulSoup
from MainFacilitator import *


def GetAllQuestions(questionsFilename):
    questionsFile = open(questionsFilename, "r")
    questionsContent = questionsFile.read()
    questionsFile.close()

    soup = BeautifulSoup(questionsContent)

    questions = []
    for target in soup.find_all('target'):
        for question in target.find_all('q'):
            question = Question(
                question.get('id').strip(),
                question.get('type').strip(),
                question.string.strip(),
                target.get('text').strip())

            if question.type == 'FACTOID':
                questions.append(question)

    return questions

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print("Usage: ./SystemEvaluator.py run_tag question_file result_file")
        sys.exit(1)

    runTag = sys.argv[1]
    questionsFilename = sys.argv[2]
    resultFilename = sys.argv[3]

    questions = GetAllQuestions(questionsFilename)

    mainFacilitator = MainFacilitator()

    with open(resultFilename, "w") as resultFile:
        for question in questions:
            session = mainFacilitator.AnswerQuestion(question)

            if (len(session.answers) == 0):
                resultFile.write("{0} {1} NIL NIL\n".format(
                  question.id,
                  runTag))
            else:
                for ans in session.answers:
                    resultFile.write("{0} {1} {2} {3}\n".format(
                        question.id,
                        runTag,
                        ans[1],
                        ans[0]))

