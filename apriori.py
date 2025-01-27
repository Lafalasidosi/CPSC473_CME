import sys
import re
#File and min_support will be whatever is taken in as command line input
try:
    file = open(sys.argv[1], 'r')
except OSError:
    print("File could not be read.")
min_support = sys.argv[2]
#Transactions will be a 2d array that will contain all the transaction data from the file
transactions = []
#For loop to add each line of the file to the Transactions 2d-array
for line in file:
    transactions.append(re.split(r'\t| +', line))
print(transactions[1][3])
# def apriori(dataset, support):