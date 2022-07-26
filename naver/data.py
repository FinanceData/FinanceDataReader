import re
import requests
import pandas as pd
from io import StringIO
from FinanceDataReader._utils import (
    _filter_by_date, _replace_ohl_0_with_c, _validate_dates)


class NaverDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end

    def read(self):
        url = 'https://fchart.stock.naver.com/sise.nhn?timeframe=day&count=6000&requestType=0&symbol='
        r = requests.get(url + self.symbol)

        data_list = re.findall('<item data=\"(.*?)\" />', r.text, re.DOTALL)
        if len(data_list) == 0:
            return pd.DataFrame()
        data = '\n'.join(data_list)
        df = pd.read_csv(StringIO(data), delimiter='|',
                         header=None, dtype={0: str})
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        df['Change'] = df['Close'].pct_change()

        df = _filter_by_date(df, self.start, self.end)

        df = _replace_ohl_0_with_c(df)

        return df
