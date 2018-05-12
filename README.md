# FinanceDataReader
Financial price data reader (an alternative to google finance and yahoo finance in pandas-datareader)

## Install
```
pip install finance-datareader
```


## Usage

```python
import FinanceDataReader as fdr
```

## Examples
```python
df = fdr.DataReader('AAPL', '2017') # AAPL price data 2017

df = fdr.DataReader('GOOG', '2018-01-01') # Alphabet Inc Class C, 2018-01-01 ~ today
```

## Examples
```python
# 105560 (KRX: KB Finance Group)

df = fdr.DataReader('105560', '2017') # year 2017

df = fdr.DataReader('105560', '2018-01-01') # '2018-01-01' ~ today 

df = fdr.DataReader('105560', '2018-01-01', '2018-03-30') # '2018-01-01' ~ '2018-03-30' 
```
