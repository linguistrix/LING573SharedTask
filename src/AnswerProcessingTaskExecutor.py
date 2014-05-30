# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# AnswerProcessingTaskExecutor.py
# Comes up with an answer given the relevant passages and query 

from TaskExecutor import *
from nltk.tree import Tree
import pickle, os, sys, nltk
import re

class AnswerProcessingTaskExecutor(TaskExecutor):
    def __init__(self):
        TaskExecutor.__init__(self, "AnswerProcessingTaskExecutor")
    
    
    def Execute(self, session):

        session.answers = []
        # Just trying out if putting an answer containing date / time for a WHEN query is sensible
        # and improves scoring. Crudely done. This is heavily hardcoded.
        
        monthRegex = r'(january|february|march|april|may|june|july|august|september|october|november|december)'
        yearRegex = r'\d{4}'
        daySet = set(['sunday','monday','tuesday','wednesday','thursday','friday','saturday'])
        numberlistFile = open(os.path.join(sys.path[0], "numberlist"))
        numberlist = [x.strip() for x in numberlistFile]
        numberlistFile.close()
        numbertextregex = '(' + '|'.join(numberlist) + ')( |-|\b)'
        #print "The regex for numbers in words is: " + numbertextregex
        numberRegex = r'\$?[{0-9},.]+'
        goodAnswers = []
        mediumAnswers = []
        badAnswers = []

        answerType = session.answerType
        
        for score, bigramMatches, passage, docId in session.relevantPassages:
            passage = passage.replace("\n", " ")

            ne_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(passage)))
            ne_types = []
            for item in ne_tree:
                if type(item) == Tree and passage.find(item.leaves()[0][0]) != -1:
                    ne_types.append(str(item.node))


            #if answerType == "HUM:gr":
            #    if "ORGANIZATION" in ne_types or "GSP" in ne_types:
            #        goodAnswers.append((passage, docId))
            #    elif "PERSON" in ne_types:
            #        mediumAnswers.append((passage, docId))
            if answerType[:3] == "HUM":
                #print ("Answer is of HUM type!")
                if "PERSON" in ne_types:
                    goodAnswers.append((passage, docId))
                elif "ORGANIZATION" in ne_types or "GSP" in ne_types:
                    mediumAnswers.append((passage, docId))
            elif answerType[:3] == "LOC":
                #print ("Answer is of LOC type!")
                if "GPE" in ne_types or "LOCATION" in ne_types:
                    goodAnswers.append((passage, docId))
                elif "ORGANIZATION" in ne_types or "GSP" in ne_types or "PERSON" in ne_types:
                    mediumAnswers.append((passage, docId))
            elif answerType == "NUM:date":
                #print ("When Question Found!")
                monthmatch = re.findall(monthRegex, passage.lower())
                daymatch = list(daySet.intersection(passage.lower().split()))
                yearmatch = re.findall(yearRegex, passage.lower())
                if monthmatch or daymatch or yearmatch:
                    #print ("Found a time match") 
                    #goodAnswers.append((' '.join(monthmatch + daymatch + yearmatch), docId))
                    goodAnswers.append((passage, docId))
                else:    
                    badAnswers.append((passage, docId))
            elif answerType[:3] == "NUM":
                nummatch = re.findall(numberRegex, passage.lower())
                #print ("Found a number match")
                #goodAnswers.append((' '.join(nummatch), docId))
                if nummatch:
                    goodAnswers.append((passage, docId))
                else:
                    badAnswers.append((passage, docId))
            else:
                badAnswers.append((passage, docId))
            
        session.logs.append("Good answers: {0} | Medium answers: {1} | Bad answers: {2}".format(
            len(goodAnswers), 
            len(mediumAnswers),
            len(badAnswers)))

        allAnswers = goodAnswers + mediumAnswers + badAnswers
        session.answers = map(lambda x: (x[0][:250], x[1]), allAnswers[:20])

        for passage, docId in session.answers:
            session.logs.append("Answer: {0} | {1}".format(passage, docId))
        
        self.LogTaskCompletion(session)
        return True
