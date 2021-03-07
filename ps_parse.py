# -*- coding=utf-8 -*-
#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

import os

import pandas as pd
import numpy as np


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


def build_price_df(
    file_name="ps_prices.csv", levels=[1, 2, 3, 4], save_to_file=True, rm_na=False
):
    # Find average prices of each level of playstation

    df = pd.DataFrame()

    for l in levels:
        s = "Playstation " + str(l)
        df = df.append(parse(str(s)))

    if save_to_file:
        df.to_csv(file_name, index=False)
    if rm_na:
        df = df.dropna()

    return df
