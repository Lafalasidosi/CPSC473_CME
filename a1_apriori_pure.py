import pandas as pd
import sys


#min_sup = sys.argv[2] / 100.0 * len(D)





def find_frequent_1_itemsets(filename):
    # first off, create a DataFrame to hold item information
    # this DataFrame will have two columns: id, count
    # starts off as empty
    # for every row of the file AFTER THE FIRST,
    # read the row into a string except the first two elements; those aren't 'items'
    # for every element in the resulting row, 
    # convert it into an integer
    # if it doesn't already exist in a DataFrame, add it with a count of 1.
    
    # TODO: comment this assignment out or remove entirely once method implemented in full
    #filename = "retail-head.txt"
    
    counts = {}
    data_file = open(filename)
    while (data_file.readline()):   # skips first line
        items = peekline(data_file).split()[2:]    # itemset portion of transaction
        for entry in items:
                entry = int(entry)
                count = counts.get(entry)
                if (count == None):
                        counts.update([(entry, 1)])
                else:
                        counts.update([(entry, int(count) + 1)])
    print(counts)
                
            
        
    

# Returns the current line of a given file
def peekline(f):
    pos = f.tell()          # set  'pos' to current reader location
    result = f.readline()   # read whole line--reader advances to next line
    f.seek(pos)             # set reader to where it was before the call to readline()
    return result           # return result of earlier read

find_frequent_1_itemsets("a1-resources/retail-head.txt")

