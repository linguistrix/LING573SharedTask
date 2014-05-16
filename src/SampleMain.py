# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# SampleMain.py
# Demonstrates how the MainFacilitator class can be used to answer questions.
# 

from MainFacilitator import *

mainFacilitator = MainFacilitator()
mainFacilitator.SetMode("TREC")

question = Question(
    "149.1",
    "FACTOID",
    "The Daily Show appears on what cable channel?",
    "The Daily Show")

session = mainFacilitator.AnswerQuestion(question)
print("\n".join(session.logs))

answer = session.answers

print("Q: {0}".format(question))
print("A: {0}".format(answer))
