import sys
from math import ceil
import linecache

def main():
    #min_sup = sys.argv[2] / 100.0 * len(D)
    # e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081
    file = sys.argv[1]
    #Uses linecache.getline to read the first line in our input file (the number of transactions) and then converts to an int
    D = int(linecache.getline(file, 1))
    print(f'Number of transactions: {D}')
    #Calculate minimum support based on user inputted percentage and the number of transactions
    min_support = ceil((int(sys.argv[2]) / 100) * D)
    print(f'minumum support: {min_support}')
    L_sets = []
    L1 = find_frequent_1_itemsets(file, min_support)
    print("L1: ", L1)

    for x in range(len(L1)):
        L_sets.append(L1[x])
    k = 2
    running = True
    while running:
        print("While-loop iteration: ", k)
        itemset_current = []
        prev_len = len(L_sets)
        find_frequent_n_itemsets(file, min_support, L1, L_sets, k, itemset_current, -1)
        if prev_len == len(L_sets):
            running = False

        k += 1
    print("final: ", L_sets)

    # create output file
    output_str = "MiningResult.txt"
    print(output_str)
    output_file = open(output_str, "w")

    # write results to file
    output_file.write("|FPs| = " + str(len(L_sets)) + "\n")
    for x in range(len(L_sets)):
        # 1-itemsets
        if x < len(L1):
            output_file.write(str(L_sets[x][0]) + " : " + str(L_sets[x][1]) + "\n")
        # n-itemsets
        else:
            itemset_str = ""
            for element in L_sets[x][0]:
                itemset_str += str(element) + ", "
            output_file.write(itemset_str[:-2] + " : " + str(L_sets[x][1]) + "\n")


def find_frequent_1_itemsets(filename, min_sup):    
    counts = get_counts(filename)                 
    has_min_sup = []
    for x in counts:
         if counts.get(x) >= min_sup:
              has_min_sup.append((x, counts.get(x)))
    return has_min_sup
                
# Parameters of find_frequent_n_itemsets:
# filename: name of file
# min_sup: minimum support threshold
# L1: list of frequent 1-itemsets
# L_sets: list of frequent n-itemsets for all n
# n_max: size of itemset being checked for frequency
# itemset_current: the itemset built by the recursive case to be checked for frequency by the base case
# last_x: see recursive case
def find_frequent_n_itemsets(filename, min_sup, L1, L_sets, n_max, itemset_current, last_x):

    # special case - when the itemset is the size of L1, the recursive case for-loop breaks. Build an itemset
    # with all values of L1 and allow it to be handled by the base case
    special_case = False
    if n_max == len(L1):
        for entry in L1:
            itemset_current.append(entry[0])
        special_case = True

    # base case
    if len(itemset_current) == n_max or special_case:
        result = []
        itemset_in_result = False
        data_file = open(filename)                      # skips first line containing number of rows of data
        while data_file.readline():                     # skips first line containing number of rows of data
            items = peekline(data_file).split()[2:]     # itemset portion of transaction = all columns except first two
            items = [int(item) for item in items]       # convert the items in the list to integers
            seen = 0                                    # determine if the current itemset is in the transaction
            for value in itemset_current:
                if value in items:
                    seen += 1
            if seen == n_max:                           # if it is, add entry to "result" or increment an existing entry
                if itemset_in_result:
                    for entry in result:
                        if entry[0] == itemset_current:
                            entry[1] += 1
                else:
                    result.append([itemset_current, 1])
                    itemset_in_result = True
                # count = result.get(itemset_current)     # lists are "unhashable" and result.get(list) does not work
        data_file.close()

        for x in result:                                  # determine if the itemset is frequent
            if x[1] > min_sup:                            # if so, add it to L_sets
                x[0] = tuple(x[0])
                L_sets.append(tuple(x))


    # recursive case - builds an itemset of size n by adding 1 value to current_itemset per recursive call until
    # itemset_current is an n-itemset. After building an n-itemset, it will remove the farthest right item in the
    # itemset and replace it with the proceeding value in L1. Thus, it creates all possible unique itemsets of size n.
    # "x > last_x" prevents a bug where itemsets containing duplicates, such as (2, 2, 3), or different permutations of
    # the same itemset, such as (2, 3) and (3, 2), were being created. I (Ryan) tried several possible solutions and
    # this is the only one I could get to work.
    else:
        for x in range(len(L1)):
            itemset_current.append(L_sets[x][0])
            if x > last_x:
                find_frequent_n_itemsets(filename, min_sup, L1, L_sets, n_max, itemset_current, x)
            itemset_current.pop()

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

if __name__ == '__main__':
    main()