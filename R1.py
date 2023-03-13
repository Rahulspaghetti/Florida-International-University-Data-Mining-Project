from collections import defaultdict
# set minimum support threshold
minsup = 200


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

# keep only items with count >= minsup
frequent_items = []
freq_items = []
for item, count in item_counts.items():
    if count >= minsup:
        frequent_items.append(item)
        freq_items.append((item, count))

# sort frequent items by count
freq_items.sort(key=lambda x: x[1], reverse=True)

# print 1-frequent
print('ITEMSETS', '|SUPPORT_COUNT')
for item, count in freq_items:
    print(f"{item}: {count}")

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
    if count >= minsup:
        # print(itemset, count)
        print(f"{itemset}: {count}")

print('----------------------------')
with open("frequent" +str(minsup)+"_items.txt", "w") as f:
    f.write("ITEMSETS |SUPPORT_COUNT\n")
    for item, count in freq_items:
        f.write(f"{item}: {count}\n")
    for itemset, count in sorted(itemset_2.items(), key = lambda x: x[1], reverse = True):
            if count >= minsup:
                f.write(f"{itemset}: {count}\n")
