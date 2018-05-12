# FinanceDataReader
Financial price data reader (an alternative to google finance and yahoo finance in pandas-datareader)

[pandas_datareader](https://pandas-datareader.readthedocs.io)로 다양한 시계열 데이터들을 손쉽게 가져올 수 있다. 특히, 개별 종목의 과거 주식 가격을 가져오기 위해 구글 파이낸스와 야후 파이낸스를 많이 사용했다. 그러나, 현재 구글 파이낸스는 UNSTABLE_WARNING 를 내고, 야후 파이낸스는 더 이상 사용되지 않는다 (deprecated). 2018년 4월 현재 버전은 (pandas 0.22.0, pandas_datareader 0.6.0) 이다. <br>

FinanceDataReader는 [pandas_datareader](https://pandas-datareader.readthedocs.io)의 구글 파이낸스와 야후 파이낸스의 개별종목 데이터 가져오기 기능을 대체하기 위해 만들어졌다.


## 설치
```
pip install finance-datareader
```

## 사용법

```python
import FinanceDataReader as fdr
```

## 예제

미국주식 종목
```python
# year 2017 (Apple)
df = fdr.DataReader('AAPL', '2017') 

# 2018-01-01 ~ today (Alphabet)
df = fdr.DataReader('GOOG', '2018-01-01') 
```

한국거래소(KRX) 종목

```python
# year 2017 (KB금융, 105560)
df = fdr.DataReader('105560', '2017') 

# '2018-01-01' ~ today (셀트리온, 068270)
df = fdr.DataReader('068270', '2018-01-01') 

# '2018-01-01' ~ '2018-03-30' (SK하이닉스, 000660)
df = fdr.DataReader('105560', '2017-01-01', '2018-03-30') 
```
