'''
Root node: item = None, frequency = 0, parent = None
FP trees are not binary trees. Keep a list of children instead of a left and right child.
internalLink connects to the next node in the tree with the same item. The rightmost node will remain null.
'''

class Node:
    def __init__(self, item, frequency, parent):
        self.item = item
        self.frequency = frequency
        self.parent = parent
        self.children = []
        self.internalLink = None

    def getItem(self):
        return self.item

    def getFrequency(self):
        return self.frequency

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

    def getInternalLink(self):
        return self.internalLink

    def setItem(self, item):
        self.item = item

    def setFrequency(self, frequency):
        self.frequency = frequency

    def setParent(self, parent):
        self.parent = parent

    def setInternalLink(self, internalLink):
        self.internalLink = internalLink

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def increment(self):
        self.frequency += 1