import io
import requests
import pandas as pd

class KrxStockListing:
    def __init__(self, market):
        self.market = market
    
    def read(self):
        marketTypeMap = {'KRX':'', 'KOSPI':'stockMkt', 'KOSDAQ':'kosdaqMkt', 'KONEX':'konexMkt' }
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?' \
                'method=download&searchType=13&marketType=' + marketTypeMap[self.market]
        df = pd.read_html(url, header=0)[0]
        df['종목코드'] = df['종목코드'].apply(lambda x: '{:06d}'.format(x))
        df['상장일'] = pd.to_datetime(df['상장일'])
        cols_ren = {'회사명':'Name', '종목코드':'Symbol', '업종':'Sector', '주요제품':'Industry'}
        df = df.rename(columns = cols_ren)
        return df[['Symbol', 'Name', 'Sector', 'Industry']]

class KrxDelisting:
    def __init__(self, market):
        self.market = market

    def read(self):
        # STEP 01: Generate OTP
        url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?' \
            'name=fileDown&filetype=xls&url=MKD/04/0406/04060600/mkd04060600&' \
            'market_gubun=ALL&isu_cdnm=%EC%A0%84%EC%B2%B4&isu_cd=&isu_nm=&' \
            'isu_srt_cd=&fromdate=19900101&todate=22001231&del_cd=1&' \
            'pagePath=%2Fcontents%2FMKD%2F04%2F0406%2F04060600%2FMKD04060600.jsp'

        header_data = {
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
        }
        r = requests.get(url, headers=header_data)

        # STEP 02: download
        url = 'http://file.krx.co.kr/download.jspx'
        form_data = {'code': r.text}
        header_data = {
            'Referer': 'http://marketdata.krx.co.kr/contents/MKD/04/0406/04060600/MKD04060600.jsp',
            'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36',
        }
        r = requests.post(url, data=form_data, headers=header_data)
        df = pd.read_excel(io.BytesIO(r.content))
        df['종목코드'] = df['종목코드'].str.replace('A', '')
        df['폐지일'] = pd.to_datetime(df['폐지일'])
        col_map = {'종목코드':'Symbol', '기업명':'Name', '폐지일':'DelistingDate', '폐지사유':'Reason'}
        return df.rename(columns=col_map)        
