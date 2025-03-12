from math import ceil
import sys
from itertools import combinations, islice
import linecache
from functools import reduce
import time
from collections import defaultdict

def main():
    D_name = sys.argv[1]
    if D_name[0] == '.':
        D_name = D_name[2:]     # no file names starting with './'
    D = open(D_name)
    transaction_size = int(linecache.getline(D_name, 1))
    min_sup = ceil((int(sys.argv[2]) / 100) * transaction_size)
    print('minsup = ' + sys.argv[2] + '% = ' + str(min_sup))
    run_time_start = time.time()
    #fp-growth in main memory here
    transactions = []
    with open(D_name, "r")as file:
        for line in islice(file, 1, None):
            row = line.strip().split()
            transactions.append(row[2:])
    fp_tree = FPTree(transactions, min_sup)
    mined_patterns = mine_patterns(fp_tree.side_table, min_sup)
    run_time_end = time.time()
    produce_output(mined_patterns, D_name)
    #produce_output(fp_tree, D_name)
    count = 0
    for _ in range(len(mined_patterns)):
            count += 1
    #Total runtime of the program
    total_run_time = run_time_end - run_time_start
    #Print frequent patterns found and the total runtime
    print('|FPs| = ' + str(count))
    print(f'Total Runtime: {total_run_time:.3f} sec')

#Produce outputted text file
def produce_output(patterns, D_name):
    inputfilewithoutextension = D_name[:-4]
    output_str = 'MiningResult_{}.txt'.format(inputfilewithoutextension)
    output_file = open(output_str, 'w')
    count = 0
    print()
    for _ in range(len(patterns)):
        count += 1
    output_file.write("|FPs| = " + str(count) + "\n")
    
    for n_itemsets, count in patterns.items():
        output_file.write(str(n_itemsets) + " : " + str(count) + "\n")

def peekline(f):
    """Return the current line of an open file 
    without moving the reader pointer.
    """
    pos = f.tell()
    result = f.readline()
    f.seek(pos)
    return result

#Nodes in an FP-tree
class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        #the next node with the same item
        self.next = None
    #increment value of FPNode
    def increment(self, count):
        self.count += count

#The FP-tree
class FPTree:
    def __init__(self, transactions, min_support):
        self.min_support = min_support
        #Side table to point to nodes
        self.side_table = {}
        #Root of tree
        self.root = FPNode(None, 1, None)
    
        item_count = defaultdict(int)
        #Loop through all transactions and increment count of item
        for transaction in transactions:
            for item in transaction:
                item_count[item] += 1
        #Based on MST, add items to frequent_items if its >= MST
        self.frequent_items = {}
        for k,v in item_count.items():
            if v >= min_support:
                self.frequent_items[k] = v
        # Add elements from frequent_items into the side table.
        for item, count in self.frequent_items.items():
            self.side_table[item] = [count, None]
        #Sort items based on support count. If item is in frequent_items, append it to sorted items and insert it into tree.
        for transaction in transactions:
            sorted_items = []
            for item in sorted(transaction, key=lambda i: -item_count[i]):
                if item in self.frequent_items:
                    sorted_items.append(item)
            self.insert_tree(self.root, sorted_items)

    #Insert elements from transaction into tree    
    def insert_tree(self, node: FPNode, items):
        if len(items) == 0:
            return
        
        first_item = items[0]
        if first_item not in node.children:
            node.children[first_item] = FPNode(first_item, 1, node)

            #update side table
            if self.side_table[first_item][1] is None:
                self.side_table[first_item][1] = node.children[first_item]
            else:
                current = self.side_table[first_item][1]
                while current.next:
                    current = current.next
                current.next = node.children[first_item]
        
        else:
            node.children[first_item].increment(1)

        self.insert_tree(node.children[first_item], items[1:])

#Mine patterns from fp-tree
def mine_patterns(side_table, min_support, prefix=frozenset()):
    #dictionary to hold patterns mined from tree
    mined_patterns = {}
    #Sort elements in side table and loop through each element in side table
    for item in sorted(side_table.keys(), key=lambda k: side_table[k][0]):
        new_prefix = prefix | {item}
        mined_patterns[frozenset(new_prefix)] = side_table[item][0]

        #find base for conditional pattern
        base = []
        node = side_table[item][1]

        while node:
            path = []
            parent = node.parent
            while parent and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent
            
            for _ in range(node.count):
                base.append(path)
            node = node.next

        #Build projected tree
        projected_tree, new_header = build_fp_tree(base, min_support)
        if new_header:
            mined_patterns.update(mine_patterns(new_header, min_support, new_prefix))
        
        return mined_patterns
#from a base condition for projection, build an fp-tree
def build_fp_tree(transactions, min_support):
    projected_tree = FPTree(transactions, min_support)
    return projected_tree, projected_tree.side_table if projected_tree.side_table else None

if __name__ == '__main__':
    main()