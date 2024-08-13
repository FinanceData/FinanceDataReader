# KRX scaper for FinanceDataReader  
# 2024 FinacneData.KR

import io
import requests
import pandas as pd
import json

key_stat_list_csv = '''
key100statId,key100statNm,key100statEngNm,untNm,baseFreq
K051,한국은행 기준금리,Bank of Korea Base Rate,% ,D
K052,콜금리(익일물),Call Rate (Overnight),% ,D
K063,KORIBOR(3개월),KORIBOR(3 month),% ,D
K053,CD수익률(91일),CD(91 day),% ,D
K055,통안증권수익률(364일),Monetary Stabilization Bonds(364 day),% ,D
K056,국고채수익률(3년),Treasury Bonds(3 year),% ,D
K062,국고채수익률(5년),Treasury Bonds(5 year),% ,D
K057,"회사채수익률(3년,AA-)","Corporate Bonds(3 year, AA-)",% ,D
K058,예금은행 수신금리,Interest Rate on Time & Savings Deposits of CBs & SBs,% ,M
K059,예금은행 대출금리,Interest Rate on Loans & Discounts of CBs & SBs,% ,M
K005,예금은행총예금(말잔),Total Deposits of CBs & SBs(Avg.),십억원 ,M
K006,예금은행대출금(말잔),Loans of CBs & SBs(Avg.),십억원 ,M
K007,가계신용,Credit to Households,십억원 ,Q
K008,가계대출연체율,Delinquency Ratio for Loans to Households,% ,M
K002,"M1(협의통화, 평잔)","M1(Narrow Money, Avg.)",십억원 ,M
K003,"M2(광의통화, 평잔)","M2(Broad Money, Avg.)",십억원 ,M
K004,Lf(평잔),Lf(Avg.),십억원 ,M
K011,L(말잔),L(End of),십억원 ,M
K152,원/달러 환율(종가),KRW/USD(Closing Rate),원 ,D
K153,원/엔(100엔) 환율(매매기준율),KRW/JPY(100 Yen),원 ,D
K154,원/유로 환율(매매기준율),KRW/EURO,원 ,D
K156,원/위안 환율(종가),KRW/CNY(Closing Rate),원 ,D
K101,코스피지수,KOSPI,1980.01.04=100 ,D
K102,코스닥지수,KOSDAQ Index,1996.07.01=1000,D
K103,주식거래대금,Stocks Trading Value,천원 ,M
K107,고객예탁금,Customer Deposit,백만원 ,M
K104,채권거래대금,Bonds Trading Value,백만원 ,M
K108,국고채발행액,Issued Amount of Treasury Bonds,십억원 ,M
K258,"경제성장률(실질, 계절조정 전기대비)",GDP Growth Rate(S.A.),% ,Q
K259,"민간소비증감률(실질, 계절조정 전기대비)","Private Consumption(S.A., % Change)",% ,Q
K260,"설비투자증감률(실질, 계절조정 전기대비)","Facilities Investment(S.A.,% Change)",% ,Q
K261,"건설투자증감률(실질, 계절조정 전기대비)","Construction Investment(S.A.,% Change)",% ,Q
K462,"재화의 수출 증감률(실질, 계절조정 전기대비)","Exports of Goods and Services(S.A., % Change)",% ,Q
K257,"GDP(명목, 계절조정)","GDP(S.A.,at Current Price)",십억원 ,Q
K263,1인당GNI,Per Capita GNI,달러 ,A
K264,총저축률,Gross Saving Ratio,% ,Q
K265,국내총투자율,Gross Dom. Investment Ratio,% ,Q
K266,수출입의 대 GNI 비율,Ratio of Exports and Imports to GNI,% ,A
K220,전산업생산지수(농림어업제외),"Index of all industry production(excluding Agriculture, Forestry and Fishing)",2020=100,M
K201,제조업생산지수,Manufacturing Production Index,2020=100,M
K202,제조업출하지수,Manufacturing Shipment Index,2020=100,M
K203,제조업재고지수,Manufacturing Inventory Index,2020=100,M
K204,제조업가동률지수,Manufacturing Operation Ratio Index,2020=100,M
K205,서비스업생산지수,Index of Service,2020=100,M
K207,도소매업지수,Wholesale and Retail Sales Index,2020=100,M
K206,소매판매액지수,Retail Business Sales Index ,2020=100,M
K210,개인신용카드사용액,Amount of Personal Credit Cards Use,백만원 ,M
K453,자동차판매액지수,Motor Vehicle Sales Index,2020=100,M
K212,설비투자지수,Estimated Index of Equipment Investment,2015=100,M
K215,기계류내수출하지수,Machinery Shipment Index for Dom. Market,2020=100,M
K213,국내수요기계수주액,Value of Dom. Machinery Orders Received,백만원 ,M
K216,건설기성액,Value of Construction Completed,백만원 ,M
K218,건축허가면적,Permits Authorized for Bldg. Construction,㎡,M
K217,건설수주액,Value of Construction Orders Received,백만원 ,M
K219,건축착공면적,Results of Construction Start,㎡,M
K253,경기동행지수순환변동치,Cyclical Component of Composite Coincident Index,,M
K254,경기선행지수순환변동치,Cyclical Component of Composite Leading Index,,M
K252,소비자심리지수,Composite Consumer Sentiment Index,,M
K268,제조업업황실적BSI,"BSI(Manufact. Business Con., Tendency)",,M
K269,경제심리지수,Economic Sentiment Index,,M
K267,제조업매출액증감률,Growth Rate of Sales in Manufacturing,% ,A
K256,제조업매출액세전순이익률,Ordinary Income to Sales in Manufacturing,% ,A
K255,제조업부채비율,Debt Ratio in Manufacturing,% ,A
K306,가구당월평균소득,Monthly Ave. Income of Households,원 ,Q
K463,평균소비성향,Average of Propensity to Consume,% ,Q
K456,지니계수,Gini's Coefficient,,A
K464,5분위배율,"Income of Highest Quintile/Income of Lowest Quintile(by quintile, ratio)",,A
K303,실업률,Unemployment Rate,% ,M
K304,고용률,Employment Rate,% ,M
K301,경제활동인구,Economically Active Pop.,천명 ,M
K302,취업자수,Employed Persons,천명 ,M
K307,시간당명목임금지수,Nominal Wage per Hour(% change),2020=100,Q
K305,노동생산성지수,Labor Productivity(% Change),2020=100,Q
K308,단위노동비용지수,Unit Labor Cost(% Change),2020=100,Q
K451,추계인구,Population Projected,명 ,A
K460,고령인구비율(65세 이상),Share of the aged population (65+),% ,A
K461,합계출산율,Total Fertility Rate,명 ,A
K351,경상수지,Current Account,백만달러,M
K356,직접투자(자산),"Direct Investment, Assets",백만달러,M
K357,직접투자(부채),"Direct Investment, Liabilities",백만달러,M
K465,증권투자(자산),"Portfolio Investment, Assets",백만달러,M
K466,증권투자(부채),"Portfolio Investment, Liabilities",백만달러,M
K358,수출금액지수,Export value index,2015=100,M
K359,수입금액지수,Import value index,2015=100,M
K360,순상품교역조건지수,Net Barter Terms of Trade Index,2015=100,M
K467,소득교역조건지수,Income Terms of Trade Index,2015=100,M
K155,외환보유액,International Reserves,천달러 ,M
K353,대외채무,External Debt,백만달러,Q
K468,대외채권,External Assets,백만달러,Q
K401,소비자물가지수,Consumer Price Index,2020=100,M
K405,농산물 및 석유류제외 소비자물가지수,CPI Excluding Agricultural Products & Oils,2020=100,M
K406,생활물가지수,CPI For Living Necessaries,2020=100,M
K402,생산자물가지수,Producer Price Index,2015=100,M
K403,수출물가지수,Export Price Index,2015=100,M
K404,수입물가지수,Import Price Index,2015=100,M
K407,주택매매가격지수,Housing Sales Price Index,2021.6=100,M
K408,주택전세가격지수,Housing Jeonse Price Index,2021.6=100,M
K409,지가변동률(전기대비),Land Price Change Rates,% ,M
KN11,"국제유가(Dubai, 현물)",International Oil Price(Dubai),달러 ,M
K469,금,Gold Price(Spot),달러 ,M
'''

