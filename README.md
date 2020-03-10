
# FinanceDataReader
[FinanceData.KR](FinanceData.KR) Open Source Financial data reader

# Overview
The FinanceDataReader is financial data reader(crawler) for finance. <br>
The main functions are as follows.

* Stock Symbol listings: 'KRX' ('KOSPI', 'KODAQ', 'KONEX'), 'NASDAQ', 'NYSE', 'AMEX' and 'S&P500'
* KRX delistings: 'KRX-DELISTING'
* ETF Symbol listings: Support for ETF lists for multiple countries ('KR', 'US', 'JP')
* Stock price(KRX): '005930'(Samsung), '091990'(Celltrion Healthcare) ...
* Stock price(Word wide): 'AAPL', 'AMZN', 'GOOG' ... (you can specify exchange(market) and symbol)
* Indexes: 'KOSPI', 'KOSDAQ', 'DJI', 'IXIC', 'US500'(S&P 500) ...
* Exchanges: 'USD/KRX', 'USD/EUR', 'CNY/KRW' ...
* Cryptocurrency price data: 'BTC/USD' (Bitfinex), 'BTC/KRW' (Bithumb)

# Install

```bash
pip install finance-datareader
```

# Quick Start

```python
import FinanceDataReader as fdr

# Apple(AAPL), 2017-01-01 ~ Now
df = fdr.DataReader('AAPL', '2017')

# Ford(F), 1980-01-01 ~ 2019-12-30 (40 years)
df = fdr.DataReader('F', '1980-01-01', '2019-12-30')

# AMAZON(AMZN), 2017
df = fdr.DataReader('AMZN', '2017-01-01', '2019-12-31')

# Samsung(005930), 1992-01-01 ~ 2018-10-31
df = fdr.DataReader('068270', '1992-01-01', '2019-10-31')

# country code: ex) 000150: Doosan(KR), Yihua Healthcare(CN)
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30') # KRX
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='KRX') # KRX
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='SZSE') # SZSE
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='심천') # SZSE

# KRX delisting stock data 상장폐지 종목 데이터 (상장일~상장폐지일)
df = fdr.DataReader('036360', exchange='krx-delisting')

# KOSPI index, 2015 ~ Now
ks11 = fdr.DataReader('KS11', '2015-01-01')

# Dow Jones Industrial(DJI), 2015 ~ Now
dji = fdr.DataReader('DJI', '2015-01-01')

# USD/KRW, 1995~Now
usdkrw = fdr.DataReader('USD/KRW', '1995-01-01')

# Bitcoin KRW price (Bithumbs), 2016 ~ Now
btc = fdr.DataReader('BTC/KRW', '2016-01-01')

# KRX stock symbol list and names
krx = fdr.StockListing('KRX')

# KRX stock delisting symbol list and names 상장폐지 종목 전체 리스트
krx_delisting = fdr.StockListing('KRX-DELISTING')

# S&P 500 symbol list
sp500 = fdr.StockListing('S&P500')
```

## Using FinanceDataReader
* [Users-Guide](https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide)
* [Quick-Reference (Symbol List)](https://github.com/FinanceData/FinanceDataReader/wiki/Quick-Reference)

## Tutorials
* [수정주가(Adjusted Price)란?](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%88%98%EC%A0%95%EC%A3%BC%EA%B0%80.ipynb)
* [여러 종목 가격을 한번에](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%97%AC%EB%9F%AC%20%EC%A2%85%EB%AA%A9%EC%9D%98%20%EA%B0%80%EA%B2%A9%EC%9D%84%20%ED%95%9C%EB%B2%88%EC%97%90.ipynb)
* VIX 지수와 관련 종목 (TBA)
* [섹터 평균 수익률과 개별 종목의 수익률 구하기](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%84%B9%ED%84%B0%20%ED%8F%89%EA%B7%A0%20%EC%88%98%EC%9D%B5%EB%A5%A0%EA%B3%BC%20%EA%B0%9C%EB%B3%84%20%EC%A2%85%EB%AA%A9%EC%9D%98%20%EC%88%98%EC%9D%B5%EB%A5%A0.ipynb)


## FinanceDataReader Notebooks
* [S&P500 가격 데이터 수집과 수익률 분석](https://nbviewer.jupyter.org/710b8f0a4bd9a8df91ae1be6c7e838b1) 
* [S&P500 팩터 데이터 수집과 분석](https://nbviewer.jupyter.org/35a1b0d5248bc9b09513e53be437ac42) 


#### 2018-2020 [FinanceData.KR](http://financedata.kr)
