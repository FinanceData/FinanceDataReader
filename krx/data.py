# KRX data reader for FinanceDataReader  
# 2023 FinacneData.KR

import requests
import json
import pandas as pd
from datetime import datetime, timedelta

__KRX_CODES = pd.DataFrame()

def _krx_fullcode(code):
    global __KRX_CODES
    if len(__KRX_CODES) == 0:
        headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
                   'Referer': 'http://data.krx.co.kr/', }
        data = {
            'locale': 'ko_KR',
            'mktsel': 'ALL',
            'searchText': '',
            'typeNo': 0,
            'bld': 'dbms/comm/finder/finder_stkisu',
        }
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        r = requests.post(url, data, headers=headers)
        __KRX_CODES = pd.DataFrame(r.json()['block1'])
        __KRX_CODES = __KRX_CODES.set_index('short_code')

    if code not in __KRX_CODES.index:
        return None
    return __KRX_CODES.loc[code]['full_code']

def _krx_index_price_2years(idx1, idx2, from_date, to_date):
    headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
               'Referer': 'http://data.krx.co.kr/', }
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00301',
        'indIdx': idx1,
        'indIdx2': idx2,
        'strtDd': from_date.strftime('%Y%m%d'),
        'endDd': to_date.strftime('%Y%m%d'),
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    r = requests.post(url, data, headers=headers)
    try:
        jo = r.json()
    except:
        raise ValueError(r.text)
    
    return pd.DataFrame(r.json()['output'])


# 1975-01-04 ~ 2001-06-10 까지의 데이터에는 Close만 제공 (KRX 원천 데이터 미제공)
# 2001-06-11 ~ 이후 데이터는 모든 컬럼(Close, UpDown, Comp, Change, Open, High, Low, Volume, Amount, MarCap)

def _krx_index_price(idx1, idx2, from_date, to_date):
    df_list = []
    _start = from_date
    _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)
    while True: 
        df = _krx_index_price_2years(idx1, idx2, _start, _end)
        df_list.append(df)
        if to_date <= _end: 
            break
        _start = _end + timedelta(days=1)
        _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)

    df = pd.concat(df_list)
    col_map = {'TRD_DD':'Date', 'CLSPRC_IDX':'Close', 'FLUC_TP_CD':'UpDown', 
               'PRV_DD_CMPR':'Comp', 'UPDN_RATE':'Change', 
               'OPNPRC_IDX':'Open', 'HGPRC_IDX':'High', 'LWPRC_IDX':'Low', 
               'ACC_TRDVOL':'Volume', 'ACC_TRDVAL':'Amount', 'MKTCAP':'MarCap'}
    if(len(df) == 0):
        print(f'no data or code("{idx1}{idx2}") not found')
        return df

    df = df.rename(columns=col_map)
    num_cols = ['Close', 'UpDown', 'Comp', 'Change', 'Open', 'High', 'Low', 'Volume', 'Amount', 'MarCap']
    for col in num_cols: 
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df = df.sort_index()
    df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Change', 'UpDown', 'Comp', 'Amount', 'MarCap']]
    df['Change'] = df['Change'] / 100.0 
    return df.loc[from_date:to_date]

def _krx_stock_price_2years(full_code, from_date, to_date):
    data = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT01701',
        'locale': 'ko_KR',
        'isuCd': full_code,
        'isuCd2': '',
        'strtDd': from_date.strftime("%Y%m%d"),
        'endDd': to_date.strftime("%Y%m%d"),
        'adjStkPrc_check': 'Y',
        'adjStkPrc': 2,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }

    headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
               'Referer': 'http://data.krx.co.kr/', }

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    r = requests.post(url, data, headers=headers)
    if r.status_code != 200:
        raise ValueError(f'{r.status_code} - {r.reason}' + '(Period is up to 2 years)')

    df = pd.DataFrame(r.json()['output'])
    col_map = {'TRD_DD':'Date', 'ISU_CD':'Code', 'ISU_NM':'Name', 'MKT_NM':'Market', 
                'SECUGRP_NM':'SecuGroup', 'TDD_CLSPRC':'Close', 'FLUC_TP_CD':'UpDown', 
                'CMPPREVDD_PRC':'Comp', 'FLUC_RT':'Change', 
                'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Low', 
                'ACC_TRDVOL':'Volume', 'ACC_TRDVAL':'Amount', 'MKTCAP':'MarCap', 'LIST_SHRS':'Shares'}
    
    df = df.rename(columns=col_map)
    if len(df) == 0:
        return df

    num_cols = ['Close', 'UpDown', 'Comp', 'Change', 'Open', 'High', 'Low', 'Volume', 'Amount', 'MarCap', 'Shares']
    for col in num_cols: 
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

    df['Date'] = pd.to_datetime(df['Date'])
    df['Change'] = df['Change'] / 100.0 
    return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change', 'UpDown', 'Comp', 'Amount', 'MarCap', 'Shares']]


