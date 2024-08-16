# KRX data reader for FinanceDataReader  
# 2024 FinacneData.KR

import requests
import pandas as pd
import json
from datetime import datetime

try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

def _ecos_stat(stat_search_ds_list, start, end, freq='D'):
    '''ECOS에서 데이터를 가져와 데이터프레임으로 반환합니다

    codes (str, list): 통계항목과 계정항목을 '통계항목/계정항목' 형식으로 지정합니다. 리스트(혹은 튜플로 여러 통계항목을 지정할 수 있습니다)
    start (datetime or str): 시작일
    end (datetime or str): 종료일
    freq (str): 데이터의 단위(주기))
    '''
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    fmt = "%Y%m" if freq.upper() == 'M' else "%Y%m%d"

    payload = {
        "header": {
            "guidSeq": 1,
            "trxCd": "OSUUA02R01", "scrId": "IECOSPCM02", "sysCd": "03", "fstChnCd": "WEB",
            "langDvsnCd": "KO", "envDvsnCd": "D",
            "sndRspnDvsnCd": "S", "sndDtm": "20400114",
            "ipAddr": "124.40.40.5", "usrId": "IECOSPC",
            "pageNum": 1,
            "pageCnt": 10000 # 충분히 크게
        },
        "data": {
            "statSrchDsList": stat_search_ds_list,
            "statSrchFreqList": [
                {
                    "freq": freq,
                    "vlidStDtm": start.strftime(fmt), # 시작날짜
                    "vlidEndDtm": end.strftime(fmt), # 끝날짜
                }
            ],
            "statTyp": "M",
            "statDataCvsnCdList": [
                "00"
            ],
            "viewType": "01",
            "holidayYn": "Y"
        }
    }
    # print(payload)

    res = requests.post('https://ecos.bok.or.kr/serviceEndpoint/httpService/request.json', json.dumps(payload))
    jo = res.json()
    if jo['message']['msgRepNum']: # 에러 메시지가 있는 경우
        print(jo['message']['detailMsgs'])
        return pd.DataFrame()

    jo_list = json.loads(jo['data']['jsonCtnt'])
    df = pd.json_normalize(jo_list).T

    # 컬럼명 지정
    df.columns = df.loc['항목명1'].values

    # 불필요한 row 삭제
    remove_indexes = ['통계표', 'StatisticalTable', 
                      '코드(항목명1)', 'Code(ItemNames1)', '항목명1', 'ItemNames1', 
                      '코드(항목명2)', 'Code(ItemNames2)', '항목명2', 'ItemNames2', 
                      '코드(항목명3)', 'Code(ItemNames3)', '항목명3', 'ItemNames3', 
                      '단위', 'Unit', '가중치', 'Wgt', '변환', 'Conversion', 'digit']
    df = df.drop(remove_indexes, errors='ignore')

    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)

    # 인덱스를 (object에서) DateTimeIndex 로 변환
    fmt = "%Y%m" if freq.upper() == 'M' else None
    df.index = pd.to_datetime(df.index, format=fmt)
    df = df.sort_index()

    # 컬럼은 모두 (object에서) 수치값으로 변환
    cols = df.columns
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    return df

