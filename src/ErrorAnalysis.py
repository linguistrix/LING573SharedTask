# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# ErrorAnalysis.py
# Module that takes in a question file, factoids file, output file and results file
# and gives out Error Analysis Statistics
import sys, os
from bs4 import BeautifulSoup
from SystemEvaluator import GetAllQuestions

if __name__ == '__main__':
    questionsFile = sys.argv[1]
    #factoidsFile = sys.argv[2]
    #outputFile = sys.argv[3]
    #resultsFile = sys.argv[4]

    questions = GetAllQuestions(questionsFile)

    for q in questions:
        print q

