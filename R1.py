import pandas as pd
from datetime import datetime

start_time = datetime.now()

# load the file
data = pd.read_csv('small.txt', sep=" ", names=['ID', 'ITEMSETS'])
# modifying the structure of the second column to the requirements for later
data['ITEMSETS'] = 'item' + data['ITEMSETS'].astype(str)
dt = data.groupby('ID')['ITEMSETS'].apply(list)

# Initialize an empty dictionary to keep track of the counts
count_dict = {}

# Loop over each list in the main list and count the occurrences of each item
for lst in dt:
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

# Sort the dictionary by value in descending order
sorted_dict = {k: v for k, v in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}

sdict = pd.DataFrame(sorted_dict.items(), columns=('ITEMSETS', 'SUPPORT_COUNT'))

minsup = int(input('Please enter the minimum support count?\n'))

# Create a dataframe of all frequent 1 itemset
F_1itemsets = sdict[sdict['SUPPORT_COUNT'] >= minsup]
print(F_1itemsets)
