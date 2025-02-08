from math import ceil
import sys
from itertools import combinations
import linecache
from functools import reduce
import time

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
    L[1] = L1
    
    while not len(L[k-1]) == 0:
        C_k = apriori_gen(L[k-1], k)
        C[k] = C_k
        while (D.readline()):
            t = peekline(D).rstrip().split()[2:]
            t = array_to_string(t)
            C_t = subset(C[k], t) 
            for c in C_t:
                count = C_k[c]
                C_k.update({c: count+1})
        L_k = dict([(c, C_k[c]) for c in C_k if C_k[c] >= min_sup])
        L.append(L_k)
        k += 1
        D.seek(0)
        C.append({})
    
    L.pop()
    run_time_end = time.time()
    produce_output(L, D_name)
    count = 0
    for i in L:
        for j in i:
            count += 1

    total_run_time = run_time_end - run_time_start
    print('|FPs| = ' + str(count))
    print(f'Total Runtime: {total_run_time:.3f} sec')
def apriori_gen(L_prev, k): 
    """Return k-itemsets which have no infrequent subsets."""
    C_k = {}
    for x in L_prev: 
        for y in L_prev:
            if all_equal_except_last(x, y):
                c = itemset_union(x, y)
                if has_infrequent_subset(c, L_prev, k-1):
                    c = ""
                else:
                    C_k.update({c: 0})
    return C_k


def has_infrequent_subset(candidate_itemset, L_prev, k):
    """Return true if candidate_itemset contains a (k-1)-subset
    not found in L_prev (L[k-1]).
    """
    C = set(to_ints(candidate_itemset))
    frequent_sets = list(map(lambda x: set(to_ints(x)), L_prev)) 
    k_candidate_subsets = list(map(lambda x: set(x), k_powersets(C, k)))
    for S in k_candidate_subsets:
        if not S in frequent_sets:
            return True
    return False


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


######## Helper functions ########

def to_ints(itemset_string):
    """Return the given array of strings as an array of integers."""
    s = itemset_string.rstrip().split()
    return list(map(lambda x: int(x), s))


def to_strings(int_array):
    """Return the given array of integers as an array of strings."""
    return list(map(lambda x: str(x), int_array))


def array_to_string(string_array):
    """Return the concatenation of all strings in an array thereof."""
    if len(string_array) == 0:
        return ''
    return reduce(lambda x, y: x + " " + y, string_array)


def peekline(f):
    """Return the current line of an open file 
    without moving the reader pointer.
    """
    pos = f.tell()
    result = f.readline()
    f.seek(pos)
    return result
    
    
def subset(C_k, transaction):
    """Return those candidate itemsets
    which are subsets of the given transaction.
    """
    results = {}
    bought_items = set(to_ints(transaction))
    for candidate_string in C_k:
        items = set(to_ints(candidate_string))
        if items.issubset(bought_items):
            results.update({candidate_string: 0})
    return results

        
def get_counts(filename):
    """Return a dictionary in which 
    the keys are singleton itemsets, and
    each value is the number of transactions
    in which the respective itemset appears.
    """
    result = {}                     
    data_file = open(filename)      
    while (data_file.readline()):  # Skips first line containing number of rows of data
        items = peekline(data_file).split()[2:]     
        for entry in items:                         
                count = result.get(entry)           
                if (count == None):                 
                    result.update({entry: 1})   
                else:                               
                    result.update({entry: count + 1})
    return result


def find_frequent_1_itemsets(filename, min_sup):
    """Return all singleton itemsets whose respective counts
    as determined by get_counts()
    are at least the given minimum support count value.
    """
    counts = get_counts(filename)                 
    has_min_sup = {} 
    for x in counts:
        if counts.get(x) >= min_sup:
            has_min_sup.update({x: counts.get(x)})
    return has_min_sup
                

def all_equal_except_last(itemset1, itemset2):
    """Return the truth value of the expression
    x[1] == y[1] and x[2] == y[2] and ... and x[k-1] < y[k-1].
    """
    x = itemset1.split()
    y = itemset2.split()
    length = len(x) # == len(l2)
    for i in range(length-1):
        if x[i] != y[i]:
            return False
    result = int(x[length-1]) < int(y[length-1])
    return result


def itemset_union(itemset1, itemset2):
    """Return the set-theoretic union of strings itemset1, itemset2.
    For example, if itemset1 == '0 1 2' and itemset2 == '0 1 3', 
    return '0 1 2 3'.
    """
    to_append = to_strings(itemset2.split())[-1]
    return itemset1 + " {}".format(to_append)
    

def k_powersets(itemset, k):
    """Return all subsets of itemset of cardinality k."""
    result = list(combinations(itemset, k))
    return result


if __name__ == '__main__':
    main()