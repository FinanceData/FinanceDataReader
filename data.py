from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.krx.listing import (KrxStockListing)

def DataReader(name, start=None, end=None, data_source=None):
    return InvestingDailyReader(symbols=name, start=start, end=end).read()

def StockListing(market):
    market = market.upper()
    if market in [ 'NASDAQ', 'NYSE', 'AMEX']:
        return NasdaqStockListing(market=market).read()
    if market in [ 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX']:
        return KrxStockListing(market).read()
    else:
        msg = "market=%s is not implemented" % market
        raise NotImplementedError(msg)