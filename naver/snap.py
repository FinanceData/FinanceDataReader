#-*- coding: utf-8 -*-
# (c) 2018~2024 FinaceData.KR

import re
import io
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime
from itertools import product
from tqdm import tqdm

def _marcap_market_page(sosok, page):
    url = f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={sosok}&page={page}'

    # 거래량, 매수호가, 거래대금(백만), 시가총액(억), 영업이익(억), PER(배): cookies = {'field_list': '12|06108810'}
    # 시가, 매도호가, 전일거래량, 자산총계(억), 영업이익증가율, ROE(%): cookies = {'field_list': '12|01882048'}
    # 고가, 매수총잔량, 외국인비율, 부채총계(억), 당기순이익(억), ROA(%): cookies = {'field_list': '12|00441424'}
    # 저가, 매도총잔량, 상장주식수(천주), 매출액(억), 주당순이익(원), PBR(배): cookies = {'field_list': '12|00234202'}
    # 매출액증가율, 보통주배당금(원), 유보율(%): cookies = {'field_list': '12|00000181'}

    field_list = [
        # field_list, columns
        ('12|06108810', ['N', '종목명', '현재가', '전일비', '등락률', '액면가', '거래량', '매수호가', '거래대금', '시가총액', '영업이익', 'PER']),
        ('12|01882048', ['시가', '매도호가', '전일거래량', '자산총계', '영업이익증가율', 'ROE']),
        ('12|00441424', ['고가', '매수총잔량', '외국인비율', '부채총계', '당기순이익', 'ROA']),
        ('12|00234202', ['저가', '매도총잔량', '상장주식수', '매출액', '주당순이익', 'PBR']),
        ('12|00000181', ['매출액증가율', '보통주배당금', '유보율']),
    ]

    marcap = pd.DataFrame()
    marcap['시장'] = sosok

    for field in field_list:
        f, cols = field
        cookies = {'field_list': f}
        html = requests.get(url, cookies=cookies).text
        df = pd.read_html(html)[1]
        if len(df) == 0:
            break
        marcap[field[1]] = df[field[1]]

    if len(marcap) == 0:
        return marcap
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[1]
    trs = table.find_all('tr')

    codes = []
    for tr in trs[1:]:
        tds = tr.find_all('td')
        code = tds[1].a['href'].split('=')[1] if len(tds) >= 2 else None
        codes.append(code)

    marcap.insert(1, '종목코드', codes)
    marcap.dropna(how='all', inplace=True)
    marcap.reset_index(drop=True, inplace=True)
    marcap['등락률'] = marcap['등락률'].astype(str).str.replace('%', '').replace(',', '').astype(float) / 100.0
    marcap['ROE'] = marcap['ROE'] / 100.0
    marcap['ROA'] = marcap['ROA'] / 100.0
    marcap['유보율'] = marcap['유보율'] / 100.0

    marcap = marcap[['N', '종목코드', '종목명', '현재가', '전일비', '등락률', '액면가',
        '거래량', '시가', '고가', '저가', '매수호가', '매도호가', '매수총잔량', '매도총잔량',
        '거래대금', '전일거래량', '외국인비율', '상장주식수', '시가총액', '자산총계', '부채총계',
        '매출액', '매출액증가율', '영업이익', '영업이익증가율', '당기순이익', '주당순이익', '보통주배당금',
        'PER', 'ROE', 'ROA', 'PBR', '유보율']]
    return marcap

def marcap(market='KRX', verbose=1):
    '''
    시가총액순 종목 데이터를 반환합니다.
    * market: 'KOSPI'=코스피, 'KOSDAQ'=코스닥, 'KRX'=코스피+코스닥
    * verbose: 1=진행상태를 표시합니다
    '''
    kospi_prod = list(product([0], range(1, 32+1)))
    kosdaq_prod = list(product([1], range(1, 29+1)))
    market = market.strip().upper()
    if market == 'KOSPI':
        page_prod = kospi_prod
        total = 32
    elif market == 'KOSDAQ':
        page_prod = kosdaq_prod
        total = 29
    elif market == 'KRX':
        page_prod = kospi_prod + kosdaq_prod
        total = 32+29
    else:
        raise ValueError("market must be one of 'KOSPI', 'KOSDAQ' or 'KRX'")

    df_list = []
    for i, (sosok, page) in tqdm(enumerate(page_prod), total=total):
        df = _marcap_market_page(sosok, page)
        df_list.append(df)
        # print('.', end='') if verbose else print('', end='')

    df_merged = pd.concat(df_list)
    df_merged.sort_values(by='시가총액', ascending=False, inplace=True)
    return df_merged


