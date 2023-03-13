

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


