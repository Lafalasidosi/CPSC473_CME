import sys
from itertools import chain, combinations

global L_sets

def main():
    #D_name = sys.argv[2]
    #min_sup = sys.argv[2] / 100.0 * len(D)
    # e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081
    D_name = "a1-resources/retail.txt"
    D = open(D_name)
    min_sup = 15.0 / 100.0 * 88162
    L = [set()]   
    C = [set(), set()]  # TODO: need to make these dicts; they store both an itemset and its count
    L1 = find_frequent_1_itemsets(D_name, 10000)
    L.append(L1)
    k = 2 
    while not len(L[k-1]) == 0:
        C.append(apriori_gen(L[k-1], k))
        while (D.readline()): # scan D for counts
            t = to_ints(peekline(D).split()[2:])
            C_t = subset(C[k], t) # get the subsets of t that are candidates
            for c, count in C_t:
                C_t.update({c, count+1})
        k += 1
        L.append(set([c for c in C_t if C_t.get(c) >= min_sup])) 
        print(L[-1])
    for L in L:
        print(L)
    
    
def to_ints(string_array):
    result = []
    for s in string_array:
        result.append(int(s))
    return result       
    
    
def subset(C_k, t):
    results = {}
    for s in C_k:
        if s in t:
            results.update({s: 0})
    return results
        

def get_counts(filename):
    result = {}                     
    data_file = open(filename)      
    while (data_file.readline()):                   # skips first line containing number of rows of data
        items = peekline(data_file).split()[2:]     # itemset portion of transaction = all columns except first two
        for entry in items:                         # for every entry in a line, 
                entry = int(entry)                  # read it as an integer,
                count = result.get(entry)           # check if it's already in `counts`:
                if (count == None):                 # if it's not, it's the first time we've seen it
                        result.update([(entry, 1)]) # so add it with a count of 1
                else:                               # otherwise, increment the value that's already there
                        result.update([(entry, int(count) + 1)])
    return result


def find_frequent_1_itemsets(filename, min_sup):    
    counts = get_counts(filename)                 
    has_min_sup = []
    for x in counts:
        if counts.get(x) > min_sup:
            has_min_sup.append((x, counts.get(x)))
    return has_min_sup
                
            
# Returns the current line of a given file
def peekline(f):
    pos = f.tell()          # set  'pos' to current reader location
    result = f.readline()   # read whole line--reader advances to next line
    f.seek(pos)             # set reader to where it was before the call to readline()
    return result           # return result of earlier read


def all_equal_except_last(l1, l2):
    length = len(l1) # == len(l2)
    for i in range(length-1):
        if l1[i] != l2[i]:
            return False
    return l1[length-1] < l2[length-1]
    

def apriori_gen(L_prev, k):
    C_k = []
    for l1 in L_prev:
        for l2 in L_prev:
            if all_equal_except_last(l1, l2):
                c = set(l1).union(set(l2))
                if has_infrequent_subset(c, L_prev):            
                    c = ()
                else:
                    C_k.append(c)
    return C_k


def k_powersets(item_set, k):
        s = list(item_set)
        return combinations(s, k)


def has_infrequent_subset(candidate, L_prev, k):
    for s in k_powersets(candidate):
        if s not in L_prev:
            return True
    return False


if __name__ == '__main__':
    main()