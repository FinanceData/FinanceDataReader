import re
from datetime import datetime
import pandas as pd

def _convert_letter_to_num(str_num):
    powers = {'B': 10 ** 9, 'M': 10 ** 6, 'K': 10 ** 3, '': 1}
    m = re.search(r"([0-9\.]+)(M|B|K|)", str_num)
    if m:
        val = m.group(1)
        mag = m.group(2)
        return float(val) * powers[mag]
    return 0.0

def _validate_dates(start, end):
    start = pd.to_datetime(start) if start else datetime(1980, 1, 1)
    end = pd.to_datetime(end) if end else datetime.today()
    return start, end
