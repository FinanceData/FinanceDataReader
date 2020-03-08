from io import StringIO
import json
import requests
import pandas as pd
from pandas.io.json import json_normalize
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class InvestingDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, kind=None):
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end
        self.exchange = exchange
        self.kind = kind

    def _get_currid_investing(self, symbol, exchange=None, kind=None):
        symbol = symbol.upper() if symbol else symbol
        symbol = symbol.replace('^', '_p') # issues/29
        exchange = exchange.upper() if exchange else exchange

        # higher priority to KRX if exchange is None and symbol is digit
        exchange = 'KRX' if exchange == None and symbol.isdigit() else exchange

        url = 'https://www.investing.com/search/service/searchTopBar'
        headers = {
            'User-Agent':'Mozilla',
            'X-Requested-With':'XMLHttpRequest',
        }
        
        # Exchage alias
        exchange_map = {
            'KRX':'Seoul', '한국거래소':'Seoul',
            'NASDAQ':'NASDAQ', '나스닥':'NASDAQ',
            'NYSE':'NYSE', '뉴욕증권거래소':'NYSE', 
            'AMEX':'AMEX', '미국증권거래소':'AMEX', 
            'SSE':'Shanghai', '상해':'Shanghai', '상하이':'Shanghai',
            'SZSE':'Shenzhen', '심천':'Shenzhen',
            'HKEX':'Hong Kong', '홍콩':'Hong Kong',
            'TSE':'Tokyo', '도쿄':'Tokyo',
        }
        exchange = exchange_map[exchange] if exchange and exchange in exchange_map.keys() else exchange

        symbol_map = {
            'HSI': {'symbol': 'HK50', 'kind':'index'}
        }
        if symbol in symbol_map:
            dic = symbol_map[symbol]
            symbol = dic['symbol'] if 'symbol' in dic else symbol
            exchange = dic['exchange'] if 'exchange' in dic else exchange
            kind = dic['kind'] if 'kind' in dic else kind

        data = {'search_text': symbol}
        r = requests.post(url, data, headers=headers)
        jo = json.loads(r.text)
        if len(jo['quotes']) == 0:
            raise ValueError("Symbol('%s'), Exchange('%s'), kind('%s') not found" % (symbol, exchange, kind))
        df = json_normalize(jo['quotes'])
        df = df[df['symbol'].str.lower() == symbol.lower()] ## issues/31
        df = df[df['exchange'].str.contains(exchange, case=False)] if exchange else df
        df = df[df['type'].str.contains('^' + kind + ' - ', case=False)] if kind else df

        if len(df) == 0:
            raise ValueError("Symbol('%s'), Exchange('%s'), kind('%s') not found" % (symbol, exchange, kind))
        return df.iloc[0]['pairId']

    def read(self):
        start_date_str = self.start.strftime('%m/%d/%Y')
        end_date_str = self.end.strftime('%m/%d/%Y')
        curr_id = self._get_currid_investing(self.symbol, self.exchange, self.kind)
        if not curr_id:
            raise ValueError("Symbol unsupported or not found")

        url = 'https://www.investing.com/instruments/HistoricalDataAjax'
        data = {    
            'curr_id':curr_id,
            'st_date': start_date_str,
            'end_date': end_date_str,
            'interval_sec':'Daily',
            'sort_col':'date',
            'sort_ord':'ASC',
            'action':'historical_data',
        }

        headers = {
            'User-Agent':'Mozilla',
            'X-Requested-With':'XMLHttpRequest',
        }

        r = requests.post(url, data, headers=headers)
        dfs = pd.read_html(StringIO(r.text))
        df = dfs[0]
        if (len(df)==0) or ("No results found" == df.iloc[0]['Date']):
            return pd.DataFrame()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        cols_dict = {'Price':'Close', 'Vol.':'Volume', 'Change %':'Change'}
        df = df.rename(columns=cols_dict)
        df['Change'] = df['Change'].str.replace(',', '')
        df['Change'] = df['Change'].str.rstrip('%').astype('float') / 100.0
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].apply(_convert_letter_to_num)
        df = df.sort_index()
        return df
