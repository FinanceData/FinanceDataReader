
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

주요 기능
* 한국거래소(KRX)와 미국3대 거래소(NASDAQ, NYSE, AMEX) 전체 상장종목 리스팅 
* S&P 500 전체 종목 리스팅 
* 국가별 ETF 전체 종목 리스팅
* 한국, 미국, 홍콩, 중국, 일본 개별종목및 ETF 가격 데이터
* 각종 지수, 환율, 암호화폐, 상품, 선물 가격 데이터

# Install

```bash
$ pip install finance-datareader
```
FinanceDataReader가 이미 설치되어 있다면 다음과 같이 업그레이드 합니다.

```bash
$ pip install --upgrade finance-datareader
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

## FinanceDataReader Notebooks
* [S&P500 가격 데이터 수집과 수익률 분석](https://nbviewer.jupyter.org/710b8f0a4bd9a8df91ae1be6c7e838b1) 
* [S&P500 팩터 데이터 수집과 분석](https://nbviewer.jupyter.org/35a1b0d5248bc9b09513e53be437ac42) 

## Notes
* All stock price of KRX is adjust price and date from year 1992<br>
가격 데이터는 모두 수정가격(djust price)이며, 1992년 부터 현재까지 가격 데이터를 제공합니다 <br>
(한번에 5000개의 데이터를 가져옵니다. 10년 이상 데이터를 가져오려면 두번에 나누어 가져오십시오)

## buymeacoffee
무료 오픈소스 FinanceDataReader 가 도움이 되셨다면 깃허브의 Star를 눌러 주세요. 아래 URL에서 후원도 하실 수 있습니다.

https://www.buymeacoffee.com/siZa4t0

#### 2018,2019 [FinanceData.KR](http://financedata.kr)
