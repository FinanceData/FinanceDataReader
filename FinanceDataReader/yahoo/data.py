# FinanceDataReader
# 2018-2022 [FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

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
        f'https://query1.finance.yahoo.com/v7/finance/download/{_map_symbol(symbol, exchange)}?'
        f'period1={start_ts}&period2={end_ts}&interval=1d&events=history&includeAdjustedClose=true'
    )
    try:
        df = pd.read_csv(url, parse_dates=True, index_col='Date')
    except Exception as e:
        print(e, f' - symbol "{symbol}" not found or invalid periods')
        df = pd.DataFrame()

    return df.loc[start:end]

    
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
    