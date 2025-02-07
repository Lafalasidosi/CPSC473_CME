import sys
from itertools import combinations

def main():
    #D_name = sys.argv[2]
    #min_sup = sys.argv[2] / 100.0 * len(D)
    # e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081
    D_name = "a1-resources/1k5L.txt"
    D = open(D_name)
    min_sup = 10
    L = [dict()]         # L & C contain these emptyset entries to keep k-indexing in line with the pseudocode
    C = [dict(), dict()]  
    L1 = find_frequent_1_itemsets(D_name, min_sup)
    L.append(L1)
    k = 2 
    while not len(L[k-1]) == 0:
        C_k = apriori_gen(L[k-1], k)
        C.append(C_k)
        if D == None:
            D = open(D_name)
        while (D.readline()): # scan D for counts
            t = to_ints(peekline(D).rstrip().split()[2:])
            C_t = subset(C[k], t) # get the subsets of t that are candidates
            for c in C_t:
                count = C_k[c]
                C_k.update({c: count+1})
        L_k = dict([(c, C_k[c]) for c in C_k if C_k[c] >= min_sup])
        L.append(L_k)
        k += 1
        D.close()
        D = None
    for x in L:
        print(x)
    
    
def to_ints(string_array):
    return list(map(lambda x: int(x), string_array))


def to_strings(int_array):
    return list(map(lambda x: str(x), int_array))
    
    
def subset(C_k, t):
    results = {}
    shopping_cart = set(to_ints(t))
    for item_string in C_k:
        items = set(to_ints(item_string.split()))
        if items.issubset(shopping_cart):
            results.update({item_string: 0})
    return results
        
# Returns a dict of entries which look like "0": 3, meaning
# the number 0 appears three times
def get_counts(filename):
    result = {}                     
    data_file = open(filename)      
    while (data_file.readline()):                   # skips first line containing number of rows of data
        items = peekline(data_file).split()[2:]     # itemset portion of transaction = all columns except first two
        for entry in items:                         # for every entry in a line, 
#                entry = int(entry)                  # read it as an integer,       #may well not need to do this anymore
                count = result.get(entry)           # check if it's already in `counts`:
                if (count == None):                 # if it's not, it's the first time we've seen it
                        result.update({entry: 1}) # so add it with a count of 1
                else:                               # otherwise, increment the value that's already there
                        result.update({entry: count + 1})
    return result


def find_frequent_1_itemsets(filename, min_sup):    
    counts = get_counts(filename)                 
    has_min_sup = {} 
    for x in counts:
        if counts.get(x) >= min_sup:
            has_min_sup.update({x: counts.get(x)})
    return has_min_sup
                
            
# Returns the current line of a given file
def peekline(f):
    pos = f.tell()          # set  'pos' to current reader location
    result = f.readline()   # read whole line--reader advances to next line
    f.seek(pos)             # set reader to where it was before the call to readline()
    return result           # return result of earlier read


def all_equal_except_last(x, y):
    l1 = x.split()
    l2 = y.split()
    length = len(l1) # == len(l2)
    for i in range(length-1):
        if l1[i] != l2[i]:
            return False
    result = int(l1[length-1]) < int(l2[length-1])
    return result


def apriori_gen(L_prev, k): 
    C_k = {}
    for l1 in L_prev:   # l1 = "0 32 44 45 678", for example
        for l2 in L_prev:
            if all_equal_except_last(l1, l2):
                c = itemset_union(l1, l2)
                if has_infrequent_subset(c, L_prev, k-1):
                    c = ""
                else:
                    C_k.update({c: 0})
    return C_k


def itemset_union(l1, l2):
    to_append = to_strings(l2.split())[-1]
    return l1 + " {}".format(to_append)
    

def k_powersets(item_set, k):
        s = item_set
        result = list(combinations(s, k))
        return result


def has_infrequent_subset(c, L_prev, k):
    candidate_itemset = set(to_ints(c.split()))
    frequent_sets = list(map(lambda x: set(to_ints(x.split())), L_prev)) # TODO: this line incorrectly turns '32' into {3, 2}
    k_candidate_subsets = list(map(lambda x: set(x), k_powersets(candidate_itemset, k)))
    for S in k_candidate_subsets:
        if not S in frequent_sets:
            return True
    return False


if __name__ == '__main__':
    main()