def _to_float(x, half=None):
    '''
    * x: 변환대상 값
    * half('l' 구분자):None=전체, 0=첫번째 절반, 1=두번째 절반
    '''
    x = re.sub(r'[\t\n, 조억원배%]', '', str(x))
    if half != None and len(x.split('l')) > 1:
        return pd.to_numeric(x.split('l')[half], errors='coerce').item()
    return pd.to_numeric(x, errors='coerce').item()

def factors(code):
    '''
    다양한 팩터데이터(dict)를 반환합니다.
    * code: 종목코드

    반환값(dict): 반환값의 항목은 다음과 같습니다
    '회사개요', '시가총액', '상장주식수',
    '외국인한도주식수', '외국인보유주식수', '외국인소진율',
    '목표주가', '최고52주', '최저52주',
    'PER', 'EPS', '추정PER', '추정EPS', 'PBR', 'BPS', '배당수익률',
    '동일업종_PER', '동일업종_등락률'
    '자사주_보유지분', '자사주_주식수',
    '''

    keys = [
        '회사개요', '시가총액', '상장주식수',
        '외국인한도주식수', '외국인보유주식수', '외국인소진율',
        '목표주가', '최고52주', '최저52주',
        'PER', 'EPS', '추정PER', '추정EPS', 'PBR', 'BPS', '배당수익률',
        '동일업종_PER', '동일업종_등락률'
        '자사주_보유지분', '자사주_주식수',
    ]
    factor_data = dict.fromkeys(keys)

    ## 회사개요
    url = 'https://finance.naver.com/item/main.nhn?code=' + code
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")

    summary_info = soup.find(id='summary_info')
    text = summary_info.text.strip() if summary_info else ''
    factor_data['회사개요'] = '\n'.join(text.split('\n')[1:4])

    try:
        df_list = pd.read_html(r.text, match='상장주식수')
        df = df_list[0]
        factor_data['시가총액'] = _to_float(df.iloc[0,1])
        factor_data['상장주식수'] = _to_float(df.iloc[2,1])
    except ValueError as e:
        print(code, e)

    try:
        df_list = pd.read_html(r.text, match='외국인한도주식수')
        df = df_list[0]
        factor_data['외국인한도주식수'] = _to_float(df.iloc[0,1])
        factor_data['외국인보유주식수'] = _to_float(df.iloc[1,1])
        factor_data['외국인소진율'] = _to_float(df.iloc[2,1])
    except ValueError as e:
        print(code, e)

    try:
        df_list = pd.read_html(r.text, match='목표주가')
        df = df_list[0]
        factor_data['목표주가'] = _to_float(df.iloc[0,1], half=1)
        factor_data['최고52주'] = _to_float(df.iloc[1,1], half=0)
        factor_data['최저52주'] = _to_float(df.iloc[1,1], half=1)
    except ValueError as e:
        print(code, e)

    try:
        df_list = pd.read_html(r.text, match='추정PER')
        df = df_list[0]
        factor_data['PER'] = _to_float(df.iloc[0,1], half=0)
        factor_data['EPS'] = _to_float(df.iloc[0,1], half=1)
        factor_data['추정PER'] = _to_float(df.iloc[1,1], half=0)
        factor_data['추정EPS'] = _to_float(df.iloc[1,1], half=1)
        factor_data['PBR'] = _to_float(df.iloc[2,1], half=0)
        factor_data['BPS'] = _to_float(df.iloc[2,1], half=1)
        factor_data['배당수익률'] = _to_float(df.iloc[3,1])
    except ValueError as e:
        print(code, e)

    try:
        df_list = pd.read_html(r.text, match='동일업종 PER')
        df = df_list[0]
        factor_data['동일업종_PER'] = _to_float(df.iloc[0,1])
        factor_data['동일업종_등락률'] = _to_float(df.iloc[1,1])
    except ValueError as e:
        print(code, e)

    # 기업현황
    try:
        url = f'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code}'
        dfs = pd.read_html(url, encoding='utf-8')

        # 기업현황 / 시세및 주주현황
        df = dfs[4].set_index('주요주주')
        자사주_주식수, 자사주_보유지분 = 0, 0
        if '자사주' in df.index:
            자사주_주식수 = df.loc['자사주']['보유주식수(보통)']
            자사주_보유지분 = df.loc['자사주']['보유지분(%)']

        factor_data['자사주_주식수'] = 자사주_주식수
        factor_data['자사주_보유지분'] = 자사주_보유지분
    except ValueError as e:
        print(code, e)

    return factor_data


