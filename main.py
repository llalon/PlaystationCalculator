# -*- coding=utf-8 -*-
#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

import os

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


def parse(item):
    # Adapted from https://www.blog.datahut.co/post/scraping-ebay

    items = []
    prices = []

    url = "https://www.ebay.com/sch/i.html?_nkw={0}&_sacat=0".format(
        item.replace(" ", "+")
    )
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")

    listings = soup.find_all("li", attrs={"class": "s-item"})

    for l in listings:
        item_name = " "
        item_price = " "

        for n in l.find_all("h3", attrs={"class": "s-item__title"}):
            # Find item names
            if str(n.find(text=True, recursive=False)) != "None":
                item_name = str(n.find(text=True, recursive=False))
                items.append(item_name)

            # Find item price
            if item_name != " ":
                item_price = l.find("span", attrs={"class": "s-item__price"})
                item_price = str(item_price.find(text=True, recursive=False))
                item_price = item_price.replace("$", "")

                try:
                    item_price = float(item_price)
                except:
                    # print("ERROR: parsing price")
                    item_price = np.nan

                prices.append(item_price)

    # Put into df
    df = pd.DataFrame({"name": items, "price": prices, "item": item})

    return df


def build_price_df(file_name="ps_prices.csv"):

    # Find average prices of each level of playstation
    playstations = [1, 2, 3, 4]

    df_playstations = pd.DataFrame()

    for p in playstations:
        s = "Playstation " + str(p)
        df = parse(str(s))
        df_playstations = df_playstations.append(df)

    # Save to file
    df_playstations.to_csv(file_name)
    return df_playstations


def main():

    FILE_NAME = "ps_prices.csv"

    # Check if price data is present
    if not os.path.exists(FILE_NAME):
        print("WARNING: PS price data not found. Building index...")
        df = build_price_df(FILE_NAME)
    else:
        # Import price data
        df = pd.read_csv("ps_prices.csv")

    df = df.dropna()


if __name__ == "__main__":
    main()
