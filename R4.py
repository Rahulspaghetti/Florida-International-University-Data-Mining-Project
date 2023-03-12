from collections import defaultdict

# Sample transaction dataset
transactions = [
    ['a', 'b', 'c', 'd'],
    ['a', 'b', 'c'],
    ['a', 'b'],
    ['a', 'c', 'd'],
    ['b', 'c', 'd'],
    ['b', 'c'],
    ['c', 'd'],
    ['d']
]

# Support threshold for infrequent itemset elimination
min_support = 3

# Count occurrences of items in transactions using a dictionary
item_counts = defaultdict(int)
for transaction in transactions:
    for item in transaction:
        item_counts[item] += 1

# Remove infrequent items that don't meet the support threshold
frequent_items = {item for item, count in item_counts.items() if count >= min_support}

# Create a prefix tree for the frequent itemsets
prefix_tree = defaultdict(int)
for transaction in transactions:
    # Filter out infrequent items
    filtered_transaction = [item for item in transaction if item in frequent_items]
    # Generate all subsets of the filtered transaction
    for i in range(len(filtered_transaction)):
        for j in range(i+1, len(filtered_transaction)+1):
            subset = frozenset(filtered_transaction[i:j])
            prefix_tree[subset] += 1

# Print the frequent itemsets and their counts
print("Frequent Itemsets:")
for itemset, count in prefix_tree.items():
    print(f"{itemset}: {count}")
