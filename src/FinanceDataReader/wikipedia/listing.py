import pandas as pd
import random
import requests

from io import StringIO

class WikipediaStockListing:
    def __init__(self, market):
        self.market = market
    
    def read(self):
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

        user_agents = [
            # Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            # Safari (Mac)
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/16.4 Safari/605.1.15",
            # Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
            # Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
            # iPhone Safari
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 "
            "(KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        ]

        headers = {
            "User-Agent" : random.choice(user_agents)
        }

        res = requests.get(url, headers = headers)
        res.raise_for_status()

        html = StringIO(res.text)
        df = pd.read_html(html, header=0)[0]

        cols_ren = {
            'Security':'Name',
            'Ticker symbol':'Symbol',
            'GICS Sector':'Sector',
            'GICS Sub-Industry':'Industry'
        }
        df = df.rename(columns = cols_ren)
        df = df[['Symbol', 'Name', 'Sector', 'Industry']]
        df['Symbol'] = df['Symbol'].str.replace('.', '', regex=False)

        return df
