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
# AAPL price data 2017
df = fdr.DataReader('AAPL', '2017') 

# Alphabet Inc Class C, 2018-01-01 ~ today
df = fdr.DataReader('GOOG', '2018-01-01') 
```

## Examples
```python
# 105560 (KRX: KB Finance Group)

# year 2017
df = fdr.DataReader('105560', '2017') 

# '2018-01-01' ~ today 
df = fdr.DataReader('105560', '2018-01-01') 

# '2018-01-01' ~ '2018-03-30'
df = fdr.DataReader('105560', '2018-01-01', '2018-03-30')  
```
