{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "204aeedd",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import requests\n",
    "import pandas as pd\n",
    "from io import StringIO\n",
    "from FinanceDataReader._utils import (_convert_letter_to_num, _validate_dates)\n",
    "\n",
    "class Reader:\n",
    "    def __init__(self, symbol, start=None, end=None, exchange=None, data_source=None):\n",
    "        self.symbol = symbol\n",
    "        start, end = _validate_dates(start, end)\n",
    "        self.start = start\n",
    "        self.end = end\n",
    "\n",
    "    def read(self):\n",
    "        url = 'https://fchart.stock.naver.com/sise.nhn?timeframe=day&count=6000&requestType=0&symbol='\n",
    "        r = requests.get(url + self.symbol)\n",
    "\n",
    "        data_list = re.findall('<item data=\\\"(.*?)\\\" />', r.text, re.DOTALL)\n",
    "        if len(data_list) == 0:\n",
    "            return pd.DataFrame()\n",
    "        data = '\\n'.join(data_list)\n",
    "        df = pd.read_csv(StringIO(data), delimiter='|', header=None, dtype={0:str})\n",
    "        df.columns  = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']\n",
    "        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')\n",
    "        df.set_index('Date', inplace=True)\n",
    "        df.sort_index(inplace=True)\n",
    "        df['Change'] = df['Close'].pct_change()\n",
    "\n",
    "        return df.loc[self.start:self.end]\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
