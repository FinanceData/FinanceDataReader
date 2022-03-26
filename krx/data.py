import requests
import json
import pandas as pd
from io import BytesIO
from datetime import datetime

class KrxDelistingReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime(2100,1,1) if end==None else pd.to_datetime(end)

    def read(self):
        headers = {'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',}
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
        full_code = df.loc[self.symbol]['full_code']

        data = {
            'bld': 'dbms/MDC/STAT/issue/MDCSTAT23902',
            'isuCd': full_code,
            'isuCd2': '',
            'strtDd': self.start.strftime("%Y%m%d"),
            'endDd': self.end.strftime("%Y%m%d"),
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }

        url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
        r = requests.post(url, data, headers=headers)
        j = json.loads(r.text)
        df = pd.json_normalize(j['output'])
        col_map = {'TRD_DD':'Date', 'ISU_CD':'Code', 'ISU_NM':'Name', 'MKT_NM':'Market', 
                   'SECUGRP_NM':'SecuGroup', 'TDD_CLSPRC':'Close', 'FLUC_TP_CD':'UpDown', 
                   'CMPPRVDD_PRC':'Change', 'FLUC_RT':'ChangeRate', 
                   'TDD_OPNPRC':'Open', 'TDD_HGPRC':'High', 'TDD_LWPRC':'Lower', 
                   'ACC_TRDVOL':'Volume', 'ACC_TRDVAL':'Amount', 'MKTCAP':'MarCap'}

        df = df.rename(columns=col_map)
        df['Date'] = pd.to_datetime(df['Date'])
        int_cols = ['Close', 'UpDown', 'Change', 'Open', 'High', 'Lower', 'Volume', 'Amount', 'MarCap']
        for col in int_cols: 
            df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
        
        # df['ChangeRate'] = pd.to_numeric(df['ChangeRate'])
        #### to deal with parse string error such as < ValueError: Unable to parse string "2,946.15" >
        from pandas.api.types import is_string_dtype
        if is_string_dtype(df['ChangeRate']):
            df['ChangeRate'] = pd.to_numeric(df['ChangeRate'].str.replace(',', ''), errors='coerce')
        
        return df
