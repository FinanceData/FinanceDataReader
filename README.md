# FinanceDataReader
[FinanceData.KR](FinanceData.KR) Open Source Financial data reader

# Overview
The FinanceDataReader is intended to complement rather than replacement [pandas-datareader](https://pandas-datareader.readthedocs.io). 
The main functions are as follows.

* Symbol listings: KRX (KOSPI, KODAQ, KONEX), NASDAQ, NYSE, AMEX and S&P 500
* Stock price(Word wide): AAPL, AMZN, GOOG ...
* Stock price(KRX): 005930(Samsung), 091990(Celltrion Healthcare) ...
* Indexes: KOSPI, KOSDAQ, DJI, IXIC, US500(S&P 500) ...
* Exchanges: USD/KRX, USD/EUR, CNY/KRW ...
* Cryptocurrency: BTC/USD (Bitfinex), BTC/KRW (Bithumb)

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

## Using FinanceDataReader
* [Users-Guide](https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide)
* [Quick-Reference (Symbol List)](https://github.com/FinanceData/FinanceDataReader/wiki/Quick-Reference)

## Tutirials
* [Tutorial_01 수정주가](tutorial/FinanceDataReader_Tutorial_01_Adjusted_closing_price.ipynb)


## FinanceDataReader Notebooks
* [S&P500 가격 데이터 수집과 수익률 분석](https://nbviewer.jupyter.org/710b8f0a4bd9a8df91ae1be6c7e838b1) 
* [S&P500 팩터 데이터 수집과 분석](https://nbviewer.jupyter.org/35a1b0d5248bc9b09513e53be437ac42) 

## Notes
* All stock price of KRX is adjust price and date from year 1992<br>
가격 데이터는 모두 수정가격(djust price)이며, 1992년 부터 현재까지 가격 데이터를 제공합니다 <br>
(한번에 5000개의 데이터를 가져옵니다. 10년 이상 데이터를 가져오려면 두번에 나누어 가져오십시오)

#### 2018 [FinanceData.KR](http://financedata.kr)
