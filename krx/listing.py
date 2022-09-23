import io
import time
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
import json
import ssl

try:
    from pandas import json_normalize
except ImportError:
    from pandas.io.json import json_normalize

class KrxStockListing:
    def __init__(self, market):
        self.market = market
    
    def read(self):
        # KRX 상장회사목록
        # For mac, SSL CERTIFICATION VERIFICATION ERROR
        ssl._create_default_https_context = ssl._create_unverified_context
        
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        df_listing = pd.read_html(url, header=0, flavor='bs4', encoding='EUC-KR')[0]
        cols_ren = {'회사명':'Name', '종목코드':'Symbol', '업종':'Sector', '주요제품':'Industry', 
                            '상장일':'ListingDate', '결산월':'SettleMonth',  '대표자명':'Representative', 
                            '홈페이지':'HomePage', '지역':'Region', }
        df_listing = df_listing.rename(columns = cols_ren)
        df_listing['Symbol'] = df_listing['Symbol'].apply(lambda x: '{:06d}'.format(x))
        df_listing['ListingDate'] = pd.to_datetime(df_listing['ListingDate'])

        # KRX 주식종목검색
        data = {'bld': 'dbms/comm/finder/finder_stkisu',}
        r = requests.post('http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd', data=data)

        jo = json.loads(r.text)
        df_finder = json_normalize(jo, 'block1')
        
        # full_code, short_code, codeName, marketCode, marketName, marketEngName, ord1, ord2
        df_finder = df_finder.rename(columns={
                        'full_code': 'FullCode',
                        'short_code': 'Symbol',
                        'codeName': 'Name',
                        'marketCode': 'MarketCode',
                        'marketName': 'MarketName',
                        'marketEngName': 'Market',
                        'ord1': 'Ord1',
                        'ord2': 'Ord2',
                    })

        # 상장회사목록, 주식종목검색 병합
        df_left = df_finder[['Symbol', 'Market', 'Name']]
        df_right = df_listing[['Symbol', 'Sector', 'Industry', 'ListingDate', 'SettleMonth', 'Representative', 'HomePage', 'Region']]

        df_master = pd.merge(df_left, df_right, how='left', left_on='Symbol', right_on='Symbol')
        if self.market in ['KONEX', 'KOSDAQ', 'KOSPI']:
            return df_master[df_master['Market'] == self.market] 
        return df_master    

class KrxDelisting:
    def __init__(self, market):
        self.market = market

    def read(self):
        data = {
            'bld': 'dbms/MDC/STAT/issue/MDCSTAT23801',
            'mktId': 'ALL',
            'isuCd': 'ALL',
            'isuCd2': 'ALL',
            'strtDd': '19900101',
            'endDd': '22001231',
            'share': '1',
            'csvxls_isNo': 'true',
        }

        headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',}

        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        r = requests.post(url, data, headers=headers)
        j = json.loads(r.text)
        df = pd.json_normalize(j['output'])
        col_map = {'ISU_CD':'Symbol', 'ISU_NM':'Name', 'MKT_NM':'Market', 
                   'SECUGRP_NM':'SecuGroup', 'KIND_STKCERT_TP_NM':'Kind',
                   'LIST_DD': 'ListingDate', 'DELIST_DD':'DelistingDate', 'DELIST_RSN_DSC':'Reason', 
                   'ARRANTRD_MKTACT_ENFORCE_DD':'ArrantEnforceDate', 'ARRANTRD_END_DD':'ArrantEndDate', 
                   'IDX_IND_NM':'Industry', 'PARVAL':'ParValue', 'LIST_SHRS':'ListingShares', 
                   'TO_ISU_SRT_CD':'ToSymbol', 'TO_ISU_ABBRV':'ToName' }

        df = df.rename(columns=col_map)
        df['ListingDate'] = pd.to_datetime(df['ListingDate'], format='%Y/%m/%d')
        df['DelistingDate'] = pd.to_datetime(df['DelistingDate'], format='%Y/%m/%d')
        df['ArrantEnforceDate'] = pd.to_datetime(df['ArrantEnforceDate'], format='%Y/%m/%d', errors='coerce')
        df['ArrantEndDate'] = pd.to_datetime(df['ArrantEndDate'], format='%Y/%m/%d', errors='coerce')
        df['ParValue'] = pd.to_numeric(df['ParValue'].str.replace(',', ''), errors='coerce')
        df['ListingShares'] = pd.to_numeric(df['ListingShares'].str.replace(',', ''), errors='coerce')
        return df

class KrxMarcapListing:
    def __init__(self, market):
        self.market = market

    def read(self):
        url = 'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B128.bld'
        j = json.loads(requests.get(url).text)
        date_str = j['result']['output'][0]['max_work_dt']
        
        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        data = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'mktId': 'ALL',
            'trdDd': date_str,
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }
        j = json.loads(requests.post(url, data).text)
        df = pd.json_normalize(j['OutBlock_1'])
        df = df.replace(',', '', regex=True)
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
        df.index = np.arange(len(df)) + 1
        return df

    
class KrxAdministrative:
    def __init__(self, market):
        self.market = market

    def read(self):
        url = "http://kind.krx.co.kr/investwarn/adminissue.do?method=searchAdminIssueSub&currentPageSize=5000&forward=adminissue_down"
        df = pd.read_html(url, header=0)[0]
        df['종목코드'] = df['종목코드'].apply(lambda x: '{:0>6d}'.format(x))
        df['지정일'] = pd.to_datetime(df['지정일'])
        col_map = {'종목코드':'Symbol', '종목명':'Name', '지정일':'DesignationDate', '지정사유':'Reason'}
        df.rename(columns=col_map, inplace=True)    
        return df[['Symbol', 'Name', 'DesignationDate', 'Reason']]    
