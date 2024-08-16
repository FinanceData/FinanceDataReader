from io import StringIO
from datetime import datetime, timedelta
import time
import json
import requests
import pandas as pd
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class InvestingDailyReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):
        self.symbol = symbol
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end
        self.exchange = exchange
        self.data_source = data_source

    def _get_currid_investing(self, symbol, exchange=None):
        url = f'https://api.investing.com/api/search/v2/search?q={symbol}'
        r = requests.get(url, headers={'user-agent':'Mozilla/5.0', 'domain-id': 'en', 'dnt': '1'})
        # print(r.text)
        jo = r.json()
        # print(json.dumps(jo['quotes'], indent=4))

        if len(jo['quotes']) == 0:
            raise ValueError(f'Symbol "{symbol}" not found')
        df = pd.DataFrame(jo['quotes'])
        df = df.sort_values('id')

        # filter symbol
        df = df.query(f'symbol.str.upper()=="{symbol}".upper()', engine='python')

        # modify exchange by priority
        exchange = 'CBOE' if symbol=='VIX' and not exchange else exchange
        exchange = 'NYMEX' if symbol=='NG' and not exchange else exchange

        # filter exchange
        if exchange:
            exchange = exchange.upper()
            exchange_map = {
                'KRX':'Seoul', 'SZSE': 'Shenzhen', 'SSE':'Shanghai',
                'TSE': 'Tokyo', 'TSX':'Toronto', 'HOSE':'Ho Chi Minh', 'LSE':'London'}
            exchange = exchange_map[exchange] if exchange in exchange_map.keys() else exchange
            df = df.query(f'exchange.str.contains("{exchange}", case=False)', engine='python')

        if len(df) == 0:
            raise ValueError(f"Symbol('{symbol}'), Exchange('{exchange}') not found")
        return df.iloc[0]['id']


    def read(self):
        start, end = self.start, self.end
        curr_id = self._get_currid_investing(self.symbol, self.exchange)
        if not curr_id:
            raise ValueError("Symbol unsupported or not found")

        merged = pd.DataFrame()
        for x in range(100):
            url = 'https://iappapi.investing.com/get_screen.php?' \
                    f'lang_ID=51&skinID=2&interval=day&time_utc_offset=7200&screen_ID=63&' \
                    f'pair_ID={curr_id}&date_from={start.strftime("%d%m%Y")}&date_to={end.strftime("%d%m%Y")}'
            for n in range(5): # retry
                try:
                    r = requests.get(url, headers={ 'X-Meta-Ver': '14', 'User-Agent': 'Mozilla/5.0' }, timeout=3)
                except requests.exceptions.Timeout:
                    # print(f'timeout (retries: {n+1})')
                    time.sleep(2)
                    continue
            try:
                jo = r.json()
            except json.decoder.JSONDecodeError as e:
                print(e); print('-' * 128); print(r.text)

            df = pd.DataFrame(jo['data'][0]['screen_data']['data'])
            if not len(df):
                break
            df['date'] = pd.to_datetime(df['date'], unit='s')
            merged = pd.concat([merged, df]) 
            if df.iloc[-1]['date'] <= start:
                break
            end = df.iloc[-1]['date'] - timedelta(1)

        if len(merged) <= 0:
            return merged # empty
        cols_dict = {'date':'Date', 'price': 'Close', 'open':'Open', 'high':'High', 'low': 'Low', 'vol': 'Volume', 'perc_chg': 'Change'}
        merged = merged.rename(columns=cols_dict)

        merged = merged[['Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Change']]
        merged['Open'] = merged['Open'].str.replace(',', '').astype('float')
        merged['High'] = merged['High'].str.replace(',', '').astype('float')
        merged['Low'] = merged['Low'].str.replace(',', '').astype('float')
        merged['Close'] = merged['Close'].str.replace(',', '').astype('float')
        merged['Volume'] = merged['Volume'].apply(_convert_letter_to_num)
        merged['Change'] = merged['Change'].str.replace(',', '').str.rstrip('%').astype('float') / 100.0
        merged = merged.sort_index()

        merged.set_index('Date', inplace=True)
        merged.sort_index(inplace=True)
        return merged
