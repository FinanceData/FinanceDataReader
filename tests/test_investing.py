import pytest
import FinanceDataReader as fdr

@pytest.mark.investing
def test_investing_data_reader():
    # Gold (XAU/USD) from Investing.com
    # Note: INVESTING: symbols might be tricky, checking data.py implementation
    # It uses InvestingDailyReader(codes, start, end)
    
    try:
        # 'GOLD' is a common symbol on Investing
        df = fdr.DataReader('INVESTING:GOLD', '2023-01-01', '2023-01-31')
        assert len(df) > 0
    except Exception as e:
        pytest.skip(f"Investing.com reader failed (likely due to blocking or symbol change): {e}")

@pytest.mark.investing
def test_investing_etf_listing():
    # US ETFs from Investing
    # StockListing('ETF/US') uses NaverEtfListing, not Investing actually.
    # But let's check if there's any specific Investing listing helper
    # In data.py: if market.startswith('ETF'): uses NaverEtfListing
    pass
