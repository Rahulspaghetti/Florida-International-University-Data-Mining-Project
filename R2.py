def candidateItemsetGeneration(itemsets):
    res = []
    for setA in itemsets:
        for setB in itemsets:
            setSubsetA = setA[0:-1]
            setSubsetB = setB[0:-1]
            if setSubsetA == setSubsetB and not setA == setB:
                arr = setSubsetA
                arr.append(setA[-1])
                arr.append(setB[-1])
                arr = sorted(arr)
                if not res.__contains__(arr):
                    res.append(arr)
    res = sorted(res)
    return res