def _ecos_keystat_listing():
    '''100대 통계지표의 데이터 항목을 데이터프레임으로 반환
    '''
    # 실시간 데이터를 가져오기
    # payload_text = {
    #     "header": {
    #         "guidSeq":1,"trxCd":"OSUSC03R01","scrId":"IECOSPCM04","sysCd":"03",
    #         "fstChnCd":"WEB","langDvsnCd":"KO","envDvsnCd":"D", "sndRspnDvsnCd":"S",
    #         "sndDtm":"20220814","ipAddr":"124.50.40.5","usrId":"IECOSPC","pageNum":1,"pageCnt":1000
    #      },
    #     "data":{"useYn":"Y"}
    # }
    # res = requests.post('https://ecos.bok.or.kr/serviceEndpoint/httpService/request.json', json.dumps(payload_text))
    # jo = res.json()
    # return pd.DataFrame(jo['data']['dataList'])
    return pd.read_csv(io.StringIO(key_stat_list_csv))


_ecos_snap_csv = '''
Ticker,Desc,Columns
ECOS/SNAP/523,"주요 단기 시장금리","한국은행 기준금리, 콜금리(익일물), KORIBOR(3개월), CD수익률(91일)"
ECOS/SNAP/512,"주요 장기 시장금리","통안증권수익률(1년), 국고채수익률(3년), 국고채수익률(5년), 회사채수익률(3년, AA-)"
ECOS/SNAP/861,"예금은행 여수신 금리","여신금리, 수신금리, 여수신 금리차"
ECOS/SNAP/517-1,"가계신용","가계신용"
ECOS/SNAP/517-2,"가계대출 연체율","가계대출 연체율"
ECOS/SNAP/527,"협의 및 광의 통화","M1(협의통화, 평잔), M2(광의통화, 평잔)"
ECOS/SNAP/528,"금융기관 및 광의 유동성","Lf(금융기관유동성, 평잔), L(광의유동성, 말잔)"
ECOS/SNAP/529,"원/달러 및 원/엔 환율","원/달러(종가, 좌축), 원/100엔(매매기준율, 우축)"
ECOS/SNAP/530,"원/유로 및 원/위안 환율","원/유로(매매기준율, 좌축), 원/위안(종가, 우축)"
ECOS/SNAP/531,"코스피 및 코스닥 지수","코스피, 코스닥"
ECOS/SNAP/532,"코스피 주식거래대금 및 고객예탁금","코스피, 코스닥"
ECOS/SNAP/533,"채권거래대금 및 국고채발행액","채권거래대금, 국고채발행액"
ECOS/SNAP/1184,"경제성장률 및 재화의 수출증가율","경제성장률, 재화의 수출증가율"
ECOS/SNAP/1191,"민간소비, 설비투자 및 건설투자 증가율","민간소비, 설비투자, 건설투자"
ECOS/SNAP/1193-1,"GDP","GDP"
ECOS/SNAP/1193-2,"1인당 GNI","1인당 GNI"
ECOS/SNAP/1195-1,"GDP 대비 총저축률","GDP 대비 총저축률"
ECOS/SNAP/1195-2,"GDP 대비 국내총투자율","GDP 대비 국내총투자율"
ECOS/SNAP/1195-3,"수출입의 대 GNI 비율","수출입의 대 GNI 비율"
ECOS/SNAP/1196,"전산업생산지수","전산업생산지수(농림어업제외), 제조업생산지수"
ECOS/SNAP/1198,"제조업 출하, 재고, 가동률지수","제조업출하지수, 제조업재고지수, 제조업가동률지수"
ECOS/SNAP/1200,"서비스업생산지수","서비스업생산지수, 도소매업지수"
ECOS/SNAP/1202,"소매 및 자동차 판매, 개인신용카드","소매판매액지수, 자동차판매액지수, 개인신용카드사용액"
ECOS/SNAP/1203,"설비투자 관련 지수","설비투자지수, 기계류내수출하지수, 국내수요기계수주액"
ECOS/SNAP/1205,"건설기성액 및 건설수주액","건설기성액, 건설수주액"
ECOS/SNAP/1206,"건축허가 및 건축착공 면적","건축허가면적, 건축착공면적"
ECOS/SNAP/1207,"경기순환지표","경기동행지수순환변동치, 경기선행지수순환변동치"
ECOS/SNAP/1208,"심리지표","소비자심리지수, 제조업업황실적BSI, 경제심리지수"
ECOS/SNAP/1209,"기업경영분석지표","제조업매출액증가율, 제조업매출액세전순이익률, 제조업부채비율"
ECOS/SNAP/1210,"가계 소득 및 소비","가구당월평균소득, 평균소비성향"
ECOS/SNAP/1211,"소득분배지표","지니계수(~2021), 5분위배율(~2021), 지니계수(2020~), 5분위배율(2020~)"
ECOS/SNAP/1212,"실업률 및 고용률","실업률, 고용률"
ECOS/SNAP/1213,"경제활동인구 및 취업자수","경제활동인구, 취업자수"
ECOS/SNAP/1214,"노동 관련 지수","시간당명목임금지수, 노동생산성지수, 단위노동비용지수"
ECOS/SNAP/1204,"추계인구 및 고령인구비율","추계인구, 고령인구비율(65세 이상)"
ECOS/SNAP/1201,"합계출산율","합계출산율"
ECOS/SNAP/1199,"경상수지","경상수지"
ECOS/SNAP/1194,"직접투자","직접투자(자산), 직접투자(부채)"
ECOS/SNAP/1192,"증권투자","증권투자(자산), 증권투자(부채)"
ECOS/SNAP/1190,"수출입 금액지수","수출금액지수, 수입금액지수"
ECOS/SNAP/1198,"교역조건지수","제조업출하지수, 제조업재고지수, 제조업가동률지수"
ECOS/SNAP/1188-1,"외환보유액","외환보유액"
ECOS/SNAP/1188-2,"대외채무","대외채무"
ECOS/SNAP/1188-3,"대외채권","대외채권"
ECOS/SNAP/1197,"소비자물가 상승률","소비자물가지수, 농산물 및 석유류제외, 생활물가지수"
ECOS/SNAP/1187,"생산자물가 및 수출입물가 상승률","생산자물가지수, 수출물가지수, 수입물가지수"
ECOS/SNAP/1186,"부동산가격","주택매매가격 상승률, 주택전세가격 상승률, 지가변동률"
ECOS/SNAP/1511,"원자재가격","국제유가(Dubai, 좌축), 금"
'''

