# FinanceDataReader
# 2018-2022 [FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

import re
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

def _map_symbol(symbol, exchange):
    symbol_map = { 
        'KS11': '^KS11', 'KQ11':'^KQ11', 'KS200':'^KS200', # KR indexes
        'DJI':'^DJI', 'IXIC':'^IXIC', 'US500':'^GSPC', 'S&P500':'^GSPC', # Major indexes
        'RUT':'^RUT', 'VIX':'^VIX', 'N225':'^N225', 'SSEC':'000001.SS',
        'FTSE':'^FTSE', 'HSI':'^HSI', 'FCHI':'^FCHI', 'GDAXI':'^GDAXI',
        'US5YT':'^FVX', 'US10YT':'^TNX', 'US30YT':'^TYX', # US Treasury Bonds
    }
    if symbol in symbol_map:
        symbol = symbol_map[symbol]

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
    symbol += '.KS' if not exchange and re.match('^\d{6}$', symbol) else ''
    return symbol

def _yahoo_data_reader(symbol, exchange, start, end):
    start_ts = int(time.mktime(start.timetuple()))
    end_ts = int(time.mktime(end.timetuple()))

    url = (
        f'https://query1.finance.yahoo.com/v7/finance/download/{_map_symbol(symbol, exchange)}?'
        f'period1={start_ts}&period2={end_ts}&interval=1d&events=history'
    )
    try:
        df = pd.read_csv(url, parse_dates=True, index_col='Date')
    except Exception as e:
        print(e, f' - symbol "{symbol}"not found or invalid periods')
        df = pd.DataFrame()
    return df.loc[start:end]

    
class YahooDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None):
        symbol = symbol.upper()
        exchange = exchange.upper() if exchange else ''
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end + timedelta(days=1) if start == end else end
        self.exchange = exchange

    def read(self):
        # single symbol
        if ',' not in self.symbol: 
            return _yahoo_data_reader(self.symbol, self.exchange, self.start, self.end)

        # multiple symbols, merge close price data as columns
        df_list = []
        sym_list = [s.strip() for s in self.symbol.split(',') if s]
        for sym in sym_list:
            df = _yahoo_data_reader(sym, self.exchange, self.start, self.end)
            if len(df):
                df_list.append(df)
        merged = pd.concat([x['Close'] for x in df_list], axis=1)
        merged.columns = sym_list
        return merged
    