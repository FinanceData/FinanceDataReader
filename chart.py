#-*- coding: utf-8 -*-

# chart_utils.py
# (c) 2018,2021 FinaceData.KR

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
 
__fact_def_params = {  # factory default params
    'width': 800,
    'height': 480,
    'volume_height': 0.3, # 30% size of figure height
    'recent_high': False,
    'volume': True,
    'title': '',
    'ylabel': '',
    'moving_average_type': 'SMA',  # 'SMA', 'WMA', 'EMA'
    'moving_average_lines': (5, 20, 60),
    'color_up': 'red',
    'color_down': 'blue',
    'color_volume_up': 'red', 
    'color_volume_down': 'blue',
}

__plot_params = dict(__fact_def_params)

# tableau 10 colors for moving_average_lines
tab_colors =['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
             'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

bokeh_install_msg = '''
FinanceDataReade.chart.plot() dependen on bokeh
bokeh not installed please install as follows

FinanceDataReade.chart.plot()는 bokeh에 의존성이 있습니다.
명령창에서 다음과 같이 bokeh를 설치하세요

pip install bokeh
'''

def config(**kwargs):
    global __plot_params
    
    for key,value in kwargs.items():
        if key.lower()=='reset' and value:
            __plot_params = dict(__fact_def_params)
        elif key=='config':
            for k,v in value.items():
                __plot_params[k] = v
        else:
            __plot_params[key] = value

def plot(df, start=None, end=None, **kwargs):
    '''
    plot candle chart with 'df'(DataFrame) from 'start' to 'end'
    * df: DataFrame to plot
    * start(default: None)
    * end(default: None)
    * recent_high: display recent high price befre n-days (if recent_high == -1 then plot recent high yesterday)
    '''
    try:
        from bokeh.plotting import figure, gridplot
        from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, Span
        from bokeh.io import output_notebook, show, export_png
        from bokeh.palettes import d3
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(bokeh_install_msg)

    params = dict(__plot_params)
    for key,value in kwargs.items():
        if key == 'config':
            for key,value in kwargs.items():
                params[key] = value
        else:
            params[key] = value

    df = df.loc[start:end].copy()
    
    ma_type = params['moving_average_type']
    weights = np.arange(240) + 1

    for n in params['moving_average_lines']: # moving average lines
        if ma_type.upper() == 'SMA':
            df[f'MA_{n}'] = df.Close.rolling(window=n).mean()
        elif ma_type.upper() == 'WMA':
            df[f'MA_{n}'] = df.Close.rolling(n).apply(lambda prices: np.dot(prices, weights[:n])/weights[:n].sum())
        elif ma_type.upper() == 'EMA':
            df[f'MA_{n}'] = df.Close.ewm(span=n).mean()
        elif ma_type.upper() == 'NONE':
            pass
        else:
            raise ValueError(f"moving_average_type '{ma_type}' is invalid")

    inc = df.Close > df.Open
    dec = df.Open > df.Close

    output_notebook()
    
    # plot price OHLC candles
    x = np.arange(len(df))
    height = params['height']
    if params['volume']:
        height = int(params['height'] - params['height'] * params['volume_height'])
    pp = figure(plot_width=params['width'], 
                plot_height=height,
                x_range=(-1, min(120, len(df))),
                y_range=(df.Low.min(), df.High.max()),
                title=params['title'],
                y_axis_label=params['ylabel'])
    
    pp.segment(x[inc], df.High[inc], x[inc], df.Low[inc], color=params['color_up'])
    pp.segment(x[dec], df.High[dec], x[dec], df.Low[dec], color=params['color_down'])
    pp.vbar(x[inc], 0.8, df.Open[inc], df.Close[inc], fill_color=params['color_up'], line_color=params['color_up'])
    pp.vbar(x[dec], 0.8, df.Open[dec], df.Close[dec], fill_color=params['color_down'], line_color=params['color_down'])
    pp.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
        
    if params['volume']:
        pp.xaxis.visible = False
    else:
        x_labels = {i: dt.strftime('%Y-%m-%d') for i,dt in enumerate(df.index)}
        x_labels.update({len(df): ''})
        pp.xaxis.major_label_overrides = x_labels
        pp.xaxis.formatter=DatetimeTickFormatter(hours=["%H:%M"], days=["%Y-%m-%d"])
        pp.xaxis.major_label_orientation = np.pi / 5
        
    for ix,n in enumerate(params['moving_average_lines']):
        pal = d3['Category10'][10]
        pp.line(x, df[f'MA_{n}'], line_color=pal[ix % len(pal)])

    if params['recent_high']:
        to = df.index.max() + timedelta(days=params['recent_high'])
        hline = Span(location=df.Close[:to].max(), dimension='width', line_dash='dashed', line_color='gray', line_width=2)
        pp.renderers.extend([hline])

    # plot volume
    if params['volume']:
        inc = df.Volume.diff() >= 0
        dec = df.Volume.diff() < 0

        height = int(params['height'] * params['volume_height'])
        pv = figure(plot_width=params['width'], plot_height=height, x_range = pp.x_range)

        pv.vbar(x[inc], 0.8, df.Volume[inc], fill_color=params['color_volume_up'], line_color="black")
        pv.vbar(x[dec], 0.8, df.Volume[dec], fill_color=params['color_volume_down'], line_color="black")

        pv.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
        x_labels = {i: dt.strftime('%Y-%m-%d') for i,dt in enumerate(df.index)}
        x_labels.update({len(df): ''})
        pv.xaxis.major_label_overrides = x_labels
        pv.xaxis.formatter=DatetimeTickFormatter(hours=["%H:%M"], days=["%Y-%m-%d"])
        pv.xaxis.major_label_orientation = np.pi / 5
        pv.y_range.range_padding = 0

        # 가격(pp)과 거래량(pv) 함께 그리기
        p = gridplot([[pp], [pv]])
    else:
        p = gridplot([[pp]])
    show(p)
    
    if 'save' in kwargs:
        export_png(p, filename=kwargs['save'])
