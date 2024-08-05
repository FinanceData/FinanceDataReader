# FinanceDataReader
# 2018-2022 [FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

from FinanceDataReader.ecos.data import (EcosDataReader, EcosKeyStatDataReader)
from FinanceDataReader.ecos.snap import (EcosSnapReader)
from FinanceDataReader.krx.data import (KrxDailyReader, KrxDailyDetailReader, KrxIndexReader, KrxDelistingReader)
from FinanceDataReader.krx.snap import (KrxSnapReader)
from FinanceDataReader.krx.listing import (KrxStockListing, KrxDelisting, KrxMarcapListing, KrxAdministrative)
from FinanceDataReader.yahoo.data import (YahooDailyReader)
from FinanceDataReader.nasdaq.listing import (NasdaqStockListing)
from FinanceDataReader.wikipedia.listing import (WikipediaStockListing)
from FinanceDataReader.investing.data import (InvestingDailyReader)
from FinanceDataReader.investing.listing import (InvestingEtfListing)
from FinanceDataReader.naver.data import (NaverDailyReader)
from FinanceDataReader.naver.snap import (NaverSnapReader)
from FinanceDataReader.naver.listing import (NaverStockListing, NaverEtfListing)
from FinanceDataReader.fred.data import (FredReader)
from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

import re
import pandas as pd

def DataReader(symbol:str, start=None, end=None, exchange=None, data_source=None) -> pd.DataFrame:
    '''
    read price data (timeseries) from various exchanges or data source
    - symbol: code or ticker (with exchange: 'KRX'(default), 'KRX-DETAIL', 'KRX-DELISTING', 'NAVER', 'YAHOO' ...)
    - start: datetime or str 
    - end: datetime or str

    usage:
        - fdr.DataReader('KRX:KOSPI', '2020')
        - fdr.DataReader('ECOS:한국은행기준금리', '1990-01-01')
    '''

    if data_source or exchange:
        deprecated_noitce = (
            "'data_source' and 'exchange' argument deprecated, use in symbol like these:\n"
            "  fdr.DataReader('FRED:DEXKOUS', '1990-01-01')\n"
            "  fdr.DataReader('FRED:DEXKOUS')\n"
            "  fdr.DataReader('FRED:NASDAQCOM,M2,HSN1F')\n"
            "  \n"
            "  fdr.DataReader('TSE:9984', '2020-01-01')\n"
            "  fdr.DataReader('NYSE:CBOE', '1990-01-01')\n"
            "  fdr.DataReader('SSE:000150', '1990-01-01')\n"
        )
        print(deprecated_noitce)

    if type(symbol) is not str:
        symbol = ','.join(list(symbol))

    symbol = symbol.upper() # ignore case
    symbol = ''.join(symbol.split()) # remove whtiespace

    source, codes = symbol.split(':') if ':' in symbol else (None, symbol)

    ## major symbols (data source NOT specified)
    if not source: # source not specified -> stocks
        # 1) major symbols (data source NOT specified)
        # 1-1) KRX major indices
        krx_index_symbol_map = {
            'KS11': '1001', 'KOSPI': '1001',  # 코스피
            'KQ11': '2001', 'KOSDAQ': '2001', # 코스닥
            'KS200': '1028', 'KPI200': '1028', # 코스피200
        }
        if symbol in krx_index_symbol_map:
            symbol = krx_index_symbol_map[symbol]
            return KrxIndexReader(symbol, start, end).read()

        # 1-2) yahoo major indices
        yahoo_index_symbol_map = { 
            'DJI':'^DJI', 'IXIC':'^IXIC', 'US500':'^GSPC', 'S&P500':'^GSPC',
            'RUT':'^RUT', 'VIX':'^VIX', 'N225':'^N225', 'SSEC':'000001.SS',
            'FTSE':'^FTSE', 'HSI':'^HSI', 'FCHI':'^FCHI', 'GDAXI':'^GDAXI',
            'US5YT':'^FVX', 'US10YT':'^TNX', 'US30YT':'^TYX', # US Treasury Bonds
        }
        if symbol in yahoo_index_symbol_map:
            symbol = yahoo_index_symbol_map[symbol]
            return YahooDailyReader(symbol, start, end).read()
        
        # 1-3) KRX stocks
        code = codes.split(',')[0]
        if code in krx_index_symbol_map:
            symbol = krx_index_symbol_map[symbol]
            return KrxIndexReader(symbol, start, end).read()

        if re.match(r'\d{5}[0-9KLMN]', code): 
            # Naver is default source for KRX stocks  
            return NaverDailyReader(codes, start, end).read()
        # 1-4) US and other stocks 
        else:
            # Yahoo is default source for US and other stocks
            return YahooDailyReader(codes, start, end).read()
        
    else:  # data source specified
        if source == 'KRX':
            return KrxDailyReader(codes, start, end).read()
        elif source == 'KRX-DETAIL':
            return KrxDailyDetailReader(codes, start, end).read()
        elif source == 'KRX-INDEX':
            return KrxIndexReader(codes, start, end).read()
        elif source == 'KRX-DELISTING':
            return KrxDelistingReader(codes, start, end).read()
        elif source == 'NAVER':
            return NaverDailyReader(codes, start, end).read()
        elif source == 'YAHOO':
            return YahooDailyReader(codes, start, end).read()
        elif source == 'INVESTING':
            return InvestingDailyReader(codes, start, end).read()
        elif source == 'FRED':
            return FredReader(codes, start, end).read()
        elif source in ['NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE']:
            return YahooDailyReader(codes, start, end, source).read()
        elif source == 'ECOS':
            return EcosDataReader(codes, start, end).read()
        elif source == 'ECOS-KEYSTAT':
            return EcosKeyStatDataReader(codes, start, end).read()
        else:
            msg = f'"{symbol}" is not implemented'
            raise NotImplementedError(msg)
 
