import pandas as pd 
import numpy as np


def pruning(candidate_itemsets, frequent_itemsets, k):
    pruned_itemsets = []
    frequent_itemsets_set = set(frequent_itemsets)
    for candidate in candidate_itemsets:
        for item in candidate:
            subset = [x for x in candidate if x != item]
            if subset not in frequent_itemsets_set:
                break
        else:
            pruned_itemsets.append(candidate)
    return pruned_itemsets