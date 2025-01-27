import sys
import re
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
print(transactions[0][0])
#container for all initial single candidates and how many times they happen in total for all transactions
single_candidates = {}
for transaction in transactions[1:]:
    for item in transaction[2:]:
        single_candidates[item] = single_candidates.get(item,0) + 1

print(single_candidates)