# -*- coding=utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import numpy as np

import ps_parse, ps_calc


def main():

    FILE_NAME = "ps_prices.csv"

    force_refresh = False

    # Check if price data is present
    if not os.path.exists(FILE_NAME) or force_refresh:
        print("WARNING: PS price data not found. Building index...")
        df = ps_parse.build_price_df(FILE_NAME)
    else:
        print("Loading data from disk...")
        df = pd.read_csv(FILE_NAME)

    # Run analysis
    ps_calc.run(df)


if __name__ == "__main__":
    main()
