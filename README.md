# FinanceDataReader
Financial price data reader (an alternative to google finance and yahoo finance in pandas-datareader)

## nstall
```
pip install finance-datareader
```


## Usage

```python
import FinanceDataReader as fdr

df = fdr.DataReader('105560', '2017') # just only year
df = fdr.DataReader('105560', '2018-01-01') # '2018-01-01' ~ today 
df = fdr.DataReader('105560', '2018-01-01', '2018-03-30') # '2018-01-01' ~ '2018-03-30' 

df.head()
```
