
# FinanceDataReader
Financial price data reader (an alternative to Google/Yahoo finance in pandas-datareader)
    

# Overview
The most basic data of market data is stock symbols and price data. [pandas-datareader](https://pandas-datareader.readthedocs.io) is one of the most well-constructed library for market data. 
But, Yahoo/Google Finance deprecated (or UNSTABLE, Raises a RemoteDataError)

The FinanceDataReader is intended to complement rather than replacement [pandas-datareader](https://pandas-datareader.readthedocs.io). 
The main functions are as follows.

* Stock price: AAPL, AMZN, GOOG ...
* Stock price: 005930(Samsung), 091990(Celltrion Healthcare) ...
* Indexes: KOSPI, KOSDAQ, DJI, IXIC, US500(S&P 500) ...
* Exchanges: USD/KRX, USD/EUR, CNY/KRW ...
* Cryptocurrency: BTC/USD (Bitfinex), BTC/KRW (Bithumb)
* Symbols lists: KRX (KOSPI, KODAQ, KONEX), NASDAQ, NYSE, AMEX and S&P 500

# Install

```bash
pip install finance-datareader # for install
pip install -U finance-datareader # for update
```


# Usage

```python
import FinanceDataReader as fdr

# Apple(AAPL), 2017~Now
df = fdr.DataReader('AAPL', '2017')

# AMAZON(AMZN), 2010~Now
df = fdr.DataReader('AMZN', '2010')

# Celltrion(068270), 2018-07-01~Now
df = fdr.DataReader('068270', '2018-07-01')

# country code: ex) 000150: Doosan(KR), Yihua Healthcare(CN)
df = fdr.DataReader('000150', '2018-01-01', '2018-03-30') # default: 'KR' 
df = fdr.DataReader('000150', '2018-01-01', '2018-03-30', country='KR')
df = fdr.DataReader('000150', '2018-01-01', '2018-03-30', country='CN')

# KOSPI index, 2015~Now
df = fdr.DataReader('KS11', '2015')

# Dow Jones Industrial(DJI), 2015년~Now
df = fdr.DataReader('DJI', '2015')

# USD/KRW, 1995~Now
df = fdr.DataReader('USD/KRW', '1995')

# Bitcoin KRW price (Bithumbs), 2016 ~ Now
df = fdr.DataReader('BTC/KRW', '2016')

# KRX stock symbols and names
df_krx = fdr.StockListing('KRX')

# S&P 500 symbols
df_spx = fdr.StockListing('S&P500')
```

# Changes
2018-08-08 v0.6.0
* Country code assigned ('KR', 'US', 'CN', 'JP')

2018-06-09 v0.5.0
* 상품선물 추가, 국채 심볼 추가, 항생지수 FIX (HSI)

2018-05-17 v0.4.0
* pip install (packaging register The Python Package Index (PyPI) repository)

2018-05-17 v0.2.0
* StockListing, SP500 (S&P500 Listings, wikipedia) added

2018-05-16 v0.1.0
* StockListing KRX, KOSPI, KODAQ, KONEX added
* StockListing NASDAQ, NYSE, AMEX added

2018-05-14 v0.0.1
* DataReader KRX,US Stock prices


# 간략한 설명 (Korean)
마켓 데이터를 다루는데 가장 기본이 되는 데이터는 거래소별 전체 심볼(종목 코드)와 개별 종목들의 가격 데이터 이다.
[pandas-datareader](https://pandas-datareader.readthedocs.io)는 매우 잘 구성된 라이브러리로 사용이 간편하고 
다양한 시계열 데이터를 수집할 수 있다는 장점이 있다. (현재 버전 : pandas_datareader 0.6.0) 
하지만, 거래소별(KRX, NASDAQ, NYSE 등) 전체 종목 코드(ticker symbol)를 가져오는 기능이 없으며, 
구글/야후 파이낸스가 더 이상지원되지 않는다(deprecated). <br>
FinanceDataReader는 [pandas-datareader](https://pandas-datareader.readthedocs.io) 를 대체하기 보다 
보완하기 위한 목적으로 만들어졌으며 주요한 기능은 다음과 같다.

* 해외주식 가격 데이터: AAPL(애플), AMZN(아마존), GOOG(구글) 등
* 국내주식 가격 데이터: 005930(삼성전자), 091990(셀트리온헬스케어) 등
* 각종 지수: KS11(코스피지수), KQ11(코스닥지수), DJI(다우지수), IXIC(나스닥 지수), US500(S&P 500)
* 환율 데이터: USD/KRX (원달러 환율), USD/EUR(달러당 유로화 환율), CNY/KRW: 위엔화 원화 환율
* 암호화폐 가격: BTC/USD (비트코인 달러 가격, Bitfinex), BTC/KRW (비트코인 원화 가격, 빗썸)
* 거래소별 전체 종목 코드: KRX (KOSPI, KODAQ, KONEX), NASDAQ, NYSE, AMEX, S&P 500 종목


#### 2018 [FinanceData.KR](http://financedata.kr)