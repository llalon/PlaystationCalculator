# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np

# Function to remove price outliers
# https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


# Returns a list of price combinations
def find_combns(levels=[1, 2, 3, 4], target=5):

    combn = []

    # Find all the combinations
    # Adapted from: https://stackoverflow.com/questions/34517540/find-all-combinations-of-a-list-of-numbers-with-a-given-sum
    def subset_sum(numbers, target, partial=[]):
        s = sum(partial)

        # check if the partial sum is equals to target
        if s == target:
            combn.append(partial)
        if s >= target:
            return  # if we reach the number why bother to continue

        for i in range(len(numbers)):
            n = numbers[i]
            subset_sum(numbers, target, partial + [n])

    subset_sum(levels, target)

    return combn


# Import price data
df = pd.read_csv("ps_prices.csv")
df = df.dropna()

# Add PS levels as column
df["levels"] = df.apply(lambda x: int(x["item"].split(" ")[1]), axis=1)

# Find average price per level
levels = df.levels.unique()
avgs = []
for l in levels:
    # Get the average price of each PS1 with outliers removed
    dfl = df.loc[df["levels"] == l]
    prices = dfl["price"].to_numpy()
    avg = np.mean(reject_outliers(prices))
    avgs.append(avg)

# Function to find the lowest price for combinations of levels that add to the target
prices_summary = []
for c in find_combns():
    p = 0
    for i in c:
        p = p + avgs[i - 1]

    prices_summary.append({"combn": c, "price": p})

# Calculate the best way to buy a PS5
print("The cheapest PS5 is...")
print(prices_summary)