def _krx_stock_price(full_code, from_date, to_date):
    df_list = []
    _start = from_date
    _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)
    while True: 
        df = _krx_stock_price_2years(full_code, _start, _end)
        df_list.append(df)
        if to_date <= _end: 
            break
        _start = _end + timedelta(days=1)
        _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)

    df = pd.concat(df_list)
    if(len(df) == 0):
        print(f'no data or code("{full_code}") not found')
        return df
    df = df.set_index('Date')
    df = df.sort_index()
    return df.loc[from_date:to_date]

def _krx_delisting_price_2years(full_code, from_date, to_date):
    headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
               'Referer': 'http://data.krx.co.kr/', }
    data = {
        'bld': 'dbms/MDC/STAT/issue/MDCSTAT23902',
        'isuCd': full_code,
        'isuCd2': '',
        'strtDd': from_date.strftime("%Y%m%d"),
        'endDd': to_date.strftime("%Y%m%d"),
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    r = requests.post(url, data, headers=headers)
    if r.status_code != 200:
        raise ValueError(f'{r.status_code} - {r.reason}')

    j = json.loads(r.text)
    df = pd.json_normalize(j['output'])
    col_map = {'TRD_DD':'Date', 'ISU_CD':'Code', 'ISU_NM':'Name', 'MKT_NM':'Market', 
                'SECUGRP_NM':'SecuGroup', 'TDD_CLSPRC':'Close', 'FLUC_TP_CD':'UpDown', 
                'CMPPRVDD_PRC':'Change', 'FLUC_RT':'ChangeRate', 
                'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Low', 
                'ACC_TRDVOL':'Volume', 'ACC_TRDVAL':'Amount', 'MKTCAP':'MarCap'}

    df = df.rename(columns=col_map)
    if len(df) == 0:
        return df
    df['Date'] = pd.to_datetime(df['Date'])
    mum_cols = ['Close', 'UpDown', 'Change', 'ChangeRate', 'Open', 'High', 'Low', 'Volume', 'Amount', 'MarCap']
    for col in mum_cols: 
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

    df['ChangeRate'] = df['ChangeRate'] / 100.0
    return df

def _krx_delisting_price(code, from_date, to_date):
    headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
               'Referer': 'http://data.krx.co.kr/', }
    data = {
        'mktsel': 'ALL',
        'searchText': '',
        'bld': 'dbms/comm/finder/finder_listdelisu',
    }

    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    r = requests.post(url, data, headers=headers)
    j = json.loads(r.text)
    df = pd.json_normalize(j['block1'])
    df = df.set_index('short_code')
    full_code = df.loc[code]['full_code']

    df_list = []
    _start = from_date
    _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)
    while True: 
        df = _krx_delisting_price_2years(full_code, _start, _end)
        df_list.append(df)
        if to_date <= _end: 
            break
        _start = _end + timedelta(days=1)
        _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)

    df = pd.concat(df_list)
    if(len(df) == 0):
        print(f'no data or code({code}, {full_code})") not found')
        return df
    
    df = df.set_index('Date')
    df = df.sort_index()
    return df.loc[from_date:to_date]


class KrxDailyReader:
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.start = datetime(1960,1,1) if self.start < datetime(1960,1,1) else self.start
        self.end = datetime.today() if end==None else pd.to_datetime(end)

        # if start==None and end==None: (default 2 years limit)
        #     self.end = datetime.today()
        #     self.start = datetime.today() - timedelta(days=365*2-1)

    def read(self):
        full_code = _krx_fullcode(self.symbol)
        if not full_code:
            raise ValueError(f'"{self.symbol}" is not supported')

        df = _krx_stock_price(full_code, from_date=self.start, to_date=self.end)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'PRICE'}
        return df

class KrxDailyDetailReader:
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime.today() if end==None else pd.to_datetime(end)

    def read(self):
        full_code = _krx_fullcode(self.symbol)
        if not full_code:
            raise ValueError(f'"{self.symbol}" is not supported')

        df = _krx_stock_price(full_code, from_date=self.start, to_date=self.end)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'PRICE'}
        return df

class KrxIndexReader:
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.start = datetime(2001,6,11) if start == None else pd.to_datetime(start)
        self.end = datetime.today() if end == None else pd.to_datetime(end)

    def read(self):
        idx1, idx2 = self.symbol[0], self.symbol[1:]
        df = _krx_index_price(idx1, idx2, self.start, self.end)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'INDEX'}
        return df


class KrxDelistingReader:
    def __init__(self, symbol, start=None, end=None):
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime(2100,1,1) if end==None else pd.to_datetime(end)

    def read(self):
        df = _krx_delisting_price(self.symbol, self.start, self.end)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        return df
