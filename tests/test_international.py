import pytest
import FinanceDataReader as fdr

@pytest.mark.international
def test_market_listing_sse():
    # Shanghai
    df = fdr.StockListing('SSE')
    assert len(df) > 1000

@pytest.mark.international
def test_market_listing_hkex():
    # Hong Kong
    df = fdr.StockListing('HKEX')
    assert len(df) > 2000

@pytest.mark.international
def test_market_listing_tse():
    # Tokyo
    df = fdr.StockListing('TSE')
    assert len(df) > 3000

@pytest.mark.international
def test_market_listing_hose():
    # Ho Chi Minh
    df = fdr.StockListing('HOSE')
    assert len(df) > 300

@pytest.mark.international
def test_data_reader_international():
    # Toyota from Tokyo
    df = fdr.DataReader('TSE:7203', '2023-01-01', '2023-01-31')
    assert len(df) > 0

    # Softbank from Tokyo
    df = fdr.DataReader('TSE:9984', '2023-01-01', '2023-01-31')
    assert len(df) > 0

    # Vietnam stock
    df = fdr.DataReader('HOSE:VCB', '2023-01-01', '2023-01-31')
    assert len(df) > 0

@pytest.mark.international
def test_exchange_rate():
    # Currency
    df = fdr.DataReader('USD/KRW', '2023-01-01', '2023-01-31')
    assert len(df) > 0
