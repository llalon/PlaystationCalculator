# -*- coding=utf-8 -*-
#!/usr/bin/env python

import os
import pandas as pd
import numpy as np

import ps_parse, ps_calc, ps_plot


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
    df_summary = ps_calc.run(df)

    # Plot
    ps_plot.plot(df_summary)


if __name__ == "__main__":
    main()
