# FinanceDataReader
# 2018-2024 [FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

import requests
import pandas as pd
import time
from datetime import timedelta
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

def _map_symbol(symbol, exchange):

    curr_list = ['KRW', 'EUR', 'CNY', 'JPY', 'CHF']
    coin_list = ['BTC', 'ETH', 'USDT', 'BNB', 'USDC', 'XRP', 'BUSD', 'ADA', 'SOL', 'DOGE']

    if symbol.startswith('USD/'):
        symbol = symbol.split('USD/')[1] + '=X'            
    elif any(map(symbol.startswith, [f'{curr}/' for curr in curr_list])):
        symbol = symbol.replace('/', '') + '=X'          
    elif any(map(symbol.startswith, [f'{coin}/' for coin in coin_list])):
        symbol = symbol.replace('/', '-')

    symbol += '.T' if exchange=='TSE' else ''
    symbol += '.SZ' if exchange=='SZSE' else ''
    symbol += '.SS' if exchange=='SSE' else ''
    symbol += '.HK' if exchange=='HKEX' else ''
    symbol += '.VN' if exchange=='HOSE' else ''
    return symbol

def _yahoo_data_reader(symbol, exchange, start, end):
    start_ts = int(time.mktime(start.timetuple()))
    end_ts = int(time.mktime(end.timetuple()))

    url = (
        f'https://query2.finance.yahoo.com/v8/finance/chart/{_map_symbol(symbol, exchange)}?'
        f'period1={start_ts}&period2={end_ts}&interval=1d&includeAdjustedClose=true'
    )
    r = requests.get(url, headers={'user-agent': 'Mozilla/5.0 AppleWebKit/537.36'})
    r.raise_for_status()
    jo = r.json()

    index = pd.to_datetime(jo['chart']['result'][0]['timestamp'], unit='s').normalize()
    values  = {**jo['chart']['result'][0]['indicators']['quote'][0], **jo['chart']['result'][0]['indicators']['adjclose'][0]}

    col_map = {'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume':'Volume', 'adjclose':'Adj Close'}
    df = pd.DataFrame(data=values, index=index)
    df = df.rename(columns=col_map) # columns rename
    df = df[col_map.values()] # columns reorder
    return df
    
class YahooDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None):
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end + timedelta(days=1) if start == end else end
        self.symbol = symbol.upper()
        self.exchange = exchange.upper() if exchange else ''

    def read(self):
        # single symbol
        if ',' not in self.symbol: 
            return _yahoo_data_reader(self.symbol, self.exchange, self.start, self.end)

        # multiple symbols, merge close price data as columns
        df_list = []
        sym_list = [s.strip() for s in self.symbol.split(',') if s]
        for sym in sym_list:
            df = _yahoo_data_reader(sym, self.exchange, self.start, self.end)
            df = df[['Adj Close']]
            df = df.rename(columns={'Adj Close':sym})
            df_list.append(df)
        merged = pd.concat(df_list, axis=1)
        merged.attrs = {'exchange':self.exchange, 'source':'YAHOO', 'data':'PRICE'}
        return merged
    