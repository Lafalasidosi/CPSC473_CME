import sys
from itertools import chain, combinations

def main():
    #min_sup = sys.argv[2] / 100.0 * len(D)
    # e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081
    file = sys.argv[1]
    min_support = int(sys.argv[2]) / 100
    
    L_sets = []
    L_sets.append([])
    L1 = find_frequent_1_itemsets(file, min_support)
    L_sets.append(L1)
    k = 2
    while L_sets[k-1]:
         C_k = apriori_gen(L_sets, k-1)
         L_sets.append(C_k)
    #Remove first list, as it is only an empty list
    del L_sets[0]
    print(L_sets)


def apriori_gen(prev_L, set_size):
     candidates_k = []
     c = ()
     for l1 in prev_L:
          for l2 in prev_L:
               if l1[set_size - 1] < l2[set_size - 1]:
                   c = l1 + l2 
                
               if has_infrequent_subset(c, prev_L):
                    del c
               else:
                    candidates_k.append(c)

     return candidates_k


def has_infrequent_subset(c, prev_L):
    power_sets = get_powerset(c)
    for s in power_sets:
         if s not in prev_L:
              return True
         else:
              return False

def find_frequent_1_itemsets(filename, min_sup):    
    counts = get_counts(filename)                 
    has_min_sup = []
    for x in counts:
        if counts.get(x) >= min_sup:
            has_min_sup.append((x, counts.get(x)))
    return has_min_sup
                
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
            
# Returns the current line of a given file
def peekline(f):
    pos = f.tell()          # set  'pos' to current reader location
    result = f.readline()   # read whole line--reader advances to next line
    f.seek(pos)             # set reader to where it was before the call to readline()
    return result           # return result of earlier read

#function that will return a list of powersets for a set. The start parameter is the size of combinations it will start with
def get_powerset(item_set):
     output = list(item_set)
     return chain.from_iterable(combinations(output,r) for r in range(len(output) + 1))
if __name__ == '__main__':
    main()