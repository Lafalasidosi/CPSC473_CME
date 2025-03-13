from helpers

class Node:
    def __init__(self, item: str, parent=None):
        self.item = item
        self.count = 1
        self.children = {}
        self.prev_nibling = None    # nibling is a term for cousin, aunt/uncle, niece/nephew, etc.
        self.next_nibling = None    # these point to FPTree nodes with same item
    
    def increment(self):
        self.count += 1
        
    def get_item(self):
        return self.item
        
    def add_child(self, child):
        self.children.update({child.get_item(): child})
        
    def set_prev_nibling(self, nibling):
        self.prev_nibling = nibling
    
    def set_next_nibling(self, nibling):
        self.next_nibling = nibling
        
    def show(self):
        print("[\"{}\", {}]".format(self.item, self.count))
    
    def get_children(self):
        return self.children.keys()

    def get_child(self, item):
        return self.children[item]
        
class FPTree:
    def __init__(self, L1: dict):
        self.root = Node('')
        self.L1 = L1
        
    def get_root(self):
        return self.root
    
    def add_node(self, child: Node, parent=None):
        '''Add a node to the tree with a specified parent.
        If no parent is specified, add node as child of root node.'''
        if parent is None:
            self.root.add_child(child)
        else:
            parent.add_child(child)
            self.L1[child.get_item()] = child
            
    def last_pointer_from_L1(self, new_node: Node):
        '''Start at the L1 table, follow pointers into FPTree
        until a dead end is reached, return a reference to 
        the last non-null node.'''
        item = new_node.get_item()
        last_node = self.L1[item]
        if last_node is None:
             self.L1[item] = new_node
        next_node = last_node.get_next_nibling()
        while next_node is not None:
            last_node = next_node
            next_node = last_node.get_next_nibling()
        return last_node
            
            
            