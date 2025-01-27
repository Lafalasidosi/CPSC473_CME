import pandas as pd
import sys

D = pd.read_csv("a1-resources/retail.txt")
min_sup = sys.argv[2] / 100.0 * len(D)





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
    filename = "a1-resources/retail.txt"
    
    counts = pd.DataFrame.from_dict(dict({}))
    data_file = open(filename)
    
    while (data_file.readline()):
        items = data_file.readline().split()[2:]
        for entry in items:
            int_rep = int(entry)
            
        
    

# Returns the current line of a given file
def peek(f):
    pos = f.tell()          # set  'pos' to current reader location
    result = f.readline()   # read whole line--reader advances to next line
    f.seek(pos)             # set reader to where it was before the call to readline()
    return result           # return result of earlier read