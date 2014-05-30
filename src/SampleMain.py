# MIM Question Answering System
# Authors: Antariksh Bothale, Julian Chan, Yi-Shul Wei

# SampleMain.py
# Demonstrates how the MainFacilitator class can be used to answer questions.
# 

from MainFacilitator import *

mainFacilitator = MainFacilitator()
mainFacilitator.SetMode("TREC")
mainFacilitator.SetDataSetType("evaltest")

question = Question(
    "216.2",
    "FACTOID",
    "At which university does Krugman teach?",
    "Paul Krugman")

session = mainFacilitator.AnswerQuestion(question)
print("\n".join(session.logs))

answer = session.answers

print("Q: {0}".format(question))
print("A: {0}".format(answer))
