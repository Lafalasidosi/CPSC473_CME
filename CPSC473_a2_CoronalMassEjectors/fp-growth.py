from math import ceil
import sys
from itertools import islice
import linecache
import time
from collections import defaultdict

def main():
    #D_name is the filename obtains from command line
    D_name = sys.argv[1]
    if D_name[0] == '.':
        D_name = D_name[2:]     # no file names starting with './'
    
    #grab the first line from the inputted file to get the number of transactions in a dataset
    transaction_size = int(linecache.getline(D_name, 1))
    #calculate minimum support
    min_sup = ceil((int(sys.argv[2]) / 100) * transaction_size)
    print('minsup = ' + sys.argv[2] + '% = ' + str(min_sup))

    run_time_start = time.time()
    #fp-growth in main memory here
    transactions = []
    text_to_2d_array(D_name, transactions)
    #Generate fp-tree
    fp_tree = FPTree(transactions, min_sup)
    #mine patterns from fp-tree
    mined_patterns = mine_patterns(fp_tree.side_table, min_sup)

    run_time_end = time.time()

    #generate output file
    produce_output(mined_patterns, D_name)

    #Total runtime of the program
    total_run_time = run_time_end - run_time_start

    #Print frequent patterns found and the total runtime
    print('|FPs| = ' + str(len(mined_patterns)))
    print(f'Total Runtime: {total_run_time:.3f} sec')

#Nodes in an FP-tree
class FPNode:
    def __init__(self, item, count, parent):
        #item that node is for
        self.item = item
        #support count for item
        self.count = count

        self.parent = parent

        self.children = {}
        #the next node with the same item
        self.next = None
    #increment value of FPNode
    def increment(self):
        self.count += 1

#The FP-tree
class FPTree:
    def __init__(self, transactions, min_support):
        self.min_support = min_support
        #Side table to point to nodes
        self.side_table = {}
        #Root of tree
        self.root = FPNode(None, 1, None)
        #a dictionary of all the items in the inputted dataset, and their count
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
            #insert sorted items into the tree, starting from the root
            self.insert_tree(self.root, sorted_items)

    #Insert elements from transaction into tree. Transactions will be inserted one node at a time    
    def insert_tree(self, node: FPNode, items):
        #Base case for recursion
        if len(items) == 0:
            return
        #The first node will be based on the first item found in items[]
        first_item = items[0]
        #if the first item is not in the children of node, then it will add it in to children as a new child node.
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
        
        #if first item is in the children of node, then it will increment that node item by 1
        else:
            node.children[first_item].increment()
        #Recurse through the tree to add the next item into the fp-tree
        self.insert_tree(node.children[first_item], items[1:])

#Mine patterns from fp-tree
def mine_patterns(side_table, min_support, prefix=frozenset()):
    #dictionary to hold patterns mined from tree
    mined_patterns = {}
    #Sort elements in side table and loop through each element in side table
    for item in sorted(side_table.keys(), key=lambda k: side_table[k][0]):
        new_prefix = prefix.union({item})
        mined_patterns[frozenset(new_prefix)] = side_table[item][0]

        #base for a pattern to use for projecting a tree
        base = []
        #set the inidital node for the while loop
        node = side_table[item][1]
        #While there are nodes in the table, find the paths that lead to that item in the tree
        while node:
            path = []
            parent = node.parent
            #while the parent node and item is not null, append nodes to the path array, and go up the tree.
            while parent and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent
            #append the path to the base conditional pattern based on the count of the node
            for _ in range(node.count):
                base.append(path)
               
            node = node.next

        #Build projected tree side table
        new_side_table = build_projected_side_table(base, min_support)
        #if new header is not empty, recurse through tree and mine more patterns.
        if new_side_table:
            mined_patterns.update(mine_patterns(new_side_table, min_support, new_prefix))
        
    return mined_patterns

#from a base condition for projection, build an fp-tree projection, and return the side table if it is not null
def build_projected_side_table(transactions, min_support):
    #build projected tree based given transactions and min_support
    projected_tree = FPTree(transactions, min_support)
    return projected_tree.side_table if projected_tree.side_table else None

'''Helper functions'''

#Produce outputted text file
def produce_output(patterns, D_name):
    #Remove extension from file name
    input_file_without_extension = D_name[:-4]
    #format for output string for output file
    output_str = 'MiningResult_{}.txt'.format(input_file_without_extension)
    output_file = open(output_str, 'w')
    
    print()
    
    #loop through mined patterns and increment count, write number of frequent patterns to file
    output_file.write("|FPs| = " + str(len(patterns)) + "\n")
    
    #write the itemset, and the count to the file
    for n_itemsets, count in patterns.items():
        output_file.write(", ".join(n_itemsets) + " : " + str(count) + "\n")

#helper function to convert inputted dataset/text file into a 2d array
def text_to_2d_array(filename, base_array):
    with open(filename, "r")as file:
        for line in islice(file, 1, None):
            row = line.strip().split()
            base_array.append(row[2:])

#Start code execution at main method
if __name__ == '__main__':
    main()