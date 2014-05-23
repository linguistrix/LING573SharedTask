# WebSnippetRetrieval.py

from MainFacilitator import *
from nltk import word_tokenize
from collections import defaultdict
import os, sys

class WebSnippetRetrieval(object):
    def __init__(self):
        self.cachedSnippetsPath = os.path.join(sys.path[0], "../CachedWebContent/DevTestSnippets")
   
    def GetTopSortedBigramsFromWeb(self, question, n):
        snippets = self.GetWebSnippets(question)
        bigramCounts = self.GetBigramsCountsFromWebSnippets(snippets)

        questionText = question.text + " " + question.target
        
        # Remove bigrams that contain words in the original question
        questionWords = set(word_tokenize(questionText.lower()))
        
        for key in bigramCounts.keys():
            for eachWord in questionWords:
                if (key.lower().find(eachWord) != -1):
                    del bigramCounts[key]
                    break

        # Sort the bigrams by their counts
        sortedBigramCounts = sorted(bigramCounts.iteritems(), key=lambda x: x[1], reverse=True)
        return map(lambda x: x[0], sortedBigramCounts[:n])
    
    def GetWebSnippets(self, question):
        try:
            filename = os.path.join(
                self.cachedSnippetsPath,
                "{0}.snippets".format(question.id))

            snippetFile = open(filename, "r")
            snippets = snippetFile.read().split("\n")
            return snippets
        except:
            return []

    def GetBigramsCountsFromWebSnippets(self, snippets):
        bigramCounts = defaultdict(int)
        for eachSnippet in snippets:
            tokens = word_tokenize(eachSnippet)
            for i in range(0, len(tokens) - 1):
                bigram = "_".join(tokens[i:i+2])
                bigramCounts[bigram] += 1

        return bigramCounts


"""
webSnippetRetrieval = WebSnippetRetrieval()

question1 = Question(
    "143.3", 
    None,
    "When was it founded?", 
    "American Enterprise Institute")

print(webSnippetRetrieval.GetTopSortedBigramsFromWeb(question1, 10))
"""

