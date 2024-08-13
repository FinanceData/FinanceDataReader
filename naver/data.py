import re
import requests
import pandas as pd
from io import StringIO
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

def _naver_data_reader(symbol, start, end):
    url = 'https://fchart.stock.naver.com/sise.nhn?timeframe=day&count=6000&requestType=0&symbol='
    r = requests.get(url + symbol)

    data_list = re.findall(r'<item data=\"(.*?)\" />', r.text, re.DOTALL)
    if len(data_list) == 0:
        print(f'"{symbol}" invalid symbol or has no data')
        return pd.DataFrame()
    data = '\n'.join(data_list)
    df = pd.read_csv(StringIO(data), delimiter='|', header=None, dtype={0:str})
    df.columns  = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    df['Change'] = df['Close'].pct_change()
    return df.loc[start:end]

class NaverDailyReader:
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.source, self.code = symbol.split(':') if ':' in symbol else (None, symbol)
        self.start, self.end = _validate_dates(start, end)

    def read(self):
        # single code
        if ',' not in self.code: 
            return _naver_data_reader(self.code, self.start, self.end)
        
        # multiple codes, merge close price data as columns
        code_list = [s.strip() for s in self.code.split(',') if s]
        df_list = []
        for sym in code_list:
            try:
                df = _naver_data_reader(sym, self.start, self.end)
            except Exception as e:
                print(e, f' - "{sym}" not found or invalid periods')
            df_list.append(df.loc[self.start:self.end])
        merged = pd.concat([x['Close'] for x in df_list], axis=1)
        merged.columns = code_list
        merged.attrs = {'exchange':'KRX', 'source':'NAVER', 'data':'PRICE'}
        return merged

