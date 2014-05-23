# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# AnswerProcessingTaskExecutor.py
# Comes up with an answer given the relevant passages and query 

from TaskExecutor import *
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
        numberlist = map(lambda x: x.strip(), open(os.path.join(sys.path[0], 'numberlist')).readlines())
        numberTextRegex = r'(' + r'|'.join(numberlist) + r')( |-|\b)'
        print "The regex for numbers in words is: " + numberTextRegex
        numberRegex = r'\$?[{0-9},.]+'
        goodAnswers = []
        badAnswers = []

        answerType = session.answerType
        
        for passage, docId in session.relevantPassages:
            passage = passage.replace("\n", " ")

            ne_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(passage)))
            ne_types = []
            for item in ne_tree:
                try:
                    ne_types.append(str(item.node))
                except AttributeError:
                    pass
            
            if answerType[:3] == "HUM" and "PERSON" in ne_types:
                print ("Answer is of HUM type!")
                # If answer is of some human type                
                goodAnswers.append((passage, docId))
            if answerType == "NUM:date":
                print ("When Question Found!")
                monthmatch = re.findall(monthRegex, passage.lower())
                daymatch = list(daySet.intersection(passage.lower().split()))
                yearmatch = re.findall(yearRegex, passage.lower())
                if monthmatch or daymatch or yearmatch:
                    print ("Found a time match") 
                    #goodAnswers.append((' '.join(monthmatch + daymatch + yearmatch), docId))
                    goodAnswers.append((passage, docId))
                else:    
                    badAnswers.append((passage, docId))
            elif answerType[:3] == "NUM":
                nummatch = re.findall(numberRegex, passage.lower())
                #numtextmatch = re.findall(numberTextRegex, passage.lower())
                print ("Found a number match")
                #goodAnswers.append((' '.join(nummatch), docId))
                #if nummatch or numtextmatch:
                if nummatch:
                    goodAnswers.append((passage, docId))
                else:
                    badAnswers.append((passage, docId))
            else:
                badAnswers.append((passage, docId))
        
                #goodAnswers.append((passage, docId))
            #if session.question.category in ["DATETIME", "DATE", "DAY", "MONTH", "YEAR"]:
            
        session.logs.append("Good answers: {0} | Bad answers: {1}".format(len(goodAnswers), len(badAnswers)))
        
            
        session.answers = goodAnswers + badAnswers
        session.answers = session.answers[:20]
        session.answers = map(lambda x: x[:250], session.answers)

        for (passage, docId) in session.answers:
            session.logs.append("Answer: {0} | {1}".format(passage, docId))
        
        self.LogTaskCompletion(session)
        return True
'''
    def CheckIfPassageContainsTopBigramsFromWeb(self, passage, topBigrams):
        passageBigrams = Set()
        tokens = word_tokenize(passage.lower())
        for i in range(0, len(tokens) - 1):
            bigram = "_".join(tokens[i:i+2])
            passageBigrams.add(bigram)
     
        for eachTopBigram in topBigrams:
            if eachTopBigram.lower() in passageBigrams:
                return True
        
        return False

'''
