
상장종목 목록 (거래소별)
===============================
거래소 별로 상장종목 목록을 가져옵니다

.. code-block:: python
	
	df = fdr.StockListing('KRX')
	df

여기에 사용할 수 있는 거래소 심볼은 다음과 같습니다


==============  ======================  =============================
심볼            거래소                      비고
==============  ======================  =============================
KRX             KRX 종목 전체               KOSPI, KOSDAQ, KONEX 모두
KOSPI           KOSPI 종목        
KOSDAQ          KOSDAQ 종목
KONEX           KONEX 종목
NASDAQ          나스닥 종목
NYSE            뉴욕 증권거래소 종목
AMEX            AMEX 종목
S&P500          S&P 500 종목                S&P 500 지수 구성종목
SSE             상하이 증권거래소 
SZSE            선전 증권거래소
HKEX            홍콩 증권거래소
TSE             도쿄 증권거래소
HOSE            호찌민 증권거래소
ETF/KR          한국 ETF 종목
==============  ======================  =============================




가격 데이터
=====================

국내 주식
---------------------
- 단축 코드(6자리)를 사용합니다. 예를 들어, '005930'(삼성전자), '215600'(신라젠)
- 전체 코드는 `fdr.StockListing('KRX')` 를 통해 얻을 수 있습니다


미국 주식
---------------------
- 티커를 사용합니다. 예를 들어, 'AAPL'(애플), 'AMZN'(아마존), 'GOOG'(구글)
- NASDAQ 티커 전체는 `fdr.StockListing('NASDAQ')` 를 통해 얻을 수 있습니다



참고
=====================

FinanceDataReader 사용자 안내서
* https://financedata.github.io/posts/finance-data-reader-users-guide.html

