import pytest
import FinanceDataReader as fdr
import pandas as pd

@pytest.mark.krx
def test_krx_daily():
    '''개별 종목'''
    df = fdr.DataReader('KRX:005930') # 삼성전자(005930) 1995-05-02 ~ 현재
    assert len(df) > 100

    df = fdr.DataReader('KRX:005930', '2023') # 삼성전자(005930) 2023-01-01 ~ 현재
    assert len(df) > 100

@pytest.mark.krx
def test_krx_major_index():
    '''주요 지수'''
    df = fdr.DataReader('KS11') # KOSPI지수: 2001-06-11 ~ 현재
    assert len(df) > 5500
    assert df.loc['2001-06-11', 'Close'] == 608.23

    df = fdr.DataReader('KOSPI') # KOSPI 지수: 2001-06-11 ~ 현재
    assert len(df) > 5500
    assert df.loc['2001-06-11', 'Close'] == 608.23

    df = fdr.DataReader('KOSPI', '2020-01-02') # KOSPI 지수: 2020-01-02 ~ 현재
    assert len(df) > 100
    assert df.loc['2020-01-02', 'Close'] == 2175.17

    df = fdr.DataReader('KOSDAQ', '2020-01-02') # KOSDAQ 지수: 2020-01-02 ~ 현재
    assert df.loc['2020-01-02', 'Close'] == 674.02

    df = fdr.DataReader('kospi', '2020-01-02') # KOSPI 지수: 2020-01-02 ~ 현재
    assert len(df) > 100
    assert df.loc['2020-01-02', 'Close'] == 2175.17

    df = fdr.DataReader('KS200', '2020-01-02') # KOSPI200 지수: 2020-01-02 ~ 현재
    assert len(df) > 100
    assert df.loc['2020-01-02', 'Close'] > 200

@pytest.mark.krx
def test_krx_index():
    df = fdr.DataReader('KRX-INDEX:1001', '2023') # 코스피지수
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1001', '2020-01-02', '2022-01-01') # KOSPI 지수: 2020-01-02 ~ 2022-01-01
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1028', '2023') # KOSPI200 지수: 2023-01-01 ~ 현재
    assert 280 < df.loc['2023-01-02', 'Close'] < 300

    df = fdr.DataReader('KRX-INDEX:2001', '2020-01-02', '2025-01-01') # KOSDAQ 지수: 2020-01-02 ~ 2025-01-01
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1001', '2020') # KOSPI 지수: 2020-01-01 ~ 현재
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1001', '2020') # KOSPI 지수: 2020-01-02 ~ 현재
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1001', '2020') # KOSPI 지수: 2020-01-01 ~ 현재
    assert len(df) > 100

    df = fdr.DataReader('KRX-INDEX:1101', '2023') # 없는코드 테스트
    assert len(df) == 0
    assert type(df) == pd.DataFrame

@pytest.mark.naver # NAVER unspecified (default)
def test_naver_daily():
    df = fdr.DataReader('005930') # 삼성전자(005930): ~현재 전체 (최대 6000 rows)
    assert len(df) == 6000

    df = fdr.DataReader('005930', '2023') # 삼성전자(005930): 2023-01-01 ~ 현재
    assert len(df) > 100

@pytest.mark.naver # NAVER specified
def test_naver_daily_source(): 
    df = fdr.DataReader('NAVER:005930') # 삼성전자(005930): ~현재 전체 (최대 6000 rows)
    assert len(df) == 6000

    df = fdr.DataReader('NAVER:005930', '2023') # 삼성전자(005930): 2023-01-01 ~ 현재
    assert len(df) > 100

@pytest.mark.naver # multiple stocks
def test_naver_multiple_stocks():
    df = fdr.DataReader('NAVER:005930, 000660', '2023') # 삼성전자(005930), SK하이닉스(000660) 종가: 2023-01-01 ~ 현재
    assert len(df) > 100

    df = fdr.DataReader('005930,000660', '1980-01-01')
    assert len(df) > 0

@pytest.mark.yahoo
def test_yahoo_us():
    df = fdr.DataReader('SPY', '2023-01-01') # SPDR S&P 500 (SPY) '2019-01-01' ~ 현재
    assert len(df) > 200
    assert round(df.loc['2023-01-03','Close'], 2) > 376

    df = fdr.DataReader('AAPL', '2018-01-01', '2018-12-31')
    assert len(df) > 100

    df = fdr.DataReader('F')
    print('\n', 'F', '\n', df.iloc[[-1],:])
    assert len(df) > 100

@pytest.mark.yahoo
def test_yahoo_hose():
    df = fdr.DataReader('HOSE:VCB')
    assert len(df) > 3700

    df = fdr.DataReader('HOSE:DAG')
    assert len(df) > 80

    df = fdr.DataReader('YAHOO:DAG.VN')
    assert len(df) > 80

    df = fdr.DataReader('yahoo:dag.vn')
    assert len(df) > 80

@pytest.mark.fred
def test_fred():
    df = fdr.DataReader('FRED:DEXKOUS', '1990')
    assert len(df) > 8000

    df = fdr.DataReader('FRED:NASDAQCOM') # 나스닥종합지수
    assert len(df) > 10000

