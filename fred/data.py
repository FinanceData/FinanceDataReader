import pandas as pd
import numpy as np
import requests
from datetime import datetime
import re
from io import BytesIO
import zipfile
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class FredReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end
        self.data_source = data_source

    def read(self):
        if type(self.symbol)==list:
            start_str = ','.join([self.start.strftime("%Y-%m-%d")] * len(self.symbol))
            end_str = ','.join([self.end.strftime("%Y-%m-%d")] * len(self.symbol))
            sym = ','.join(self.symbol)
        else:
            start_str = self.start.strftime("%Y-%m-%d")
            end_str = self.end.strftime("%Y-%m-%d")
            sym = self.symbol

        url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sym}&cosd={start_str}&coed={end_str}'
        r = requests.get(url)
        fname = re.findall('filename="(.+)"', r.headers['content-disposition'])[0]
        if fname=='fredgraph.zip':
            df_list = []
            with zipfile.ZipFile(BytesIO(r.content)) as zf:
                for zfn in zf.namelist():
                    df = pd.read_csv(zf.open(zfn), parse_dates=['DATE'], na_values='.')
                    df.set_index('DATE', inplace=True)
                    df.replace('.', '', inplace=True)
                    df_list.append(df)
            merged = pd.concat(df_list, axis=1)
            merged.fillna(method='ffill', inplace=True)
            return merged

        elif '.csv' in fname:
            df = pd.read_csv(url, parse_dates=['DATE'], na_values='.')
            df.set_index('DATE', inplace=True)
            df.replace('.', '', inplace=True)
            df.fillna(method='ffill', inplace=True)
            return df
