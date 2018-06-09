FinanceDataReader 
=====================
FinanceDataReader, The Ultimate Financial Data Reader

.. toctree::
	:maxdepth: 2

	tickers.rst


Features
---------------------
금융 데이터를 다루는데 가장 기본이 되는 데이터는 거래소별 전체 종목 코드와 가격 데이터입니다.

FinanceDataReader는 `pandas-datareader <https://pandas-datareader.readthedocs.io>`__ 를 대체하기 보다 보완하기 위한 목적으로 만들어졌으며, 주요한 기능은 다음과 같습니다.

* 해외주식 가격: AAPL(애플), AMZN(아마존), GOOG(구글) 등
* 국내주식 가격: 005930(삼성전자), 091990(셀트리온헬스케어) 등
* 지수: KS11(코스피), KQ11(코스닥), DJI(다우), IXIC(나스닥), US500(S&P 500)
* 환율: USD/KRX (원달러), USD/EUR(달러/유로화), CNY/KRW: 위엔화/원화
* 암호화폐: BTC/USD (비트코인/달러, Bitfinex), BTC/KRW (비트코인/원화, 빗썸)
* 거래소별 전체 종목 코드: KRX, NASDAQ, NYSE, AMEX, S&P 500 종목


Installation
---------------------
.. code-block:: bash

	pip install -U finance-datareader


설치 (wheel 설치)
--------------------------------
망분리 혹은 방화벽등의 이슈로 pip로 설치가어려운 경우 아래 디렉토리에서 whl 파일을 다운로드합니다.

   https://github.com/FinanceData/FinanceDataReader/tree/master/dist

.whl 파일을 다음과 같이 pip로 설치합니다.

.. code-block:: bash

	pip install finance_datareader-x.x.x-py3-none-any.whl


Quick Start
--------------------------------

종목과 종목코드 읽기
...............................
.. code-block:: python

	# 한국거래소 상장종목과 코드명 전체
	df_krx = fdr.StockListing('KRX')

	# S&P 500 종목과 코드명 전체
	df_spx = fdr.StockListing('S&P500')



가격 데이터 읽기
.......................

.. code-block:: python

	import FinanceDataReader as fdr

	# 애플(AAPL), 2017-01-01 ~ 현재
	df = fdr.DataReader('AAPL', '2017')

	# 셀트리온(068270), 2017-01-01 ~ 2018-05-30
	df = fdr.DataReader('068270', '2017-01-01', '2018-05-30')

	# KS11 (KOSPI 지수), 2015-01-01~현재
	df = fdr.DataReader('KS11', '2015')

	# 다우지수, 2015년~현재
	df = fdr.DataReader('DJI', '2015-01-01')

	# 원달러 환율, 1995-01-01 ~ 현재
	df = fdr.DataReader('USD/KRW', '1995')

	# 비트코인 원화 가격 (빗썸), 2016년~현재
	df = fdr.DataReader('BTC/KRW', '2016')




Release
-------------------
2018-05-17 v0.2.0
- StockListing, SP500 (S&P 500 Listings, wikipedia), 추가

2018-05-16 v0.1.0
- StockListing KRX, KOSPI, KODAQ, KONEX, 추가 
- StockListing NASDAQ, NYSE, AMEX, 추가

2018-05-14 v0.0.1
- DataReader 국내/매국 주가 데이터, 추가


Contribute
---------------------
제안, 버그, 개선, 질문 등 이슈는 다음에 등록해 주시면 개선하는데 큰 도움이 됩니다

- 이슈 트래커: https://github.com/FinanceData/FinanceDataReader/issues



license
---------------------
MIT license를 따릅니다


찾아보기 
==================
* :ref:`genindex`
* :ref:`search`


2018 FinanceData.KR http://financedata.kr

