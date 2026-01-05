# import sys
# sys.path.insert(0, r'G:\내 드라이브\g_dev\FinanceDataReader-dev\FinanceDataReader\src')

import pytest
import FinanceDataReader as fdr

@pytest.mark.us
def test_us_stock_listing_nasdaq():
    df = fdr.StockListing('NASDAQ')
    assert len(df) > 3000
    assert 'Symbol' in df.columns

@pytest.mark.us
def test_us_stock_listing_nyse():
    df = fdr.StockListing('NYSE')
    assert len(df) > 2000

@pytest.mark.us
def test_us_sp500_listing():
    df = fdr.StockListing('S&P500')
    assert len(df) >= 500
    assert 'Symbol' in df.columns

@pytest.mark.us
def test_us_data_reader_yahoo():
    # Apple from Yahoo (Default source for US)
    df = fdr.DataReader('AAPL', '2023-01-01', '2023-01-31')
    assert len(df) > 0
    assert 'Close' in df.columns

@pytest.mark.us
def test_us_major_indices():
    # S&P 500 Index
    df = fdr.DataReader('US500', '2023-01-01', '2023-01-31')
    assert len(df) > 0

    # NASDAQ Index
    df = fdr.DataReader('IXIC', '2023-01-01', '2023-01-31')
    assert len(df) > 0

    # Dow Jones
    df = fdr.DataReader('DJI', '2023-01-01', '2023-01-31')
    assert len(df) > 0
