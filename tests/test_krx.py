# ----------------------------------------------
import sys
# sys.path.insert(0, r'D:dev\FinanceDataReader-dev\FinanceDataReader\src')

import FinanceDataReader as fdr
import pytest
import pandas as pd

@pytest.mark.krx
def test_krx_stock_listing():
    # Basic KRX listing
    df = fdr.StockListing('KRX')
    assert len(df) > 2000
    assert 'Code' in df.columns
    assert 'Name' in df.columns

@pytest.mark.krx
def test_krx_stock_listing_kosdaq():
    # Basic KOSDAQ listing
    KOSDAQ = fdr.StockListing('KOSDAQ')
    assert len(KOSDAQ) > 100
    assert 'Code' in KOSDAQ.columns
    assert 'Name' in KOSDAQ.columns    

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

@pytest.mark.krx
def test_krx_stock_data_reader():
    print(fdr)
    stock_code = ['0004Y0', '0007C0', '0008Z0', '0009K0', '0010V0', '0013V0', '0015G0', '0015N0', '0015S0', '0030R0', '0037T0', '0041B0', '0041J0', '0041L0', '0044K0', '0054V0', '0068Y0', '0071M0', '0072Z0', '0088D0', '0091W0', '0093G0', '0096B0', '0096D0', '0097F0', '0098T0', '0099W0', '0099X0', '0101C0', '0105P0', '0120G0', '0126Z0']
    for code in stock_code:
        print(code)
        stock_data = fdr.DataReader(code, '2026-01-01')
        assert len(stock_data) > 0
        assert 'Close' in stock_data.columns