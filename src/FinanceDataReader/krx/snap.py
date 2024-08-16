# KRX scaper for FinanceDataReader  
# 2023 FinacneData.KR

import requests
import pandas as pd

_krx_headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
               'Referer': 'http://data.krx.co.kr/', }

def _krx_last_working_day(date=None):
    '''지정한 날짜에서 가장 가까운 영업일
    * date: 날짜 (지정하지 않으면 오늘 포함 가장 가까운 영업일)
    '''
    date = pd.to_datetime(date) if date else pd.Timestamp.today()
    date_str = date.strftime('%Y%m%d')
    url = (
         'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?'
        f'baseName=krx.mdc.i18n.component&key=B161.bld&inDate={date_str}'
    )
    r = requests.get(url, headers=_krx_headers)
    if '서비스 에러' in r.text:
        print('Servie Error')

    j = r.json()
    return pd.to_datetime(j['result']['output'][0]['bis_work_dt']).to_pydatetime()

def _krx_index_codes():
    '''
    [11006] 지수목록 조회
    '''
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    form_data = {
        'locale': 'ko_KR',
        'mktsel': '1',
        'searchText':'',
        'bld': 'dbms/comm/finder/finder_equidx',
    }
    r = requests.post(url, form_data, headers=_krx_headers)
    j = r.json()
    krx_index = pd.DataFrame(j['block1'])
    krx_index = krx_index.sort_values(['full_code','short_code'])
    krx_index = krx_index.reset_index(drop=True)
    return krx_index

def _krx_index_listings(idx1, idx2, date=None):
    '''
    [11006] 지수구성종목: 해당지수 항목의 구성종목 데이터
    * idx1= full (index_codes 참고)
    * idx2='013' (index_codes 참고)
    * date: 날짜 (기본값 오늘)
    '''
    end = _krx_last_working_day(date)
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    form_data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00601',
        'indIdx': idx1,
        'indIdx2': idx2,
        'param1indIdx_finder_equidx0_1': '',
        'trdDd': end.strftime('%Y%m%d'),
        'money': '1',
        'csvxls_isNo': 'false',
    }
    r = requests.post(url, form_data, headers=_krx_headers)
    j = r.json()
    df = pd.DataFrame(j['output'])

    cols_map = {'ISU_SRT_CD':'Code', 'ISU_ABBRV':'Name',
                'TDD_CLSPRC':'Close', 'FLUC_TP_CD':'RateCode',
                'CMPPREVDD_PRC':'ComparedRate', 'FLUC_RT':'Rate',
                'MKTCAP':'Marcap'}

    if not len(df):
        print('No data found')
        return pd.DataFrame({}, columns=cols_map.values())

    df = df.replace(r',', '', regex=True)
    numeric_cols = ['TDD_CLSPRC', 'STR_CMP_PRC', 'FLUC_RT', 'MKTCAP']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    df = df.rename(columns=cols_map)
    return df

class KrxSnapReader:
    def __init__(self, ticker):
        self.ticker = ticker

    def read(self):
        if self.ticker == 'KRX/INDEX/LIST': # 지수목록
            df = _krx_index_codes()
            df['Code'] = df['full_code'] + df['short_code']
            df = df.rename(columns={'codeName':'Name', 'marketName':'Market'})
            return df[['Code', 'Name', 'Market']]
        elif self.ticker.startswith('KRX/INDEX/STOCK/'): # 지수구성종목
            code = self.ticker.split('/')[-1]
            df = _krx_index_listings(code[0], code[1:])
            return df
        else:
            raise NotImplementedError(f'"{self.ticker}" is not implemented')
            
