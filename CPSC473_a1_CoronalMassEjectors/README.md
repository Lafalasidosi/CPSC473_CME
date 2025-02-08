# Assignment 1 - Apriori

By the Coronal Mass Ejectors (CME)

---

## How to execute

By the time you've decompressed, unarchived, and navigated into this assignment folder, all you have to do is run something like

```shell script
python3.XX apriori.py ./data.txt 50
```

You don't _have_ to prepend the data file name with './'. The final argument is the minimum support desired _as a percentage_.

That is, the above command calls our apriori.py program to find itemsets in `data.txt` which appear in at least 50% of all entries.
