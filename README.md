# FinanceDataReader
[FinanceData.KR](https://financedata.github.io/) Open Source Financial data reader

# Overview
The FinanceDataReader is financial data reader(crawler) for finance. <br>
The main functions are as follows.

* KRX Stock Symbol listings: 'KRX', 'KOSPI', 'KODAQ', 'KONEX'
* Global Stock Symbol listings: 'NASDAQ', 'NYSE', 'AMEX' and 'S&P500', 'SSE'(상해), 'SZSE'(심천), 'HKEX'(홍콩), 'TSE'(도쿄)
* KRX delistings: 'KRX-DELISTING'(상장폐지종목), 'KRX-ADMINISTRATIVE' (관리종목)
* ETF Symbol listings(for multiple countries): 'KR', 'US', 'JP'
* Stock price(KRX): '005930'(Samsung), '091990'(Celltrion Healthcare) ...
* Stock price(Word wide): 'AAPL', 'AMZN', 'GOOG' ... (you can specify exchange(market) and symbol)
* Indexes: 'KS11'(코스피지수), 'KQ11'(코스닥지수), 'DJI'(다우존스지수), 'IXIC'(나스닥지수), 'US500'(S&P 500지수) ...
* Exchanges: 'USD/KRX', 'USD/EUR', 'CNY/KRW' ... (조합가능한 화폐별 환율 데이터 일자별)
* Cryptocurrency price data: 'BTC/USD' (Bitfinex), 'BTC/KRW' (Bithumb)

    
# Install

```bash
pip install finance-datareader
```

# Quick Start

```python
import FinanceDataReader as fdr

# 삼성전자(005930) 전체 (1996-11-05 ~ 현재)
df = fdr.DataReader('005930')

# Apple(AAPL), 2017-01-01 ~ Now
df = fdr.DataReader('AAPL', '2017')

# Ford(F), 1980-01-01 ~ 2019-12-30 (40년 데이터)
df = fdr.DataReader('F', '1980-01-01', '2019-12-30')

# AMAZON(AMZN), 2017 (1년)
df = fdr.DataReader('AMZN', '2017-01-01', '2019-12-31')

# Samsung(005930), 2000-01-01 ~ 2019-12-31
df = fdr.DataReader('068270', '2000-01-01', '2019-12-31')

# country code: ex) 000150: Doosan(KR), Yihua Healthcare(CN)
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30') # KRX
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='KRX') # KRX (위와 동일)
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='SZSE') # SZSE
df = fdr.DataReader('000150', '2018-01-01', '2019-10-30', exchange='심천') # SZSE

# TSE (도쿄증권거래소)
fdr.DataReader('7203', '2020-01-01', exchange='TSE') # 토요타 자동차(7203)
fdr.DataReader('9984', '2020-01-01', exchange='TSE') # 소프트뱅크그룹(9984)

# HOSE (호치민증권거래소)
fdr.DataReader('VCB', '2020-01-01', exchange='HOSE') # 베트남 무역은행(VCB)
fdr.DataReader('VIC', '2020-01-01', exchange='HOSE') # Vingroup (JSC)

# AMEX(아메리카증권거래소)
fdr.DataReader('LNG', '2020-01-01', exchange='AMEX') # Cheniere Energy (LNG)
fdr.DataReader('CBOE', '2020-01-01', exchange='AMEX') # Cboe Global Markets (CBOE)

# KRX delisting stock data 상장폐지된 종목 가격 데이터 (상장일~상장폐지일)
df = fdr.DataReader('036360', exchange='KRX-DELISTING')

# KOSPI index, 2015 ~ Now
ks11 = fdr.DataReader('KS11', '2015-01-01')

# Indexes, 2015 ~ Now
dji = fdr.DataReader('DJI', '2015-01-01') # Dow Jones Industrial(DJI)
sp = fdr.DataReader('US500', '2015-01-01') # S&P 500 지수 (NYSE)

# FX 환율, 1995 ~ 현재
usdkrw = fdr.DataReader('USD/KRW', '1995-01-01') # 달러 원화
usdeur = fdr.DataReader('USD/EUR', '1995-01-01') # 달러 유로화
usdcny = fdr.DataReader('USD/CNY', '1995-01-01') # 달러 위엔화

# 상품 선물 가격 데이터
df = fdr.DataReader('NG') # NG 천연가스 선물 (NYMEX)
df = fdr.DataReader('ZG') # 금 선물 (ICE)
df = fdr.DataReader('ZI') # 은 선물 (ICE)
df = fdr.DataReader('HG') # 구리 선물 (COMEX)

# Bitcoin KRW price (Bithumbs), 2016 ~ Now
btc = fdr.DataReader('BTC/KRW', '2016-01-01')

# 채권 수익률
df = fdr.DataReader('KR1YT=RR') # 1년만기 한국국채 수익률
df = fdr.DataReader('KR10YT=RR') # 10년만기 한국국채 수익률

df = fdr.DataReader('US1MT=X') # 1개월 만기 미국국채 수익률
df = fdr.DataReader('US10YT=X') # 10년 만기 미국국채 수익률

# KRX stock symbol list
stocks = fdr.StockListing('KRX') # 코스피, 코스닥, 코넥스 전체
stocks = fdr.StockListing('KOSPI') # 코스피
stocks = fdr.StockListing('KOSDAQ') # 코스닥
stocks = fdr.StockListing('KONEX') # 코넥스

# NYSE, NASDAQ, AMEX stock symbol list
stocks = fdr.StockListing('NYSE')   # 뉴욕거래소
stocks = fdr.StockListing('NASDAQ') # 나스닥
stocks = fdr.StockListing('AMEX')   # 아멕스

# S&P 500 symbol list
sp500 = fdr.StockListing('S&P500')

# 기타 주요 거래소 상장종목 리스트
stocks = fdr.StockListing('SSE') # 상해 거래소
stocks = fdr.StockListing('SZSE') # 신천 거래소
stocks = fdr.StockListing('HKEX') # 홍콩거래소
stocks = fdr.StockListing('TSE') # 도쿄 증권거래소
stocks = fdr.StockListing('HOSE') # 호치민 증권거래소

# KRX stock delisting symbol list 상장폐지 종목 전체 리스트
krx_delisting = fdr.StockListing('KRX-DELISTING')

# KRX stock delisting symbol list and names 관리종목 리스트
krx_adm = fdr.StockListing('KRX-ADMINISTRATIVE') # 관리종목


# FRED 데이터
m2 = fdr.DataReader('M2', data_source='fred') #  M2통화량
nq = fdr.DataReader('NASDAQCOM', data_source='fred') # NASDAQCOM 나스닥종합지수
hou_nas = fdr.DataReader(['HSN1F', 'NASDAQCOM'], data_source='fred') # HSN1F 주택판매지수, NASDAQCOM 나스닥종합지수 

# 캔들차트 그리기
df = fdr.DataReader('005930', '2021-01-01', '2021-02-15')

fdr.chart.plot(df)
fdr.chart.plot(df, title='삼성전자(005930)')

# 차트 설정
config = {'title':'fdr.chart.config()를 사용하여 설정을 한번에 지정할 수 있습니다', 
          'width': 600, 
          'height': 300,
          'volume': True,
}

fdr.chart.config(config=config)
fdr.chart.plot(df)

```

## Using FinanceDataReader
* [Users-Guide](https://github.com/FinanceData/FinanceDataReader/wiki/Users-Guide)
* [Quick-Reference (Symbol List)](https://github.com/FinanceData/FinanceDataReader/wiki/Quick-Reference)

## Tutorials
* [FRED 주요 경기 선행 지표](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20FRED%20%EA%B2%BD%EA%B8%B0%20%EC%84%A0%ED%96%89%20%EC%A7%80%ED%91%9C.ipynb)
* [수정주가(Adjusted Price)란?](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%88%98%EC%A0%95%EC%A3%BC%EA%B0%80.ipynb)
* [여러 종목 가격을 한번에](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%97%AC%EB%9F%AC%20%EC%A2%85%EB%AA%A9%EC%9D%98%20%EA%B0%80%EA%B2%A9%EC%9D%84%20%ED%95%9C%EB%B2%88%EC%97%90.ipynb)
* [VIX 지수와 관련 종목](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20VIX%20%EC%A7%80%EC%88%98%EC%99%80%20%EA%B4%80%EB%A0%A8%20%EC%A2%85%EB%AA%A9.ipynb)
* [섹터 평균 수익률과 개별 종목의 수익률 구하기](https://nbviewer.jupyter.org/github/FinanceData/FinanceDataReader/blob/master/tutorial/FinanceDataReader%20Tutorial%20-%20%EC%84%B9%ED%84%B0%20%ED%8F%89%EA%B7%A0%20%EC%88%98%EC%9D%B5%EB%A5%A0%EA%B3%BC%20%EA%B0%9C%EB%B3%84%20%EC%A2%85%EB%AA%A9%EC%9D%98%20%EC%88%98%EC%9D%B5%EB%A5%A0.ipynb)
* [차트 그리기와 활용하기](http://nbviewer.jupyter.org/c6c336c4727386810bec9264e81f6bba)



## FinanceDataReader Notebooks
* [S&P500 가격 데이터 수집과 수익률 분석](https://nbviewer.jupyter.org/710b8f0a4bd9a8df91ae1be6c7e838b1) 
* [S&P500 팩터 데이터 수집과 분석](https://nbviewer.jupyter.org/35a1b0d5248bc9b09513e53be437ac42) 


#### 2018-2020 [FinanceData.KR](http://financedata.kr)
