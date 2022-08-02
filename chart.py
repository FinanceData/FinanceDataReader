#-*- coding: utf-8 -*-

# chart_utils.py
# (c) 2018,2021 FinaceData.KR

import numpy as np
import pandas as pd
import pandas_ta as ta
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

pio.templates.default = "plotly_white"


def plot(df: pd.DataFrame, start: str = None, end: str = None, indicators: list = None, **kwargs):

    df = df.loc[start:end].copy()

    # 1. 기술적 지표에 대한 데이터프레임 만들기
    for indicator in indicators:
        if indicator in dir(df.ta):
            continue
        else:
            raise AttributeError(f"indicator {indicator} is invalid")
    else:
        df = calculate_indicator_value(df, indicators)

    # 2. 각 기술적 지표에 대한 데이터프레임에 맞는 Chart 그림 그리기.
    # plotly_chart(df)
    plotly_chart(df, n=len(indicators))

    # 3. 어노테이션


def calculate_indicator_value(df: pd.DataFrame, indicators: list) -> pd.DataFrame:

    for indicator in indicators:
        df = pd.concat([df, getattr(df.ta, indicator)()], axis=1)

    return df


def plotly_chart(df: pd.DataFrame, n: int = 2):

    # n x 1 형태의 subplot 세팅하기
    fig = plotly_subplot(n)

    # defalut setting. OHLC + Volumne
    fig.add_trace(plotly_candlestick(df), row=1, col=1)
    fig.add_trace(plotly_bar(df), row=2, col=1)

    # # 추가되는 indicator마다 차트 그려주기. 각 지표마다 시각화하는 방식이 다를 수 있음을 고려
    # chart_for_each_indicator = {}
    # for indicator in indicators:
    #     fig.add_trace(plotly_scatter(df, ))

    plotly_xaxes(df, fig)
    plotly_yaxes(df, fig)

    fig.show()


def plotly_subplot(rows: int = 2, cols: int = 1):

    fig = make_subplots(rows=rows,
                        cols=cols,
                        shared_xaxes=True,
                        vertical_spacing=0.03,
                        row_width=[0.3] + [0.7/rows for _ in range(1, rows)]
                        )

    return fig


def plotly_candlestick(df: pd.DataFrame, config: dict = None):

    trace = go.Candlestick(x=df.index,
                           open=df["Open"],
                           high=df["High"],
                           low=df["Low"],
                           close=df["Close"],
                           increasing_line_color='red', increasing_fillcolor='red',
                           decreasing_line_color='blue', decreasing_fillcolor='blue'
                           )
    return trace


def plotly_bar(df: pd.DataFrame, config: dict = None):

    trace = go.Bar(x=df.index,
                   y=df['Volume'],
                   showlegend=False,
                   marker_color=list(
                       map(lambda x: "red" if x else "blue", df.Volume.diff() >= 0))
                   )

    return trace


def plotly_scatter(df: pd.DataFrame, config: dict = None):
    pass


def plotly_xaxes(df, fig):
    # Hide no trading days
    fig.update_xaxes(
        tickangle=-45,
        tickformat='%Y-%m-%d',
        ticks="outside",
        minor_ticks="outside",
        linecolor='black',
        showgrid=True,
        rangeslider_visible=False,
        rangebreaks=[
            dict(values=pd.date_range(
                df.index[1], df.index[-1]).difference(df.index))
        ]
    )


def plotly_yaxes(df, fig):

    fig.update_yaxes(
        ticks="outside",
        minor_ticks="outside",
        linecolor='black',
        exponentformat="none",
        showgrid=True
    )


def plotly_layout(df, fig):
    pass
    
