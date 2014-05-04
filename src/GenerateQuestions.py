__author__ = 'Antariksh Bothale'

from SystemEvaluator import GetAllQuestions
from QuestionClassifier import ClassifyQuestions, QCat

print ('Getting all questions')
questions = GetAllQuestions("D:\Documents\Academics\NLP Systems\LING573SharedTask\devtest\TREC-2006.xml")
print ('Classifying')
questions = ClassifyQuestions(questions)
with open('D:\Documents\Academics\NLP Systems\LING573SharedTask\devtest\WHENdevtestquestions.txt' ,'w') as f:
    for q in questions:
        if q.category is not None:
            f.write('{0}\t{1}\t{2}\t{3}\n'.format(q.id, q.type, q.target, q.text))


print ('Done')
