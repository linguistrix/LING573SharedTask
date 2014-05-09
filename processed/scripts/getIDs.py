from SystemEvaluator import GetAllQuestions
from nltk import word_tokenize
import sys

questions = GetAllQuestions(sys.argv[1])
for q in questions:
    print q.id
