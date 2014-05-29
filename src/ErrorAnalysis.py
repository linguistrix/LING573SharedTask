# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# ErrorAnalysis.py
# Module that takes in a question file, factoids file, output file and results file
# and gives out Error Analysis Statistics
import sys, os
from bs4 import BeautifulSoup
from SystemEvaluator import GetAllQuestions
import pickle
from QuestionFeatureFactory import QuestionFeatureFactory

def WriteFeatureFile(questionsFile, featureFileName):
    questions = GetAllQuestions(questionsFile)

    with open(os.path.join(sys.path[0], "QuestionClassifier.svm"), "rb") as classiFile:
            classifier = pickle.load(classiFile)
    questionFeatureFactory = QuestionFeatureFactory()

    featureDict = {}

    for q in questions[:3]:
        features = questionFeatureFactory.GetAllFeatures(q)
        q.type = classifier.classify(features)
        featureDict[q.id] = features

        print q.id, q.type, q.target, q.text


    featurefile = open(featureFileName, 'w')
    pickle.dump(featureDict, featurefile)
    featurefile.close()


if __name__ == '__main__':
    questionsFile = sys.argv[1]
    #factoidsFile = sys.argv[2]
    #outputFile = sys.argv[3]
    #resultsFile = sys.argv[4]
    WriteFeatureFile(questionsFile, 'DevTestQuestionFeatures.pickle')
    '''
    factoids = {}
    with open(factoidsFile) as f:
        for line in f:
            qno, ans = line.split('\t')[:2]
            factoids[qno] = ans
    '''
