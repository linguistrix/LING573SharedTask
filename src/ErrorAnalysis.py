#!/opt/python-2.7/bin/python2.7
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

def WriteStats(questionsFile, factoidsFile, resutlsFile):
    questions = GetAllQuestions(questionsFile)

    factoids = {}
    results = {}
    with open(factoidsFile) as f:
        for line in f:
            qno, ans = line.split('\t')[:2]
            factoids[qno] = ans

    with open(resultsFile) as f:
        for line in f:
            if line[:2] != 'No':
                qno, score = line.split('\t')
                qno = qno.strip(':')
                results[qno] = float(score)

    with open(os.path.join(sys.path[0], "QuestionClassifier.svm"), "rb") as classiFile:
            classifier = pickle.load(classiFile)
    questionFeatureFactory = QuestionFeatureFactory()
    questionFeatureFactory.SetMode('TREC')
    classDict = {}

    for q in questions:
	
    	features = questionFeatureFactory.GetAllFeatures(q)
        q.type = classifier.classify(features)
        classDict[q.id] = q.type

        #print ('{0}\t{1}\t{2}\t{3}'.format(q.id, q.type, q.target, q.text))
    
    print ('Statistics')
    print ('----------')
    print ('Total Questions: {0}'.format(len(questions)))
    print ('Total Questions with patterns: {0}'.format(len(factoids)))
    print ('Total Answers with non-zero score: {0}'.format(len(filter(lambda x: results[x] > 0, results))))
    print ('Total Answers in Top-10 position: {0}'.format(len(filter(lambda x: results[x] >= 0.1, results))))
    print ('Total Answers in 1st position: {0}'.format(len(filter(lambda x: results[x] == 1, results))))


    #classfile = open(classFileName, 'w')
    #pickle.dump(classDict, classfile)
    #classfile.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: ./ErrorAnalysis.py questionsFile factoidsFile resultsFile')
        sys.exit(1)
    
    questionsFile = sys.argv[1]
    factoidsFile = sys.argv[2]
    resultsFile = sys.argv[3]
    
    WriteStats(questionsFile, factoidsFile, resultsFile)
    

    
