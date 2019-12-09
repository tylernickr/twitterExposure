import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import numpy as np
from time import sleep
from random import shuffle

API_KEY = 'L5WZMGM1SOA1PFUC'

STOCK_DIR = './stock_data/'

if __name__ == '__main__':

    if not os.path.exists(STOCK_DIR):
        os.mkdir(STOCK_DIR)

    tickers = [
        'MMM',
        'AXP',
        'AAPL',
        'BA',
        'CAT',
        'CVX',
        'CSCO',
        'KO',
        'DWDP'
        'XOM',
        'GS',
        'HD',
        'IBM',
        'INTC',
        'JNJ',
        'JPM',
        'MCD',
        'MRK',
        'MSFT',
        'NKE',
        'PFE',
        'PG',
        'TRV',
        'UNH',
        'UTX',
        'VZ',
        'V',
        'WMT',
        'WBA',
        'DIS'
    ]

    for stock in tickers:
        print(stock)
        sleep(15)

        # Your key here
        key = 'L5WZMGM1SOA1PFUC'
        # Chose your output format, or default to JSON (python dict)
        ts = TimeSeries(key, output_format='pandas')
        ti = TechIndicators(key)

        try:
            stock_data, stock_meta_data = ts.get_daily(symbol=stock, outputsize='full')
        except:
            continue

        stock_data.reset_index(level=0, inplace=True)

        results = []
        values = np.flip(stock_data.values, 0)
        for i in range(0, len(values) - 1):
            point1 = values[i]
            point2 = values[i+1]
            price_delta = round((point2[4] - point1[4]) / point1[4], 6)
            movement_marker = 0
            if price_delta > .03:
                movement_marker = 1
            results.append([str(point2[0]), str(point2[4]), '{:.6}'.format(price_delta), str(movement_marker)])
        with open(STOCK_DIR + stock + '.dat', 'w') as stock_file:
            for item in results:
                print('|'.join(item), file=stock_file)