def stock_price_day(code, start=None, end=None):
    '''
    기간(start ~ end)사이의 종목(code)의 일별 가격 데이터를 데이터프레임으로 반환합니다
    * code: 종목코드
    * start: 시작일(기본값: 1970-01-01)
    * end: 종료일(기본값: 오늘)
    '''

    start, end = pd.to_datetime(start), pd.to_datetime(end)
    start = datetime(1970, 1, 1) if start is None else start
    end = datetime.today() if end is None else end

    url = 'https://fchart.stock.naver.com/sise.nhn?timeframe=day&count=6000&requestType=0&symbol='
    r = requests.get(url + code)

    data_list = re.findall(r'<item data=\"(.*?)\" />', r.text, re.DOTALL)
    if len(data_list) == 0:
        return pd.DataFrame()
    data = '\n'.join(data_list)
    df = pd.read_csv(StringIO(data), delimiter='|', header=None, dtype={0:str})
    df.columns  = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    df['Change'] = df['Close'].pct_change()

    return df.query('index>=%r and index<=%r' % (start, end))


def stock_price_minute(code, date=None):
    '''
    지정한 날짜의 분봉 데이터를 데이터프레임으로 반환합니다 (지난 5영업일까지 가능)
    * code: 종목코드
    * date: 날짜 (기본값: 오늘)
    '''
    dt = datetime.today() if date==None else pd.to_datetime(date)
    dt_str = dt.strftime('%Y%m%d')

    df_list = []
    prev_html = ''

    # 1~40 page 크롤링
    for page in range(1,50):
        url = f'https://finance.naver.com/item/sise_time.nhn?code={code}&thistime={dt_str}180000&page={page}'
        r = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})
        df = pd.read_html(r.text, header=0)[0]
        if page > 1 and prev_html==r.text:
            break
        prev_html = r.text
        df.dropna(inplace=True)
        df_list.append(df)
        if len(df) == 0 or df.iloc[-1, 0] == '09:00':
            break
    result = pd.concat(df_list)
    result['체결시각'] = dt.strftime('%Y-%m-%d') + ' ' + result['체결시각']
    result['체결시각'] = pd.to_datetime(result['체결시각'])
    result.set_index('체결시각', inplace=True)
    result.sort_index(inplace=True)
    return result


