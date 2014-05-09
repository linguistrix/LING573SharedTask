from SystemEvaluator import GetAllQuestions
from nltk import word_tokenize
import sys

questions = GetAllQuestions(sys.argv[1])
for q in questions:
    tokens = word_tokenize(q.text)
    for i in range(len(tokens)):
        if tokens[i] == "(":
            tokens[i] = "-LRB-"
        elif tokens[i] == ")":
            tokens[i] = "-RRB-"
    print ' '.join(tokens)
