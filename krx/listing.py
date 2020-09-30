import io
import time
import requests
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
        df_listing = pd.read_html(url, header=0)[0]
        cols_ren = {'회사명':'Name', '종목코드':'Symbol', '업종':'Sector', '주요제품':'Industry', 
                            '상장일':'ListingDate', '결산월':'SettleMonth',  '대표자명':'Representative', 
                            '홈페이지':'HomePage', '지역':'Region', }
        df_listing = df_listing.rename(columns = cols_ren)
        df_listing['Symbol'] = df_listing['Symbol'].apply(lambda x: '{:06d}'.format(x))
        df_listing['ListingDate'] = pd.to_datetime(df_listing['ListingDate'])
        df_listing.head()

        # KRX 주식종목검색
        header_data = { 'User-Agent': 'Chrome/78.0.3904.87 Safari/537.36', }

        url_tmpl = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx?bld=COM%2Ffinder_stkisu&name=form&_={}' 
        url = url_tmpl.format( int(time.time() * 1000) )
        r = requests.get(url, headers=header_data)

        down_url = 'http://marketdata.krx.co.kr/contents/MKD/99/MKD99000001.jspx'
        down_data = {
            'mktsel':'ALL',
            'pagePath':'/contents/COM/FinderStkIsu.jsp',
            'code': r.content,
            'geFirstCall':'Y',
        }
        r = requests.post(down_url, down_data, headers=header_data)
        jo = json.loads(r.text)
        df_finder = json_normalize(jo, 'block1')
        df_finder.columns = ['FullCode', 'ShortCode', 'Name', 'Market']
        df_finder['Symbol'] = df_finder['ShortCode'].str[1:]

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
