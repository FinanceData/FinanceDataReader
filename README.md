# FinanceDataReader
Financial price data reader (an alternative to google finance and yahoo finance in pandas-datareader)

(pandas-datareader가 야후 파이낸스와 구글 파이낸스를 더 이상 지원하지 않게됨에 따라, 동일한 수준의 편의성을 지원하기 위해 제작)


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
