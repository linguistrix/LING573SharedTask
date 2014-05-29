# AgregateParallelRunResults.py
# Agregate the results from the paralle runs into one result file

import sys
from os import listdir
from os.path import isfile, join

if (len(sys.argv) < 3):
    print("Usage: ./AgregateParallelRunResults.py input_dir output_result_file")

inputDir = sys.argv[1]
outputResultFilename = sys.argv[2]

onlyFiles = [ f for f in listdir(inputDir) if isfile(join(inputDir,f)) ]
onlyResultFiles = [ f for f in onlyFiles if f.endswith(".result")]

onlyResultFiles.sort()

output = []
for eachFile in onlyResultFiles:
    file = open(join(inputDir, eachFile), "r") 
    output += file.readlines()[:20]
    file.close()
    
outputFile = open(outputResultFilename, "w")
outputFile.write("".join(output))
outputFile.close()

