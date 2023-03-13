

def pruning(candidateitemsets, frequentitemsets, k):
    pruneditemsets = []
    frequentitemsetsset = set(map(tuple, frequentitemsets))  
    for candidate in candidateitemsets:
        for item in candidate:
            subset = [x for x in candidate if x != item]
            if tuple(subset) not in frequentitemsetsset: 
                break
        else:
            pruneditemsets.append(candidate)
    return pruneditemsets


candidateitemsets = [{'A', 'B', 'C'}, {'A', 'B', 'D'}, {'B', 'C', 'D'}, {'A', 'C', 'D'}, {'A', 'B', 'E'}, {'A', 'C', 'E'}, {'B', 'C', 'E'}, {'C', 'D', 'E'}]
frequentitemsets = [{'A', 'B'}, {'A', 'C'}, {'B', 'C'}, {'C', 'D'}, {'B', 'D'}, {'A', 'D'}, {'C', 'E'}, {'B', 'E'}, {'A', 'E'}]
k = 3
pruneditemsets = pruning(candidateitemsets, frequentitemsets, k)

# Print pruned itemsets
print("Pruned itemsets:", pruneditemsets)