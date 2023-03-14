# R1
import collections
from time import time
import itertools
import csv
from itertools import combinations
import matplotlib.pyplot as plt

start_time = time()

# References from internet for syntax and few write logic was referred


def generate_candidates(freq_itemsets):
    candidate_sets = set()
    for index, itemset1 in enumerate(freq_itemsets):
        for itemset2 in freq_itemsets[index + 1:]:
            # Take the union of the two itemsets
            candidate = frozenset(itemset1.union(itemset2))
            # Only add the candidate if its length is one greater than the length of itemset1
            if len(candidate) == len(itemset1) + 1:
                candidate_sets.add(candidate)
    return candidate_sets


def get_subsets(itemset):
    subsets = []
    for i in range(1, len(itemset) + 1):
        subsets += itertools.combinations(itemset, i)
    return subsets


def prune_candidates(candidates, freq_itemsets):
    """
    Prune candidate_set that are not subsets of frequent itemsets
    """
    pruned_candidates = []
    for candidate in candidates:
        subsets = get_subsets(candidate)
        if all(subset in freq_itemsets for subset in subsets):
            pruned_candidates.append(candidate)
    return pruned_candidates


def filter_frequent_itemsets(freq_itemsets):
    """
    Remove pruned candidate_set from frequent itemsets and generate text file of format itemset|supportcount
    """
    # Convert frequent itemsets to a set for faster lookup
    frequent_set = {itemset for itemset, support in freq_itemsets}

    # Prune candidate_set and create new frequent itemsets
    new_frequent_itemsets = []
    for itemset, support in freq_itemsets:
        subsets = get_subsets(itemset)
        pruned_subsets = [subset for subset in subsets if subset in frequent_set]
        new_itemset = frozenset(itemset)
        if pruned_subsets:
            new_frequent_itemsets.append((new_itemset, support))

    # Write new frequent itemsets to file
    with open("output_file.txt", 'w') as f:
        for itemset, support in new_frequent_itemsets:
            f.write("{}|{}\n".format(' '.join(itemset), support))


MIN_SUPPORT = 120
MIN_CONFIDENCE = 0.9

transactions = collections.defaultdict(list)
item_counts = collections.defaultdict(int)

# Scan input file and count item occurrences
with open("small.txt", "r") as f:
    for line in f:
        t_id, item_id = line.strip().split()
        item_id = "item" + str(item_id)  # add the word "item" in front of each item
        transactions[int(t_id)].append(item_id)
        item_counts[item_id] += 1

# Generate frequent 1-itemsets
frequent_itemsets = [(frozenset([item_id]), count) for item_id, count in item_counts.items() if count >= MIN_SUPPORT]

# Output frequent 1-itemsets to file
with open("DataMiningProjectGroup10_items.txt", "w") as f:
    f.write("ITEMSETS |SUPPORT_COUNT\n")
    for itemset, support_count in frequent_itemsets:
        f.write(f"{' '.join(itemset)}|{support_count}\n")

# Generate frequent k-itemsets for k > 1
k = 2
while frequent_itemsets:
    candidate_itemsets = collections.defaultdict(int)
    for transaction in transactions.values():
        for itemset in frequent_itemsets:
            if itemset[0].issubset(transaction):
                for item in transaction:
                    if item not in itemset[0]:
                        candidate_itemsets[itemset[0].union(frozenset([item]))] += 1
    frequent_itemsets = [(itemset, count) for itemset, count in candidate_itemsets.items() if count >= MIN_SUPPORT]
    if frequent_itemsets:
        # Output frequent k-itemsets to file
        with open("DataMiningProjectGroup10_items.txt", "a") as f:
            for itemset, support_count in frequent_itemsets:
                f.write(f"{' '.join(itemset)}|{support_count}\n")
    k += 1

end_time_initial = time()

# Pruning

frequent_itemsets = []

with open("DataMiningProjectGroup10_items.txt", 'r') as f:
    for line in f:
        items, support = line.strip().split('|')
        itemset = set(items.split())
        frequent_itemsets.append(itemset)

# Generate pruned candidate_set
candidates = generate_candidates(frequent_itemsets)
pruned_candidates = [(frozenset(candidate), 0) for candidate in prune_candidates(candidates, frequent_itemsets)]

filter_frequent_itemsets(pruned_candidates)

end_time_between = time()

# R2


# Set input and output file names
input_file_name = 'DataMiningProjectGroup10_items.txt'
output_file_name = 'DataMiningProjectGroup10_rules.txt'

itemsets = []


def read_itemsets(input_file_name):
    with open(input_file_name, 'r') as f:
        for line in f:
            items, support = line.strip().split('|')
            itemset = tuple(items.split())
            itemsets.append((itemset, int(support)))
    return itemsets


# Define function to generate rules from itemset
def generate_rules(itemset, support_count, minconf):
    rules = []
    for i in range(1, len(itemset)):
        for lhs in combinations(itemset, i):
            lhs = tuple(sorted(lhs))
            rhs = tuple(item for item in itemset if item not in lhs)
            support = int(support_count)
            lhs_support = int(next((count for subset, count in itemsets if set(lhs).issubset(subset)), 0))
            if lhs_support == 0:
                continue
            confidence = support / lhs_support
            if confidence >= minconf:
                # lift = confidence / (sum(1 for , count in itemsets if set(rhs).issubset()) / len(itemset))
                rules.append((lhs, rhs, support, confidence))
    return sorted(rules, key=lambda x: x[2], reverse=True)


# Open input and output files
with open(input_file_name, 'r') as input_file, open(output_file_name, 'w', newline='') as output_file:
    # Create CSV reader and writer objects

    input_reader = csv.reader(input_file, delimiter='|')

