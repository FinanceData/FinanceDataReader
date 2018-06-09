
# FinanceDataReader
Financial price data reader (an alternative to google finance and yahoo finance in pandas-datareader)

https://github.com/FinanceData/FinanceDataReader
    

# Overview
금융 데이터를 다루는데 가장 기본이 되는 데이터는 거래소별 전체 종목 코드와 가격 데이터 이다.

[pandas-datareader](https://pandas-datareader.readthedocs.io) 는 잘 구성된 시계열 데이터 수집 라이브러리로 사용이 간편하고 다양한 시계열 데이터를 수집할 수 있다는 장점이 있다.  (현재 버전 : pandas_datareader 0.6.0) 하지만, 거래소별(KRX, NASDAQ, NYSE 등) 전체 종목 코드(ticker symbol)를 가져오는 기능이 없으며, 야후 파이낸스가 더 이상지원되지 않고(deprecated), 구글 파이낸스는 UNSTABLE_WARNING + RemoteDataError 를 낸다. 

FinanceDataReader는 [pandas-datareader](https://pandas-datareader.readthedocs.io) 를 대체하기 보다 보완하기 위한 목적으로 만들어졌다. 주요한 기능은 다음과 같다.

* 해외주식 가격 데이터: AAPL(애플), AMZN(아마존), GOOG(구글) 등
* 국내주식 가격 데이터: 005930(삼성전자), 091990(셀트리온헬스케어) 등
* 각종 지수: KS11(코스피지수), KQ11(코스닥지수), DJI(다우지수), IXIC(나스닥 지수), US500(S&P 5000)
* 환율 데이터: USD/KRX (원달러 환율), USD/EUR(달러당 유로화 환율), CNY/KRW: 위엔화 원화 환율
* 암호화폐 가격: BTC/USD (비트코인 달러 가격, Bitfinex), BTC/KRW (비트코인 원화 가격, 빗썸)
* 거래소별 전체 종목 코드: KRX (KOSPI, KODAQ, KONEX), NASDAQ, NYSE, AMEX, S&P 500 종목

FinanceDataReader 심볼 리스트는 다음 문서에 정리되어 있다. (빠른 참조)
* http://nbviewer.jupyter.org/540b4c74a898bbe1af8715926eed24f8


# Install

```bash
pip install -U finance-datareader
```


# Usage

```python
import FinanceDataReader as fdr

# 애플(AAPL), 2017년~현재
df = fdr.DataReader('AAPL', '2017')

# 아마존(AMZN), 2010~현재
df = fdr.DataReader('AMZN', '2010')

# 셀트리온(068270), 2017년~현재
df = fdr.DataReader('068270', '2017')

# KS11 (KOSPI 지수), 2015년~현재
df = fdr.DataReader('KS11', '2015')

# 다우지수, 2015년~현재
df = fdr.DataReader('DJI', '2015')

# 원달러 환율, 1995년~현재
df = fdr.DataReader('USD/KRW', '1995')

# 비트코인 원화 가격 (빗썸), 2016년~현재
df = fdr.DataReader('BTC/KRW', '2016')

# 한국거래소 상장종목과 코드명 전체
df_krx = fdr.StockListing('KRX')

# S&P 500 종목과 코드명 전체
df_spx = fdr.StockListing('S&P500')
```


# Changes
2018-05-17 v0.4.0
* pip install (packaging register The Python Package Index (PyPI) repository)

2018-05-17 v0.2.0
* StockListing, SP500 (S&P 500 Listings, wikipedia), 추가

2018-05-16 v0.1.0
* StockListing KRX, KOSPI, KODAQ, KONEX, 추가 
* StockListing NASDAQ, NYSE, AMEX, 추가

2018-05-14 v0.0.1
* DataReader 국내/매국 주가 데이터, 추가



#### 2018 [FinanceData.KR](http://financedata.kr)