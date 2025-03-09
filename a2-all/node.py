class Node:
    def __init__(self, item):
        self.item = item
        self.count = 1
        self.frequency = {self.item: self.count}
        self.children = []
        self.prev_nibling = None
        self.next_nibling = None
    
    def increment(self):
        self.count.update({self.item, self.count+1})
        
    def add_child(self, child):
        self.children.append(child)