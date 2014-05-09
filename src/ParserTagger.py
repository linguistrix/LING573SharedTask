from nltk import word_tokenize
from nltk.tag.stanford import POSTagger

tagPOS = POSTagger("/NLP_TOOLS/pos_taggers/postagger/latest/models/english-bidirectional-distsim.tagger",
    "/NLP_TOOLS/pos_taggers/postagger/latest/stanford-postagger.jar").tag

if __name__ == "__main__":
    import sys
    while True:
        line = word_tokenize(sys.stdin.readline())
        if len(line) == 0: break
        print tagPOS(line)
