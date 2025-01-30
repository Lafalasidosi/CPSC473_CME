import sys
import re
from math import ceil
#File and min_support will be whatever is taken in as command line input
try:
    file = open(sys.argv[1], 'r')
    min_support = int(sys.argv[2]) / 100
except OSError:
    print("File could not be read.")
except:
    print("Error in inputs")
#Transactions will be a 2d array that will contain all the transaction data from the file
transactions = []
#For loop to add each line of the file to the Transactions 2d-array
for line in file:
    line = line.replace('\n', '')
    transactions.append(re.split(r'\t| +', line))
#print(transactions[0][0])
#container for all initial single candidates and how many times they happen in total for all transactions
single_candidates = {}
for transaction in transactions[1:]:
    for item in transaction[2:]:
        single_candidates[item] = single_candidates.get(item,0) + 1
#Set the support count to be based on the minimum support times the total # of transactions
support_count = ceil(min_support * int(transaction[0][0]))
#Setting initial itemsets
frequent_itemsets = {}
for item, count in single_candidates.items():
    if(count >= support_count):
        frequent_itemsets[frozenset([item])] = count
#set initial start to look for pairs
k = 2
#This loop goes through all candidates and weeds out any candidates that don't meet MST. Once there are no more itemsets that meet MST, it will break out of the loop.
while True:
    #dictionary of total candidates for the dataset.
    total_candidates = {}
    current_itemsets = list(frequent_itemsets.keys())
    #make initial candidate list by forming unions looping through the itemset. If the number of items in an itemset matches our k value, then it will be kept and initial count set to 0.
    for i in range(len(current_itemsets)):
        for j in range(i + 1, len(current_itemsets)):
            set_union = current_itemsets[i].union(current_itemsets[j])
            if len(set_union) == k:
                total_candidates[set_union] = 0
    
    for transaction in transactions[1:]:
        for candidate in total_candidates:
            #check if candidate is a subset of transactions. If so, increment total candidates
            if candidate.issubset(transaction):
                total_candidates[candidate] += 1
    #Update the frequent itemset by first looping through candidates and seeing if an itemset's count is >= the minimum support count. If so, update itemset's count and add it to frequent_itemsets.
    for itemset, count in total_candidates.items():
        if count >= support_count:
            total_candidates[itemset] = count
            # add new itemsets to frequent itemsets
            frequent_itemsets.update(total_candidates)
    
    #if no candidates are frequent, leave loop
    if not total_candidates:
        break

    #increment number of items per itemset to look at
    k += 1
#Remove any itemsets that don't meet MST. For some reason, this doesn't happen in while-loop, and needs to be done again here.
final_frequent_itemset = {}
for item, count in frequent_itemsets.items():
    if count >= support_count:
        final_frequent_itemset[item] = count
print(support_count)
print(str(final_frequent_itemset).replace("frozenset", ""))