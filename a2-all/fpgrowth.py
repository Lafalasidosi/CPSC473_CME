from math import ceil
import sys
from itertools import combinations
import linecache
from functools import reduce
import time
from helpers import find_frequent_1_itemsets

def main():
    D_name = sys.argv[1]
    if D_name[0] == '.':
        D_name = D_name[2:]     # no file names starting with './'
    D = open(D_name)
    transaction_size = int(linecache.getline(D_name, 1))
    min_sup = ceil((int(sys.argv[2]) / 100) * transaction_size)
    print('minsup = ' + sys.argv[2] + '% = ' + str(min_sup))
    k = 2 
    L = [dict(), dict()]            # So that L[k] refers to frequent k-itemsets
    C = [dict(), dict(), dict()]    # So that C[k] refers to candidate k-itemsets
    run_time_start = time.time()
    L1 = find_frequent_1_itemsets(D_name, min_sup)
    L1_to_FPTree = dict([(x, None) for x in L1.keys()])
    L[1] = L1
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    main()