def _ecos_keystat(keys, start, end, freq=None):
    '''100대 통계지표 목록의 키를 사용하여 ECOS데이터를 가져옵니다
    '''
    base_freq_map = {
        'K051': 'D', 'K052': 'D', 'K063': 'D', 'K053': 'D', 'K055': 'D', 'K056': 'D', 'K062': 'D', 'K057': 'D', 'K058': 'M', 'K059': 'M',
        'K005': 'M', 'K006': 'M', 'K007': 'Q', 'K008': 'M', 'K002': 'M', 'K003': 'M', 'K004': 'M', 'K011': 'M', 'K152': 'D', 'K153': 'D',
        'K154': 'D', 'K156': 'D', 'K101': 'D', 'K102': 'D', 'K103': 'M', 'K107': 'M', 'K104': 'M', 'K108': 'M', 'K258': 'Q', 'K259': 'Q',
        'K260': 'Q', 'K261': 'Q', 'K462': 'Q', 'K257': 'Q', 'K263': 'A', 'K264': 'Q', 'K265': 'Q', 'K266': 'A', 'K220': 'M', 'K201': 'M',
        'K202': 'M', 'K203': 'M', 'K204': 'M', 'K205': 'M', 'K207': 'M', 'K206': 'M', 'K210': 'M', 'K453': 'M', 'K212': 'M', 'K215': 'M',
        'K213': 'M', 'K216': 'M', 'K218': 'M', 'K217': 'M', 'K219': 'M', 'K253': 'M', 'K254': 'M', 'K252': 'M', 'K268': 'M', 'K269': 'M',
        'K267': 'A', 'K256': 'A', 'K255': 'A', 'K306': 'Q', 'K463': 'Q', 'K456': 'A', 'K464': 'A', 'K303': 'M', 'K304': 'M', 'K301': 'M',
        'K302': 'M', 'K307': 'Q', 'K305': 'Q', 'K308': 'Q', 'K451': 'A', 'K460': 'A', 'K461': 'A', 'K351': 'M', 'K356': 'M', 'K357': 'M',
        'K465': 'M', 'K466': 'M', 'K358': 'M', 'K359': 'M', 'K360': 'M', 'K467': 'M', 'K155': 'M', 'K353': 'Q', 'K468': 'Q', 'K401': 'M',
        'K405': 'M', 'K406': 'M', 'K402': 'M', 'K403': 'M', 'K404': 'M', 'K407': 'M', 'K408': 'M', 'K409': 'M', 'KN11': 'M', 'K469': 'M'}

    key_list = [keys] if type(keys) == str else keys
    base_freq = freq if freq else base_freq_map[key_list[0]]

    stat_search_ds_list = []
    for key in key_list:
        if key not in base_freq_map:
            raise ValueError(f'invalid key: {key}')

        payload = {
            "header":{
                "guidSeq":1,"trxCd":"OSUSC04R01","scrId":"IECOSPCM04","sysCd":"03",
                "fstChnCd":"WEB","langDvsnCd":"KO","envDvsnCd":"D","sndRspnDvsnCd":"S",
                "sndDtm":"20220822","ipAddr":"124.50.40.5","usrId":"IECOSPC","pageNum":1,"pageCnt":1000
            },
            "data":{"key100statId":key}
        }
        res = requests.post('https://ecos.bok.or.kr/serviceEndpoint/httpService/request.json', json.dumps(payload))
        jo = res.json()

        stat_search_ds = {
            'dsId': jo['data']['dsId'],
            'dsItmId1': jo['data']['dsItmId1'],
            'dsItmId2': jo['data']['dsItmId2'],
            'dsItmId3': jo['data']['dsItmId3'],
            'dsItmVal1': jo['data']['dsItmVal1'],
            'dsItmVal2': jo['data']['dsItmVal2'],
            'dsItmVal3': jo['data']['dsItmVal3'],
        }
        if key in ['K258', 'K259', 'K260', 'K261', 'K462', 'K264', 'K265']:
            stat_search_ds = {
                'dsId': jo['data']['dsId'],
                'dsItmId1': jo['data']['dsItmId1'],
                'dsItmVal1': jo['data']['dsItmVal1'],
            }
        stat_search_ds_list.append(stat_search_ds)
    return _ecos_stat(stat_search_ds_list, start, end, base_freq)

class EcosDataReader: 
    def __init__(self, symbol, start=None, end=None):
        '''ex) ECOS:722Y001/0101000 (한국은행 기준금리)'''
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime.today() if end==None else pd.to_datetime(end)

    def read(self):
        df = _ecos_stat(self.symbol, self.start, self.end, freq='D')
        df.attrs = {'exchange':'ECOS', 'source':'ECOS', 'data':'SERIES'}
        return df

class EcosKeyStatDataReader: 
    def __init__(self, symbol, start=None, end=None):
        '''ex) # ECOS-KEYSTAT:K051'''
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime.today() if end==None else pd.to_datetime(end)

    def read(self):
        df = _ecos_keystat(self.symbol, self.start, self.end)
        df.attrs = {'exchange':'ECOS', 'source':'ECOS', 'data':'SERIES'}
        return df
