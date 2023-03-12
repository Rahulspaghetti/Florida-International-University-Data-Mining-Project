
def pruning(CandidateItemset, previtemsets, length):
    prunedSet = []
    for candidate in CandidateItemset:
        subsets = [candidate[:i] + candidate[ i +1:] for i in range(length)]
        if all(subset in previtemsets for subset in subsets):
            prunedSet.append(candidate)
    return prunedSet

# canidateitemsets are the results from r2, previtems are all frequent itemsets, length is k-1
