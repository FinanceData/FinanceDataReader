import requests
import json
from json.decoder import JSONDecodeError
import pandas as pd

from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

__tqdm_msg = '''
tqdm not installed. please install as follows

pip install tqdm
'''

class NaverStockListing:
    def __init__(self, market):
        self.market = market.upper()
        
    def read(self):
        verbose, raw = 1, False
        # verbose: 0=미표시, 1=진행막대와 진척율 표시, 2=진행상태 최소표시
        # raw: 원본 데이터를 반환
        exchange_map = {
            'NYSE':'NYSE', 
            'NASDAQ':'NASDAQ', 
            'AMEX':'AMEX',
            'SSE':'SHANGHAI',
            'SZSE':'SHENZHEN',
            'HKEX':'HONG_KONG',
            'TSE':'TOKYO',
            'HOSE':'HOCHIMINH', 
        }
        try:
            exchange = exchange_map[self.market]
        except KeyError as e:
            raise ValueError(f'exchange "{self.market}" does not support')

        try:
            from tqdm import tqdm
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(__tqdm_msg)
                
        url = f'http://api.stock.naver.com/stock/exchange/{exchange}/marketValue?page=1&pageSize=60'
        headers={'user-agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers)
            jo = json.loads(r.text)
        except JSONDecodeError as e:
            print(r.text)
            raise Exception(f'{r.status_code} "{r.reason}" Server response delayed. Retry later.')
            
        if verbose == 1:
            t = tqdm(total=jo['totalCount'])

        df_list = []
        for page in range(100): 
            url = f'http://api.stock.naver.com/stock/exchange/{exchange}/marketValue?page={page+1}&pageSize=60'
            try:
                r = requests.get(url, headers=headers)
                jo = json.loads(r.text)
            except JSONDecodeError as e:
                print(r.text)
                raise Exception(f'{r.status_code} "{r.reason}" Server response delayed. Retry later.')

            df = pd.DataFrame(jo['stocks'])
            if not len(df):
                break
            if verbose == 1:
                t.update(len(df))
            elif verbose == 2:
                print('.', end='')
            df_list.append(df)
        if verbose == 1:
            t.close()
            t.clear()
        elif verbose == 2:
            print()
        merged = pd.concat(df_list)
        if raw:
            return merged 
        
        merged['_code'] = merged['industryCodeType'].apply(lambda x: x['code'] if x else '')
        merged['_industryGroupKor'] = merged['industryCodeType'].apply(lambda x: x['industryGroupKor'] if x else '')
        ren_cols = {'symbolCode':'Symbol', 
                    'stockNameEng':'Name', 
                    '_code': 'IndustryCode',
                    '_industryGroupKor':'Industry',
        }
        merged = merged[ren_cols.keys()]
        merged.rename(columns=ren_cols, inplace=True)
        merged.reset_index(drop=True, inplace=True)
        merged.attrs = {'exchange':'KRX', 'source':'NAVER', 'data':'LISTINGS'}
        return merged

class NaverEtfListing:
    def __init__(self, country):
        self.country = country.upper()
        
    def read(self):
        if self.country == "KR": return self.read_kr()
        elif self.country == "US": return self.read_us()
        else: raise ValueError(f'country "{self.country}" does not support')

    def read_kr(self):
        url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        r = requests.get(url)
        df = pd.DataFrame(r.json()['result']['etfItemList'])
        rename_cols = {
            'amonut':'Amount', 'changeRate':'ChangeRate', 'changeVal':'Change', 
            'etfTabCode':'Category', 'itemcode':'Symbol', 'itemname':'Name', 
            'marketSum':'MarCap', 'nav':'NAV', 'nowVal':'Price', 
            'quant':'Volume', 'risefall':'RiseFall', 'threeMonthEarnRate':'EarningRate'
        }
        # 'Symbol', 'Name', 'Price', 'NAV', 'EarningRate', 'Volume', 
        # 'Change', 'ChangeRate', 'Amount', 'MarCap', 'EarningRate'
        df = df.rename(columns=rename_cols)
        df.attrs = {'exchange':'KRX', 'source':'NAVER', 'data':'LISTINGS'}
        return df

    # 해외 ETF 수집 업데이트 건의 #198
    def read_us(self):
        verbose, raw = 1, False
        # verbose: 0=미표시, 1=진행막대와 진척율 표시, 2=진행상태 최소표시
        # raw: 원본 데이터를 반환
        try:
            from tqdm import tqdm
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(__tqdm_msg)
                
        url = f'https://api.stock.naver.com/etf/priceTop?page=1&pageSize=60'
        headers={'user-agent': 'Mozilla/5.0'}
        try:
            r = requests.get(url, headers=headers)
            jo = json.loads(r.text)
        except JSONDecodeError as e:
            print(r.text)
            raise Exception(f'{r.status_code} "{r.reason}" Server response delayed. Retry later.')
            
        if verbose == 1:
            t = tqdm(total=jo['totalCount'])

        df_list = []
        for page in range(100): 
            url = f'https://api.stock.naver.com/etf/priceTop?page={page+1}&pageSize=60'
            try:
                r = requests.get(url, headers=headers)
                jo = json.loads(r.text)
            except JSONDecodeError as e:
                print(r.text)
                raise Exception(f'{r.status_code} "{r.reason}" Server response delayed. Retry later.')

            df = pd.DataFrame(jo['etfs'])
            if not len(df):
                break
            if verbose == 1:
                t.update(len(df))
            elif verbose == 2:
                print('.', end='')
            df_list.append(df)
        if verbose == 1:
            t.close()
            t.clear()
        elif verbose == 2:
            print()
        merged = pd.concat(df_list)
        if raw:
            return merged 
        
        ren_cols = {'symbolCode':'Symbol', 
                    'stockNameEng':'Name', 
        }
        merged = merged[ren_cols.keys()]
        merged.rename(columns=ren_cols, inplace=True)
        merged.reset_index(drop=True, inplace=True)
        merged.attrs = {'exchange':'KRX', 'source':'NAVER', 'data':'LISTINGS'}
        return merged