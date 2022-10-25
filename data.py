# FinanceDataReader
# 2018-2022 [FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

from FinanceDataReader.yahoo.data import (YahooDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.data import (KrxDelistingReader)
from FinanceDataReader.krx.listing import (KrxStockListing, KrxDelisting, KrxMarcapListing, KrxAdministrative)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)
from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.investing.listing import (InvestingEtfListing)
from FinanceDataReader.naver.data import (NaverDailyReader)
from FinanceDataReader.naver.listing import (NaverStockListing, NaverEtfListing)
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)
from FinanceDataReader.fred.data import (FredReader)

import re
import pandas as pd
from datetime import datetime, timedelta

def DataReader(symbol, start=None, end=None, exchange=None, data_source=None):
    '''
    read price data from various exchanges or data source
    * symbol: code or ticker
    * start, end: date time string
    * exchange: 'KRX'(default), 'KRX-DELISTING', 'NYSE', 'NASDAQ', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE'
    '''
    start, end = _validate_dates(start, end)
    if (data_source and ':' not in symbol) or type(symbol)==list:
        deprecated_noitce = (
            "'data_source' argument deprecated, use in symbol like these:\n"
            "  fdr.DataReader('FRED:DEXKOUS', '1990-01-01')\n"
            "  fdr.DataReader('FRED:DEXKOUS')\n"
            "  fdr.DataReader('FRED:NASDAQCOM,M2,HSN1F')\n"
        )
        print(deprecated_noitce)
        return pd.DataFrame()

    if ':' in symbol:
        data_source, symbol = symbol.split(':')
    
    # FRED Reader
    if data_source and data_source.upper() == 'FRED':
        return FredReader(symbol, start, end).read()

    # KRX and Naver Finance
    if (symbol[:5].isdigit() and exchange==None) or \
       (symbol[:5].isdigit() and exchange and exchange.upper() == 'KRX'):
        return NaverDailyReader(symbol, start, end).read()

    # KRX-DELISTING
    if (symbol[:5].isdigit() and exchange and exchange.upper() in ['KRX-DELISTING']):
        return KrxDelistingReader(symbol, start, end, exchange, data_source).read()

    # yahoo
    return YahooDailyReader(symbol, start, end, exchange).read()

def StockListing(market):
    '''
    read stock list of stock exchanges
    * market: 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP', 
            'KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC',
            'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE',
            'S&P500',
            'KRX-DELISTING', 'KRX-ADMINISTRATIVE', 'KRX-MARCAP'
            'ETF/KR'
    '''
    market = market.upper()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP' ]:
        return KrxMarcapListing(market).read()
    if market in [ 'KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC' ]:
        return KrxStockListing(market).read()
    if market in [ 'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE' ]:
        return NaverStockListing(market).read()
    if market in [ 'KRX-DELISTING' ]:
        return KrxDelisting(market).read()
    if market in [ 'KRX-ADMINISTRATIVE' ]:
        return KrxAdministrative(market).read()
    if market in [ 'S&P500', 'SP500']:
        return WikipediaStockListing(market).read()
    if market.startswith('ETF'):
        toks = market.split('/')
        etf, country = toks[0], toks[1]
        if country.upper() == 'KR':
            return NaverEtfListing().read()
    else:
        # 해외 ETF 지원 잠정 중단
        msg = "market='%s' is not implemented" % market
        raise NotImplementedError(msg)

def EtfListing(country='KR'):
    '''
    'EtfListing() will deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")'
    '''
    # Deprecation warnings
    print('EtfListing() deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")')
    return None

