from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.listing import (KrxStockListing)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)

def DataReader(symbol, start=None, end=None, country=None):
    return InvestingDailyReader(symbols=symbol, start=start, end=end, country=country).read()

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