# -*- coding=utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import numpy as np

import ps_parse, ps_calc


def main():

    FILE_NAME = "ps_prices.csv"

    # Check if price data is present
    if not os.path.exists(FILE_NAME):
        print("WARNING: PS price data not found. Building index...")
        df = ps_parse.build_price_df(FILE_NAME)
    else:
        # Import price data
        df = pd.read_csv("ps_prices.csv")


if __name__ == "__main__":
    main()
