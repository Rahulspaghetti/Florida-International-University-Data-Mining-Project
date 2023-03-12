from collections import defaultdict

def get_transactions(filename):
    transactions = defaultdict(list)
    with open(filename, 'r') as f:
        for line in f:
            tid, item = map(int, line.strip().split())
            item = "item" + str(item)  # add the word "item" in front of each item ID
            transactions[tid].append(item)
    return transactions


transactions = get_transactions('small.txt')

# print(transactions)

# create a list of all items
items = []
for transaction in transactions.values():
    for item in transaction:
        items.append(item)

# count the occurrence of each item
item_counts = {}
for item in items:
    if item in item_counts:
        item_counts[item] += 1
    else:
        item_counts[item] = 1

# keep only items with count >= 1
frequent_items = []
for item, count in item_counts.items():
    if count >= 200:
        frequent_items.append(item)


# print 1-frequent
print('ITEMSETS', '|SUPPORT_COUNT')
for item in frequent_items:
    print(f"{item}: {item_counts[item]}")

# create a set of 2-itemsets and their count in data
itemset_2 = {}
for i in frequent_items:
    for j in frequent_items:
        if i != j:
            # create 2-itemset
            itemset = set([i, j])
            count = 0
            for transaction in transactions.values():
                # check if 2-itemset is present in transaction
                if itemset.issubset(transaction):
                    count += 1
            itemset_2[tuple(itemset)] = count

print('----------------------------')
print('ITEMSETS', '|SUPPORT_COUNT')
for itemset, count in sorted(itemset_2.items(), key=lambda x: x[1], reverse=True):
    if count >= 200:
        print(itemset, count)
