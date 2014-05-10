from nltk.tree import Tree
from collections import deque
import pickle

WH_LIST = ["who", "whom", "when", "where", "what", "which", "why", "how"]

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
        # however, that should not be one that introducce a subordinating clause
        for path in GetAllPaths(target):
            leafWord = path[-1].lower()
            if leafWord in WH_LIST and "SBAR" not in path[1:]:
                return leafWord
    return "rest"

class QuestionFeatureFactory(object):
    def __init__(self):
        with open("AllParses", "rb") as AllParses:
            self.parse = pickle.load(AllParses)

    def GetAllFeatures(self, question):
        parse = self.parse
        features = {}

        # Get the unigram features
        wordList = [w.lower() for w in question.GetWordList()]
        #for w in wordList:
        #    features["unigram=" + w] = 1 #+=1

        # Get other features
        t = parse[question.id]
        target = FindTarget(t)
        
        whWord = FindWhWord(target)
        features["Wh=" + whWord] = 1

        head = None
        if whWord == "how":
            head = wordList[wordList.index("how") + 1]
        elif whWord == "what" or whWord == "which" or whWord == "rest":
            focus = None
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

        if head is not None:
            features["head=" + str(head)] = 1

        return features