def finstate_detail(code, rpt='0', freq='0', gubun='MAIN'):
    '''
    네이버 파이낸스로 부터 상세재무제표를 읽어온다
    :param code: 종목코드: '005930'
    :param rpt: 종류: '0'=손익계산서(기본값), '1'=재무상태표, '2'=현금흐름표
    :param freq: 기간: '0'=연간(기본값), '1'=분기
    :param gubun: 구분: 'MAIN'=주재무제표(기본값), 'IFRSS'=KIFRS별도, 'IFRSL'=IFRS연결, 'GAAPS'=GAAP개별, 'GAAPL'=GAAP연결
    '''

    # encparam 가져오기
    url = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930'
    html_text = requests.get(url).text
    encparam = re.findall (r"encparam: '(.*?)'", html_text)[0]

    url = f'https://navercomp.wisereport.co.kr/v2/company/cF3002.aspx?cmp_cd={code}&frq={freq}&rpt={rpt}&finGubun={gubun}&frqTyp={freq}&cn=&encparam={encparam}'
    # 페이지 가져오기
    headers={'Referer': url}
    r = requests.get(url, headers=headers)
    jo = json.loads(r.text)

    # DataFrame 생성
    df = pd.json_normalize(jo, 'DATA')

    # DATA1~DATA6 컬럼 이름 바꾸기
    jo_yymm = jo['YYMM'][:6]
    date_str_list = []
    for yymm in jo_yymm:
        m = re.search(r'(\d{4}/\d{0,2}).*', yymm)
        date_str_list.append(m.group(1) if m else '')
    data_n_list = ['DATA' + str(i) for i in range(1,7)]
    yymm_cols = zip(data_n_list, date_str_list)
    cols_map = dict(yymm_cols)
    df.rename(columns=cols_map, inplace=True)
    if not len(df):
        print(f'no data found {code}')
        return df
    df['ACC_NM'] = df['ACC_NM'].str.strip().replace(r'[\.*\[\]]', '', regex=True)
    df.set_index(['ACCODE', 'ACC_NM'], inplace=True)
    df = df.iloc[:, 5:11] # 날짜 컬럼만 추출
    df = df.T # Transpose (컬럼, 인덱스 바꾸기)
    df.index = pd.to_datetime(df.index)
    df.index.name = '날짜'
    return df


def finstate_summary(code, fin_type='0', freq='Y'):
    '''
    요약제무제표데이터를 데이터프레임으로 반환합니다
    :param code: 종목코드
    :param fin_type: 재무제표 종류 '0'=주재무제표, '1'=K-GAAP개별, '2'=K-GAAP연결, '3'=K-IFRS별도, '4'=K-IFRS연결
    :param freq: 기간: Y=년(기본), Q=분기, 'A'=연간분기 전체
    '''
    # encparam 읽어오기
    url = 'https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930'
    html_text = requests.get(url).text

    if not re.search(r"encparam: '(.*?)'", html_text):
        print('encparam not found') # encparam이 없는 경우
        return None
    encparam = re.findall (r"encparam: '(.*?)'", html_text)[0]

    url = f'https://navercomp.wisereport.co.kr/v2/company/ajax/cF1001.aspx?cmp_cd={code}&fin_typ={fin_type}&freq_typ={freq}&encparam={encparam}'
    r = requests.get(url, headers={'Referer': url})
    df_list = pd.read_html(io.StringIO(r.text), encoding='euc-kr')
    df = df_list[1]
    df.columns = [col[1] for col in df.columns]
    df.set_index('주요재무정보', inplace=True)
    df.columns = [re.sub(r'[^\.\d]', '', col) for col in df.columns]
    df.columns = [pd.to_datetime(col, format='%Y%m', errors='coerce') for col in df.columns]
    df = df.transpose()
    df.index.name = '날짜'
    return df


def invest_index(code, rpt='5', frq='1', finGubun='IFRSL'):
    '''
    네이버 파이낸스로 부터 투자지표 읽어옵니다
    * code (종목코드): '005930'
    * rpt (종류): '1'=수익성, '2'=성장성, '3'=안정성, '4'=활동성, '5'=가치분석 (기본값)
    * frq (기간): '0'=연간, '1'=분기(기본값)
    * finGubun (구분): 'MAIN'=주재무제표, 'IFRSS'=KIFRS별도, 'IFRSL'=IFRS연결(기본값), 'GAAPS'=GAAP개별, 'GAAPL'=GAAP연결
    '''
    # encparam 읽어오기
    url = 'http://companyinfo.stock.naver.com/v1/company/c1040001.aspx?cmp_cd=005930'
    html_text = requests.get(url).text

    if not re.search(r"encparam: '(.*?)'", html_text):
        print('encparam not found') # encparam이 없는 경우
        return None
    encparam = re.findall (r"encparam: '(.*?)'", html_text)[0]

    # 투자지표 데이터 가져오기
    url = f'http://companyinfo.stock.naver.com/v1/company/cF4002.aspx?' \
          f'cmp_cd={code}&frq={frq}&rpt={rpt}&finGubun={finGubun}&frqTyp={frq}&cn=&encparam={encparam}'

    # DataFrame 생성
    headers={'Referer': 'http://companyinfo.stock.naver.com'}
    jo = json.loads(requests.get(url, headers=headers).text)
    df = pd.json_normalize(jo, 'DATA')

    # DATA1~DATA6 컬럼 이름 바꾸기
    jo_yymm = jo['YYMM'][:6]
    date_str_list = []
    for yymm in jo_yymm:
        m = re.search(r'(\d{4}/\d{0,2}).*', yymm)
        date_str_list.append(m.group(1) if m else '')
    data_n_list = ['DATA' + str(i) for i in range(1,7)]
    yymm_cols = zip(data_n_list, date_str_list)
    cols_map = dict(yymm_cols)
    df.rename(columns=cols_map, inplace=True)
    df['ACC_NM'] = df['ACC_NM'].str.strip().replace(r'[\.*\[\]]', '', regex=True)
    df = df.drop_duplicates(['ACCODE', 'ACC_NM'], keep='last')
    df.set_index(['ACCODE', 'ACC_NM'], inplace=True)
    df = df.iloc[:, 5:11] # 날짜 컬럼만 추출
    df = df.T # Transpose (컬럼, 인덱스 바꾸기)
    df = df.dropna(how='all')
    df.index = pd.to_datetime(df.index)
    df.index.name = '날짜'
    return df


