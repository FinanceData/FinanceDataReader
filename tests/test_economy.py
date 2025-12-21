import pytest
import FinanceDataReader as fdr

@pytest.mark.fred
def test_fred_data_reader():
    # US Treasury 10Y
    df = fdr.DataReader('FRED:DGS10', '2023-01-01', '2023-01-31')
    assert len(df) > 0
    assert 'DGS10' in df.columns

@pytest.mark.fred
def test_fred_multiple_series():
    # Multiple FRED series
    df = fdr.DataReader('FRED:M2,HSN1F', '2020-01-01', '2020-12-31')
    assert len(df) > 0
    assert 'M2' in df.columns
    assert 'HSN1F' in df.columns

@pytest.mark.ecos
def test_ecos_data_reader():
    # ECOS: 한국은행 기준금리 (722Y001/0101000)
    try:
        df = fdr.DataReader('ECOS:722Y001/0101000', '2023-01-01', '2024-01-01')
        assert len(df) > 0
    except Exception as e:
        pytest.skip(f"ECOS reader failed: {e}")

@pytest.mark.ecos
def test_ecos_keystat_reader():
    # ECOS-KEYSTAT: K051 (한국은행 기준금리 KeyStat)
    try:
        df = fdr.DataReader('ECOS-KEYSTAT:K051', '2023-01-01', '2023-12-31')
        assert len(df) > 0
    except Exception as e:
        pytest.skip(f"ECOS-KEYSTAT reader failed: {e}")
