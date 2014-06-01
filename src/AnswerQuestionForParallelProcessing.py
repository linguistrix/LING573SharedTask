# AnswerQuestionForParallelProcessing.py
# Used by condor script to answer a question 

import sys
import unicodedata
from MainFacilitator import *

permitted_dataset_types = ['devtest', 'evaltest']

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print("Usage: ./AnswerQuestionForParallelProcessing.py run_tag question_id question_dir")
        sys.exit(1)

    runTag = sys.argv[1]
    questionId = sys.argv[2]
    questionDir = sys.argv[3]
    if len(sys.argv) > 4:
        dataSetType = sys.argv[4]
        if dataSetType not in permitted_dataset_types:
            print ("Currently permitted Data Set Types: 'devtest' (default), 'evaltest' (Enter without quotes)")
            sys.exit(1)
    else:
        dataSetType = 'devtest'

    questionType, questionText, questionTarget = open(os.path.join(questionDir, questionId + ".question")).read().split("\n")
    
    # questionId = questionData[0]
    # questionType = questionData[1]
    # questionText = questionData[2]
    # questionTarget = questionData[3]
    
    resultFile = open(os.path.join(questionDir, questionId + ".result"), "w")

    mainFacilitator = MainFacilitator()
    mainFacilitator.SetMode("TREC")
    mainFacilitator.SetDataSetType(dataSetType)
    question = Question(
        questionId, questionType, questionText, questionTarget)
    session = mainFacilitator.AnswerQuestion(question)

    if (len(session.answers) == 0):
        resultFile.write("{0} {1} NIL NIL\n".format(
          question.id,
          runTag))
    else:
        for ans in session.answers:
            resultFile.write("{0} {1} {2} {3}\n".format(
                question.id,
                runTag,
                unicodedata.normalize('NFKD', ans[1]).encode("utf-8", "ignore"),
                unicodedata.normalize('NFKD', ans[0]).encode("utf-8", "ignore")))

    resultFile.close()

