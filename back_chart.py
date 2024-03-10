#-*- coding: utf-8 -*-
#
# FinaceDataReader chart.py
# (c)2018-2024 FinaceData.KR

from FinanceDataReader.chart import (plot, candle, line)

# import numpy as np
# import pandas as pd
# from datetime import datetime, date
# import itertools

# plotly_install_msg = f'''
#     {'-' * 80}
#     FinanceDataReade.chart.plot() dependen on plotly
#     plotly not installed please install as follows

#     pip install plotly

#     FinanceDataReade.chart.plot()는 plotly에 의존성이 있습니다.
#     명령창에서 다음과 같이 plotly를 설치하세요

#     pip install plotly
#     '''

# try:
#     import plotly.graph_objects as go
#     from plotly.subplots import make_subplots
# except ModuleNotFoundError as e:
#     raise ModuleNotFoundError(plotly_install_msg)

# ## holiday Calendar
# holidays_url_base = 'https://raw.githubusercontent.com/FinanceData/FinanceDataReader/master/calendars'

# holidays_krx,holidays_hyse = None, None 

# ## Chart plot
# def plot(df, tools=None, layout=None):
#     '''
#     plot candle chart with DataFrame
#     * df: OHLCV data(DataFrame)
#     * updates: additional chart configurations
#     '''
#     global holidays_krx, holidays_hyse
    
#     if holidays_krx is None:
#         holidays_krx = pd.read_csv(f'{holidays_url_base}/holidays-krx.csv')['date'].values
#     if holidays_hyse is None:
#         holidays_hyse = pd.read_csv(f'{holidays_url_base}/holidays-nyse.csv')['date'].values


#     tools = {'SMA': [10, 20, 60]} if not tools else tools
#     layout = dict() if not layout else layout

#     x_ticks = df.index

#     change = df["Close"].pct_change()
#     oc_ratio = (df["Close"]-df["Open"])/df["Open"]
#     oh_ratio = (df["High"]-df["Open"])/df["Open"]
#     hover_text = [f'DoD: {chg:.1%} OC: {oc:.1%}, OH: {oh:.1%}' for chg, oc, oh in zip(change, oc_ratio, oh_ratio)]
    
#     # OHLC candle chart
#     candle = go.Candlestick(
#         x=x_ticks, 
#         open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], 
#         name='',
#         text = hover_text,
#         increasing_fillcolor = 'red',
#         decreasing_fillcolor = 'blue',
#         increasing_line_color = 'red',
#         decreasing_line_color = 'blue',
#         increasing_line_width = 1.5,
#         decreasing_line_width = 1.5,
#         showlegend = False, 
#         opacity=0.75,
#     )

#     # volume bar chart
#     vol_colors = np.where(df['Close'].shift(1) > df['Close'], 'blue', 'red')
#     vol_bar = go.Bar(
#         x=x_ticks, 
#         y=df['Volume'],
#         showlegend=False,
#         name='', 
#         opacity = 0.5,
#         marker={'color': vol_colors},
#     )

#     fig = make_subplots(rows=2, cols=1, 
#                         shared_xaxes=True, 
#                         vertical_spacing=0,
#                         row_width=[0.3, 0.7])

#     fig.add_trace(candle, row=1, col=1)
#     fig.add_trace(vol_bar, row=2, col=1)

#     # hide rangeslider
#     fig.update_xaxes(rangeslider_visible=False)

#     # holidays
#     holidays = holidays_krx
#     if df.attrs.get('exchange') != 'KRX':
#         holidays = holidays_hyse

#     # Remove non-business days 
#     fig.update_xaxes(rangebreaks = [ 
#         dict(bounds=['sat','mon']), # remove weekend
#         dict(values=holidays), # remove non biz days
#         # dict(bounds=[15.5, 9], pattern='hour'), # remove non biz hours
#     ])

#     # draw axes and grid
#     fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')
#     fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgray')

#     # x-axis tick format
#     fig.update_xaxes(tickformat='%Y-%m-%d', row=2, col=1)
#     fig.update_xaxes(tickangle=45)

#     # y-axis tick format
#     fig.update_yaxes(tickformat=',', row='all', col=1)

#     # spikes
#     fig.update_xaxes(showspikes=True, spikethickness=1, spikedash="dot", spikecolor="lightgray", spikemode="across", spikesnap='cursor')
#     # fig.update_traces(xaxis="x2") # binding x-axis

#     # bgcolor
#     fig.update_layout(plot_bgcolor='white')
#     fig.update_layout(paper_bgcolor='white')

#     ## tools (tools: indicators and annotations)

#     # available_tools  
#     available_tools = ['SMA', 'EMA', 'HLINE', 'VLINE', 'VRECT']

#     for key in tools:
#         if key.upper() not in available_tools:
#             raise ValueError(f"Unsupport tool: {key}") 
        
#     tools = {key.upper(): tools[key] for key in tools} # keys to upper case 
     
#     # default tools
#     # default_ma_params = [10, 20, 60] # default moving averages params
#     # if all(x not in tools.keys() for x in ['SMA', 'EMA']):
#     #     tools['SMA'] = default_ma_params

