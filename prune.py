
def pruning(candidateItemSets, frequentItemsets):
    prunedItemSets = []
    frequentItemsetsSet = set(map(tuple, frequentItemsets))
    max_k = len(frequentItemsets[0])
    for k in range(1, max_k + 1): 
        frequentItemsetsK = [itemset for itemset in frequentItemsets if len(itemset) == k]
        prunedItemsetsK = []
        for candidate in candidateItemSets:
            for item in candidate:
                subset = tuple(sorted(set(candidate) - {item}))
                if subset not in frequentItemsetsSet:
                    break
            else:
                prunedItemsetsK.append(candidate)
        prunedItemSets.extend(prunedItemsetsK)
    return prunedItemSets


