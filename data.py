
from FinanceDataReader.investing.data import (InvestingDailyReader)

def DataReader(name, start=None, end=None, data_source=None):
    return InvestingDailyReader(symbols=name, start=start, end=end).read()