def investors(code):
    '''
    투자자별 매매 동향을 반환합니다 (20일)
    * code: 종목코드
    '''
    url = f'https://finance.naver.com/item/frgn.nhn?code={code}'
    r = requests.get(url, headers={'User-Agent':'Mozilla/5.0 AppleWebKit/537.36 Edg/122.0.0.0'})
    print()
    try:
        df_list = pd.read_html(io.StringIO(r.text), encoding='euc-kr')
    except ValueError as e:
        print(e)
        raise Exception(f'invalid stock code or url: {url}')

    df = df_list[2].dropna(how='all').copy()
    df.columns = ['날짜', '종가', '전일비', '등락률', '거래량', '기관순매매량', '외국인순매매량', '외국인보유주수', '외국인보유율']
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['등락률'] = df['등락률'].str.replace('%', '').astype('float')
    df.sort_values('날짜', inplace=True)
    df.set_index('날짜', inplace=True)
    return df


def sector_stock_list(verbose=False):
    '''
    업종별 종목리스트 데이터를 가져옵니다

    반환값(DataFrame): 컬럼=[종목코드,종목명,시장,업종명,업종코드]
    '''
    url = 'https://finance.naver.com/sise/sise_group.nhn?type=upjong'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    a_list = soup.select('a[href*=sise_group_detail]')

    row_list = []
    for ix, a in enumerate(a_list):
        sector_name = a.text
        sector_no = a['href'].replace('/sise/sise_group_detail.nhn?type=upjong&no=', '')
        sector_url = 'https://finance.naver.com' + a['href']
        url = f'https://finance.naver.com/sise/sise_group_detail.nhn?type=upjong&no={sector_no}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        divs = soup.select('div[class="name_area"]')
        if verbose:
            print(f'{ix:2} {sector_name}({len(divs)}종목) {sector_url}')
        for div in divs:
            code = div.a['href'].replace('/item/main.nhn?code=', '')
            name = div.text
            market = 'KOSDAQ' if ' *' in name else 'KOSPI'
            name = name.replace(' *', '')
            row_list.append([code, name, market, sector_name, sector_no])
            # print(code, name, market, sector_name, sector_no)
    sector_stocks = pd.DataFrame(row_list, columns=['종목코드', '종목명', '시장', '업종명', '업종코드'])
    return sector_stocks

