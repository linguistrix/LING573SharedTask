# AnswerQuestionForParallelProcessing.py
# Used by condor script to answer a question 

import sys
from MainFacilitator import *

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print("Usage: ./AnswerQuestionForParallelProcessing.py run_tag question_id question_dir")
        sys.exit(1)

    runTag = sys.argv[1]
    questionId = sys.argv[2]
    questionDir = sys.argv[3]

    questionType, questionText, questionTarget = open(os.path.join(questionDir, questionId + ".question")).read().split("\n")
    
    # questionId = questionData[0]
    # questionType = questionData[1]
    # questionText = questionData[2]
    # questionTarget = questionData[3]
    
    resultFile = open(os.path.join(questionDir, questionId + ".result"), "w")

    mainFacilitator = MainFacilitator()
    mainFacilitator.SetMode("TREC")

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
                ans[1],
                ans[0]))

    resultFile.close()

