# GetWebQueries.py
# Read in the questions set and generates queries for getting snippets from 
# Web search

import sys
from bs4 import BeautifulSoup
from MainFacilitator import *
from QuestionClassifier import *

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
    if (len(sys.argv) < 3):
        print("Usage: ./SystemEvaluator.py question_file result_file")
        sys.exit(1)
    
    questionsFilename = sys.argv[1]
    queriesFilename = sys.argv[2]
    
    questions = GetAllQuestions(questionsFilename)

    output = ""
    for question in questions:
        output += (question.id + ":" + question.text + " " + question.target + "\n")

    queriesFile = open(queriesFilename, "w")
    queriesFile.write(output)
    queriesFile.close()


