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

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def setItem(self, item):
        self.item = item

    def setFrequency(self, frequency):
        self.frequency = frequency

    def setParent(self, parent):
        self.parent = parent

    def setInternalLink(self, internalLink):
        self.internalLink = internalLink