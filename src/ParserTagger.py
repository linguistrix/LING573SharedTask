from nltk import word_tokenize
from nltk.tag.stanford import POSTagger
from nltk.tree import Tree
from subprocess import Popen, PIPE

tagPOS = POSTagger("/NLP_TOOLS/pos_taggers/postagger/latest/models/english-bidirectional-distsim.tagger",
    "/NLP_TOOLS/pos_taggers/postagger/latest/stanford-postagger.jar").tag

def tokenize(s):
    tokens = word_tokenize(s)
    for i in range(len(tokens)):
        if tokens[i] == "(":
            tokens[i] = "-LRB-"
        elif tokens[i] == ")":
            tokens[i] = "-RRB-"
    return tokens

def parse(tokenized_string):
    cmd = ["java",
        "-jar", "/NLP_TOOLS/parsers/berkeleyparser/latest/berkeleyParser.jar",
        "-gr", "/NLP_TOOLS/parsers/berkeleyparser/latest/eng_sm6.gr"]

    p = Popen(cmd, stdin=PIPE, stdout=PIPE)

    return Tree( p.communicate(input=tokenized_string)[0] )
    

if __name__ == "__main__":
    import sys
    while True:
        line = tokenize(sys.stdin.readline())
        if len(line) == 0: break
        print tagPOS(line)
        print parse(' '.join(line)).pprint()
