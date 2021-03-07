import pandas as pd
import numpy as np

# https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


# Returns a list of price combinations
def find_combos(levels=[1, 2, 3, 4], target=5):

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


def run(df):

    # Drop NA
    df = df.dropna()

    # Add PS levels as column
    df["levels"] = df.apply(lambda x: int(x["item"].split(" ")[1]), axis=1)

    # Find average price per level with outliers removed.
    levels = df.levels.unique()
    avg_price = []
    for l in levels:
        dfl = df.loc[df["levels"] == l]
        prices = dfl["price"].to_numpy()
        avg = np.mean(reject_outliers(prices))
        avg_price.append(avg)

    # Calculate best price combinations
    combo_prices = []
    combos = find_combos()
    for c in combos:
        p = 0
        for i in c:
            p = p + avg_price[i - 1]

        combo_prices.append(p)

    df_summary = pd.DataFrame({"combo": combos, "price": combo_prices})
    print(df_summary)