import re
import pandas as pd

from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class NasdaqStockListing:
    def __init__(self, market):
        self.market = market
        
    def read(self):
        url = 'http://old.nasdaq.com/screening/companies-by-name.aspx?' \
                'letter=0&render=download&exchange=' + self.market.lower()
        df = pd.read_csv(url)
        df['MarketCap'] = df['MarketCap'].fillna('')
        df['MarketCap'] = df['MarketCap'].apply(_convert_letter_to_num)
        df = df.sort_values('MarketCap', ascending=False)
        df = df.drop('Unnamed: 8', axis=1)
        df = df.reset_index(drop=True)
        df = df.rename(columns={'industry':'Industry'})
        return df[['Symbol', 'Name', 'Sector', 'Industry']]
