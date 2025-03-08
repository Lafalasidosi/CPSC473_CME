from math import ceil
import sys
from itertools import combinations
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
    run_time_end = time.time()
    #Total runtime of the program
    total_run_time = run_time_end - run_time_start

def produce_output(L, D_name):
    inputfilewithoutextension = D_name[:-4]
    output_str = 'MiningResult_{}.txt'.format(inputfilewithoutextension)
    output_file = open(output_str, 'w')
    count = 0
    print()
    for i in L:
        for j in i:
            count += 1
    output_file.write("|FPs| = " + str(count) + "\n")
    
    for n_itemsets in L:
        for itemset, count in n_itemsets.items():
            output_file.write(str(itemset) + " : " + str(count) + "\n")

def peekline(f):
    """Return the current line of an open file 
    without moving the reader pointer.
    """
    pos = f.tell()
    result = f.readline()
    f.seek(pos)
    return result

if __name__ == '__main__':
    main()

class FPNode:
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None
    
    def increment(self, count):
        self.count += count

class FPTree:
    def __init__(self, transactions, min_support):
        self.min_support = min_support
        self.side_table = {}
        self.root = FPNode(None, 1, None)
    
        item_count = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                item_count[item] += 1

        self.frequent_items = {}
        for k,v in item_count.items():
            if v >= min_support:
                self.frequent_items[k] = v
        
        self.header_table = {}
        for item, count in self.frequent_items.items():
            self.header_table[item] = [count, None]
        
        for transaction in transactions:
            sorted_items = []
            for item in sorted(transaction, key=lambda i: -item_count[i]):
                if item in self.frequent_items:
                    sorted_items.append(item)
            self.insert_tree(sorted_items, self.root)
    
    