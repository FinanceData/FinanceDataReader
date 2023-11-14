# #%%
# import os
# print(os.getcwd())

# #%%
# import os
# os.chdir(r'g:/내 드라이브/dev')

# import FinanceDataReader as fdr
# df = fdr.DataReader('KRX:KS11')
# df

# #%%
# df = fdr.DataReader('YAHOO:KS11')
# print(df)


# # 두산(000150) - 한국 KRX
# # Yihua Healthcare(000150) - 심천 SZSE
# # Huaan 펀드(000150) - 상하이 SSE

# df = fdr.DataReader('000150', '2018-01-01', '2020-09-30')
# df.tail()


# # 두산(000150) - 한국 KRX
# # Yihua Healthcare(000150) - 심천 SZSE
# # Huaan 펀드(000150) - 상하이 SSE

# df = fdr.DataReader('000150', '2018-01-01', '2020-09-30', exchange='KRX')
# df.tail()

# # 두산(000150) - 한국 KRX
# # Yihua Healthcare(000150) - 심천 SZSE
# # Huaan 펀드(000150) - 상하이 SSE

# df = fdr.DataReader('000150', '2018-01-01', '2020-09-30', exchange='SZSE')
# df.tail()


# # 두산(000150) - 한국 KRX
# # Yihua Healthcare(000150) - 심천 SZSE
# # Huaan 펀드(000150) - 상하이 SSE
# import FinanceDataReader as fdr

# df = fdr.DataReader('000150', '2018-01-01', '2020-09-30', exchange='SSE')
# df.tail()


# # KR모터스(000040) - 한국 KRX
# # Baoan(000040) - 심천 SZSE 

# df = fdr.DataReader('000040', '2018-01-01', '2020-09-30')
# df.tail(10)


# # KR모터스(000040) - 한국 KRX
# # Baoan(000040) - 심천 SZSE

# df = fdr.DataReader('000040', '2018-01-01', '2020-09-30', exchange='SZSE')
# df.tail(10)


# import FinanceDataReader as fdr

# # 공상은행(601398:SSE 상해증권거래소)
# fdr.DataReader('601398', '2020-01-01', exchange='SSE')

# # 귀주 마오타이(600519:SSE 상해증권거래소)
# fdr.DataReader('600519', '2020-01-01', exchange='SSE')

# # 우량예 이빈(000858:SZSE 심천증권거래소)
# fdr.DataReader('000858', '2020-01-01', exchange='SZSE')

# # 메이디그룹(000333:SZSE 심천증권거래소)
# fdr.DataReader('000333', '2020-01-01', exchange='SZSE')


# # 토요타 자동차(7203:TSE) 
# fdr.DataReader('7203', '2020-01-01', exchange='TSE')

# # 소프트뱅크그룹(9984:TSE) 
# fdr.DataReader('9984', '2020-01-01', exchange='TSE')


# import FinanceDataReader as fdr

# # AMEX

# # Cheniere Energy Partners LP(CQP:NYSE)
# # fdr.DataReader('CQP', '2020-01-01', exchange='NYSE')

# # Cheniere Energy Inc (LNG:NYSE)
# fdr.DataReader('LNG', '2020-01-01', exchange='NYSE')

# # Cboe Global Markets Inc (CBOE:AMEX)
# fdr.DataReader('CBOE', '2020-01-01', exchange='NYSE')


# import FinanceDataReader as fdr

# # Vanguard Canadian Corporate Bond Index ETF (TSX)
# fdr.DataReader('VCB', '2020-01-01')

# # Vietcombank(VCB 베트남 무역은행) (VCB:HOSE 호치민증권거래소)
# fdr.DataReader('VCB', '2020-01-01', exchange='HOSE')

# # Vingroup JSC(VIC:HOSE 호치민증권거래소)
# fdr.DataReader('VIC', '2020-01-01', exchange='HOSE')

# ## 상장폐지종목 가격 데이터 (상장일 ~ 상장폐지일)
# # 3SOFT(036360): 2009년 4월 29일 상장폐지
# df = fdr.DataReader('036360', exchange='krx-delisting') # 상장일 ~ 상장폐지 기간의 가격 데이터
# df

# df = fdr.DataReader('036360', '2009-01-01', exchange='krx-delisting') # 2009-01-01 ~ 상장폐지 기간의 가격 데이터
# df

# df = fdr.DataReader('036360', '2009-01-01', '2009-01-30', exchange='krx-delisting') # 2009-01-01 ~ 2009-01-30 가격 데이터
# df

# krx_adm = fdr.StockListing('krx-administrative') # 관리종목
# krx_adm



# ## 종목 리스트 - 미국

# # 나스닥
# nasdaq = fdr.StockListing('NASDAQ')
# nasdaq.head()


# # https://github.com/FinanceData/FinanceDataReader/issues/12
# # BRK.B -> BRKB, BF.B -> BFB 확인

# excepts = ['BRKB', 'BFB']
# sp500[sp500['Symbol'].isin(excepts)]


# # SP 500 종목 전체 가격데이터 수집 테스트 (심볼 테스트)
# for ix, row in sp500[500:].iterrows():
#     symbol, name = row['Symbol'], row['Name']
#     df = fdr.DataReader(symbol, '2020-12')
#     print('.', end='')
#     if (ix+1) % 100 == 0:
#         print()


# etf_kr = fdr.EtfListing('KR')

# fdr.StockListing('ETF/KR')

# etf_us = fdr.StockListing('ETF/US')
# etf_us        


# ## 미국 우선주 (NYSE, NASDAQ, AMEX)

# fdr.DataReader('ABR_pd', '2020') # Arbor Realty Trust Pa Pref

# fdr.DataReader('28513K', '2020') # SK케미컬우


# stocks = fdr.StockListing('KRX')
# stocks[stocks['Code'].str.contains('285130')]


# stocks[stocks['Code'].str.contains('005930')]