with open(input_file_name, 'r') as f, open(output_file_name, 'w', newline='') as output_file:
    output_writer = csv.writer(output_file, delimiter=' ')
    output_file.write(f"LHS|RHS|SUPPORT|CONFIDENCE\n")
    next(f)  # because there is a header, start reading at line 2
    for line in f:
        items, support = line.strip().split('|')
        itemset = tuple(items.split())
        itemsets.append((itemset, int(support)))
        # Generate rules from itemset
        for lhs, rhs, support, confidence in generate_rules(itemset, support, minconf=0.9):
            output_file.write(f"{' '.join(lhs)}|{' '.join(rhs)}|{support}|{confidence}\n")

end_time_final = time()

# R3
start_time2 = time()
# Define variables
min_sup = MIN_SUPPORT
min_conf = MIN_CONFIDENCE
input_file = "small.txt"
output_name = "DataMiningProjectGroup10"

items = set()
with open(input_file) as f:
    for line in f:
        transaction = line.strip().split(',')
        for item in transaction:
            items.add(item)
num_items = len(items)
print(f"Number of items: {num_items}")

with open(input_file, 'r') as f:
    transactions = [line.strip().split(' ') for line in f.readlines()]
num_transactions = len(transactions)

# Read in the frequent itemsets from a text file
frequent_itemsets = []
with open('DataMiningProjectGroup10_items.txt', 'r') as f:
    for line in f:
        itemset, support = line.strip().split('|')
        frequent_itemsets.append(itemset)

# Count the number of frequent k-itemsets for different values of k
freq_counts = {}
for itemset in frequent_itemsets:
    k = len(itemset.split())
    freq_counts[k] = freq_counts.get(k, 0) + 1

total_freq_items = 0

with open('DataMiningProjectGroup10_items.txt', 'r') as f:
    for line in f:
        itemset, support_count = line.strip().split('|')
        freq_items = itemset.split(',')
        total_freq_items += len(freq_items)

max_k_itemset = None
max_k_itemset_count = 0
with open('DataMiningProjectGroup10_items.txt', 'r') as output_file:
    for line in output_file:
        itemset, count = line.strip().split('|')
        items = itemset.split(',')
        if len(items) > max_k_itemset_count:
            max_k_itemset = items
            max_k_itemset_count = len(items)

with open('DataMiningProjectGroup10_items.txt', 'r') as f:
    # Read each line in the output file
    lines = f.readlines()[1:]

    # Create a dictionary to keep track of the count of each itemset
    itemset_counts = {}

    # Loop through each line in the file
    for line in lines:
        # Split the line by '|' separator
        itemset, count = line.strip().split('|')
        # Add the count of the itemset to the dictionary
        itemset_counts[itemset] = int(count)

    # Find the itemset with the highest count
    most_freq_itemset = max(itemset_counts, key=itemset_counts.get)

with open('DataMiningProjectGroup10_rules.txt', 'r') as f:
    lines = f.readlines()[1:]
    num_high_conf_rules = sum(
        1 for line in lines
        if float(line.split('|')[-1].strip()) >= min_conf
    )

with open('DataMiningProjectGroup10_rules.txt', 'r') as f:
    reader = csv.reader(f, delimiter='|')
    header = next(reader)  # Skip header
    highest_confidence = 0
    highest_conf_rule = None
    for row in reader:
        lhs, rhs, confidence, support = row[0].split(','), row[1].split(','), int(row[2]), float(row[3])
        if confidence > highest_confidence:
            highest_confidence = confidence
            highest_conf_rule = (lhs, rhs, support, confidence)
    print("The rule with the highest confidence is:", highest_conf_rule)
    rule_with_highest_conf = highest_conf_rule

time_to_find_freq_itemsets = end_time_initial - start_time
time_to_find_conf_rules = end_time_final - end_time_initial

# Writing to file info
with open(f"{output_name}_info.txt", "w") as f:
    f.write(f"minsup: {min_sup}\n")
    f.write(f"minconf: {min_conf}\n")
    f.write(f"input file: {input_file}\n")
    f.write(f"output name: {output_name}\n")
    f.write(f"Number of items: {num_items}\n")
    f.write(f"Number of transactions: {num_transactions}\n")
    for k, v in dict(freq_counts).items():
        f.write(f"Number of frequent {k}-itemsets: {v}\n")

    f.write(f"Total number of frequent items: {total_freq_items}\n")
    f.write(f"The length of the largest k-itemset: {k}\n")
    f.write(f"The most frequent itemset: {most_freq_itemset}\n")
    f.write(f"Number of high confidence rules: {num_high_conf_rules}\n")
    f.write(f"The rule with the highest confidence: {rule_with_highest_conf}\n")
    f.write(f"Time in seconds to find the frequent itemsets: {time_to_find_freq_itemsets:.2f}\n")
    f.write(f"Time in seconds to find the confident rules: {time_to_find_conf_rules:.2f}\n")

# R4
# Read in the frequent itemsets from a text file
frequent_itemsets = []
with open('DataMiningProjectGroup10_items.txt', 'r') as f:
    for line in f:
        itemset, support = line.strip().split('|')
        frequent_itemsets.append(itemset)

# Count the number of frequent k-itemsets for different values of k
freq_counts = {}
for itemset in frequent_itemsets:
    k = len(itemset.split())
    freq_counts[k] = freq_counts.get(k, 0) + 1


# Create a bar plot of the number of frequent itemsets
plt.bar(freq_counts.keys(), freq_counts.values())
plt.xlabel('Values of K')
plt.ylabel('Number of Frequent itemset')
plt.title('Number of Frequent Itemsets by Values of K')
plt.show()
