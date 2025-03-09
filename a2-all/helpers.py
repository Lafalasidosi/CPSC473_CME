from itertools import combinations
from functools import reduce

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
                if (count is None):                 
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