@pytest.mark.fred
def test_fred_multiple():
    # M2통화량과 나스닥종합지수 
    df = fdr.DataReader('FRED:M2,HSN1F,NASDAQCOM')
    assert len(df) > 10000

    df = fdr.DataReader('FRED: M2 , HSN1F , NASDAQCOM')
    assert len(df) > 10000

@pytest.mark.pref
def test_pref_kr():
    # 영문자가 들어 있는 국내 종목코드 (우선주)
    df = fdr.DataReader('00104K', '2020-01-01') # CJ4우
    assert len(df) > 0

    df = fdr.DataReader('28513K', '2020-01-01') # SK케미칼우(28513K)
    assert len(df) > 0

@pytest.mark.pref
def test_pref_us():
    # 우선주(다른 CLASS)
    df = fdr.DataReader('ABR-PF', start='2020') # Arbor Realty Trust Pa Preferred
    assert len(df) > 0

@pytest.mark.krx_listings
def test_stocklistings():

    # KRX 상장회사(발행회사)목록 (가격 중심, 주식 종목) - 시가총액순
    # Code, ISU_CD, Name, Market, Dept, Close, ChangeCode, Changes, ChagesRatio, Open, High, Low, Volume, Amount, Marcap, Stocks, MarketId
    df = fdr.StockListing('KRX') # 2,700+ 종목 - 한국거래소(=코스피+코스닥+코넥스)
    assert len(df) > 2700

    df = fdr.StockListing('KRX-MARCAP') # KRX 와 동일
    assert len(df) > 2700

    df = fdr.StockListing('krx') # KRX 와 동일
    assert len(df) > 2700

    df = fdr.StockListing('KOSPI') # 900+ 종목 - 코스피 (주식, 부동산투자회사, 선박투자회사, 주식예탁증권)
    assert len(df) > 90

    df = fdr.StockListing('KOSDAQ') # 1600+ 종목 - 코스닥 (주식, 주식예탁증권)
    assert len(df) > 1600
    
    df = fdr.StockListing('KONEX') # 126 종목 - 코넥스 (주식)
    assert len(df) > 120

@pytest.mark.krx_listings
def test_stocklisting_desc():
    # KRX 전종목 목록 (설명 중심, 주식 + 펀드등 전종목)
    # Symbol, Market, Name, Sector, Industry, ListingDate, SettleMonth, Representative, HomePage, Region

    df = fdr.StockListing('KRX-DESC') # 한국거래소 전체 7000+ 종목
    assert len(df) > 7700
    
    df = fdr.StockListing('KOSPI-DESC') # KOSPI 5000+ 종목
    assert len(df) > 5000
    
    df = fdr.StockListing('KOSDAQ-DESC') # KOSDAQ 1600+ 종목
    assert len(df) > 1600
    
    df = fdr.StockListing('KONEX-DESC') # 100+ 종목
    assert len(df) > 100

@pytest.mark.krx_listings
def test_krx_listing():
    df = fdr.StockListing('KRX-DELISTING') # 3500+ 종목 - KRX 상장폐지 종목 전체
    assert len(df) > 3500

    df = fdr.StockListing('KRX-ADMINISTRATIVE') # 50+ 종목 - KRX 관리종목
    assert len(df) > 50

@pytest.mark.sp500_listings
def test_stocklisting_sp500():
    df = fdr.StockListing('S&P500') # S&P500 503 종목
    assert len(df) == 503

@pytest.mark.global_listings
def test_stocklisting_markets():

    df = fdr.StockListing('NASDAQ') # 3900+ 종목 - 나스닥 (NASDAQ)
    assert len(df) > 3900

    df = fdr.StockListing('NYSE') # 2800+ 종목 - 뉴욕증권거래소 (NYSE)
    assert len(df) > 2800

    df = fdr.StockListing('SSE') # 1400+ 종목 - 상하이 증권거래소 (Shanghai Stock Exchange: SSE)
    assert len(df) > 1400

    df = fdr.StockListing('SZSE') # 1700+ 종목 - 선전 증권거래소(Shenzhen Stock Exchange: SZSE)
    assert len(df) > 1700

    df = fdr.StockListing('HKEX') # 2000+ 종목 - 홍콩 증권거래소(Hong Kong Exchange: HKEX)
    assert len(df) > 2500

    df = fdr.StockListing('TSE') # 3900+ 종목 - 도쿄 증권거래소(Tokyo Stock Exchange: TSE) 
    assert len(df) > 3900

    df = fdr.StockListing('HOSE') # 300+ 종목 - 호찌민 증권거래소(Ho Chi Minh City Stock Exchange: HOSE)
    assert len(df) > 300

@pytest.mark.etf_listings
def test_etf_kr():
    # 한국 ETF 목록
    df = fdr.StockListing('ETF/KR') # 한국 ETF 전체
    assert len(df) > 700

def test_etf_us():
    # 미국 ETF 목록
    df = fdr.StockListing('ETF/US') # 미국 ETF 전체
    assert len(df) > 700


@pytest.mark.exchange
def test_exchange():
    df = fdr.DataReader('USD/KRW', '2018-01-01', '2020-08-30')
    assert len(df) > 600

@pytest.mark.snap
def test_snap_krx():
    df = fdr.SnapDataReader('KRX/INDEX/LIST') # KRX 지수목록
    assert len(df) >= 150

    df = fdr.SnapDataReader('KRX/INDEX/STOCK/1002') # 코스피 대형주 종목 리스트
    assert len(df) >= 100