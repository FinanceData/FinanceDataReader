import requests
import pandas as pd
import json
from io import StringIO
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class InvestingDailyReader:
    def __init__(self, symbols, start=None, end=None, country=None):
        self.symbols = symbols
        start, end = _validate_dates(start, end)
        self.start = start
        self.end = end
        self.country = country

    def _get_currid_investing(self, symbol, country):
        predef_table = { # for exceptional case
            'HSI': '179', # Hang Seng (HSI)
        }
        if symbol in predef_table.keys():
            return predef_table[symbol]
        
        country_map = {'KR':'11', 'US':'5', 'CN':'37', 'HK':'39', 'JP':'35'}
        if country:
            country_id = country_map[country.upper()] if country in country_map.keys() else '0'
        else:
            country_id = '11' if symbol.isnumeric() else '0'

        url = 'https://kr.investing.com/search/service/search'
        headers = {
            'User-Agent':'Mozilla',
            'X-Requested-With':'XMLHttpRequest',
        }

        data = {
            'search_text': symbol,
            'term': symbol,
            'country_id': country_id,
            'tab_id': 'All',
        }
        r = requests.post(url, data=data, headers=headers)
        jo = json.loads(r.text)
        for row in jo['All']:
            if row['symbol'] == symbol.upper():
                return row['pair_ID']
        return None

    def read(self):
        start_date_str = self.start.strftime('%m/%d/%Y')
        end_date_str = self.end.strftime('%m/%d/%Y')
        curr_id = self._get_currid_investing(self.symbols, self.country)
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