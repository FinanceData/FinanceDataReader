import io
import time
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
import json
import ssl

class KrxMarcapListing:
    def __init__(self, market):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }
        
    def read(self):
        url = 'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B128.bld'
        j = json.loads(requests.get(url, headers=self.headers).text)
        date_str = j['result']['output'][0]['max_work_dt']
        
        mkt_map = {'KRX-MARCAP':'ALL', 'KRX':'ALL', 'KOSPI':'STK', 'KOSDAQ':'KSQ', 'KONEX':'KNX'}
        if self.market not in mkt_map:
            raise ValueError(f"market shoud be one of {list(mkt_map.keys())}")
        
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'mktId': mkt_map[self.market], # 'ALL'=전체, 'STK'=KOSPI, 'KSQ'=KOSDAQ, 'KNX'=KONEX
            'trdDd': date_str,
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }
        html_text = requests.post(url, headers=self.headers, data=data).text
        j = json.loads(html_text)
        df = pd.DataFrame(j['OutBlock_1'])
        df = df.replace(r',', '', regex=True)
        numeric_cols = ['CMPPREVDD_PRC', 'FLUC_RT', 'TDD_OPNPRC', 'TDD_HGPRC', 'TDD_LWPRC', 
                        'ACC_TRDVOL', 'ACC_TRDVAL', 'MKTCAP', 'LIST_SHRS'] 
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        df = df.sort_values('MKTCAP', ascending=False)
        cols_map = {'ISU_SRT_CD':'Code', 'ISU_ABBRV':'Name', 
                    'TDD_CLSPRC':'Close', 'SECT_TP_NM': 'Dept', 'FLUC_TP_CD':'ChangeCode', 
                    'CMPPREVDD_PRC':'Changes', 'FLUC_RT':'ChagesRatio', 'ACC_TRDVOL':'Volume', 
                    'ACC_TRDVAL':'Amount', 'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Low',
                    'MKTCAP':'Marcap', 'LIST_SHRS':'Stocks', 'MKT_NM':'Market', 'MKT_ID': 'MarketId' }
        df = df.rename(columns=cols_map)
        df = df.reset_index(drop=True)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        return df

    
class KrxStockListing: # descriptive information
    def __init__(self, market):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }

    def read(self):
        # KRX 상장회사목록
        # For MacOS, SSL CERTIFICATION VERIFICATION ERROR
        ssl._create_default_https_context = ssl._create_unverified_context
        
        mkt_list = ['KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC']
        if self.market not in mkt_list:
            raise ValueError(f"market shoud be one of {mkt_list}")
        
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        r = requests.get(url, headers=self.headers)
        dfs = pd.read_html(io.StringIO(r.text), header=0)
        df_listing = dfs[0]
        cols_ren = {'회사명':'Name', '종목코드':'Code', '업종':'Sector', '주요제품':'Industry', 
                            '상장일':'ListingDate', '결산월':'SettleMonth',  '대표자명':'Representative', 
                            '홈페이지':'HomePage', '지역':'Region', }
        df_listing = df_listing.rename(columns = cols_ren)
        df_listing['Code'] = df_listing['Code'].apply(lambda x: '{:06d}'.format(x))
        df_listing['ListingDate'] = pd.to_datetime(df_listing['ListingDate'])

        # KRX 주식종목검색
        data = {'bld': 'dbms/comm/finder/finder_stkisu',}
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        r = requests.post(url, data, headers=self.headers)
        jo = json.loads(r.text)
        df_finder = pd.DataFrame(jo['block1'])
        
        # full_code, short_code, codeName, marketCode, marketName, marketEngName, ord1, ord2
        df_finder = df_finder.rename(columns={
                        'full_code': 'FullCode',
                        'short_code': 'Code',
                        'codeName': 'Name',
                        'marketCode': 'MarketCode',
                        'marketName': 'MarketName',
                        'marketEngName': 'Market',
                        'ord1': 'Ord1',
                        'ord2': 'Ord2',
                    })

        # 상장회사목록, 주식종목검색 병합
        df_left = df_finder[['Code', 'Name', 'Market']]
        df_right = df_listing[['Code', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'Representative', 'HomePage', 'Region']]

        merged = pd.merge(df_left, df_right, how='left', left_on='Code', right_on='Code')
        if self.market in ['KONEX-DESC', 'KOSDAQ-DESC', 'KOSPI-DESC']:
            merged = merged[merged['Market']==self.market.replace('-DESC','')].reset_index(drop=True)
        merged.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        merged = merged.drop_duplicates(subset='Code').reset_index(drop=True)
        return merged

