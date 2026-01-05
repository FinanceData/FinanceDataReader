# import sys
# sys.path.insert(0, r'G:\내 드라이브\g_dev\FinanceDataReader-dev\FinanceDataReader\src')

import pytest
import FinanceDataReader as fdr

@pytest.mark.snap
def test_snap_krx_indices():
    # KRX Index List
    df = fdr.SnapDataReader('KRX/INDEX/LIST')
    assert len(df) > 100

@pytest.mark.snap
def test_snap_krx_index_stocks():
    # KOSPI Index Stocks (1001)
    df = fdr.SnapDataReader('KRX/INDEX/STOCK/1001')
    assert len(df) >= 200

@pytest.mark.snap
def test_snap_naver_finstate():
    # Naver Finance State (Samsung)
    df = fdr.SnapDataReader('NAVER/FINSTATE/005930')
    assert len(df) > 0

@pytest.mark.snap
def test_snap_ecos_keystat():
    # ECOS Key Statistics List
    try:
        df = fdr.SnapDataReader('ECOS/KEYSTAT/LIST')
        assert len(df) > 50
    except Exception as e:
        pytest.skip(f"ECOS Snap reader failed: {e}")
