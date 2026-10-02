from datetime import datetime
from urllib.parse import parse_qs, urlparse

import pandas as pd
import pytest

import FinanceDataReader as fdr
from FinanceDataReader.yahoo.data import YahooDailyReader


COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']


def chart_response(timestamps, rows):
    fields = ['open', 'high', 'low', 'close', 'volume', 'adjclose']
    values = dict(zip(fields, zip(*rows)))
    values = {key: list(value) for key, value in values.items()}
    return {
        'chart': {
            'result': [{
                'timestamp': [int(pd.Timestamp(value, tz='UTC').timestamp())
                              for value in timestamps],
                'indicators': {
                    'quote': [{key: values[key] for key in fields[:-1]}],
                    'adjclose': [{'adjclose': values['adjclose']}],
                },
            }],
            'error': None,
        },
    }


def mock_charts(monkeypatch, responses):
    requested = []

    def get(url, headers):
        requested.append(url)
        symbol = urlparse(url).path.rsplit('/', 1)[-1]
        response = responses[symbol]

        class Response:
            def raise_for_status(self):
                pass

            def json(self):
                return response

        return Response()

    monkeypatch.setattr('FinanceDataReader.yahoo.data.requests.get', get)
    return requested


@pytest.mark.parametrize('last_timestamp', [
    '2026-03-20 20:00:00',
    '2026-03-20 13:30:00',
])
def test_yahoo_daily_retains_last_row_for_duplicate_date(monkeypatch, last_timestamp):
    rows = [
        [21871.039062, 22187.060547, 21851.050781, 22090.689453,
         8547870000, 22090.689453],
        [21989.330078, 21997.089844, 21522.750000, 21647.609375,
         11743490000, 21647.609375],
        [21989.332031, 21997.089844, 21522.750000, 21647.611328,
         10441715000, 21647.611328],
    ]
    response = chart_response([
        '2026-03-19 13:30:00', '2026-03-20 13:30:00', last_timestamp,
    ], rows)
    mock_charts(monkeypatch, {'^IXIC': response})

    actual = YahooDailyReader('^IXIC', '2026-03-19', '2026-03-21').read()
    expected = pd.DataFrame([rows[0], rows[2]], columns=COLUMNS,
                            index=pd.to_datetime(['2026-03-19', '2026-03-20']))
    pd.testing.assert_frame_equal(actual, expected, check_index_type=False)
    assert actual.index.is_unique


def test_yahoo_multiple_symbols_align_duplicate_dates(monkeypatch):
    mock_charts(monkeypatch, {
        'AAPL': chart_response([
            '2026-03-19 13:30:00', '2026-03-20 13:30:00', '2026-03-20 20:00:00',
        ], [[1, 2, 0, 1, 10, 1], [2, 3, 1, 2, 20, 2], [3, 4, 2, 3, 30, 3]]),
        'MSFT': chart_response([
            '2026-03-20 13:30:00', '2026-03-23 13:30:00',
        ], [[5, 6, 4, 5, 50, 5], [6, 7, 5, 6, 60, 6]]),
    })

    actual = fdr.DataReader('YAHOO:AAPL,MSFT', '2026-03-19', '2026-03-24')
    expected = pd.DataFrame({'AAPL': [1.0, 3.0, float('nan')],
                             'MSFT': [float('nan'), 5.0, 6.0]},
                            index=pd.to_datetime(['2026-03-19', '2026-03-20', '2026-03-23']))
    pd.testing.assert_frame_equal(actual, expected, check_index_type=False, check_freq=False)
    assert actual.index.is_unique
    assert actual.attrs == {'exchange': '', 'source': 'YAHOO', 'data': 'PRICE'}


def test_yahoo_unique_dates_and_request_bounds_are_preserved(monkeypatch):
    rows = [[1, 2, 0, 1, 10, 1], [2, 3, 1, 2, 20, 2]]
    requested = mock_charts(monkeypatch, {
        'AAPL': chart_response(['2026-03-19 13:30:00', '2026-03-20 13:30:00'], rows),
    })

    actual = YahooDailyReader('AAPL', '2026-03-19', '2026-03-21').read()
    expected = pd.DataFrame(rows, columns=COLUMNS,
                            index=pd.to_datetime(['2026-03-19', '2026-03-20']))
    pd.testing.assert_frame_equal(actual, expected, check_index_type=False)
    query = parse_qs(urlparse(requested[0]).query)
    assert datetime.fromtimestamp(int(query['period1'][0])) == datetime(2026, 3, 19)
    assert datetime.fromtimestamp(int(query['period2'][0])) == datetime(2026, 3, 21)
    assert query['interval'] == ['1d']


def test_yahoo_single_day_request_keeps_next_day_end_boundary(monkeypatch):
    rows = [[2, 3, 1, 2, 20, 2], [3, 4, 2, 3, 30, 3]]
    requested = mock_charts(monkeypatch, {
        'AAPL': chart_response(['2026-03-20 13:30:00', '2026-03-20 20:00:00'], rows),
    })

    actual = YahooDailyReader('AAPL', '2026-03-20', '2026-03-20').read()
    expected = pd.DataFrame([rows[-1]], columns=COLUMNS,
                            index=pd.to_datetime(['2026-03-20']))
    pd.testing.assert_frame_equal(actual, expected, check_index_type=False)
    query = parse_qs(urlparse(requested[0]).query)
    assert datetime.fromtimestamp(int(query['period1'][0])) == datetime(2026, 3, 20)
    assert datetime.fromtimestamp(int(query['period2'][0])) == datetime(2026, 3, 21)