def __up(sosok=0):
    url = f'https://finance.naver.com/sise/sise_rise.naver?sosok={sosok}'

    # 거래량, 거래대금(백만), 매수호가, 시가총액(억), 영업이익(억), PER(배): cookies = {'field_list': '2|06108810'}
    # 시가, 매도호가, 자산총계(억), 영업이익증가율, ROE(%): cookies = {'field_list': '2|01882048'}
    # 고가, 매수총잔량, 외국인비율, 부채총계(억), 당기순이익(억), ROA(%): cookies = {'field_list': '12|00441424'}
    # 저가, 매도총잔량, 상장주식수(천주), 매출액(억), 주당순이익(원), PBR(배): cookies = {'field_list': '12|00234202'}
    # 매출액증가율, 보통주배당금(원), 유보율(%): cookies = {'field_list': '12|00000181'}

    field_list = [
        # field_list, columns
        ('2|06108810', ['N', '종목명', '현재가', '전일비', '등락률', '거래량', '거래대금', '매수호가', '시가총액', '영업이익', 'PER']),
        ('2|01882048', ['시가', '매도호가', '전일거래량', '자산총계', '영업이익증가율', 'ROE']),
        ('2|00441424', ['고가', '매수총잔량', '외국인비율', '부채총계', '당기순이익', 'ROA']),
        ('2|00234202', ['저가', '매도총잔량', '상장주식수', '매출액', '주당순이익', 'PBR']),
        ('2|00000181', ['매출액증가율', '보통주배당금', '유보율']),
    ]

    up = pd.DataFrame()
    up['시장'] = sosok

    for field in field_list:
        f, cols = field
        cookies = {'field_list': f}
        html = requests.get(url, cookies=cookies).text
        df = pd.read_html(html)[1]
        if len(df) == 0:
            break
        up[field[1]] = df[field[1]]

    if len(up) == 0:
        return up
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[1]
    trs = table.find_all('tr')

    codes = []
    for tr in trs[1:]:
        tds = tr.find_all('td')
        code = tds[1].a['href'].split('=')[1] if len(tds) >= 2 else None
        codes.append(code)

    up.insert(1, '종목코드', codes)
    up.dropna(how='all', inplace=True)
    up.reset_index(drop=True, inplace=True)
    up['등락률'] = up['등락률'].astype(str).str.replace('%', '').replace(',', '').astype(float) / 100.0
    up['ROE'] = up['ROE'] / 100.0
    up['ROA'] = up['ROA'] / 100.0
    up['유보율'] = up['유보율'] / 100.0

    up = up[['N', '종목코드', '종목명', '현재가', '전일비', '등락률',
        '거래량', '시가', '고가', '저가', '매수호가', '매도호가', '매수총잔량', '매도총잔량',
        '거래대금', '전일거래량', '외국인비율', '상장주식수', '시가총액', '자산총계', '부채총계',
        '매출액', '매출액증가율', '영업이익', '영업이익증가율', '당기순이익', '주당순이익', '보통주배당금',
        'PER', 'ROE', 'ROA', 'PBR', '유보율']]
    return up

def up():
    return pd.concat([__up(0), __up(1)]).sort_values('등락률', ascending=False)


def free_float_rate(code):
    '''
    유동비율을 반환합니다 (100% 기준)
    * code: 종목코드
    '''
    url = f'https://navercomp.wisereport.co.kr/v2/company/c1070001.aspx?cmp_cd={code}'
    df_list = pd.read_html(url, encoding='utf-8')
    df = df_list[1]
    return float(df[('유동주식', '유동주식비율')][0].replace('%', ''))


class NaverSnapReader:
    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def read(self):
        if self.ticker.startswith('NAVER/FINSTATE'):
            tokens = self.ticker.split('/')
            if len(tokens) < 3:
                usage_text = '''Usage examples:
                NAVER/FINSTATE/005930
                NAVER/FINSTATE-Q/005930
                NAVER/FINSTATE-Q1/005930
                NAVER/FINSTATE-Y/005930
                NAVER/FINSTATE-Y3/005930
                '''
                raise ValueError(usage_text)
            fin_type, freq='0', 'Y' # default
            if '-' in tokens[1]:
                for ch in tokens[1].split('-')[1]: # for each char in options
                    fin_type = ch if ch in '01234' else fin_type
                    freq = ch if ch in 'YQA' else freq
            code = tokens[2]
            return finstate_summary(code, fin_type, freq)
        elif self.ticker.startswith('NAVER/INVESTORS'):
            tokens = self.ticker.split('/')
            if len(tokens) < 3:
                usage_text = '''Usage examples:
                NAVER/INVESTORS/005930
                NAVER/INVESTORS/000660
                '''
                raise ValueError(usage_text)
            return investors(tokens[2])
        else:
            raise NotImplementedError(f'"{self.ticker}" is not implemented')
