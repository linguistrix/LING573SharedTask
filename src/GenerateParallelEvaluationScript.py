# GenerateParallelEvaluationScript.py
# Reads in the questions set and generates a result file

import sys,os
from bs4 import BeautifulSoup
from MainFacilitator import *


def GetAllQuestions(questionsFilename):
    questionsFile = open(questionsFilename, "r")
    questionsContent = questionsFile.read()
    questionsFile.close()

    soup = BeautifulSoup(questionsContent)

    questions = []
    for target in soup.find_all('target'):
        for question in target.find_all('q'):
            question = Question(
                question.get('id').strip(),
                question.get('type').strip(),
                question.string.strip(),
                target.get('text').strip())

            if question.type == 'FACTOID':
                questions.append(question)
    
    return questions

if __name__ == '__main__':
    if (len(sys.argv) < 4):
        print("Usage: ./GenerateParallelEvaluationScript.py run_tag data_set question_file output_dir condor_script_file")
        sys.exit(1)

    runTag = sys.argv[1]
    dataSet = sys.argv[2]
    questionsFilename = sys.argv[3]
    outputDir = os.path.abspath(sys.argv[4])
    condorScriptFilename = sys.argv[5]

    questions = GetAllQuestions(questionsFilename)

    condorScriptOutput = "Executable = AnswerQuestionForParallelProcessing.sh\nUniverse = vanilla\ngetenv = true\nnotification = error\n"

    for question in questions:

        condorScriptOutput += "arguments = \"{0} {1} {2} {3}\"\n".format( 
                runTag,
                question.id,
                outputDir,
                dataSet)
       
        questionOutputFile = os.path.join(outputDir, "{0}.question".format(question.id))
        consoleOutputFile = os.path.join(outputDir, "{0}.consoleOutput".format(question.id))
        errorOutputFile = os.path.join(outputDir, "{0}.errorOutput".format(question.id))
        logOutputFile = os.path.join(outputDir, "{0}.logOutput".format(question.id))
      
        questionFile = open(questionOutputFile, "w")
        questionFile.write("\n".join([question.type, question.text, question.target]))
        questionFile.close()

        condorScriptOutput += "output = {0}\nerror = {1}\nlog = {2}\nrequest_memory = 2 * 1024\nqueue\n\n".format(
                consoleOutputFile,
                errorOutputFile,
                logOutputFile)

    condorScriptFile = open(condorScriptFilename, "w")
    condorScriptFile.write(condorScriptOutput)
    condorScriptFile.close()


