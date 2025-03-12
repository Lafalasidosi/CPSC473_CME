import sys

def main():
    #min_sup = sys.argv[2] / 100.0 * len(D)
    # e.g. len(D) = 88162 => argv[2] = 50 => minimum support = 44081

    filename = "a2-resources/data.txt"
    min_sup = 2

    L1 = find_frequent_1_itemsets(filename, min_sup)

    # Sort the list based on the second element, in ascending order
    L1_sorted = sorted(L1, key=lambda x: x[1])
    L1_sorted.reverse()

    print(L1_sorted)

    # Create the Ordered-Item set



    # Create the FP tree



    # Create the Conditional Pattern Base for each item



    # Create the Conditional Frequent Pattern Tree for each item



    # Identify frequent patterns



    """

    # create output file
    output_str = filename.replace("a2-resources/", "a2-resources/MiningResult_")
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



    print("End of program.")
"""

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
    while data_file.readline():  # skips first line containing number of rows of data
        items = peekline(data_file).split()[2:]  # itemset portion of transaction = all columns except first two
        for entry in items:  # for every entry in a line,
            entry = int(entry)  # read it as an integer,
            count = result.get(entry)  # check if it's already in `counts`:
            if count is None:  # if it's not, it's the first time we've seen it
                result.update([(entry, 1)])  # so add it with a count of 1
            else:  # otherwise, increment the value that's already there
                result.update([(entry, int(count) + 1)])
    data_file.close()
    return result


# Returns the current line of a given file
def peekline(f):
    pos = f.tell()  # set  'pos' to current reader location
    result = f.readline()  # read whole line--reader advances to next line
    f.seek(pos)  # set reader to where it was before the call to readline()
    return result  # return result of earlier read


if __name__ == '__main__':
    main()