def _krx_delisting_2years(from_date, to_date):
    data = {
        'bld': 'dbms/MDC/STAT/issue/MDCSTAT23801',
        'mktId': 'ALL',
        'isuCd': 'ALL',
        'isuCd2': 'ALL',
        'strtDd': from_date.strftime("%Y%m%d"),
        'endDd': to_date.strftime("%Y%m%d"),
        'share': '1',
        'csvxls_isNo': 'true',
    }
    _krx_headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
                    'Referer': 'http://data.krx.co.kr/', }
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    r = requests.post(url, data, headers=_krx_headers)
    try:
        jo = r.json()
    except:
        msg = r.text
        raise ValueError(msg)

    df = pd.DataFrame(jo['output'])
    col_map = {'ISU_CD':'Symbol', 'ISU_NM':'Name', 'MKT_NM':'Market', 
                'SECUGRP_NM':'SecuGroup', 'KIND_STKCERT_TP_NM':'Kind',
                'LIST_DD': 'ListingDate', 'DELIST_DD':'DelistingDate', 'DELIST_RSN_DSC':'Reason', 
                'ARRANTRD_MKTACT_ENFORCE_DD':'ArrantEnforceDate', 'ARRANTRD_END_DD':'ArrantEndDate', 
                'IDX_IND_NM':'Industry', 'PARVAL':'ParValue', 'LIST_SHRS':'ListingShares', 
                'TO_ISU_SRT_CD':'ToSymbol', 'TO_ISU_ABBRV':'ToName' }

    df = df.rename(columns=col_map)
    if len(df):
        df['ListingDate'] = pd.to_datetime(df['ListingDate'], format='%Y/%m/%d')
        df['DelistingDate'] = pd.to_datetime(df['DelistingDate'], format='%Y/%m/%d')
        df['ArrantEnforceDate'] = pd.to_datetime(df['ArrantEnforceDate'], format='%Y/%m/%d', errors='coerce')
        df['ArrantEndDate'] = pd.to_datetime(df['ArrantEndDate'], format='%Y/%m/%d', errors='coerce')
        df['ParValue'] = pd.to_numeric(df['ParValue'].str.replace(',', ''), errors='coerce')
        df['ListingShares'] = pd.to_numeric(df['ListingShares'].str.replace(',', ''), errors='coerce')
    return df

def _krx_delisting(from_date, to_date):
    df_list = []
    _start = from_date
    _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)
    while True: 
        df = _krx_delisting_2years(_start, _end)
        df_list.append(df)
        if to_date <= _end: 
            break
        _start = _end + timedelta(days=1)
        _end = datetime(_start.year+2, _start.month, _start.day) - timedelta(days=1)

    df = pd.concat(df_list)
    if(len(df) == 0):
        print(f'No data found for KRX Delisting')
        return df
    return df[(from_date <= df['DelistingDate']) & (df['DelistingDate'] <= to_date)]

class KrxDelisting:
    def __init__(self, market, start=None, end=None):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }
        
        self.start = datetime(1960,1,1) if start==None else pd.to_datetime(start)
        self.start = datetime(1960,1,1) if self.start < datetime(1960,1,1) else self.start
        self.end = datetime.today() if end==None else pd.to_datetime(end)
        
    def read(self):
        df = _krx_delisting(self.start, self.end)
        df = df.reset_index(drop=True)
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        return df
    
class KrxAdministrative:
    def __init__(self, market):
        self.market = market
        self.headers = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
            'Referer': 'http://data.krx.co.kr/'
            }
        
    def read(self):
        url = "http://kind.krx.co.kr/investwarn/adminissue.do?method=searchAdminIssueSub&currentPageSize=5000&forward=adminissue_down"
        r = requests.get(url,headers=self.headers)
        df = pd.read_html(io.StringIO(r.text), header=0, encoding='euc-kr')[0]
        df['지정일'] = pd.to_datetime(df['지정일'])
        col_map = {'종목코드':'Symbol', '종목명':'Name', '지정일':'DesignationDate', '지정사유':'Reason'}
        df.rename(columns=col_map, inplace=True)    
        df.attrs = {'exchange':'KRX', 'source':'KRX', 'data':'LISTINGS'}
        return df[['Symbol', 'Name', 'DesignationDate', 'Reason']]    

