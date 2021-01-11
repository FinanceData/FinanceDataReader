from io import StringIO
import json
import requests
import pandas as pd
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

try:
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

class InvestingDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end
        self.exchange = exchange
        self.data_source = data_source

    def _get_currid_investing(self, symbol, exchange=None, data_source=None):
        symbol = symbol.upper()

        url = 'https://kr.investing.com/search/service/searchTopBar'
        headers = {
            'User-Agent':'Mozilla',
            'X-Requested-With':'XMLHttpRequest',
        }
        r = requests.post(url, data={'search_text': symbol}, headers=headers)
        jo = json.loads(r.text)
        if len(jo['quotes']) == 0:
            raise ValueError(f"Symbol('{symbol}') not found")
        df = json_normalize(jo['quotes'])
        df['symbol'] = df['symbol'].str.upper()

        # filter symbol
        df = df.query(f'symbol=="{symbol}"', engine='python')

        # filter exchange
        if exchange:
            exchange_map = {
                'KRX':'서울', '한국거래소':'서울',
                'NYSE':'뉴욕', '뉴욕증권거래소':'뉴욕', 
                'NASDAQ':'나스닥',
                'AMEX': '뉴욕', 
                'SSE':'상하이', '상해':'상하이',
                'SZSE':'심천',
                'HKEX':'홍콩',
                'TSE':'도쿄',
                'HOSE':'Ho Chi Minh',
            }
            exchange = exchange_map[exchange] if exchange in exchange_map.keys() else exchange
            df = df.query(f'exchange.str.contains("{exchange}", case=False)', engine='python')

        if len(df) == 0:
            raise ValueError(f"Symbol('{symbol}'), Exchange('{exchange}') not found")
        return df.iloc[0]['pairId']

    def read(self):
        start_date_str = self.start.strftime('%m/%d/%Y')
        end_date_str = self.end.strftime('%m/%d/%Y')
        curr_id = self._get_currid_investing(self.symbol, self.exchange, self.data_source)
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
        exp_syms = ['US500', 'RUTNU', 'VIX', ] # exceptial symbols (vol == 0)
        if 'Volume' in df.columns and self.symbol not in exp_syms:
            df = df[df['Volume'] > 0]
        return df
