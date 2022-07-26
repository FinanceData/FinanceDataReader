import re
from datetime import datetime
from pandas import DataFrame, to_datetime


def _convert_letter_to_num(str_num):
    powers = {'B': 10 ** 9, 'M': 10 ** 6, 'K': 10 ** 3, '': 1}
    m = re.search("([0-9\.]+)(M|B|K|)", str_num)
    if m:
        val = m.group(1)
        mag = m.group(2)
        return float(val) * powers[mag]
    return 0.0


def _validate_dates(start, end):
    start = to_datetime(start)
    end = to_datetime(end)

    if start is None:
        start = datetime(1970, 1, 1)
    if end is None:
        end = datetime.today()
    return start, end


def _filter_by_date(df: DataFrame, start, end):
    """
    Retrieves a dataframe based on a given start and end date.

    :param df: an original dataframe
    :param start: start date
    :param end: end date
    """
    date_query = 'index>=%r and index<=%r'
    filtered_df = df.query(date_query % (start, end))
    return filtered_df


def _replace_ohl_0_with_c(df: DataFrame):
    """
    Due to events such as stock split,
    if there is a row with no trading volume
    and the closing price of the previous day is maintained,
    it is replaced with an ohl value.

    :param df: an original dataframe
    """
    is_trading_holiday = df['Volume'] == 0

    replace_target_columns = ['Open', 'High', 'Low']
    replace_value = df['Close']

    df.loc[is_trading_holiday, replace_target_columns] = replace_value
    return df
