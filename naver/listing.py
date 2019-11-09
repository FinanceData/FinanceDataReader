import requests
import json
from pandas.io.json import json_normalize

from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

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
        return df[['Symbol', 'Name']]
