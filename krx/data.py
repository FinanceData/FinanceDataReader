import requests
import pandas as pd
from io import BytesIO
from datetime import datetime

class KrxDelistingReader:
    def __init__(self, symbol, start=None, end=None, exchange=None, kind=None):
        self.symbol = symbol
        self.start = datetime(1990,1,1) if start==None else pd.to_datetime(start)
        self.end = datetime(2100,1,1) if end==None else pd.to_datetime(end)

    def read(self):
        # STEP 01: Generate OTP
        url = "http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx"
        form_data = {
            'name':'fileDown',
            'filetype':'xls',
            'url':'MKD/04/0406/04060300/mkd04060300',
            'isu_srt_cd':'A' + self.symbol,
            'fromdate': self.start.strftime("%Y%m%d"),
            'todate': self.end.strftime("%Y%m%d"),
            'pagePath':'/contents/MKD/04/0406/04060300/MKD04060300.jsp',
        }
        header_data = {
            'User-Agent': 'Chrome/78 Safari/537',
        }
        r = requests.post(url, data=form_data, headers=header_data)
        # STEP 02: download
        url = 'http://file.krx.co.kr/download.jspx'
        form_data = {
            'code': r.text,
        }

        header_data = {
            'Referer': 'http://marketdata.krx.co.kr/',
            'User-Agent': 'Chrome/78 Safari/537',
        }
        r = requests.post(url, form_data, headers=header_data)
        dfx = pd.read_excel(BytesIO(r.content), thousands=',')
        dfx['일자'] = pd.to_datetime(dfx['일자'])

        col_map = {'일자':'Date', '종가':'Close', '등락구분코드':'UpDown', '대비':'Change', 
                    '거래량':'Volume', '거래대금':'Amount', 
                    '시가':'Open', '고가':'High', '저가':'Low', 
                    '기준가':'StandardPrice', '상장주식수':'Stocks', '액면가':'FaceValue', 
                    '통화구분':'Currency', '거래정지\r여부':'StopOrder', '관리종목\r여부':'Issues' }
        dfx.rename(columns=col_map, inplace=True)
        dfx.set_index('Date', inplace=True)
        dfx.sort_index(inplace=True)
        use_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Change', 'Amount', 'Stocks', 
                    'FaceValue', 'StandardPrice', 'StopOrder', 'Issues']
        return dfx[use_cols]
