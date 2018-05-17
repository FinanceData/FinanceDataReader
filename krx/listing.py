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