from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.naver.data import (NaverDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.listing import (KrxStockListing)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)

import re

def DataReader(symbol, start=None, end=None, country=None):
    is_stock_krx = re.match('\d{6}', symbol) and (country==None or country.upper()=='KR')
    reader = NaverDailyReader if is_stock_krx else InvestingDailyReader
    return reader(symbol=symbol, start=start, end=end, country=country).read()

def StockListing(market):
    market = market.upper()
    if market in [ 'NASDAQ', 'NYSE', 'AMEX']:
        return NasdaqStockListing(market=market).read()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX']:
        return KrxStockListing(market).read()
    if market in [ 'S&P500', 'SP500']:
        return WikipediaStockListing(market).read()
    else:
        msg = "market=%s is not implemented" % market
        raise NotImplementedError(msg)
