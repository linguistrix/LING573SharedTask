# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# SampleMain.py
# Demonstrates how the MainFacilitator class can be used to answer questions.
# 

from MainFacilitator import *

mainFacilitator = MainFacilitator()

question = "When did Idaho become a state?"
answer = mainFacilitator.AnswerQuestion(question).answers

print("Q: {0}".format(question))
print("A: {0}".format(answer))