#     line_dashes = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
#     line_colors = ['darkmagenta', 'gold', 'limegreen', 'maroon', 'chocolate', 'seagreen', 'coral']
#     line_style_cycler = itertools.cycle(itertools.product(line_dashes, line_colors))

#     default_line_width = 0.75

#     if 'SMA' in tools: # SMA: simple moving average 
#         args = tools.pop('SMA')
#         for arg in args:
#             line_dash, line_color = next(line_style_cycler)
#             ma_args = dict()
#             ma_args['line_width'] = default_line_width
#             if type(arg) == int:
#                 window = arg
#                 ma_args['line_dash'] = line_dash
#                 ma_args['line_color'] = line_color
#                 ma_args['line_width'] = default_line_width
#             elif type(arg) == dict:
#                 window = arg['window']
#                 ma_args['line_dash'] = arg['line_dash'] if 'line_dash' in arg else line_dash
#                 ma_args['line_color'] = arg['line_color'] if 'line_color' in arg else line_color
#                 ma_args['line_width'] = arg['line_width'] if 'line_width' in arg else default_line_width
#             ma_price = df['Close'].rolling(window).mean().round(0)
#             ma_args['x'] = ma_price.index
#             ma_args['y'] = ma_price
#             ma_args['name'] = f'SMA_{window}'
#             fig.add_trace(go.Scatter(**ma_args), row=1, col=1)

#     if 'EMA' in tools: # EMA: exponential moving average
#         args = tools.pop('EMA')
#         for arg in args:
#             line_dash, line_color = next(line_style_cycler)
#             ma_args = dict()
#             ma_args['line_width'] = default_line_width
#             if type(arg) == int:
#                 window = arg
#                 ma_args['line_dash'] = line_dash
#                 ma_args['line_color'] = line_color
#                 ma_args['line_width'] = default_line_width
#             elif type(arg) == dict:
#                 window = arg['window']
#                 ma_args.update(arg)
#                 ma_args['line_dash'] = arg['line_dash'] if 'line_dash' in arg else line_dash
#                 ma_args['line_color'] = arg['line_color'] if 'line_color' in arg else line_color
#                 ma_args['line_width'] = arg['line_width'] if 'line_width' in arg else default_line_width
#             ma_price = df['Close'].ewm(span=window).mean()
#             ma_args['x'] = ma_price.index
#             ma_args['y'] = ma_price
#             ma_args['name'] = f'EMA_{window}'
#             fig.add_trace(go.Scatter(**ma_args), row=1, col=1)

#     if 'HLINE' in tools: # HLINE: Horizontal line
#         hline_args = dict(line_width=1.5, line_dash="dot", line_color="tomato", layer="below")
#         hline_value = tools.pop('HLINE')
#         if hasattr(hline_value, '__iter__'):
#             for hline in hline_value:
#                 if type(hline) in [int, float]:
#                     hline_args['y'] = hline
#                 elif type(hline) == dict:
#                     hline_args.update(hline)
#                 else:
#                     raise ValueError("'HLINE' must be list of str or list of dict")
#                 fig.add_hline(**hline_args)
#         else:
#             hline_args['y'] = hline_value
#             fig.add_hline(**hline_args) # just one value

#     if 'VLINE' in tools: # VLINE: vertical line
#         vline_args = dict(line_width=1.5, line_dash="dot", line_color="tomato", layer="below")
#         vline_value = tools.pop('VLINE')
#         if hasattr(vline_value, '__iter__'):
#             for vline in vline_value:
#                 if type(vline) in [pd.Timestamp, str, datetime, date]:
#                     vline_args['x'] = pd.to_datetime(vline).timestamp() * 1000
#                 elif type(vline) == dict:
#                     vline_args.update(vline)
#                     vline_args['x'] = pd.to_datetime(vline_args['x']).timestamp() * 1000
#                 else:
#                     raise ValueError("'VLINE' must be list of str or list of dict")
#                 fig.add_vline(**vline_args)
#         else:
#             vline_args['y'] = vline_value
#             fig.add_hline(**vline_args) # just one value

#     if 'VRECT' in tools: # VRECT: highlighting period
#         vrect_list = tools.pop('VRECT') if 'VRECT' in tools else {}
#         for vrect in vrect_list:
#             vrect_args = dict(fillcolor="LightSalmon", opacity=0.3, layer="below", line_width=0)
#             if type(vrect) == tuple:
#                 vrect_args['x0'] = str(vrect[0])
#                 vrect_args['x1'] = str(vrect[1])
#             elif type(vrect) == dict:
#                 vrect_args.update(vrect)
#             else:
#                 raise ValueError("'vrect' must be list of tuple or list of dict")
#             fig.add_vrect(**vrect_args)

#     ## update_layout
#     layout_defaults = {
#         'hovermode': 'x', # available hovermodes: 'closest', 'x', 'x unified', 'y', 'y unified'
#         'margin': go.layout.Margin(l=0, r=0, b=0, t=0), # margins
#         'width': 1280,
#         'height': 640,
#     }
#     layout.update(layout_defaults)
#     fig.update_layout(layout)
#     return fig

