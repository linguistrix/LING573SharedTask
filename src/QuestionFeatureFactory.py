from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer
from collections import deque, Counter
import ParserTagger
import pickle, os, sys

WH_LIST = ["who", "whom", "when", "where", "what", "which", "whose", "why", "how"]
stem = WordNetLemmatizer().lemmatize

# Get all paths from the root to the leaves, from left to right
def GetAllPaths(tree):
    if not isinstance(tree, Tree):
        return [(tree,)]

    path = []
    for subtree in tree:
        path.extend((tree.node,) + x for x in GetAllPaths(subtree))
    return path

# Find target node in a BFS manner
def FindTarget(tree):
    targets = ["SBARQ", "S", "SINV", "SBAR", "SQ", "FRAG", "NP"]
    queue = deque()
    queue.append(tree)
    while len(queue) > 0:
        subtree = queue.popleft()
        if subtree.node in targets:
            return subtree
        queue.extend(child for child in subtree if isinstance(child, Tree))
    return None

# Find a specific node in a DFS manner
def FindNode(tree, node = "NP"):
    stack = [tree]
    while len(stack) > 0:
        subtree = stack.pop()
        if subtree.node == node:
            return subtree
        children = [child for child in subtree if isinstance(child, Tree)]
        children.reverse()
        stack.extend(children)
    return None

def FindWhWord(target=None):
    if target is None:
        return "rest"
    elif target.node == "NP":
        return "rest"
    else:
        # find the first wh-word
        # however, that should not be one that introducce a subordinate clause
        for path in GetAllPaths(target):
            leafWord = path[-1].lower()
            if leafWord in WH_LIST and "SBAR" not in path[1:]:
                return leafWord
    return "rest"

class QuestionFeatureFactory(object):
    def __init__(self):
        self.mode = None

    def SetMode(self, mode):
        if (self.mode == mode):
            return

        self.mode = mode
        if not mode:
            self.parse = (lambda q: ParserTagger.parse(ParserTagger.tokenize(q.text)))
        elif mode == "TREC":
            with open(os.path.join(sys.path[0], "TRECParses"), "rb") as parseFile:
                AllParses = pickle.load(parseFile)
                self.parse = (lambda q: AllParses[q.id])
        elif mode == "UIUC":
            with open(os.path.join(sys.path[0], "UIUCParses"), "rb") as parseFile:
                AllParses = pickle.load(parseFile)
                self.parse = (lambda q: AllParses[q.id])

    def GetAllFeatures(self, question):
        parse = self.parse
        features = Counter()

        # Get the unigram features
        wordList = [w.lower() for w in question.GetWordList()]
        for word in wordList:
            features["unigram=" + word] += 1

        # Get other features
        t = parse(question)
        target = FindTarget(t)
        
        whWord = FindWhWord(target)
        features["Wh=" + whWord] = 1

        head = None
        if whWord == "how":
            head = wordList[wordList.index("how") + 1]
        
        elif whWord == "rest" or whWord == "what" or whWord == " which" or whWord == "whose":
            if target is not None:
                focus = FindNode(target, "WHNP")
                if focus is not None:
                    for path in GetAllPaths(focus):
                        if path[-2][:2] == "NN":
                            head = path[-1]
                if head is None:
                    focus = FindNode(target, "NP")
                    if focus is not None:
                        minDepth = 99999
                        paths = GetAllPaths(focus)
                        for path in paths:
                            if path[-2][:2] == "NN" and len(path) <= minDepth:
                                minDepth = len(path)
                                head = path[-1]
                        if minDepth == 99999:
                            head = paths[-1][-1]
            if head is None:
                for word, POS in ParserTagger.tagPOS(wordList):
                    if POS[:2] == "NN":
                        head = word
                        break
        
        if head is not None:
            head = stem(head.lower())
            features["head=" + head] = 1
        
        return features