def SnapDataReader(ticker: str) -> pd.DataFrame:
    '''
    read data snapshots from various finance data source
    * symbol: code or ticker

    usage:
        - fdr.SnapDataReader('ECOS/KEYSTAT/LIST') # 100대 경제지표 
        - fdr.SnapDataReader('KRX/INDEX/LIST') # KRX 지수목록(KRX index list)
        - fdr.SnapDataReader('KRX/INDEX/STOCK/1001') # 지수구성종목 (1001: 코스피)
        - fdr.SnapDataReader('NAVER/STOCK/005930/FINSTATE') # 재무제표
        - fdr.SnapDataReader('NAVER/STOCK/005930/FOREIGN') # 외국인소진율
        - fdr.SnapDataReader('NAVER/STOCK/005930/INVSTORS') # 투자자별종합매매동향
        - fdr.SnapDataReader('DART/CORP_CODES')
    '''
    ticker = ticker.upper()
    if ticker.startswith('KRX/'):
        return KrxSnapReader(ticker).read()
    elif ticker.startswith('ECOS/'):
        return EcosSnapReader(ticker).read()
    elif ticker.startswith('NAVER/'):
        return NaverSnapReader(ticker).read()
    else:
        msg = f'"{ticker}" is not implemented'
        raise NotImplementedError(msg)

def StockListing(market: str, start=None, end=None) -> pd.DataFrame:
    '''
    read stock list of stock exchanges
    * market: 'KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP', 
            'KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC',
            'KRX-DELISTING', 'KRX-ADMINISTRATIVE', 'KRX-MARCAP',
            'NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE',
            'S&P500',
            'ETF/KR',
    '''
    market = market.upper()
    if market in ['KRX', 'KOSPI', 'KOSDAQ', 'KONEX', 'KRX-MARCAP']:
        return KrxMarcapListing(market).read()
    elif market in ['KRX-DESC', 'KOSPI-DESC', 'KOSDAQ-DESC', 'KONEX-DESC']:
        return KrxStockListing(market).read()
    elif market in ['NASDAQ', 'NYSE', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE']:
        return NaverStockListing(market).read()
    elif market in ['KRX-DELISTING' ]:
        return KrxDelisting(market, start, end).read()
    elif market in ['KRX-ADMINISTRATIVE', 'KRX-ADMIN' ]:
        return KrxAdministrative(market).read()
    elif market in ['S&P500', 'SP500']:
        return WikipediaStockListing(market).read()
    elif market.startswith('ETF'):
        toks = market.split('/')
        _, country = toks[0], toks[1]
        return NaverEtfListing(country).read()
    else:
        # 해외 ETF 지원 잠정 중단
        msg = f'"{market}" is not implemented'
        raise NotImplementedError(msg)

def EtfListing(country='KR'):
    '''
    'EtfListing() will deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")'
    '''
    # Deprecation warnings
    print('EtfListing() deprecated. Use fdr.StockListing("ETF/KR") instead of fdr.EtfListing("KR")')
    return None
