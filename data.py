from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.fred.data import (FredReader)
from FinanceDataReader.krx.data import (KrxDelistingReader)
from FinanceDataReader.naver.data import (NaverDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.listing import (KrxStockListing, KrxDelisting, KrxMarcapListing, KrxAdministrative)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)
from FinanceDataReader.investing.listing import (InvestingEtfListing)
from FinanceDataReader.naver.listing import (NaverStockListing, NaverEtfListing)
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

import re
import pandas as pd
from datetime import datetime, timedelta

def DataReader(symbol, start=None, end=None, exchange=None, data_source=None):
    '''
    read price data from various exchanges or data source
    * symbol: code or ticker
    * start, end: date time string
    * exchange: 'KRX'(default), 'KRX-DELISTING', 'NYSE', 'NASDAQ', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE'
    * data_source: 'FRED' 
    '''
    start, end = _validate_dates(start, end)
    
    # FRED Reader
    if data_source and data_source.upper() == 'FRED':
        return FredReader(symbol, start, end, exchange, data_source).read()

    # KRX and Naver Finance
    if (symbol[:5].isdigit() and exchange==None) or \
       (symbol[:5].isdigit() and exchange and exchange.upper() in ['KRX', '한국거래소']):
        return NaverDailyReader(symbol, start, end, exchange, data_source).read()

    # KRX-DELISTING
    if (symbol[:5].isdigit() and exchange and exchange.upper() in ['KRX-DELISTING']):
        return KrxDelistingReader(symbol, start, end, exchange, data_source).read()

    # Investing
    reader = InvestingDailyReader
    df = reader(symbol, start, end, exchange, data_source).read()
    end = min([pd.to_datetime(end), datetime.today()])
    while len(df) and df.index[-1] < end: # issues/30
        more = reader(symbol, df.index[-1] + timedelta(1), end, exchange, data_source).read()
        if len(more) == 0:
            break
        df = pd.concat([df, more])
    return df

def StockListing(market):
    '''
    read stock list of stock exchanges
    * market: 'S&P500', 'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE', 
            'KRX', 'KOSPI', 'KOSDAQ', 'KONEX'
            'KRX-DELISTING', 'KRX-MARCAP', 'KRX-ADMINISTRATIVE'
            'ETF/KR'
    '''
    market = market.upper()
    if market in [ 'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE']:
        return NaverStockListing(market).read()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX']:
        return KrxStockListing(market).read()
    if market in [ 'KRX-DELISTING' ]:
        return KrxDelisting(market).read()
    if market in [ 'KRX-MARCAP' ]:
        return KrxMarcapListing(market).read()
    if market in [ 'KRX-ADMINISTRATIVE' ]:
        return KrxAdministrative(market).read()
    if market in [ 'S&P500', 'SP500']:
        return WikipediaStockListing(market).read()
    if market.startswith('ETF'):
        toks = market.split('/')
        etf, country = toks[0], toks[1]
        if country.upper() == 'KR':
            return NaverEtfListing().read()
        return InvestingEtfListing(country).read()        
    else:
        msg = "market='%s' is not implemented" % market
        raise NotImplementedError(msg)

def EtfListing(country='KR'):
    '''
    'EtfListing() will deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")'
    '''
    # Deprecation warnings
    print('EtfListing() will deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")')
    if country.upper() == 'KR':
        return NaverEtfListing().read()
    return InvestingEtfListing(country).read()
