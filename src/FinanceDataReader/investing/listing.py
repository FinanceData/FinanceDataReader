import pandas as pd
import requests
from bs4 import BeautifulSoup

from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)

class InvestingEtfListing:
    def __init__(self, country):
        self.country = country.upper()
        
    def read(self):
        country_map = {
            'US':'usa', 'CN':'china', 
            'HK':'hong-kong', 'JP':'japan', 
            'UK':'uk', 'FR':'france', 
        }
        if self.country not in country_map.keys():
            msg = "country unsupported. support countries:" + str(list(country_map.keys()))
            raise ValueError(msg)

        headers = { 'User-Agent':'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/98.0.4758.109', }
        url = 'https://kr.investing.com/etfs/' + country_map[self.country] + '-etfs'
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        table = soup.find('table', id='etfs')

        values = []
        trs = table.tbody.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            sym = tds[2].text
            name = tds[1].text
            values.append([sym, name])

        df = pd.DataFrame(values, columns=['Symbol', 'Name'])  
        return df
