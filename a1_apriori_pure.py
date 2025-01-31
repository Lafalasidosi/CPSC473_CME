import pandas as pd
import sys


#min_sup = sys.argv[2] / 100.0 * len(D)
# e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081





def find_frequent_1_itemsets(filename, min_sup):    
    counts = {}                     
    data_file = open(filename)      
    while (data_file.readline()):                   # skips first line containing number of rows of data
        items = peekline(data_file).split()[2:]     # itemset portion of transaction = all columns except first two
        for entry in items:                         # for every entry in a line, 
                entry = int(entry)                  # read it as an integer,
                count = counts.get(entry)           # check if it's already in `counts`:
                if (count == None):                 # if it's not, it's the first time we've seen it
                        counts.update([(entry, 1)]) # so add it with a count of 1
                else:                               # otherwise, increment the value that's already there
                        counts.update([(entry, int(count) + 1)])    
                        
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

find_frequent_1_itemsets("a1-resources/retail.txt", 44081)

