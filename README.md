
# FinanceDataReader
[FinanceData.KR](FinanceData.KR) Open Source Financial data reader

# Overview
The FinanceDataReader is intended to complement rather than replacement [pandas-datareader](https://pandas-datareader.readthedocs.io). 
The main functions are as follows.

* Stock price(Word wide): AAPL, AMZN, GOOG ...
* Stock price(KRX): 005930(Samsung), 091990(Celltrion Healthcare) ...
* Indexes: KOSPI, KOSDAQ, DJI, IXIC, US500(S&P 500) ...
* Exchanges: USD/KRX, USD/EUR, CNY/KRW ...
* Cryptocurrency: BTC/USD (Bitfinex), BTC/KRW (Bithumb)
* Symbol listings: KRX (KOSPI, KODAQ, KONEX), NASDAQ, NYSE, AMEX and S&P 500

# Install

```bash
pip install finance_datareader
```

# Quick Start

```python
import FinanceDataReader as fdr

# Apple(AAPL), 2017-01-01 ~ Now
df = fdr.DataReader('AAPL', '2017')

# AMAZON(AMZN), 2017
df = fdr.DataReader('AMZN', '2017-01-01', '2017-12-31')

# Samsung(005930), 1992-01-01 ~ 2018-10-31
df = fdr.DataReader('068270', '1992-01-01', '2018-10-31')

# country code: ex) 000150: Doosan(KR), Yihua Healthcare(CN)
df = fdr.DataReader('000150', '2018-01-01', '2018-10-30') # default: 'KR' 
df = fdr.DataReader('000150', '2018-01-01', '2018-10-30', country='KR')
df = fdr.DataReader('000150', '2018-01-01', '2018-10-30', country='CN')

# KOSPI index, 2015~Now
df = fdr.DataReader('KS11', '2015-01-01')

# Dow Jones Industrial(DJI), 2015년~Now
df = fdr.DataReader('DJI', '2015-01-01')

# USD/KRW, 1995~Now
df = fdr.DataReader('USD/KRW', '1995-01-01')

# Bitcoin KRW price (Bithumbs), 2016 ~ Now
df = fdr.DataReader('BTC/KRW', '2016-01-01')

# KRX stock symbol list and names
df_krx = fdr.StockListing('KRX')

# S&P 500 symbol list
df_spx = fdr.StockListing('S&P500')
```

## Using FinanceData
* [Users-Guide](https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide)
* [Quick-Reference (Symbol List)](https://github.com/FinanceData/FinanceDataReader/wiki/Quick-Reference)


# Notes (Korean)
* All stock price of KRX is adjust price and date from year 1992<br>
한국거래소 종목의 모두 수정가격 adjust 이며, 1992년 부터 현재까지 가격 데이터를 제공합니다

#### 2018 [FinanceData.KR](http://financedata.kr)
