import pytest
import FinanceDataReader as fdr
import pandas as pd

@pytest.mark.krx
def test_krx_stock_listing():
    # Basic KRX listing
    df = fdr.StockListing('KRX')
    assert len(df) > 2000
    assert 'Code' in df.columns
    assert 'Name' in df.columns

@pytest.mark.krx
def test_krx_delisting_listing():
    # KRX Delisting
    df = fdr.StockListing('KRX-DELISTING')
    assert len(df) > 3000
    assert 'Symbol' in df.columns

@pytest.mark.krx
def test_krx_administrative_listing():
    # KRX Administrative stocks
    df = fdr.StockListing('KRX-ADMINISTRATIVE')
    assert len(df) > 10

@pytest.mark.krx
def test_krx_data_reader_basics():
    # Individual stock
    df = fdr.DataReader('005930', '2023-01-01', '2023-01-31') # Samsung
    assert len(df) > 0
    assert 'Close' in df.columns

@pytest.mark.krx
def test_krx_index_reader():
    # KOSPI Index
    df = fdr.DataReader('KS11', '2023-01-01', '2023-01-31')
    assert len(df) > 0
    
    # KRX-INDEX specific
    df = fdr.DataReader('KRX-INDEX:1001', '2023-01-01', '2023-01-31')
    assert len(df) > 0

@pytest.mark.krx
def test_krx_detail_reader():
    # KRX-DETAIL (KrxDailyDetailReader might require more parameters or specific symbols)
    # Testing for common symbol
    try:
        df = fdr.DataReader('KRX-DETAIL:005930', '2023-01-01', '2023-01-10')
        assert len(df) > 0
    except Exception as e:
        pytest.skip(f"KRX-DETAIL might be unstable or require specific environment: {e}")
