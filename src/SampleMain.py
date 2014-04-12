# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# SampleMain.py
# Demonstrates how the MainFacilitator class can be used to answer questions.
# 

from MainFacilitator import *

mainFacilitator = MainFacilitator()

question = "What is the meaning of life?"
answer = mainFacilitator.AnswerQuestion(question)

print("Q: {0}".format(question))
print("A: {0}".format(answer))
