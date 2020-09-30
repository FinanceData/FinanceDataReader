import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

try:
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

__tqdm_msg = '''
tqdm not installed. please install as follows

시간이 오래 걸리는 작업을 진행을 표시하기 위해 tqdm 에 의존성이 있습니다.
다음과 같이 tqdm를 설치하세요

C:\> pip insatll tqdm
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

            df = json_normalize(jo['stocks'])
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
                    'industryCodeType.industryGroupKor':'Industry', 
                    'industryCodeType.code': 'IndustryCode'}
        merged = merged[ren_cols.keys()]
        merged.rename(columns=ren_cols, inplace=True)
        merged.reset_index(drop=True, inplace=True)
        return merged

class NaverEtfListing:
    def __init__(self):
        pass
        
    def read(self):
        url = 'https://finance.naver.com/api/sise/etfItemList.nhn'
        df = json_normalize(json.loads(requests.get(url).text), ['result', 'etfItemList'])
        rename_cols = {
            'amonut':'Amount', 'changeRate':'ChangeRate', 'changeVal':'Change', 
            'etfTabCode':'Category', 'itemcode':'Symbol', 'itemname':'Name', 
            'marketSum':'MarCap', 'nav':'NAV', 'nowVal':'Price', 
            'quant':'Volume', 'risefall':'RiseFall', 'threeMonthEarnRate':'EarningRate'
        }
        df.rename(columns=rename_cols, inplace=True)
        # 'Symbol', 'Name', 'Price', 'NAV', 'EarningRate', 'Volume', 
        # 'Change', 'ChangeRate', 'Amount', 'MarCap', 'EarningRate'
        df = df[['Symbol', 'Name']]
        return df
