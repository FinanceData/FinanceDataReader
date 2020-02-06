from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.krx.data import (KrxDelistingReader)
from FinanceDataReader.naver.data import (NaverDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.listing import (KrxStockListing, KrxDelisting)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)
from FinanceDataReader.investing.listing import (InvestingEtfListing)
from FinanceDataReader.naver.listing import (NaverEtfListing)

import re
import pandas as pd
from datetime import datetime, timedelta

def DataReader(symbol, start=None, end=None, exchange=None, kind=None):
    if (symbol.isdigit() and len(symbol)==6 and exchange==None) or \
       (symbol.isdigit() and exchange and exchange.upper() in ['KRX', '한국거래소']):
        return NaverDailyReader(symbol, start, end, exchange, kind).read()

    if (symbol.isdigit() and exchange and exchange.upper() in ['KRX-DELISTING']):
        return KrxDelistingReader(symbol, start, end, exchange, kind).read()

    reader = InvestingDailyReader
    df = reader(symbol, start, end, exchange, kind).read()
    end = min([pd.to_datetime(end), datetime.today()])
    while df.index[-1] < end:
        more = reader(symbol, df.index[-1] + timedelta(1), end, exchange, kind).read()
        if len(more) == 0:
            break
        df = df.append(more)
    return df

def StockListing(market):
    market = market.upper()
    if market in [ 'NASDAQ', 'NYSE', 'AMEX']:
        return NasdaqStockListing(market=market).read()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX']:
        return KrxStockListing(market).read()
    if market in [ 'KRX-DELISTING' ]:
        return KrxDelisting(market).read()
    if market in [ 'S&P500', 'SP500']:
        return WikipediaStockListing(market).read()
    else:
        msg = "market=%s is not implemented" % market
        raise NotImplementedError(msg)

def EtfListing(country='KR'):
    if country.upper() == 'KR':
        return NaverEtfListing().read()
    return InvestingEtfListing(country).read()
