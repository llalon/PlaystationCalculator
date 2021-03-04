# -*- coding=utf-8 -*-
#!/usr/bin/env python

import pandas as pd

def search_item(name, pages):
    ''' Search ebay for name, across the number of pages pages
    '''

    url = "https://www.ebay.com/sch/i.html?_from=R40&amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;amp;_nkw="
    name = name.replace(" ", "+")

    for p in range(1, pages):
        url = url + name + "_sacat=0_pgn=" + str(p)

def main():

    # Search top 10 pages of E-Bay for 'iphone 8' and return the prices as data frame
    item_1 = search_item("iphone 8", 10)

if __name__ == "__main__":
    main()
