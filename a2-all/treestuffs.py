class Node:
    def __init__(self, item, parent=None):
        self.item = item
        self.count = 1
        self.frequency = {self.item: self.count}
        self.children = []
        self.parent = parent
        self.prev_nibling = None    # nibling is a term for cousin, aunt/uncle, niece/nephew, etc.
        self.next_nibling = None    # these point to FPTree nodes with same item
    
    def increment(self):
        self.count.update({self.item, self.count+1})
        
    def add_child(self, child):
        self.children.append(child)
        
    def set_prev_nibling(self, nibling):
        self.prev_nibling = nibling
    
    def set_next_nibling(self, nibling):
        self.next_nibling = nibling
        
class FPTree:
    def __init__(self):
        self.root = Node('')
    
    def add_node(self, child, parent=None):
        '''Add a node to the tree with a specified parent.
        If no parent is specified, add node as child of root node.'''
        if parent is None:
            self.root.add_child(child)
        else:
            parent.add_child(child)