def _ecos_snap_reader(ticker):
    full_code = ticker.replace('ECOS/SNAP/', '')
    code, sub_code = full_code.split('-') if '-' in ticker else (full_code, None)

    url = f'https://snapshot.bok.or.kr/api/chart/exportChart?chart_id={code}'
    r = requests.get(url)
    df = pd.read_excel(io.BytesIO(r.content), index_col=0, skiprows=3)
    df = df.drop(['단위', '주기', '기간'])
    df.columns = [col.replace('(좌축)', '').replace('(우축)', '').replace('좌축, ', '').replace('우축, ','') for col in df.columns]

    if sub_code:
        col_inx = (int(sub_code)-1) * 2
        df = df.iloc[:, col_inx:col_inx+2]
        col_name = df.columns[0]
        df.columns = ['날짜', col_name]
        df['날짜'] = pd.to_datetime(df['날짜'])
        df = df.set_index('날짜') 
        df = df.dropna(how='all')
    else:
        df.index = pd.to_datetime(df.index)
        df.index.name = '날짜'
        df = df.astype(float)
    return df


class EcosSnapReader:
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def read(self):
        snap_df = pd.read_csv((io.StringIO(_ecos_snap_csv)))
        if self.ticker == 'ECOS/KEYSTAT/LIST':
            return _ecos_keystat_listing()
        elif self.ticker == 'ECOS/SNAP/LIST':
            return snap_df
        elif self.ticker in snap_df['Ticker'].values:
            return _ecos_snap_reader(self.ticker)
        else:
            raise NotImplementedError(f'"{self.ticker}" is not implemented')
            
