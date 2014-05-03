# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# SampleMain.py
# Demonstrates how the MainFacilitator class can be used to answer questions.
# 

from MainFacilitator import *

mainFacilitator = MainFacilitator()

question = Question("123", "FACTOID", "When did it become a state?", "Idaho")
answer = mainFacilitator.AnswerQuestion(question).answers

print("Q: {0}".format(question))
print("A: {0}".format(answer))
