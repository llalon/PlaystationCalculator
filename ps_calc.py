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
